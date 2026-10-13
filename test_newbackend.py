"""Regression checks for the scalable local quiz backend features."""

import contextlib
import io
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import mock_open, patch


BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent
os.chdir(PROJECT_DIR)
sys.path.insert(0, str(BACKEND_DIR))
with contextlib.redirect_stdout(io.StringIO()):
    import new as backend


class BackendFeatureTests(unittest.TestCase):
    def setUp(self):
        self.bank = backend.Question_bank()
        self.quiz = backend.Quiz(self.bank)

    def add_question(self, category="maths", difficulty="easy", prompt="q", answer="a", skill_tags=None):
        question = backend.Question(
            prompt, answer, category, difficulty, "normal", skill_tags=skill_tags
        )
        self.bank.questions.setdefault(category, {}).setdefault(difficulty, []).append(question)
        return question

    def test_normalization_keeps_difficulty_rules_and_numeric_equivalents(self):
        hard = backend.Question("q", "Café", "maths", "hard", "normal")
        self.assertTrue(self.quiz.rules_to_check_answer(hard, " Cafe\u0301 "))
        self.assertFalse(self.quiz.rules_to_check_answer(hard, "CAFÉ"))
        medium = backend.Question("q", "New York", "maths", "medium", "normal")
        self.assertTrue(self.quiz.rules_to_check_answer(medium, " new\tYork "))
        numeric = backend.Question("q", "1234.5", "maths", "medium", "normal")
        self.assertTrue(self.quiz.rules_to_check_answer(numeric, "1,234.5"))
        self.assertTrue(self.quiz.rules_to_check_answer(
            backend.Question("q", "-7", "maths", "easy", "normal"), "−7"
        ))

    def test_legacy_question_json_loads_without_new_skill_field(self):
        legacy = {"maths": {"easy": [{
            "question": "old question", "answer": "yes", "question_type": "normal", "options": None
        }]}}
        bank = backend.Question_bank()
        with patch.object(backend.os.path, "exists", side_effect=lambda path: path == "questions.json"), \
             patch("builtins.open", mock_open(read_data=json.dumps(legacy))):
            bank.load_questions()
        question = bank.questions["maths"]["easy"][0]
        self.assertEqual(question.skill_tags, [])
        self.assertEqual(question.answer, "yes")

    def test_question_loader_recovers_from_its_backup(self):
        backup = {"economics": {"easy": [{
            "question": "What is a choice?", "answer": "An option", "question_type": "normal"
        }]}}

        def open_question_file(path, *_args, **_kwargs):
            if path == "questions.json":
                raise json.JSONDecodeError("truncated", "{", 1)
            return io.StringIO(json.dumps(backup))

        bank = backend.Question_bank()
        with patch.object(backend.os.path, "exists", return_value=True), \
             patch("builtins.open", side_effect=open_question_file):
            bank.load_questions()
        self.assertEqual(bank.questions["economics"]["easy"][0].answer, "An option")

    def test_question_save_uses_atomic_backup_path(self):
        self.add_question(category="history", prompt="event", skill_tags=["causes"])
        with patch.object(backend, "write_json_atomically", return_value=None) as writer:
            self.bank.save_questions()
        self.assertEqual(writer.call_args.args[0], "questions.json")
        self.assertTrue(writer.call_args.kwargs["keep_backup"])
        self.assertEqual(writer.call_args.args[1]["history"]["easy"][0]["skill_tags"], ["causes"])

    def test_question_import_and_export_preserve_optional_skill_tags(self):
        payload = {"history": {"medium": [{
            "question": "Why?", "answer": "Because", "question_type": "normal",
            "skill_tags": ["causes", "evidence"],
        }]}}
        with patch("builtins.open", mock_open(read_data=json.dumps(payload))):
            self.bank.import_questions("import.json")
        question = self.bank.questions["history"]["medium"][0]
        self.assertEqual(question.skill_tags, ["causes", "evidence"])
        self.assertEqual(self.bank.to_dictionary()["history"]["medium"][0]["skill_tags"], ["causes", "evidence"])

    def test_learning_map_falls_back_for_old_answers_and_scales_to_new_categories(self):
        history = [{
            "answer_review": [{"category": "history", "difficulty": "hard", "is_correct": False}]
        }]
        self.quiz.load_quiz_history = lambda: (history, None)
        self.assertEqual(self.quiz.get_skill_outcomes(), {"history · hard": [False]})
        self.add_question(category="history", difficulty="hard", prompt="cause", skill_tags=["causation"])
        self.assertIn("history", self.quiz.get_concept_categories())
        self.assertEqual(self.quiz.question_skills(self.bank.questions["history"]["hard"][0]), ["causation"])

    def test_targeted_practice_uses_weak_skill_and_allows_mixed_categories(self):
        target = self.add_question(category="history", prompt="cause", skill_tags=["causation"])
        history = [{
            "answer_review": [{
                "category": "history", "difficulty": "easy", "question": "cause",
                "skill_tags": ["causation"], "is_correct": False,
            }]
        }]
        self.quiz.get_skill_outcomes = lambda: {"causation": [False]}
        with patch("builtins.input", side_effect=["1", "1"]), patch.object(self.quiz, "start_quiz") as start:
            self.quiz.practice_focus_skill()
        self.assertEqual(start.call_args.kwargs["question_set"], [target])
        self.assertEqual(start.call_args.kwargs["mode"], "skill_practice")

    def test_adaptive_weights_increase_for_recent_errors(self):
        question = self.add_question(prompt="weak")
        record = {
            "category": "maths", "difficulty": "easy", "question": "weak",
            "is_correct": False, "retried": False,
        }
        self.quiz.load_quiz_history = lambda: ([{"answer_review": [record]}], None)
        weight = self.quiz.get_adaptive_question_weights()[self.quiz.question_identity(question)]
        self.assertGreater(weight, 1)

    def test_daily_challenge_includes_questions_from_new_categories(self):
        for index in range(7):
            self.add_question(category="economics" if index % 2 else "history", prompt=f"q{index}")
        with patch.object(self.quiz, "start_quiz") as start, contextlib.redirect_stdout(io.StringIO()):
            self.quiz.start_daily_challenge()
        chosen = start.call_args.kwargs["question_set"]
        self.assertEqual(len(chosen), 5)
        self.assertTrue(all(question in self.quiz.all_questions() for question in chosen))

    def test_due_review_finds_added_categories(self):
        question = self.add_question(category="economics", difficulty="hard", prompt="scarcity")
        self.quiz.load_quiz_history = lambda: ([{
            "date": "2020-01-01",
            "answer_review": [{
                "category": "economics", "difficulty": "hard", "question": "scarcity",
                "is_correct": True, "next_review_date": "2020-01-02",
            }],
        }], None)
        self.assertEqual(self.quiz.get_due_questions(), [question])

    def test_review_intervals_grow_after_confident_recall_and_reset_after_lapse(self):
        today = backend.date.today()
        self.assertEqual(self.quiz.get_next_review_date(True, "sure"), (today + backend.timedelta(days=7)).isoformat())
        self.assertEqual(self.quiz.get_next_review_date(True, "sure", previous_streak=1), (today + backend.timedelta(days=14)).isoformat())
        self.assertEqual(self.quiz.get_next_review_date(True, "somewhat"), (today + backend.timedelta(days=3)).isoformat())
        self.assertEqual(self.quiz.get_next_review_date(False, "sure", previous_streak=3), (today + backend.timedelta(days=1)).isoformat())

    def test_history_saves_atomically_keeps_backup_and_recovers_backup(self):
        self.quiz.score = 2
        saved_history = []

        def load_history():
            return list(saved_history), None

        def write_history(_path, data, keep_backup=False):
            saved_history[:] = data
            return None

        with patch.object(self.quiz, "load_quiz_history", side_effect=load_history), \
             patch.object(backend, "write_json_atomically", side_effect=write_history) as writer:
            self.assertTrue(self.quiz.save_history("maths", "easy", 1, 1, 0, 2, 100))
            self.assertTrue(self.quiz.save_history("maths", "easy", 1, 0, 1, 2, 0))
        self.assertEqual(len(saved_history), 2)
        self.assertEqual(writer.call_args.args[0], "history.json")
        self.assertTrue(writer.call_args.kwargs["keep_backup"])

    def test_history_loader_uses_backup_after_truncated_primary(self):
        valid_history = [{"date": "2026-10-13", "answer_review": []}]

        def open_history(path, *_args, **_kwargs):
            if path == "history.json":
                raise json.JSONDecodeError("truncated", "{", 1)
            return io.StringIO(json.dumps(valid_history))

        with patch.object(backend.os.path, "exists", return_value=True), patch("builtins.open", side_effect=open_history):
            loaded, error = self.quiz.load_quiz_history()
        self.assertIsNone(error)
        self.assertEqual(loaded, valid_history)

    def test_concept_library_is_valid_for_existing_and_custom_categories(self):
        for lessons in backend.Quiz.CONCEPT_LIBRARY.values():
            for lesson in lessons:
                self.assertIn(lesson["visual"], {"balance", "function", "derivative", "variables", "loop", "alias"})
                self.assertGreaterEqual(len(lesson["check"]["choices"]), 2)
                self.assertIn(lesson["check"]["answer"], range(len(lesson["check"]["choices"])))
        custom = {
            "history": [{
                "id": "custom-history-1", "title": "Causes and effects", "analogy": "Dominoes",
                "idea": "An event can have more than one cause.", "example": "Trace a cause to an outcome.",
                "visual": "steps", "visual_steps": ["Event", "Cause", "Effect"],
                "check": {"prompt": "What follows a cause?", "choices": ["An effect", "A category"], "answer": 0, "why": "Causes contribute to effects."},
            }]
        }
        def open_concepts(path, *_args, **_kwargs):
            if path == "concepts.json":
                return io.StringIO(json.dumps(custom))
            raise OSError("no backup")

        with patch.object(backend.os.path, "exists", side_effect=lambda path: path == "concepts.json"), \
             patch("builtins.open", side_effect=open_concepts):
            library, error = self.quiz.load_concept_library()
        self.assertIsNone(error)
        self.assertEqual(library["history"][0]["visual_steps"], ["Event", "Cause", "Effect"])

    def test_admin_can_add_a_concept_for_a_new_category(self):
        self.add_question(category="economics")
        answers = [
            "economics", "Opportunity cost", "Choosing one path means leaving another",
            "The next-best alternative is what you give up", "Choosing study over work gives up wages",
            "What does opportunity cost mean?", "The next-best option|The total price", "1",
            "It is the value of the next-best alternative", "Choose|Compare|Reflect",
        ]
        with patch("builtins.input", side_effect=answers), \
             patch.object(backend.os.path, "exists", return_value=False), \
             patch.object(backend, "write_json_atomically", return_value=None) as writer, \
             contextlib.redirect_stdout(io.StringIO()):
            self.quiz.manage_concept_lessons()
        self.assertEqual(writer.call_args.args[0], "concepts.json")
        self.assertEqual(writer.call_args.args[1]["economics"][0]["visual"], "steps")
        self.assertIn("economics", self.quiz.get_concept_categories())

    def test_concept_progress_uses_backup_when_primary_is_damaged(self):
        backup = {"lesson": {"seen_count": 2}}

        def open_progress(path, *_args, **_kwargs):
            if path == "concept_progress.json":
                raise json.JSONDecodeError("truncated", "{", 1)
            return io.StringIO(json.dumps(backup))

        with patch.object(backend.os.path, "exists", return_value=True), patch("builtins.open", side_effect=open_progress):
            progress, error = self.quiz.load_concept_progress()
        self.assertIsNone(error)
        self.assertEqual(progress["lesson"]["seen_count"], 2)


if __name__ == "__main__":
    unittest.main()
