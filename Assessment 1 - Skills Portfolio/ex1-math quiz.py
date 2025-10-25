import tkinter as tk
from tkinter import messagebox
import random

class MathQuiz:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Math Quiz Game")
        self.window.geometry("400x300")
        
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.difficulty = None
        self.first_attempt = True
        
        self.create_widgets()
        self.show_difficulty_menu()
    
    def create_widgets(self):
        # Main frame
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(pady=20)
        
        # the difficulty selection frame
        self.difficulty_frame = tk.Frame(self.main_frame)
        
        # the Question frame
        self.question_frame = tk.Frame(self.main_frame)
        
        # the Rsults frame
        self.results_frame = tk.Frame(self.main_frame)
        
        # Widgets for a difficulty selection
        self.difficulty_label = tk.Label(self.difficulty_frame, text="Choose your difficulty level:", font=("Arial", 14))
        self.difficulty_label.pack(pady=10)
        
        self.easy_btn = tk.Button(self.difficulty_frame, text="Easy (1-digit numbers)", command=lambda: self.set_difficulty("easy"))
        self.easy_btn.pack(pady=5)
        
        self.moderate_btn = tk.Button(self.difficulty_frame, text="Moderate (2-digit numbers)", command=lambda: self.set_difficulty("moderate"))
        self.moderate_btn.pack(pady=5)
        
        self.advanced_btn = tk.Button(self.difficulty_frame, text="Advanced (4-digit numbers)", command=lambda: self.set_difficulty("advanced"))
        self.advanced_btn.pack(pady=5)
        
        # widgets for the questions
        self.question_label = tk.Label(self.question_frame, text="", font=("Arial", 20))
        self.question_label.pack(pady=20)
        
        self.answer_entry = tk.Entry(self.question_frame, font=("Arial", 14), width=10)
        self.answer_entry.pack(pady=10)
        
        self.submit_btn = tk.Button(self.question_frame, text="Submit Answer", command=self.check_answer)
        self.submit_btn.pack(pady=10)
        
        self.score_label = tk.Label(self.question_frame, text="Score: 0")
        self.score_label.pack()
        
        # the widgets for the results
        self.results_label = tk.Label(self.results_frame, text="", font=("Arial", 13))
        self.results_label.pack(pady=20)
        
        self.play_again_btn = tk.Button(self.results_frame, text="Play Again", command=self.restart_quiz)
        self.play_again_btn.pack(pady=10)
    
    def show_difficulty_menu(self):
        self.question_frame.pack_forget()
        self.results_frame.pack_forget()
        self.difficulty_frame.pack()
    
    def set_difficulty(self, level):
        self.difficulty = level
        self.start_quiz()
    
    def start_quiz(self):
        self.difficulty_frame.pack_forget()
        self.question_frame.pack()
        self.score = 0
        self.current_question = 0
        self.next_question()
    
    def randomInt(self):
        if self.difficulty == "easy":
            return random.randint(0, 9)
        elif self.difficulty == "moderate":
            return random.randint(10, 99)
        else:  # advanced
            return random.randint(1000, 9999)
    
    def decideOperation(self):
        return random.choice(['+', '-'])
    
    def displayProblem(self):
        num1 = self.randomInt()
        num2 = self.randomInt()
        operation = self.decideOperation()
        
        # For subtraction no negative answers
        if operation == '-' and num1 < num2:
            num1, num2 = num2, num1
        
        self.current_num1 = num1
        self.current_num2 = num2
        self.current_operation = operation
        
        question_text = f"{num1} {operation} {num2} = ?"
        self.question_label.config(text=question_text)
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
    
    def isCorrect(self, answer):
        if self.current_operation == '+':
            correct_answer = self.current_num1 + self.current_num2
        else:
            correct_answer = self.current_num1 - self.current_num2
        
        return int(answer) == correct_answer
    
    def check_answer(self):
        user_answer = self.answer_entry.get()
        
        if not user_answer:
            messagebox.showwarning("no", "Please enter the answer!")
            return
        
        try:
            user_answer = int(user_answer)
        except ValueError:
            messagebox.showwarning("no!", "Please enter thr number!")
            return
        
        if self.isCorrect(user_answer):
            if self.first_attempt:
                self.score += 10
                messagebox.showinfo("true!", "Good job! +10 points more")
            else:
                self.score += 5
                messagebox.showinfo("true!", "You smashed it! +5 points more")
            
            self.current_question += 1
            self.first_attempt = True
            self.next_question()
        else:
            if self.first_attempt:
                self.first_attempt = False
                messagebox.showwarning("false!", "Try one more time please!")
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus()
            else:
                messagebox.showerror("false!", f"Sorry, the correct answer was {self.current_num1 + self.current_num2 if self.current_operation == '+' else self.current_num1 - self.current_num2}")
                self.current_question += 1
                self.first_attempt = True
                self.next_question()
    
    def next_question(self):
        self.score_label.config(text=f"Score: {self.score} | Question: {self.current_question + 1}/{self.total_questions}")
        
        if self.current_question < self.total_questions:
            self.displayProblem()
        else:
            self.show_results()
    
    def displayResults(self):
        percentage = (self.score / 100) * 100
        
        if percentage >= 90:
            grade = "A+ - Excellent!"
        elif percentage >= 80:
            grade = "A - Great job!"
        elif percentage >= 70:
            grade = "B - Good work!"
        elif percentage >= 60:
            grade = "C - Not bad!"
        else:
            grade = "Need more practice!*"
        
        return f"Final Score: {self.score}/100\nGrade: {grade}"
    
    def show_results(self):
        self.question_frame.pack_forget()
        self.results_frame.pack()
        
        results_text = self.displayResults()
        self.results_label.config(text=results_text)
    
    def restart_quiz(self):
        self.results_frame.pack_forget()
        self.show_difficulty_menu()
    
    def run(self):
        self.window.mainloop()

# Start the quiz
if __name__ == "__main__":
    quiz = MathQuiz()
    quiz.run()