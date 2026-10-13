import json   
import os   
import random 
import re
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import date, timedelta
from datetime import datetime
from fractions import Fraction
from tkinter import filedialog
import uuid


def parse_feedback_criteria(raw_text):
    """Parse required ideas separated by semicolons and aliases separated by |."""
    return [
        [alias.strip() for alias in idea.split("|") if alias.strip()]
        for idea in raw_text.split(";")
        if any(alias.strip() for alias in idea.split("|"))
    ]


def choose_question_file(save=False):
    root = tk.Tk()
    root.withdraw()
    if save:
        selected_path = filedialog.asksaveasfilename(
            title="Export question bank",
            defaultextension=".json",
            initialfile="questions-export.json",
            filetypes=[("JSON files", "*.json")],
        )
    else:
        selected_path = filedialog.askopenfilename(
            title="Import questions",
            filetypes=[("JSON files", "*.json")],
        )
    root.destroy()
    return selected_path


class Question:
    def __init__(self,question,answer,category,difficulty,question_type,options=None,explanation="",feedback_criteria=None):
        self.question = question 
        self.answer = answer 
        self.category = category 
        self.difficulty = difficulty 
        self.question_type = question_type 
        self.options = options 
        self.explanation = str(explanation or "").strip()
        raw_criteria = feedback_criteria if isinstance(feedback_criteria, list) else []
        self.feedback_criteria = [
            [str(alias).strip() for alias in criterion if str(alias).strip()]
            for criterion in raw_criteria
            if isinstance(criterion, list) and any(str(alias).strip() for alias in criterion)
        ]
    def __str__(self): 
        return f"{self.question},{self.answer},{self.category},{self.difficulty},{self.question_type},{self.options}" 
    def to_dictionary(self): 
        data = { 
            "question":self.question, 
            "answer":self.answer, 
            "category":self.category, 
            "difficulty":self.difficulty, 
            "question_type":self.question_type, 
            "options":self.options,
            "explanation":self.explanation,
            "feedback_criteria":self.feedback_criteria,
 
        } 
        return data 
 
 
maths_medium_1 = Question("Derivative of x^2", "2x", "maths", "medium","normal") 
 
maths_questions = [ 
    
    
    maths_medium_1, 
] 
all_questions = ( 
    maths_questions  
) 
class Question_bank: 
    def __init__(self): 
        self.questions = {} 
    def add_question(self,question): 
        
        if question.category in self.questions: 
            print("the category already exist so moving on to difficulties") 
             
        else : 
            self.questions.update({question.category:{}}) 
        if question.difficulty in  self.questions[question.category]: 
            print("the difficulties already exist now adding question objects in list") 
        else: 
            self.questions[question.category][question.difficulty]= [] 
        self.questions[question.category][question.difficulty].append(question) 
    def display_questions(self): 
        if len(self.questions)== 0: 
            print("the question bank is empty:") 
        else: 
            for category in self.questions: 
                print(f"category:{category}") 
                for difficulty in self.questions[category]: 
                    print(f"difficulties:{difficulty}") 
                    for question_object  in self.questions[category][difficulty]: 
                        print(question_object) 
    def find_question(self,question_text):  
        for category in self.questions: 
            print(category) 
            for difficulty in self.questions[category]: 
                for question_object in self.questions[category][difficulty]: 
                     
                    if question_object.question == question_text: 
                        return question_object 
        return None 
                     
 
 
                   
 
        
    def delete_question(self,question_text): 
        question = self.find_question(question_text) 
        if question is None: 
            print("that question deosnt exixt :") 
        else: 
            self.questions[question.category][question.difficulty].remove(question)    
            print("the question has been removed ") 
    def load_questions(self):
            self.questions =  {}
            
            
 
            if not os.path.exists("questions.json"): 
                with open("questions.json", "w", encoding="utf-8") as f: 
                    json.dump({}, f) 
            with open("questions.json","r", encoding="utf-8")as f: 
                question_data = json.load(f) 
                     
                for category in question_data: 
                    for difficulty in question_data[category]: 
                        for question_dict in question_data[category][difficulty]: 
                            question = Question( 
                                                question_dict["question"], 
                                                question_dict["answer"], 
                                                category, 
                                                difficulty, 
                                                question_dict["question_type"], 
                                                question_dict.get("options"),
                                                question_dict.get("explanation", ""),
                                                question_dict.get("feedback_criteria", []),
                                                                            ) 
                            self.add_question(question) 
                           
                             
 
        
             
             
             
 
                 
    def edit_question(self,question,field,new_value): 
      
            if field == "answer": 
                question.answer = new_value 
            elif field == "question": 
                question.question = new_value 
            elif field == "explanation":
                question.explanation = new_value.strip()
            elif field == "feedback_criteria":
                question.feedback_criteria = new_value
            elif field == "category": 
                new_category,new_difficulty = new_value 
                self.questions[question.category][question.difficulty].remove(question) 
                if new_category not in self.questions : 
                    self.questions[new_category]= {} 
                if  new_difficulty not in self.questions[new_category]: 
                    self.questions[new_category][ new_difficulty] =[] 
                question.category = new_category 
                question.difficulty = new_difficulty 
                self.questions[question.category][question.difficulty].append(question) 
            elif field == "difficulty": 
                new_difficulty = new_value 
                self.questions[question.category][question.difficulty].remove(question)  
                if new_difficulty not in self.questions[question.category]: 
                    self.questions[question.category][ new_difficulty] =[] 
                question.difficulty = new_difficulty 
                self.questions[question.category][question.difficulty].append(question) 
            elif field == "question_type":

                new_question_type, new_options = new_value

    
                if new_question_type == "normal":

                    if question.question_type == "mcq":
                        question.answer = question.options[question.answer]

                    question.question_type = "normal"
                    question.options = None

                elif new_question_type == "mcq":
                    if question.question_type == "normal":
                        for key, value in new_options.items():
                            if value == question.answer:
                                question.answer = key
                                question.question_type = "mcq"
                                question.options = new_options
                                break
                            
                                
                                
                        
                                
                        else:
                            print("The existing answer must be one of the options.")
                            return
                    elif question.question_type == "mcq":
                        old_answer = question.options[question.answer]
                    
                        
                    
                        for key, value in new_options.items():
                            if value == old_answer:
                                question.answer = key
                                question.options = new_options
                                break
                        else:
                            print("your existing correct answer isnt in your new options so change failed")
                            return    
                    else:
                        print("the question type doesnt exist so change cant occur")
                        return
                    
                else:   
                    print("invalid question types.") 
                    return   
    
                
                






                         
 
 
    def save_questions(self): 
        data = self.to_dictionary()
        with open("questions.json", "w", encoding="utf-8") as question_file:
            json.dump(data, question_file, indent=4, ensure_ascii=False)

    def to_dictionary(self):
        data = {} 
        for category in self.questions: 
            data[category]={} 
            for difficulty in self.questions[category]: 
                data[category][difficulty]=[] 
                for questions in self.questions[category][difficulty]: 
                     data[category][difficulty].append(questions.to_dictionary()) 
        return data

    def export_questions(self, file_path):
        with open(file_path, "w", encoding="utf-8") as question_file:
            json.dump(self.to_dictionary(), question_file, indent=4, ensure_ascii=False)

    def import_questions(self, file_path):
        with open(file_path, "r", encoding="utf-8") as question_file:
            imported_data = json.load(question_file)
        if not isinstance(imported_data, dict):
            raise ValueError("The question file must contain categories and difficulty groups.")

        candidates = []
        existing = {
            (question.category, question.difficulty, question.question)
            for category in self.questions.values()
            for group in category.values()
            for question in group
        }
        skipped = 0
        for category, difficulty_groups in imported_data.items():
            if not str(category).strip() or not isinstance(difficulty_groups, dict):
                raise ValueError(f"Category '{category}' must contain difficulty groups.")
            for difficulty, question_list in difficulty_groups.items():
                if not str(difficulty).strip() or not isinstance(question_list, list):
                    raise ValueError(f"'{category}/{difficulty}' must contain a list of questions.")
                for item in question_list:
                    if not isinstance(item, dict):
                        raise ValueError(f"A question in '{category}/{difficulty}' is not an object.")
                    prompt = item.get("question")
                    answer = item.get("answer")
                    question_type = item.get("question_type", "normal")
                    if not isinstance(prompt, str) or not prompt.strip() or not isinstance(answer, str):
                        raise ValueError(f"A question in '{category}/{difficulty}' is missing its text or answer.")
                    if question_type not in ("normal", "mcq"):
                        raise ValueError(f"Question '{prompt}' has an unsupported question type.")
                    options = item.get("options") or None
                    if question_type == "mcq" and (
                        not isinstance(options, dict) or item.get("answer") not in options
                    ):
                        raise ValueError(f"MCQ '{prompt}' needs options and a valid answer key.")
                    prompt = prompt.strip()
                    identity = (str(category).strip(), str(difficulty).strip(), prompt)
                    if identity in existing:
                        skipped += 1
                        continue
                    candidates.append(Question(
                        prompt.strip(),
                        answer.strip(),
                        str(category).strip(),
                        str(difficulty).strip(),
                        question_type,
                        options,
                        item.get("explanation") or "",
                        item.get("feedback_criteria", []),
                    ))
                    existing.add(identity)

        for question in candidates:
            self.questions.setdefault(question.category, {}).setdefault(question.difficulty, []).append(question)
        return len(candidates), skipped
    def retiriving_questions(self,selected_category,selected_difficulty):
        stored_questions = []
        if selected_category in self.questions:
            if selected_difficulty in self.questions[selected_category]:
                for retrived_questions in self.questions[selected_category][selected_difficulty]:
                    stored_questions.append(retrived_questions)
                    
                return stored_questions

            else:
                print("the difficutly doesnt exist:")
                return None

        else:
            print("the question category doesnt exist so question isnt also there")
            return None
            
                

           


