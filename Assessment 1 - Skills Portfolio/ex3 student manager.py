import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

class StudentManager:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Student Manager")
        self.window.geometry("900x600")
        
        self.students = []
        self.filename = "studentMarks.txt"
        self.load_students()
        
        self.create_widgets()
        self.show_all_students()
    
    def load_students(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    lines = file.readlines()
                    
                # the first line number
                num_students = int(lines[0].strip())
                
                # Reading eachone of tudent
                self.students = []
                for i in range(1, len(lines)):
                    if lines[i].strip():  # Skip empty lines
                        data = lines[i].strip().split(',')
                        if len(data) == 6:
                            student = {
                                "code": int(data[0]),
                                "name": data[1],
                                "course1": int(data[2]),
                                "course2": int(data[3]),
                                "course3": int(data[4]),
                                "exam": int(data[5])
                            }
                            self.students.append(student)
                
                print(f"Loaded {len(self.students)} students from file")
            else:
                
                self.students = [
                    {"code": 1345, "name": "John Curry", "course1": 8, "course2": 15, "course3": 7, "exam": 45},
                    {"code": 2345, "name": "Sam Sturtivant", "course1": 14, "course2": 15, "course3": 14, "exam": 77},
                    {"code": 9876, "name": "Lee Scott", "course1": 17, "course2": 11, "course3": 16, "exam": 99},
                    {"code": 3724, "name": "Matt Thompson", "course1": 19, "course2": 11, "course3": 15, "exam": 81},
                    {"code": 1212, "name": "Ron Herrema", "course1": 14, "course2": 17, "course3": 18, "exam": 66},
                    {"code": 8439, "name": "Jake Hobbs", "course1": 10, "course2": 11, "course3": 10, "exam": 43},
                    {"code": 2344, "name": "Jo Hyde", "course1": 6, "course2": 15, "course3": 10, "exam": 55},
                    {"code": 9384, "name": "Gareth Southgate", "course1": 5, "course2": 6, "course3": 8, "exam": 33},
                    {"code": 8327, "name": "Alan Shearer", "course1": 20, "course2": 20, "course3": 20, "exam": 100},
                    {"code": 2983, "name": "Les Ferdinand", "course1": 15, "course2": 17, "course3": 18, "exam": 92}
                ]
                self.save_students()  
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not load students: {str(e)}")
    
    def save_students(self):
        try:
            with open(self.filename, 'w') as file:
                # Write number of thr students
                file.write(f"{len(self.students)}\n")
                
                # Writinfge each student
                for student in self.students:
                    file.write(f"{student['code']},{student['name']},{student['course1']},{student['course2']},{student['course3']},{student['exam']}\n")
            
            print(f"Saved {len(self.students)} students to the file")
        except Exception as e:
            messagebox.showerror("Error", f"could not save the students: {str(e)}")
    
    def calculate_totals(self, student):
        course_total = student['course1'] + student['course2'] + student['course3']
        total_marks = course_total + student['exam']
        percentage = (total_marks / 160) * 100
        
        if percentage >= 70:
            grade = "A"
        elif percentage >= 60:
            grade = "B"
        elif percentage >= 50:
            grade = "C"
        elif percentage >= 40:
            grade = "D"
        else:
            grade = "F"
            
        return course_total, total_marks, percentage, grade
    
    def create_widgets(self):
        # the Title
        title_label = tk.Label(self.window, text="student Manager", 
                              font=("Arial", 22, "bold"))
        title_label.pack(pady=10)
        
        # the Menu buttons frame
        menu_frame = tk.Frame(self.window)
        menu_frame.pack(pady=10)
        
        #  buttons
        buttons = [
            ("1. View All Students", self.show_all_students),
            ("2. search Student", self.find_student),
            ("3. the Highest Score", self.show_highest),
            ("4. the Lowest Score", self.show_lowest),
            ("5. Sort the Students", self.sort_students),
            ("6. Add Student", self.add_student),
            ("7. Delete Student", self.delete_student),
            ("8. Update the Student", self.update_student)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(menu_frame, text=text, command=command, 
                           width=15, height=2, font=("Arial", 10))
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)
        
        # Results displayng
        self.results_frame = tk.Frame(self.window)
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for displaying students
        self.tree = ttk.Treeview(self.results_frame, 
                                columns=("Code", "Name", "Course1", "Course2", "Course3", "CourseTotal", "Exam", "Total", "Percentage", "Grade"), 
                                show="headings")
        
        # 
        columns = {
            "Code": "Student Code",
            "Name": "Student Name", 
            "Course1": "Course 1",
            "Course2": "Course 2",
            "Course3": "Course 3",
            "CourseTotal": "Course Total",
            "Exam": "Exam",
            "Total": "Total Marks",
            "Percentage": "Percentage",
            "Grade": "Grade"
        }
        
        for col, text in columns.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=70)
        
        self.tree.column("Name", width=120)
        self.tree.column("Percentage", width=80)
        
        # the Scrollbar
        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # 
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 
        self.summary_label = tk.Label(self.window, text="", font=("Arial", 12, "bold"))
        self.summary_label.pack(pady=5)
    
    def display_students(self, students_list):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        

        total_percentage = 0
        for student in students_list:
            course_total, total_marks, percentage, grade = self.calculate_totals(student)
            total_percentage += percentage
            
            self.tree.insert("", "end", values=(
                student['code'],
                student['name'],
                f"{student['course1']}/20",
                f"{student['course2']}/20", 
                f"{student['course3']}/20",
                f"{course_total}/60",
                f"{student['exam']}/100",
                f"{total_marks}/160",
                f"{percentage:.1f}%",
                grade
            ))
        
        # 
        if students_list:
            avg_percentage = total_percentage / len(students_list)
            self.summary_label.config(text=f"Total Students: {len(students_list)} | Average Percentage: {avg_percentage:.1f}%")
        else:
            self.summary_label.config(text="No students found")
    
    def show_all_students(self):
        self.display_students(self.students)
    
    def find_student(self):
        search_term = simpledialog.askstring("Find Student", "Enter student name or code:")
        if search_term:
            found_students = []
            for student in self.students:
                if (search_term.lower() in student['name'].lower() or 
                    search_term == str(student['code'])):
                    found_students.append(student)
            
            if found_students:
                self.display_students(found_students)
                messagebox.showinfo("Found", f"Found {len(found_students)} student(s)")
            else:
                messagebox.showinfo("Not Found", "No student found with that name or code.")
                self.show_all_students()
    
    def show_highest(self):
        if not self.students:
            messagebox.showinfo("No Data", "No student records available.")
            return
        
        highest_student = max(self.students, key=lambda s: self.calculate_totals(s)[2])
        self.display_students([highest_student])
        messagebox.showinfo("Highest Score", f"Highest scoring student: {highest_student['name']}")
    
    def show_lowest(self):
        if not self.students:
            messagebox.showinfo("No Data", "No student records available.")
            return
        
        lowest_student = min(self.students, key=lambda s: self.calculate_totals(s)[2])
        self.display_students([lowest_student])
        messagebox.showinfo("Lowest Score", f"Lowest scoring student: {lowest_student['name']}")
    
    def sort_students(self):
        if not self.students:
            messagebox.showinfo("No Data found", "student records not available.")
            return
        
        choice = simpledialog.askstring("Sort Students", "Sort by:\n1. Name (A-Z)\n2. Percentage (High-Low)\n3. Percentage (Low-High)\n4. Student Code")
        
        if choice == "1":
            sorted_students = sorted(self.students, key=lambda s: s['name'])
            messagebox.showinfo("Sorted", "Students sorted by name (A-Z)")
        elif choice == "2":
            sorted_students = sorted(self.students, key=lambda s: self.calculate_totals(s)[2], reverse=True)
            messagebox.showinfo("Sorted", "Students sorted by percentage (Highest first)")
        elif choice == "3":
            sorted_students = sorted(self.students, key=lambda s: self.calculate_totals(s)[2])
            messagebox.showinfo("Sorted", "Students sorted by percentage (Lowest first)")
        elif choice == "4":
            sorted_students = sorted(self.students, key=lambda s: s['code'])
            messagebox.showinfo("Sorted", "Students sorted by student code")
        else:
            return
        
        self.display_students(sorted_students)
    
    def add_student(self):
        # Creating the form
        add_window = tk.Toplevel(self.window)
        add_window.title("Add New Student")
        add_window.geometry("300x300")
        
        tk.Label(add_window, text="Student Name:").pack(pady=5)
        name_entry = tk.Entry(add_window, width=30)
        name_entry.pack(pady=5)
        
        tk.Label(add_window, text="Student Code:").pack(pady=5)
        code_entry = tk.Entry(add_window, width=30)
        code_entry.pack(pady=5)
        
        tk.Label(add_window, text="Course 1 Mark (0-20):").pack(pady=5)
        course1_entry = tk.Entry(add_window, width=30)
        course1_entry.pack(pady=5)
        
        tk.Label(add_window, text="Course 2 Mark (0-20):").pack(pady=5)
        course2_entry = tk.Entry(add_window, width=30)
        course2_entry.pack(pady=5)
        
        tk.Label(add_window, text="Course 3 Mark (0-20):").pack(pady=5)
        course3_entry = tk.Entry(add_window, width=30)
        course3_entry.pack(pady=5)
        
        tk.Label(add_window, text="Exam Mark (0-100):").pack(pady=5)
        exam_entry = tk.Entry(add_window, width=30)
        exam_entry.pack(pady=5)
        
        def save_new_student():
            try:
                new_student = {
                    "code": int(code_entry.get()),
                    "name": name_entry.get(),
                    "course1": int(course1_entry.get()),
                    "course2": int(course2_entry.get()),
                    "course3": int(course3_entry.get()),
                    "exam": int(exam_entry.get())
                }
                
                # 
                for student in self.students:
                    if student['code'] == new_student['code']:
                        messagebox.showerror("Error", "Student code already exists!")
                        return
                
                self.students.append(new_student)
                self.save_students()
                self.show_all_students()
                add_window.destroy()
                messagebox.showinfo("Success", f"Student {new_student['name']} added successfully!")
                
            except ValueError:
                messagebox.showerror("Error", " enter valid numbers for marks and code!")
        
        tk.Button(add_window, text="Save Student", command=save_new_student, bg="green", fg="white").pack(pady=10)
    
    def delete_student(self):
        search_term = simpledialog.askstring("delete the Student", "Enter student name or code to delete:")
        if search_term:
            for i, student in enumerate(self.students):
                if (search_term.lower() in student['name'].lower() or 
                    search_term == str(student['code'])):
                    
                    confirm = messagebox.askyesno("Confirm Delete", 
                                                f"Are you sure you want to delete the {student['name']} (Code: {student['code']})?")
                    if confirm:
                        self.students.pop(i)
                        self.save_students()
                        self.show_all_students()
                        messagebox.showinfo("Deleted", "Student record deleted successfully.")
                    return
            
            messagebox.showinfo("Not Found", "No student found with that name or code.")
    
    def update_student(self):
        search_term = simpledialog.askstring("Update Student", "Enter student name or code to update:")
        if search_term:
            for student in self.students:
                if (search_term.lower() in student['name'].lower() or 
                    search_term == str(student['code'])):
                    
                    # 
                    update_window = tk.Toplevel(self.window)
                    update_window.title(f"Update {student['name']}")
                    update_window.geometry("300x250")
                    
                    tk.Label(update_window, text="Student Name:").pack(pady=5)
                    name_entry = tk.Entry(update_window, width=30)
                    name_entry.insert(0, student['name'])
                    name_entry.pack(pady=5)
                    
                    tk.Label(update_window, text="Course 1 Mark:").pack(pady=5)
                    course1_entry = tk.Entry(update_window, width=30)
                    course1_entry.insert(0, str(student['course1']))
                    course1_entry.pack(pady=5)
                    
                    tk.Label(update_window, text="Course 2 Mark:").pack(pady=5)
                    course2_entry = tk.Entry(update_window, width=30)
                    course2_entry.insert(0, str(student['course2']))
                    course2_entry.pack(pady=5)
                    
                    tk.Label(update_window, text="Course 3 Mark:").pack(pady=5)
                    course3_entry = tk.Entry(update_window, width=30)
                    course3_entry.insert(0, str(student['course3']))
                    course3_entry.pack(pady=5)
                    
                    tk.Label(update_window, text="Exam Mark:").pack(pady=5)
                    exam_entry = tk.Entry(update_window, width=30)
                    exam_entry.insert(0, str(student['exam']))
                    exam_entry.pack(pady=5)
                    
                    def save_updates():
                        try:
                            student['name'] = name_entry.get()
                            student['course1'] = int(course1_entry.get())
                            student['course2'] = int(course2_entry.get())
                            student['course3'] = int(course3_entry.get())
                            student['exam'] = int(exam_entry.get())
                            
                            self.save_students()
                            self.show_all_students()
                            update_window.destroy()
                            messagebox.showinfo("Updated", "Student record updated successfully.")
                            
                        except ValueError:
                            messagebox.showerror("Error", "Please enter valid numbers for marks!")
                    
                    tk.Button(update_window, text="Save Changes", command=save_updates, bg="blue", fg="white").pack(pady=10)
                    return
            
            messagebox.showinfo("Not Found", "No student found with that name or code.")
    
    def run(self):
        self.window.mainloop()

# Start the student manager
if __name__ == "__main__":
    print("Starting Student Manager...")
    app = StudentManager()
    app.run()