bank =Question_bank()

            
                
               


                         
               
     
                   
 
 
           
                  
             
 
            
                 
# bank = Question_bank()
# bank.load_questions()

 
class Quiz: 
    QUESTION_TIME_LIMIT = 30
    OPINION_HISTORY_FILE = "opinion_responses.json"
    MISTAKE_PATTERN_LABELS = {
        "concept_gap": "Concept not clear",
        "working_slip": "Calculation or working slip",
        "misread": "Misread the question",
        "guess": "Guessed or felt unsure",
        "answer_format": "Answer format or wording",
        "other": "Something else",
        "not_sure": "Not sure",
    }
    OPINION_PROMPTS = [
        ("Everyday life", "Should schools give students more choice in how they show what they have learned? Why or why not?"),
        ("Technology", "When does using technology make learning better, and when can it get in the way?"),
        ("Economics", "Should people pay a little more for products made to last longer? Explain your view."),
        ("History", "Which is more important when studying history: understanding leaders' decisions or ordinary people's lives?"),
        ("Science", "Should communities spend more to prevent environmental problems before they happen? Why?"),
        ("Everyday life", "Is it better to become very good at one skill or to learn several skills? Support your view."),
        ("Technology", "Should apps be designed to encourage people to take breaks from screens? Why or why not?"),
        ("Economics", "What matters more when choosing a job: reliable income or meaningful work? Explain your thinking."),
        ("History", "Should museums focus more on telling difficult parts of history, even when those stories are uncomfortable?"),
        ("Science", "When resources are limited, should a community prioritize preventing illness or treating it later?"),
        ("Everyday life", "Is working in a group usually better than working alone? Give reasons for your view."),
        ("Technology", "Should people be able to use online services without sharing more personal data than necessary?"),
        ("Economics", "Should a community prioritize affordable public transport even if it costs more to run?"),
        ("History", "What can personal letters and diaries teach us that official records may miss?"),
        ("Science", "Should scientific discoveries be shared openly, even when they could be misused? Explain your view."),
        ("Everyday life", "Is consistency more useful than motivation when building a new habit? Why?"),
        ("Technology", "Should important decisions made with computer algorithms always be explainable to people affected by them?"),
        ("Economics", "When a town has a limited budget, should it invest first in parks or roads? Make your case."),
    ]

    def __init__(self,question_bank): 
        self.question_bank = question_bank 
        self.current_questions = None 
        self.category = None 
        self.difficulty = None 
        self.score = 0 
    def select_questions(self,selected_category,selected_difficulty,selected_question_no): 
        self.current_questions = self.question_bank.retiriving_questions(selected_category,selected_difficulty)
        

        
        self.category= selected_category
        self.difficulty = selected_difficulty
        if len(self.current_questions) == 0:
            print("There are no questions in this category and difficulty.")
            return    
        if len(self.current_questions) >= selected_question_no: 
            self.current_questions = self.select_weighted_questions(self.current_questions, selected_question_no)
            
            return 
         
            
           
 
           
 
           
 
                
                    
 
                    
                       
 
 
        elif len(self.current_questions) < selected_question_no: 
            print("we dont have that much questions currently in this category/difficulty so make peace with it :") 
            selected_question_no = len(self.current_questions) 
            self.current_questions = self.select_weighted_questions(self.current_questions, selected_question_no) 
            return 
 
 
     
 
        
    def start_quiz(self,selected_category,selected_difficulty,selected_question_no,question_set=None,mode="standard"):
        self.score = 0 
        if question_set is None:
            self.select_questions(selected_category,selected_difficulty,selected_question_no)
        else:
            self.current_questions = list(question_set)
            self.category = selected_category
            self.difficulty = selected_difficulty
        if not self.current_questions:
            return

        correct_answers = 0 
        wrong_answers = 0 
        partial_answers = 0
        correct_on_retry = 0
        answer_review = []
        
        for question_number, question in enumerate(self.current_questions, start=1):
            first_answer = self.get_timed_answer(question, question_number)
            first_is_correct, first_analysis = self.evaluate_answer(question, first_answer)
            retried = False
            retry_answer = None
            retry_correct = False
            user_answer = first_answer
            is_correct = first_is_correct
            answer_analysis = first_analysis

            if not first_is_correct and self.ask_retry_now(question_number):
                retried = True
                retry_answer = self.get_timed_answer(question, question_number, is_retry=True)
                user_answer = retry_answer
                is_correct, answer_analysis = self.evaluate_answer(question, retry_answer)
                retry_correct = is_correct

            reflection = self.ask_for_reasoning(
                question,
                user_answer,
                first_mistake_answer=first_answer if not first_is_correct else None,
            )
            reasoning = reflection["reasoning"]
            confidence = reflection["confidence"]
            mistake_pattern = reflection["mistake_pattern"]
            numeric_difference = self.get_numeric_difference(question, user_answer)
            next_review_date = self.get_next_review_date(is_correct, confidence, was_retried=retried)
            if is_correct: 
                mark = self.get_marks(question) 
                self.score += mark 
                correct_answers += 1 
            else: 
                if answer_analysis.get("kind") == "key_ideas":
                    total_ideas = answer_analysis["total_key_ideas"]
                    matched_ideas = len(answer_analysis["matched_key_ideas"])
                    if total_ideas and matched_ideas:
                        self.score += self.get_marks(question) * matched_ideas / total_ideas
                        partial_answers += 1
                wrong_answers += 1 

            if question.question_type == "mcq":
                submitted_answer = (
                    f"{user_answer}. {question.options[user_answer]}"
                    if user_answer in question.options
                    else "(no answer — time expired)"
                )
                correct_answer = f"{question.answer}. {question.options[question.answer]}"
            else:
                submitted_answer = user_answer or "(no answer)"
                correct_answer = question.answer

            self.show_question_feedback(
                question,
                question_number,
                submitted_answer,
                correct_answer,
                is_correct,
                reasoning,
                numeric_difference,
                answer_analysis,
                confidence,
                next_review_date,
                first_submitted_answer=(
                    self.format_submitted_answer(question, first_answer)
                    if retried else None
                ),
                was_retried=retried,
                mistake_pattern=mistake_pattern,
            )

            submitted_answer = self.format_submitted_answer(question, user_answer)
            first_submitted_answer = self.format_submitted_answer(question, first_answer)
            if retried and retry_correct:
                correct_on_retry += 1

            answer_review.append({
                "question": question.question,
                "category": question.category,
                "difficulty": question.difficulty,
                "question_type": question.question_type,
                "options": question.options,
                "your_answer": submitted_answer,
                "first_answer": first_submitted_answer,
                "retry_answer": submitted_answer if retried else None,
                "retried": retried,
                "retry_correct": retry_correct,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "explanation": question.explanation,
                "reasoning": reasoning,
                "mistake_pattern": mistake_pattern,
                "numeric_difference": (
                    float(numeric_difference) if numeric_difference is not None else None
                ),
                "answer_analysis": answer_analysis,
                "confidence": confidence,
                "next_review_date": next_review_date,
            })
            print("Correct!" if is_correct else "Not quite.")
        total_marks = self.get_total_marks() 
         
        percentage = (self.score/total_marks)*100 if total_marks else 0
 
        print(f"Correct: {correct_answers}") 
        print(f"Wrong: {wrong_answers}") 
        print(f"Partial-credit answers: {partial_answers}")
        print(f"Correct on retry: {correct_on_retry}")
        print(f"Score: {self.score}") 
        print(f"Percentage: {percentage:.1f}%") 
        print(f"Category: {self.category}") 
        print(f"Difficulty: {self.difficulty}") 
        
        self.show_answer_review(answer_review)
        self.save_history(self.category, 
                self.difficulty, 
                len(self.current_questions), 
                correct_answers, 
                wrong_answers, 
                total_marks, 
                percentage,
                answer_review,
                mode,
                        ) 

    @staticmethod
    def format_submitted_answer(question, user_answer):
        if question.question_type == "mcq":
            return (
                f"{user_answer}. {question.options[user_answer]}"
                if user_answer in question.options
                else "(no answer — time expired)"
            )
        return user_answer or "(no answer)"

    @staticmethod
    def ask_retry_now(question_number):
        window = tk.Tk()
        window.withdraw()
        wants_retry = messagebox.askyesno(
            "Try once more?",
            f"That answer isn't correct. Would you like one more try for question {question_number}?\n\n"
            "The correct answer will stay hidden until after your retry.",
            parent=window,
        )
        window.destroy()
        return wants_retry

    @staticmethod
    def question_identity(question):
        return (question.category, question.difficulty, question.question)

    def get_adaptive_question_weights(self):
        """Increase selection odds for questions with unresolved recent errors."""
        if not os.path.exists("history.json"):
            return {}
        try:
            with open("history.json", "r", encoding="utf-8") as history_file:
                history = json.load(history_file)
        except (OSError, json.JSONDecodeError, UnicodeError):
            return {}
        if not isinstance(history, list):
            return {}

        outcomes_by_question = {}
        for attempt in history:
            if not isinstance(attempt, dict):
                continue
            for item in attempt.get("answer_review", []):
                if not isinstance(item, dict):
                    continue
                identity = (item.get("category"), item.get("difficulty"), item.get("question"))
                if not all(isinstance(part, str) for part in identity):
                    continue
                outcomes_by_question.setdefault(identity, []).append(item)

        weights = {}
        for identity, outcomes in outcomes_by_question.items():
            unresolved_errors = 0
            for item in reversed(outcomes):
                clean_correct = item.get("is_correct") and not item.get("retried", False)
                if clean_correct:
                    break
                unresolved_errors += 1
            if unresolved_errors:
                weights[identity] = 1 + min(unresolved_errors, 4) * 2
        return weights

    def select_weighted_questions(self, questions, count):
        """Sample without replacement, favoring questions with unresolved errors."""
        remaining = list(questions)
        weights_by_identity = self.get_adaptive_question_weights()
        selected = []
        for _ in range(min(count, len(remaining))):
            weights = [
                weights_by_identity.get(self.question_identity(question), 1)
                for question in remaining
            ]
            selected_index = random.choices(range(len(remaining)), weights=weights, k=1)[0]
            selected.append(remaining.pop(selected_index))
        return selected

    def all_questions(self):
        return [
            question
            for category in self.question_bank.questions.values()
            for questions in category.values()
            for question in questions
        ]

    def start_daily_challenge(self):
        question_pool = sorted(
            self.all_questions(),
            key=lambda question: (question.category, question.difficulty, question.question),
        )
        if not question_pool:
            print("There are no questions available for today's challenge.")
            return

        challenge_day = date.today().isoformat()
        daily_rng = random.Random(date.today().toordinal())
        question_count = min(5, len(question_pool))
        daily_questions = daily_rng.sample(question_pool, question_count)
        print(f"\\n========== DAILY CHALLENGE · {challenge_day} ==========")
        print(f"Today's five-question set is fixed for the day. Each answer has {self.QUESTION_TIME_LIMIT} seconds.")
        self.start_quiz(
            "Daily Challenge",
            "Mixed",
            question_count,
            question_set=daily_questions,
            mode="daily_challenge",
        )

    def get_missed_questions(self):
        questions_by_identity = {}
        questions_by_text = {}
        for question in self.all_questions():
            identity = (question.category, question.difficulty, question.question)
            questions_by_identity[identity] = question
            questions_by_text.setdefault(question.question, question)

        if not os.path.exists("history.json"):
            return []
        with open("history.json", "r", encoding="utf-8") as history_file:
            history = json.load(history_file)

        missed_questions = {}
        for attempt in history:
            for item in attempt.get("answer_review", []):
                if item.get("is_correct"):
                    continue
                category = item.get("category")
                difficulty = item.get("difficulty")
                identity = (category, difficulty, item.get("question"))
                question = questions_by_identity.get(identity) if category and difficulty else None
                if question is None:
                    question = questions_by_text.get(item.get("question"))
                if question is not None:
                    key = (question.category, question.difficulty, question.question)
                    missed_questions[key] = question
        return list(missed_questions.values())

    def practice_missed_questions(self):
        missed_questions = self.get_missed_questions()
        if not missed_questions:
            print("No missed questions to practise yet. Finish a quiz first.")
            return

        print(f"\\nYou have {len(missed_questions)} unique missed question(s) to practise.")
        count_text = input(f"How many would you like to retry? (1-{len(missed_questions)}, Enter for all): ").strip()
        if not count_text:
            count = len(missed_questions)
        else:
            try:
                count = int(count_text)
            except ValueError:
                print("Enter a whole number.")
                return
            if count < 1 or count > len(missed_questions):
                print(f"Choose a number between 1 and {len(missed_questions)}.")
                return

        selected_questions = self.select_weighted_questions(missed_questions, count)
        self.start_quiz(
            "Missed Questions",
            "Mixed",
            count,
            question_set=selected_questions,
            mode="missed_review",
        )

    def get_due_questions(self):
        """Return questions whose latest answer is scheduled for review or was missed historically."""
        if not os.path.exists("history.json"):
            return []
        with open("history.json", "r", encoding="utf-8") as history_file:
            history = json.load(history_file)

        questions_by_identity = {
            (question.category, question.difficulty, question.question): question
            for question in self.all_questions()
        }
        latest_attempts = {}
        for attempt in history:
            attempt_date = attempt.get("date", date.today().isoformat())
            for item in attempt.get("answer_review", []):
                category = item.get("category")
                difficulty = item.get("difficulty")
                prompt = item.get("question")
                identity = (category, difficulty, prompt)
                if identity in questions_by_identity:
                    latest_attempts[identity] = (attempt_date, item)

        today = date.today().isoformat()
        due = []
        for identity, (attempt_date, item) in latest_attempts.items():
            next_review = item.get("next_review_date")
            # Old history has no schedule; retain missed answers as immediately due.
            is_due = next_review <= today if next_review else not item.get("is_correct", False)
            if is_due:
                due.append(questions_by_identity[identity])
        return due

    def practice_due_questions(self):
        due_questions = self.get_due_questions()
        if not due_questions:
            window = tk.Tk()
            window.withdraw()
            messagebox.showinfo("Smart review", "Nothing is due for review today. Your next review will appear here.", parent=window)
            window.destroy()
            return
        window = tk.Tk()
        window.withdraw()
        count = simpledialog.askinteger(
            "Smart review",
            f"{len(due_questions)} question(s) are due. How many would you like to review?",
            parent=window,
            minvalue=1,
            maxvalue=len(due_questions),
            initialvalue=len(due_questions),
        )
        window.destroy()
        if count is None:
            return
        selected = self.select_weighted_questions(due_questions, count)
        self.start_quiz(
            "Smart Review",
            "Mixed",
            count,
            question_set=selected,
            mode="smart_review",
        )

    def show_progress_dashboard(self):
        if not os.path.exists("history.json"):
            history = []
        else:
            with open("history.json", "r", encoding="utf-8") as history_file:
                history = json.load(history_file)

        total_score = sum(attempt.get("score", 0) for attempt in history)
        total_marks = sum(attempt.get("total_marks", 0) for attempt in history)
        overall = total_score / total_marks * 100 if total_marks else 0
        by_category = {}
        by_difficulty = {}
        by_confidence = {}
        by_mistake_pattern = {}
        for attempt in history:
            for group, key in ((by_category, attempt.get("category", "Unknown")),
                               (by_difficulty, attempt.get("difficulty", "Unknown"))):
                stats = group.setdefault(key, [0, 0])
                stats[0] += attempt.get("score", 0)
                stats[1] += attempt.get("total_marks", 0)
            for item in attempt.get("answer_review", []):
                confidence = item.get("confidence")
                if confidence:
                    stats = by_confidence.setdefault(confidence, [0, 0])
                    stats[0] += int(bool(item.get("is_correct")))
                    stats[1] += 1
                mistake_pattern = item.get("mistake_pattern")
                if isinstance(mistake_pattern, str) and mistake_pattern in self.MISTAKE_PATTERN_LABELS:
                    by_mistake_pattern[mistake_pattern] = by_mistake_pattern.get(mistake_pattern, 0) + 1

        lines = [
            f"Quiz attempts: {len(history)}",
            f"Overall points accuracy: {overall:.1f}% ({total_score:g} / {total_marks:g})",
            f"Questions due for review: {len(self.get_due_questions())}",
            "",
            "By subject:",
        ]
        if by_category:
            for category, (score, marks) in sorted(by_category.items()):
                pct = score / marks * 100 if marks else 0
                lines.append(f"  {category}: {pct:.1f}% ({score:g} / {marks:g})")
        else:
            lines.append("  Complete a quiz to see subject progress.")
        lines.extend(["", "By difficulty:"])
        if by_difficulty:
            for difficulty, (score, marks) in sorted(by_difficulty.items()):
                pct = score / marks * 100 if marks else 0
                lines.append(f"  {difficulty}: {pct:.1f}% ({score:g} / {marks:g})")
        else:
            lines.append("  No attempts yet.")
        lines.extend(["", "Accuracy by confidence:"])
        if by_confidence:
            labels = {"sure": "Sure", "somewhat": "Somewhat sure", "guess": "Guessed"}
            for confidence in ("sure", "somewhat", "guess"):
                if confidence in by_confidence:
                    correct, answered = by_confidence[confidence]
                    lines.append(f"  {labels.get(confidence, confidence)}: {correct}/{answered} correct")
        else:
            lines.append("  Confidence data will appear after your next quiz.")
        lines.extend(["", "Mistake patterns (self-reported):"])
        if by_mistake_pattern:
            for pattern, count in sorted(by_mistake_pattern.items(), key=lambda item: (-item[1], item[0])):
                label = self.MISTAKE_PATTERN_LABELS[pattern]
                lines.append(f"  {label}: {count}")
        else:
            lines.append("  No mistake patterns recorded yet. They appear after you tag a wrong answer.")
        lines.extend(["", "Recent quiz scores:"])
        for attempt in history[-8:]:
            lines.append(f"  {attempt.get('date', 'Unknown date')}: {attempt.get('percentage', 0):.1f}% — {attempt.get('category', 'Mixed')}")

        opinion_entries, opinion_error = self.load_opinion_entries()
        lines.extend(["", "Writing practice — Today’s Take:"])
        if opinion_error:
            lines.append(f"  Writing history could not be read: {opinion_error}")
        elif opinion_entries:
            latest_scores = [
                entry.get("revisions", [])[-1].get("score", 0)
                for entry in opinion_entries
                if entry.get("revisions")
            ]
            average_score = sum(latest_scores) / len(latest_scores) if latest_scores else 0
            lines.append(f"  Prompts completed: {len(opinion_entries)}")
            lines.append(f"  Average structure-signal score: {average_score:.1f}/10")
            lines.append("  Recent takes:")
            recent_entries = opinion_entries[-5:]
            recent_scores = []
            for entry in recent_entries:
                latest = entry.get("revisions", [])[-1] if entry.get("revisions") else {}
                recent_scores.append(latest.get("score", 0))
            if recent_scores:
                lines.append("  Score trend (older to newer): " + " → ".join(f"{score}/10" for score in recent_scores))
            for entry in recent_entries[::-1]:
                latest = entry.get("revisions", [])[-1] if entry.get("revisions") else {}
                attempt_date = str(latest.get("submitted_at") or entry.get("created_at") or "Unknown date")[:10]
                lines.append(
                    f"    {attempt_date}: "
                    f"{latest.get('score', 0)}/10 — {entry.get('topic', 'Topic')}"
                )
        else:
            lines.append("  No writing attempts yet. Try Today’s Take to begin.")

        window = tk.Tk()
        window.title("Progress dashboard")
        window.geometry("660x560")
        window.minsize(480, 380)
        tk.Label(
            window,
            text="Your progress",
            font=("Segoe UI", 18, "bold"),
            anchor="w",
            padx=18,
            pady=14,
        ).pack(fill="x")
        content = tk.Frame(window, padx=18, pady=4)
        content.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(content)
        scrollbar.pack(side="right", fill="y")
        report = tk.Text(content, wrap="word", font=("Segoe UI", 10), padx=12, pady=10,
                         yscrollcommand=scrollbar.set)
        report.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=report.yview)
        report.insert("end", "\n".join(lines))
        report.config(state="disabled")
        tk.Button(window, text="Close", command=window.destroy, padx=12, pady=6).pack(pady=(8, 16))
        window.mainloop()

    def load_opinion_entries(self):
        """Read separate writing history without disturbing quiz history."""
        if not os.path.exists(self.OPINION_HISTORY_FILE):
            return [], None
        try:
            with open(self.OPINION_HISTORY_FILE, "r", encoding="utf-8") as history_file:
                entries = json.load(history_file)
            if not isinstance(entries, list):
                return None, "the file does not contain a list of entries"
            if any(
                not isinstance(entry, dict)
                or not isinstance(entry.get("revisions", []), list)
                or any(
                    not isinstance(revision, dict)
                    or not isinstance(revision.get("criteria", []), list)
                    or any(not isinstance(item, dict) for item in revision.get("criteria", []))
                    for revision in entry.get("revisions", [])
                )
                for entry in entries
            ):
                return None, "one or more entries have an unsupported format"
            return entries, None
        except (OSError, json.JSONDecodeError) as error:
            return None, str(error)

    def save_opinion_entries(self, entries):
        """Write atomically so an interrupted save does not truncate prior work."""
        temporary_path = self.OPINION_HISTORY_FILE + ".tmp"
        try:
            with open(temporary_path, "w", encoding="utf-8") as history_file:
                json.dump(entries, history_file, ensure_ascii=False, indent=2)
            os.replace(temporary_path, self.OPINION_HISTORY_FILE)
            return None
        except OSError as error:
            try:
                if os.path.exists(temporary_path):
                    os.remove(temporary_path)
            except OSError:
                pass
            return str(error)

    @staticmethod
    def score_opinion_response(response):
        """Score only visible structure signals; never judge stance or factual truth."""
        text = response.strip()
        lowered = text.casefold()
        words = re.findall(r"\b[\w’'-]+\b", text)
        sentence_count = len(re.findall(r"[.!?]+(?:\s|$)", text))

        signal_groups = [
            {
                "name": "Clear view",
                "patterns": [r"\bi think\b", r"\bi believe\b", r"\bmy view is\b", r"\bi would argue\b", r"\bi feel\b", r"\bi prefer\b"],
                "advice": "State your view directly near the start, for example, “I think…” or “My view is…”.",
                "partial": "Your view is stated; make it more direct near the start of your response.",
                "strength": "Your response clearly signals your view.",
            },
            {
                "name": "Supporting reasons",
                "patterns": [r"\bbecause\b", r"\bsince\b", r"\bone reason\b", r"\bfor example\b", r"\bfor instance\b", r"\balso\b", r"\bfirst\b"],
                "advice": "Add a reason or a concrete example to support your view.",
                "partial": "You signaled a supporting reason; add another reason or a concrete example.",
                "strength": "You included wording that signals a supporting reason or example.",
            },
            {
                "name": "Explanation",
                "patterns": [r"\bthis means\b", r"\bthis shows\b", r"\bthis matters\b", r"\bas a result\b", r"\btherefore\b", r"\bwhich means\b", r"\bthis can lead to\b"],
                "advice": "Explain how your reason supports your view; add a sentence beginning with “This matters because…” or “This means…”.",
                "partial": "You started to explain a connection; make clear how it supports your view.",
                "strength": "You included a phrase that connects an idea to its meaning or result.",
            },
            {
                "name": "Another perspective",
                "patterns": [r"\bhowever\b", r"\balthough\b", r"\bon the other hand\b", r"\bsome people\b", r"\bothers may\b", r"\ba different view\b", r"\bwhile\b"],
                "advice": "Briefly recognize another reasonable perspective, then explain why you still hold your view.",
                "partial": "You acknowledged another perspective; add a short explanation of why you still hold your view.",
                "strength": "You signaled that another perspective may exist.",
            },
        ]

        results = []
        for group in signal_groups:
            matches = [pattern for pattern in group["patterns"] if re.search(pattern, lowered)]
            score = min(2, len(matches))
            if group["name"] == "Clear view" and matches and len(words) >= 20:
                score = 2
            results.append({
                "criterion": group["name"],
                "score": score,
                "detected_signals": len(matches),
                "feedback": group["strength"] if score == 2 else group["partial"] if score == 1 else group["advice"],
            })

        if len(words) >= 35 and sentence_count >= 2:
            clarity_score = 2
            clarity_feedback = "Your response has enough detail and sentence breaks to be easy to follow."
        elif len(words) >= 12 and sentence_count >= 1:
            clarity_score = 1
            clarity_feedback = "Add a little more detail and separate your main ideas into sentences."
        else:
            clarity_score = 0
            clarity_feedback = "Write at least a few complete sentences so your view and reasons are easier to follow."
        results.append({
            "criterion": "Clarity",
            "score": clarity_score,
            "detected_signals": int(len(words) >= 12) + int(sentence_count >= 2),
            "feedback": clarity_feedback,
        })

        score = sum(item["score"] for item in results)
        next_step = next((item["feedback"] for item in results if item["score"] < 2),
                         "Try adding a specific example or explaining the strongest reason behind your view.")
        return {"score": score, "criteria": results, "next_step": next_step}

    def start_todays_take(self):
        entries, error = self.load_opinion_entries()
        if error:
            window = tk.Tk()
            window.withdraw()
            messagebox.showerror(
                "Today’s Take",
                f"Your writing history could not be read, so it was left unchanged.\n\n{error}",
                parent=window,
            )
            window.destroy()
            return

        window = tk.Tk()
        window.title("Today’s Take")
        window.geometry("700x650")
        window.minsize(540, 500)
        state = {"prompt": random.choice(self.OPINION_PROMPTS), "entry": None}

        def clear_window():
            for widget in window.winfo_children():
                widget.destroy()

        def submit_response(response_box, influence_box):
            response = response_box.get("1.0", "end").strip()
            influence = influence_box.get("1.0", "end").strip()
            if not response:
                messagebox.showwarning("Add your view", "Write a response before submitting.", parent=window)
                return
            assessment = self.score_opinion_response(response)
            revision = {
                "submitted_at": datetime.now().isoformat(timespec="seconds"),
                "response": response,
                "thinking_note": influence,
                "score": assessment["score"],
                "criteria": assessment["criteria"],
                "next_step": assessment["next_step"],
            }
            entry = state["entry"]
            if entry is None:
                entry = {
                    "id": str(uuid.uuid4()),
                    "topic": state["prompt"][0],
                    "prompt": state["prompt"][1],
                    "created_at": revision["submitted_at"],
                    "revisions": [],
                }
                entries.append(entry)
                state["entry"] = entry
            entry["revisions"].append(revision)
            save_error = self.save_opinion_entries(entries)
            if save_error:
                entry["revisions"].pop()
                if not entry["revisions"]:
                    entries.remove(entry)
                    state["entry"] = None
                messagebox.showerror("Could not save response", f"Your response was not saved.\n\n{save_error}", parent=window)
                return
            render_feedback(revision)

        def render_challenge(response_text="", influence_text=""):
            clear_window()
            topic, prompt = state["prompt"]
            tk.Label(window, text="Today’s Take", font=("Segoe UI", 20, "bold"), anchor="w", padx=20, pady=14).pack(fill="x")
            tk.Label(window, text=topic.upper(), font=("Segoe UI", 9, "bold"), fg="#52606d", anchor="w", padx=22).pack(fill="x")
            tk.Label(window, text=prompt, font=("Segoe UI", 13), wraplength=650, justify="left", anchor="w", padx=22, pady=12).pack(fill="x")
            tk.Label(
                window,
                text="Share your view and why. The score checks writing signals only; it does not judge your opinion or verify facts.",
                font=("Segoe UI", 9), fg="#52606d", wraplength=650, justify="left", padx=22, pady=8,
            ).pack(fill="x")
            tk.Label(window, text="Your view and reasons", font=("Segoe UI", 10, "bold"), anchor="w", padx=22).pack(fill="x")
            response_box = tk.Text(window, height=9, wrap="word", font=("Segoe UI", 10), padx=10, pady=8)
            response_box.pack(fill="both", expand=True, padx=22, pady=(4, 12))
            response_box.insert("1.0", response_text)
            tk.Label(window, text="Optional: what shaped your thinking?", font=("Segoe UI", 10, "bold"), anchor="w", padx=22).pack(fill="x")
            influence_box = tk.Text(window, height=3, wrap="word", font=("Segoe UI", 10), padx=10, pady=6)
            influence_box.pack(fill="x", padx=22, pady=(4, 10))
            influence_box.insert("1.0", influence_text)
            button_text = "Save revision" if state["entry"] else "Get feedback"
            tk.Button(window, text=button_text, command=lambda: submit_response(response_box, influence_box), padx=14, pady=8).pack(pady=(0, 16))
            response_box.focus_set()

        def render_feedback(revision):
            clear_window()
            tk.Label(window, text="Your feedback", font=("Segoe UI", 20, "bold"), anchor="w", padx=20, pady=14).pack(fill="x")
            tk.Label(window, text=f"Structure-signal score: {revision['score']} / 10", font=("Segoe UI", 15, "bold"), fg="#175cd3", anchor="w", padx=22, pady=6).pack(fill="x")
            tk.Label(window, text="These checks look for wording patterns and sentence structure. They cannot judge whether your view is right, your evidence is true, or your reasoning is insightful.", font=("Segoe UI", 9), fg="#52606d", wraplength=650, justify="left", padx=22, pady=10).pack(fill="x")
            content = tk.Frame(window, padx=22)
            content.pack(fill="both", expand=True)
            scrollbar = tk.Scrollbar(content)
            scrollbar.pack(side="right", fill="y")
            feedback_box = tk.Text(content, wrap="word", font=("Segoe UI", 10), padx=10, pady=8, yscrollcommand=scrollbar.set)
            feedback_box.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=feedback_box.yview)
            feedback_box.insert("end", f"Topic: {state['prompt'][0]}\n{state['prompt'][1]}\n\nYour response:\n{revision['response']}\n\n")
            if revision.get("thinking_note"):
                feedback_box.insert("end", f"What shaped your thinking: {revision['thinking_note']}\n\n")
            for item in revision["criteria"]:
                feedback_box.insert("end", f"{item['criterion']}: {item['score']}/2\n")
                feedback_box.insert("end", f"Signal check: {item.get('detected_signals', 0)} wording cue(s) found.\n")
                feedback_box.insert("end", f"{item['feedback']}\n\n")
            feedback_box.insert("end", f"One next step: {revision['next_step']}\n")
            feedback_box.config(state="disabled")
            buttons = tk.Frame(window, padx=18, pady=12)
            buttons.pack(fill="x")
            tk.Button(buttons, text="Revise response", command=lambda: render_challenge(revision["response"], revision.get("thinking_note", "")), padx=10, pady=7).pack(side="left")
            tk.Button(buttons, text="Past takes", command=lambda: self.show_opinion_history(window), padx=10, pady=7).pack(side="left", padx=8)

            def next_prompt():
                if len(self.OPINION_PROMPTS) > 1:
                    choices = [prompt for prompt in self.OPINION_PROMPTS if prompt != state["prompt"]]
                    state["prompt"] = random.choice(choices)
                state["entry"] = None
                render_challenge()

            tk.Button(buttons, text="New topic", command=next_prompt, padx=10, pady=7).pack(side="right")
            tk.Button(buttons, text="Close", command=window.destroy, padx=10, pady=7).pack(side="right", padx=8)

        render_challenge()
        window.mainloop()

    def show_opinion_history(self, parent=None):
        entries, error = self.load_opinion_entries()
        if error:
            messagebox.showerror("Past takes", f"Writing history could not be read.\n\n{error}", parent=parent)
            return
        history_window = tk.Toplevel(parent) if parent is not None else tk.Tk()
        history_window.title("Past takes")
        history_window.geometry("720x560")
        history_window.minsize(520, 380)
        tk.Label(history_window, text="Past takes", font=("Segoe UI", 18, "bold"), anchor="w", padx=18, pady=14).pack(fill="x")
        frame = tk.Frame(history_window, padx=18, pady=4)
        frame.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        report = tk.Text(frame, wrap="word", font=("Segoe UI", 10), padx=12, pady=10, yscrollcommand=scrollbar.set)
        report.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=report.yview)
        if not entries:
            report.insert("end", "No writing attempts saved yet.")
        else:
            for entry in reversed(entries):
                revisions = entry.get("revisions", [])
                report.insert("end", f"{entry.get('topic', 'Topic')}\n")
                report.insert("end", f"{entry.get('prompt', '')}\n")
                if not revisions:
                    report.insert("end", "No response revisions saved.\n")
                for revision_number, revision in enumerate(revisions, start=1):
                    attempt_date = str(revision.get("submitted_at") or entry.get("created_at") or "Unknown date")[:10]
                    label = "First response" if revision_number == 1 else f"Revision {revision_number - 1}"
                    report.insert("end", f"\n{label} · {attempt_date} · {revision.get('score', 0)}/10\n")
                    if revision.get("response"):
                        report.insert("end", f"Response: {revision['response']}\n")
                    if revision.get("thinking_note"):
                        report.insert("end", f"What shaped the view: {revision['thinking_note']}\n")
                    for criterion in revision.get("criteria", []):
                        report.insert(
                            "end",
                            f"  {criterion.get('criterion', 'Criterion')}: {criterion.get('score', 0)}/2; "
                            f"{criterion.get('detected_signals', 0)} wording cue(s) found — "
                            f"{criterion.get('feedback', '')}\n",
                        )
                    if revision.get("next_step"):
                        report.insert("end", f"Next step: {revision['next_step']}\n")
                report.insert("end", "\n" + "─" * 48 + "\n\n")
        report.config(state="disabled")
        tk.Button(history_window, text="Close", command=history_window.destroy, padx=12, pady=6).pack(pady=(8, 16))
        if parent is None:
            history_window.mainloop()

    def get_timed_answer(self, question, question_number, is_retry=False):
        """Show a timed answer window; retries never expose the correct answer."""
        window = tk.Tk()
        window.title(f"{'Retry — ' if is_retry else 'Quiz — '}Question {question_number}")
        window.resizable(False, False)
        answer = {"value": ""}
        remaining = self.QUESTION_TIME_LIMIT

        tk.Label(
            window,
            text=f"Question {question_number}: {question.question}",
            wraplength=520,
            justify="left",
            font=("Segoe UI", 12),
            padx=20,
            pady=16,
        ).pack(fill="x")
        if is_retry:
            tk.Label(
                window,
                text="Second try — the correct answer is still hidden.",
                font=("Segoe UI", 10, "bold"),
                fg="#175cd3",
                padx=20,
                pady=4,
            ).pack(fill="x")
        timer_label = tk.Label(window, font=("Segoe UI", 11, "bold"), fg="#b42318")
        timer_label.pack(pady=(0, 8))
        answer_area = tk.Frame(window, padx=20, pady=8)
        answer_area.pack(fill="x")

        def finish(value=""):
            answer["value"] = value
            window.destroy()

        if question.question_type == "mcq":
            selected = tk.StringVar(value="")
            for option, value in question.options.items():
                tk.Radiobutton(
                    answer_area,
                    text=f"{option}. {value}",
                    variable=selected,
                    value=option,
                    anchor="w",
                    justify="left",
                    wraplength=500,
                ).pack(fill="x", anchor="w")
            tk.Button(
                window,
                text="Submit answer",
                command=lambda: finish(selected.get()),
            ).pack(pady=(4, 16))
        else:
            answer_entry = tk.Entry(answer_area, width=62, font=("Segoe UI", 11))
            answer_entry.pack(fill="x")
            answer_entry.focus_set()
            answer_entry.bind("<Return>", lambda _event: finish(answer_entry.get().strip()))
            tk.Button(
                window,
                text="Submit answer",
                command=lambda: finish(answer_entry.get().strip()),
            ).pack(pady=(4, 16))

        def tick():
            nonlocal remaining
            if not window.winfo_exists():
                return
            timer_label.config(text=f"Time remaining: {remaining} seconds")
            if remaining <= 0:
                finish()
                return
            remaining -= 1
            window.after(1000, tick)

        window.after(0, tick)
        window.mainloop()
        return answer["value"].strip()

    def ask_for_reasoning(self, question, user_answer, first_mistake_answer=None):
        """Collect the learner's approach and optional self-reported mistake pattern."""
        window = tk.Tk()
        window.title("Your thinking")
        window.geometry("620x590" if first_mistake_answer is not None else "600x410")
        window.minsize(480, 440 if first_mistake_answer is not None else 280)
        response = {"reasoning": "", "confidence": "somewhat", "mistake_pattern": None}
        answer_label = user_answer if user_answer else "No answer (time expired)"
        if first_mistake_answer is not None:
            first_label = first_mistake_answer or "No answer (time expired)"
            prompt = f"Your first try: {first_label}\n\nWhat were you thinking as you worked it out?"
        else:
            prompt = f"You answered: {answer_label}\n\nWhat were you thinking as you worked it out?"

        tk.Label(
            window,
            text=prompt,
            wraplength=550,
            justify="left",
            font=("Segoe UI", 11),
            padx=20,
            pady=16,
        ).pack(fill="x")
        reasoning_box = tk.Text(window, height=5, wrap="word", font=("Segoe UI", 10))
        reasoning_box.pack(fill="both", expand=True, padx=20, pady=(0, 12))
        confidence = tk.StringVar(value="somewhat")
        confidence_frame = tk.Frame(window, padx=20)
        confidence_frame.pack(fill="x", pady=(0, 10))
        tk.Label(confidence_frame, text="How confident were you?").pack(side="left", padx=(0, 10))
        for label, value in (("Sure", "sure"), ("Somewhat", "somewhat"), ("Guessed", "guess")):
            tk.Radiobutton(confidence_frame, text=label, variable=confidence, value=value).pack(side="left")

        mistake_pattern = tk.StringVar(value="")
        if first_mistake_answer is not None:
            tk.Label(
                window,
                text="What may have led to it? Choose one (optional).",
                font=("Segoe UI", 10, "bold"),
                anchor="w",
                padx=20,
            ).pack(fill="x", pady=(2, 4))
            pattern_frame = tk.Frame(window, padx=20)
            pattern_frame.pack(fill="x", pady=(0, 8))
            for value, label in self.MISTAKE_PATTERN_LABELS.items():
                tk.Radiobutton(
                    pattern_frame,
                    text=label,
                    variable=mistake_pattern,
                    value=value,
                    anchor="w",
                ).pack(anchor="w")
            tk.Radiobutton(
                pattern_frame,
                text="Skip",
                variable=mistake_pattern,
                value="",
                anchor="w",
            ).pack(anchor="w")

        def continue_to_feedback():
            response["reasoning"] = reasoning_box.get("1.0", "end-1c").strip()
            response["confidence"] = confidence.get()
            response["mistake_pattern"] = mistake_pattern.get() or None
            window.destroy()

        tk.Button(
            window,
            text="Show my feedback",
            command=continue_to_feedback,
            padx=12,
            pady=6,
        ).pack(pady=(0, 16))
        window.mainloop()
        return response

    def get_next_review_date(self, is_correct, confidence, was_retried=False):
        """Schedule recently missed or retried answers for an earlier check."""
        if not is_correct or was_retried:
            days_until_review = 1
        elif confidence == "guess":
            days_until_review = 1
        elif confidence == "somewhat":
            days_until_review = 3
        else:
            days_until_review = 7
        return (date.today() + timedelta(days=days_until_review)).isoformat()

    def get_numeric_difference(self, question, user_answer):
        """Return submitted minus correct value when both answers are numeric."""
        if question.question_type != "normal" or not user_answer.strip():
            return None

        def parse_number(value):
            normalized = value.strip().replace("−", "-").replace(",", "")
            if not re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:\s*/\s*[+-]?(?:\d+(?:\.\d*)?|\.\d+))?", normalized):
                return None
            try:
                return Fraction(normalized.replace(" ", ""))
            except (ValueError, ZeroDivisionError):
                return None

        submitted = parse_number(user_answer)
        correct = parse_number(question.answer)
        if submitted is None or correct is None:
            return None
        return submitted - correct

    def evaluate_answer(self, question, user_answer):
        """Grade exact, numeric, or rubric-based answers and retain actionable feedback."""
        if question.question_type == "mcq":
            return user_answer == question.answer, {"kind": "choice"}

        numeric_difference = self.get_numeric_difference(question, user_answer)
        if numeric_difference is not None:
            return numeric_difference == 0, {"kind": "numeric"}

        if question.feedback_criteria:
            answer_text = user_answer.casefold()
            matched = []
            missing = []
            for aliases in question.feedback_criteria:
                label = aliases[0]
                if any(self.contains_answer_phrase(answer_text, alias) for alias in aliases):
                    matched.append(label)
                else:
                    missing.append(label)
            analysis = {
                "kind": "key_ideas",
                "matched_key_ideas": matched,
                "missing_key_ideas": missing,
                "total_key_ideas": len(question.feedback_criteria),
            }
            return not missing, analysis

        return self.rules_to_check_answer(question, user_answer), {"kind": "exact"}

    @staticmethod
    def contains_answer_phrase(answer_text, phrase):
        normalized_phrase = phrase.casefold().strip()
        if not normalized_phrase:
            return False
        return re.search(r"(?<!\w)" + re.escape(normalized_phrase) + r"(?!\w)", answer_text) is not None

    def show_question_feedback(
        self,
        question,
        question_number,
        submitted_answer,
        correct_answer,
        is_correct,
        reasoning,
        numeric_difference,
        answer_analysis,
        confidence,
        next_review_date,
        first_submitted_answer=None,
        was_retried=False,
        mistake_pattern=None,
    ):
        """Show a correction immediately after the learner reflects on their answer."""
        window = tk.Tk()
        window.title(f"Feedback — Question {question_number}")
        window.geometry("700x540")
        window.minsize(500, 380)
        has_partial_key_ideas = (
            answer_analysis.get("kind") == "key_ideas"
            and bool(answer_analysis.get("matched_key_ideas"))
            and bool(answer_analysis.get("missing_key_ideas"))
        )
        if is_correct and was_retried:
            title, title_color = "Correct on your retry — nice recovery!", "#18794e"
        elif is_correct:
            title, title_color = "Correct — nice work!", "#18794e"
        elif has_partial_key_ideas:
            title, title_color = "Partly there — keep going", "#9a6700"
        else:
            title, title_color = "Let's work through it", "#b42318"

        tk.Label(
            window,
            text=title,
            font=("Segoe UI", 17, "bold"),
            fg=title_color,
            anchor="w",
            padx=18,
            pady=14,
        ).pack(fill="x")

        content_frame = tk.Frame(window, padx=18, pady=4)
        content_frame.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(content_frame)
        scrollbar.pack(side="right", fill="y")
        feedback_text = tk.Text(
            content_frame,
            wrap="word",
            font=("Segoe UI", 10),
            padx=12,
            pady=10,
            yscrollcommand=scrollbar.set,
        )
        feedback_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=feedback_text.yview)

        feedback_text.insert("end", f"Question\n{question.question}\n\n")
        if was_retried:
            feedback_text.insert("end", f"First try\n{first_submitted_answer}\n\n")
        feedback_text.insert("end", f"Your answer\n{submitted_answer}\n")
        if not is_correct:
            feedback_text.insert("end", f"Correct answer\n{correct_answer}\n")
        if numeric_difference is not None and numeric_difference != 0:
            gap = abs(numeric_difference)
            direction = "higher" if numeric_difference > 0 else "lower"
            gap_text = f"{float(gap):.4g} {direction}"
            correct_value = Fraction(question.answer)
            if correct_value != 0:
                percent = float(gap / abs(correct_value) * 100)
                gap_text += f" ({percent:.4g}% away)"
            feedback_text.insert("end", f"How far off: Your value is {gap_text} than the correct value.\n")
        elif answer_analysis.get("kind") == "key_ideas":
            matched = answer_analysis["matched_key_ideas"]
            missing = answer_analysis["missing_key_ideas"]
            total = answer_analysis["total_key_ideas"]
            coverage = round(len(matched) / total * 100) if total else 100
            feedback_text.insert("end", f"Key ideas found: {len(matched)} of {total} ({coverage}%).\n")
            if matched:
                feedback_text.insert("end", f"Already included: {', '.join(matched)}.\n")
            if missing:
                feedback_text.insert("end", f"Add or clarify: {', '.join(missing)}.\n")

        feedback_text.insert("end", "\nYour thinking\n")
        feedback_text.insert("end", f"{reasoning or 'You left this blank.'}\n\n")
        mistake_label = self.MISTAKE_PATTERN_LABELS.get(mistake_pattern)
        if mistake_label:
            feedback_text.insert("end", f"Your selected mistake pattern\n{mistake_label}\n\n")
        if is_correct:
            feedback_text.insert("end", "Keep using the same steps. Here is the reasoning to reinforce it:\n")
        else:
            feedback_text.insert(
                "end",
                f"Correction focus: {self.get_correction_guidance(reasoning, numeric_difference, answer_analysis)}\n",
            )
        feedback_text.insert("end", f"Worked explanation\n{question.explanation or 'No worked explanation has been added yet.'}\n\n")
        feedback_text.insert("end", f"Confidence: {confidence.title()} · review due: {next_review_date}\n")
        feedback_text.config(state="disabled")

        tk.Button(
            window,
            text="Next question",
            command=window.destroy,
            padx=12,
            pady=6,
        ).pack(pady=(8, 16))
        window.mainloop()

    def get_correction_guidance(self, reasoning, numeric_difference, answer_analysis=None):
        """Choose a small next step from the learner's reflection and numeric gap."""
        thought = reasoning.casefold()
        if any(word in thought for word in ("guess", "not sure", "unsure", "random")):
            return "You mentioned guessing or feeling unsure. Start again from the information in the question and write one small step at a time."
        if any(word in thought for word in ("round", "rounded", "approx")):
            return "You mentioned an approximation. Keep the exact value through the working, then round only at the end if the question asks for it."
        if numeric_difference is not None and numeric_difference > 0:
            return "Your value is too high. First check for an extra addition or multiplication, or a subtraction that was too small."
        if numeric_difference is not None and numeric_difference < 0:
            return "Your value is too low. First check for a missed addition or multiplication, or a subtraction that was too large."
        if answer_analysis and answer_analysis.get("missing_key_ideas"):
            missing = ", ".join(answer_analysis["missing_key_ideas"])
            return f"Add or correct these key ideas in your response: {missing}. Then compare them with the worked explanation."
        if not reasoning:
            return "Write down the first step you would try, then compare it with the first step in the worked solution."
        return "Compare your approach with the worked steps. Find the first point where they differ, then retry from that point."

    def show_answer_review(self, answer_review):
        review_window = tk.Tk()
        review_window.title("Quiz answer review")
        review_window.geometry("760x620")
        review_window.minsize(520, 400)

        tk.Label(
            review_window,
            text="Answer review",
            font=("Segoe UI", 18, "bold"),
            anchor="w",
            padx=18,
            pady=14,
        ).pack(fill="x")

        content_frame = tk.Frame(review_window, padx=18, pady=4)
        content_frame.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(content_frame)
        scrollbar.pack(side="right", fill="y")
        review_text = tk.Text(
            content_frame,
            wrap="word",
            font=("Segoe UI", 10),
            padx=12,
            pady=10,
            yscrollcommand=scrollbar.set,
        )
        review_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=review_text.yview)

        for question_number, item in enumerate(answer_review, start=1):
            analysis = item.get("answer_analysis", {})
            if item.get("retried") and item.get("retry_correct"):
                status = "Correct on retry"
            elif item.get("is_correct"):
                status = "Correct"
            elif analysis.get("kind") == "key_ideas" and analysis.get("matched_key_ideas"):
                status = "Partial credit"
            else:
                status = "Incorrect"
            review_text.insert("end", f"{question_number}. {item.get('question', 'Question')} · {status}\n")
            if item.get("retried"):
                review_text.insert("end", f"First try: {item.get('first_answer', '(no answer)')}\n")
                review_text.insert("end", f"Retry: {item.get('retry_answer', item.get('your_answer', '(no answer)'))}\n")
            else:
                review_text.insert("end", f"Your answer: {item.get('your_answer', '(no answer)')}\n")
            if not item.get("is_correct"):
                review_text.insert("end", f"Correct answer: {item.get('correct_answer', 'Not recorded')}\n")
            if item.get("reasoning"):
                review_text.insert("end", f"Your thinking: {item['reasoning']}\n")
            mistake_label = self.MISTAKE_PATTERN_LABELS.get(item.get("mistake_pattern"))
            if mistake_label:
                review_text.insert("end", f"Self-reported mistake pattern: {mistake_label}\n")
            if item.get("confidence"):
                review_text.insert("end", f"Confidence: {item['confidence'].title()}\n")
            if item.get("next_review_date"):
                review_text.insert("end", f"Next review due: {item['next_review_date']}\n")
            if analysis.get("kind") == "key_ideas":
                total = analysis.get("total_key_ideas", 0)
                matched = analysis.get("matched_key_ideas", [])
                missing = analysis.get("missing_key_ideas", [])
                coverage = round(len(matched) / total * 100) if total else 100
                review_text.insert("end", f"Key ideas covered: {len(matched)} of {total} ({coverage}%).\n")
                if missing:
                    review_text.insert("end", f"Still needed: {', '.join(missing)}.\n")
            difference = item.get("numeric_difference")
            if difference not in (None, 0):
                direction = "higher" if difference > 0 else "lower"
                review_text.insert("end", f"Your numeric answer was {abs(difference):.4g} {direction} than the correct value.\n")
            if item.get("explanation"):
                review_text.insert("end", f"How to reach it: {item['explanation']}\n")
            else:
                review_text.insert("end", "How to reach it: No explanation has been added yet.\n")
            review_text.insert("end", f"Result: {status}\n\n")

        review_text.config(state="disabled")
        tk.Button(
            review_window,
            text="Close review",
            command=review_window.destroy,
            padx=12,
            pady=6,
        ).pack(pady=(8, 16))
        review_window.mainloop()
        
 
 
                
       
 
                 
                 
                 
                 
 
             
                     
 
 
                         
    def get_marks(self,question): 
        marks = {"easy":2,"medium":4,"hard":6} 
        mark = marks[question.difficulty] 
        if question.question_type == "mcq": 
            mark = mark/2 
        return mark 
    def rules_to_check_answer(self,question,user_answer): 
          if question.question_type == "mcq": 
              return user_answer == question.answer 
          else: 
              numeric_difference = self.get_numeric_difference(question, user_answer)
              if numeric_difference is not None:
                  return numeric_difference == 0
              if question.difficulty == "easy": 
                  return user_answer.lower() == question.answer.lower() 
              elif question.difficulty == "medium": 
                  user_answer = " ".join(user_answer.split()) 
                  correct_answer = " ".join(question.answer.split()) 
                  return user_answer.lower() == correct_answer.lower() 
              else: 
                  return user_answer.strip() == question.answer.strip() 
 
    def get_total_marks(self): 
        total_marks = 0 
        for question in self.current_questions: 
            total_marks += self.get_marks(question) 
        return total_marks     
                   
    def save_history(self,category,difficulty,total_questions,correct_answers,wrong_answers,total_marks,percentage,answer_review=None,mode="standard"):
         
        if not os.path.exists("history.json"): 
                        with open("history.json", "w", encoding="utf-8") as f:
                            json.dump([], f) 
        with open("history.json","r", encoding="utf-8")as f:
                                history =json.load(f) 
                                
                                history.append({ 
                                "category": category, 
                                "difficulty": difficulty, 
                                "total_questions": total_questions, 
                                "correct_answers": correct_answers, 
                                "wrong_answers": wrong_answers, 
                                "score": self.score, 
                                "total_marks": total_marks, 
                                "percentage": percentage,
                                "answer_review": answer_review or [],
                                "date": date.today().isoformat(),
                                "mode": mode,
                                                          }) 
        with open("history.json", "w", encoding="utf-8") as f: 
            json.dump(history, f, indent=4) 
    def show_history(self): 
        quiz_counter =0 
        if not os.path.exists("history.json"): 
            with open("history.json","w", encoding="utf-8")as f: 
                json.dump([],f)   
        with open("history.json","r", encoding="utf-8")as f :  
            history = json.load(f)       
        if not history:
            print("No quiz attempts yet. Start a quiz to build your history.")
            return

        print(f"Daily challenge streak: {self.get_daily_streak(history)} day(s)")
        for quiz in history: 
            quiz_counter += 1 
 
            print(f"\n========== Quiz {quiz_counter} ==========") 
            print(f"Category: {quiz['category']}") 
            print(f"Difficulty: {quiz['difficulty']}") 
            print(f"Questions: {quiz['total_questions']}") 
            print(f"Correct: {quiz['correct_answers']}") 
            print(f"Wrong: {quiz['wrong_answers']}") 
            print(f"Score: {quiz['score']} / {quiz['total_marks']}") 
            print(f"Percentage: {quiz['percentage']}%") 
            if quiz.get("date"):
                print(f"Date: {quiz['date']}")
            if quiz.get("mode") == "daily_challenge":
                print("Mode: Daily challenge")

    def get_daily_streak(self, history=None):
        if history is None:
            if not os.path.exists("history.json"):
                return 0
            with open("history.json", "r", encoding="utf-8") as history_file:
                history = json.load(history_file)

        completed_days = {
            attempt.get("date")
            for attempt in history
            if attempt.get("mode") == "daily_challenge" and attempt.get("date")
        }
        today = date.today()
        current_day = today if today.isoformat() in completed_days else date.fromordinal(today.toordinal() - 1)
        streak = 0
        while current_day.isoformat() in completed_days:
            streak += 1
            current_day = date.fromordinal(current_day.toordinal() - 1)
        return streak
             
                 
 
 
 
 
 
 
 
 
           
                 
         
         
            
 
     
        
         
 
        
             
 
        
                                                                 
                                                                     
     
quiz = Quiz(bank)         
 
 
def admin_menu(bank): 
    while True: 
         
        choice = input(""" 
         ===== ADMIN MENU ===== 
                1. Add Question 
                2. Delete Question 
                3. Edit Question 
                4. Display Questions 
                5. find question 
                6.load questions 
                7.save_questions 
                8.Back 
                9.Export Question Bank
                10.Import Questions
                 
                """).strip() 
         
 
        if choice == "1": 
             
            new_question = input("Enter your question here") 
            new_answer = input("Enter your answer here or (option letter for mcq):") 
            new_category = input("Enter your category here:") 
            new_difficulty = input("Enter you difficulty here:") 
            new_question_type = input("Enter your question type here:").strip().lower() 
            new_explanation = input("Enter a short explanation showing how to reach the answer: ").strip()
            new_feedback_criteria = []
                 
            if new_question_type == "mcq": 
                options = input("Enter 4 options separated by commas: ").split(",") 
                options = [option.strip() for option in options] 
 
                new_options = { 
                    "A": options[0], 
                    "B": options[1], 
                    "C": options[2], 
                    "D": options[3] 
                                    } 
 
                new_answer = new_answer.strip().upper() 
 
                if new_answer not in new_options: 
                        print("Correct answer must be A, B, C, or D.") 
                         
                        continue 
            elif new_question_type == "normal": 
                    new_options = None 
                    criteria_text = input(
                        "Key ideas for written-answer feedback (required ideas separated by ;, accepted wording by |; Enter to skip): "
                    ).strip()
                    new_feedback_criteria = parse_feedback_criteria(criteria_text)
 
            else: 
                print("the question type must be in between(normal,mcq)")     
                continue 
                  
            question = Question(
                new_question,
                new_answer,
                new_category,
                new_difficulty,
                new_question_type,
                new_options,
                new_explanation,
                new_feedback_criteria,
            )
            bank.add_question(question) 
            print("the question has been sucesfully added::") 
                     
        elif choice == "2": 
            question_text =input("enetr your question here you want to delete") 
            bank.delete_question(question_text)  
            print("the question has been suceesfully deleted:") 
        elif choice == "3": 
            question_text = input("enter your question you want to edit") 
            question = bank.find_question(question_text) 
            if question is None: 
                print("the question isnt found :") 
            else: 
                menu = input(''' 
                            1:edit answer 
                            2:edit question 
                            3:edit category 
                            4:edit difficulty 
                            5.edit question type 
                            6.edit options 
                            7.edit explanation
                            8.edit written-answer key ideas
                            enter your number here''').strip() 
                if menu == "1": 
                    field = "answer" 
                    new_answer = input("enter the answer you want to change:") 
                    new_value = new_answer 
                    bank.edit_question(question,field,new_value) 
                    
                elif menu == "2": 
                    field = "question" 
                    new_question = input("enter the question you want to change :") 
                    new_value = new_question 
 
                    bank.edit_question(question,field,new_value) 
                elif menu == "3": 
                    field = "category" 
                    new_category = input("enter your new category here:") 
                    new_difficulty = input("enter you new difficulty here:") 
                    new_value = (new_category,new_difficulty) 
                    bank.edit_question(question,field,new_value) 
                 
                elif menu == "4": 
                    field = "difficulty" 
                    new_difficulty = input("enter your new difficulty here:") 
                    new_value = new_difficulty 
 
                    bank.edit_question(question,field,new_value) 
                elif menu == "5": 
                    field = "question_type" 
                    new_question_type = input('enter your new question type you want to change here:').strip().lower() 
                    if new_question_type == "normal": 
                        new_options = None 
                    elif  new_question_type == "mcq": 
                        while True: 
 
                            new_options = input("please enter four options separted by comas,").split(",") 
                            new_options = [option.strip() for option in new_options]
                            if len(new_options) != 4:
                                print("you must enter exactly enter four options") 
                                continue
                            new_options = { 
                                            "A":new_options[0], 
                                            "B":new_options[1], 
                                            "C":new_options[2], 
                                            "D":new_options[3] 
                                                            } 
                         
                            break 
                    new_value =(new_question_type,new_options) 
                    bank.edit_question(question,field,new_value) 
                                         
                    
                                         
                elif menu == '6': 
                    print       
                elif menu == "7":
                    new_explanation = input("Enter the worked explanation: ").strip()
                    bank.edit_question(question, "explanation", new_explanation)
                elif menu == "8":
                    criteria_text = input(
                        "Required ideas separated by ;, accepted wording by | (Enter to clear): "
                    ).strip()
                    bank.edit_question(
                        question,
                        "feedback_criteria",
                        parse_feedback_criteria(criteria_text),
                    )
                print("chages has been succesfully taken place:")     
        elif choice == "4": 
            bank.display_questions() 
        elif choice == "5": 
            question_text = input("enter your question here you want find").strip() 
            result = bank.find_question(question_text) 
            if result is None: 
                print("the question  isnt there")  
            else: 
                print("the question was found") 
                print(result)  
        elif choice == "6": 
            bank.load_questions() 
            print("Questions loaded successfully.") 
 
        elif choice == "7": 
            bank.save_questions() 
            print("Questions saved successfully.") 
 
        elif choice == "8": 
             
            bank.save_questions() 
            print("goodbye") 
            break       

        elif choice == "9":
            export_path = choose_question_file(save=True)
            if export_path:
                try:
                    bank.export_questions(export_path)
                    print(f"Question bank exported to {export_path}")
                except OSError as error:
                    print(f"Could not export questions: {error}")

        elif choice == "10":
            import_path = choose_question_file()
            if import_path:
                try:
                    imported, skipped = bank.import_questions(import_path)
                    bank.save_questions()
                    print(f"Imported {imported} question(s); skipped {skipped} duplicate(s).")
                except (OSError, ValueError) as error:
                    print(f"Could not import questions: {error}")
 
        else : 
            print("inavlid choice:") 
                        
 
 
 
 
 
def player_menu(quiz,question_bank): 
    while True: 
        choice = input(""" 
        ===== PLAYER MENU ===== 
 
        1. Start Quiz 
        2. Daily Challenge 
        3. Practise Missed Questions
        4. Smart Review (due questions)
        5. Progress Dashboard
        6. Show History
        7. Today’s Take
        8. Past Takes
        9. Back 
 
        Enter your choice: """).strip() 
 
        if choice == "1":
            for category in question_bank.questions: 
                print(category) 
            selected_category =input("enter your category here you want to answer questions:").strip()
            if selected_category not in question_bank.questions:
                print('the category doesnt exist so restarting again :')
                continue
            for difficulties in question_bank.questions[selected_category]: 
                print(f"the available difficulties are {difficulties}") 
            selected_difficulty =input("enter your difficulty here you want to answer questions:").strip()
            if selected_difficulty not in question_bank.questions[selected_category]:
                print("the difficulty doesnt exist  restarting again :")
                continue 
            
                
             
            try:
                selected_question_no = int(input("Enter the number of questions: ").strip())
            except ValueError:
                print("Enter a whole number of questions.")
                continue
            if selected_question_no < 1:
                print("Choose at least one question.")
                continue
            quiz.start_quiz(selected_category,selected_difficulty,selected_question_no) 
           
            
           
           
            

 
        elif choice == "2": 
            quiz.start_daily_challenge()
 
        elif choice == "3": 
            quiz.practice_missed_questions()

        elif choice == "4":
            quiz.practice_due_questions()

        elif choice == "5":
            quiz.show_progress_dashboard()

        elif choice == "6":
            quiz.show_history()

        elif choice == "7":
            quiz.start_todays_take()

        elif choice == "8":
            quiz.show_opinion_history()

        elif choice == "9":
            break 
 
        else: 
            print("Invalid choice.") 
 
 
question_bank = Question_bank()         
 
                  
    
             
             
 
             
            
def main_menu(bank, quiz): 
    while True: 
        choice = input(""" 
        ========== QUIZ APP ========== 
 
        1. Admin Menu 
        2. Player Menu 
        3. Exit 
 
        Enter your choice: """).strip() 
 
        if choice == "1": 
            admin_menu(bank) 
 
        elif choice == "2": 
            player_menu(quiz,bank) 
 
        elif choice == "3": 
            print("Exiting quiz...") 
            break 
 
        else: 
            print("Invalid choice.") 
               
 
         
question_bank = Question_bank()

question_bank.load_questions()

quiz = Quiz(question_bank)

if __name__ == "__main__":
    main_menu(question_bank, quiz)
