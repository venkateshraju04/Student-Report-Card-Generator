import os
import pandas as pd
from fpdf import FPDF
import tkinter as tk
from tkinter import filedialog, messagebox
import json

# Report Card Class
class ReportCard(FPDF):
    def __init__(self, college_name, college_logo, college_address,dept_name):
        super().__init__()
        self.college_name = college_name
        self.college_logo = college_logo
        self.college_address = college_address
        self.dept_name=dept_name

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.image(self.college_logo, 10, 8, 30)

        self.set_xy(5, 10)
        self.set_font('Arial', 'B', 18)
        self.cell(210, 10, self.college_name,ln=True, align="C")

        self.set_xy(0, 18)
        self.set_font('Arial', '', 12)
        self.cell(210, 10, self.college_address,ln=True, align="C")
        self.ln(10)

        self.set_font('Arial', 'B', 13)
        self.cell(0, 10, f"DEPARTMENT OF {self.dept_name}", ln=True, align="C")

        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, "PROGRESS REPORT", ln=True, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, self.college_name, 0, 0, 'C')

    def add_intro_message(self, student_name, usn):
        self.set_y(66)
        self.set_x(10)
        self.set_font("Times", "", 11)
        intro_message = (
            f"To\nParent Of {student_name}\nDear Sir/Madam,\n"
            f"     I am here with furnishing the progress report of your ward Mr./Ms. {student_name} "
            f"USN: {usn} for the Internal Assessment Examination as under. "
            "You are hereby requested to go through the report and give us your feedback.\n"
        )
        self.multi_cell(0, 10, intro_message)
        self.ln(10)

    def add_score_table(self, scores,subject_mappings):
        self.set_y(self.get_y() + 2)
        table_width = 160
        margin = (self.w - table_width) / 2
        self.set_x(margin)
        self.set_font("Times", "", 11)
        self.cell(30, 10, "Course Code", 1, 0, "C")
        self.cell(70, 10, "Course Title", 1, 0, "C")
        self.cell(30, 10, "Marks Scored", 1, 0, "C")
        self.cell(30, 10, "Max Marks", 1, 1, "C")

        self.set_font("Times", size=11)
        for subject, score in scores.items():
            subject_name = subject_mappings.get(subject, "N/A")
            self.set_x(margin)
            self.cell(30, 10, subject, 1, 0, "C")
            self.cell(70, 10, subject_name, 1, 0, "C")
            self.cell(30, 10, str(score), 1, 0, "C")
            self.cell(30, 10, "50", 1, 1, "C")

    def add_remarks(self):
        self.ln(10)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Remarks:", ln=True)
        self.set_font("Arial", "", 12)
        for _ in range(3):
            self.cell(0, 10, "_" * 80, ln=True)
        self.ln(15)
        self.cell(0, 10, "Signature of Parent", 0, 0, "L")
        self.cell(0, 10, "Signature of Counselor", 0, 0, "R")


# File Browsing Functions
def browse_file(entry_widget, file_types):
    file_path = filedialog.askopenfilename(filetypes=file_types)
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

def load_subject_mappings(file_path="subjects.json"):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "Subject mapping file not found!")
        return {}
# Report Generation
def generate_reports():
    college_name = entry_college.get().strip()
    college_address = entry_address.get().strip()
    college_logo = entry_logo.get().strip()
    excel_path = entry_excel.get().strip()
    dept_name = entry_dept.get().strip()

    if not all([college_name, college_address, college_logo, excel_path, dept_name]):
        messagebox.showerror("Error", "Please fill in all fields and select files.")
        return

    try:
       
        subject_mappings = load_subject_mappings()
        print(subject_mappings)
        data = pd.read_excel(excel_path)

        subject_codes=list(data.columns[3:])
        OUTPUT_DIR = "generated_reports"
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        for _, row in data.iterrows():
            usn = row["USN"]
            name = row["NAME"]
            scores = {subject: int(row[subject]) if pd.notna(row[subject]) else 0 for subject in subject_codes}


            pdf = ReportCard(college_name, college_logo, college_address,dept_name)
            pdf.add_page()
            pdf.add_intro_message(name, usn)
            pdf.add_score_table(scores, subject_mappings)
            pdf.add_remarks()

            output_file = os.path.join(OUTPUT_DIR, f"{usn}.pdf")
            pdf.output(output_file)

        messagebox.showinfo("Success", "Report cards generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI Setup
root = tk.Tk()
root.title("Report Card Generator")
root.geometry("450x220")

# Labels and Inputs
tk.Label(root, text="College Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_college = tk.Entry(root, width=40)
entry_college.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="College Address:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_address = tk.Entry(root, width=40)
entry_address.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="College Logo:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_logo = tk.Entry(root, width=30)
entry_logo.grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: browse_file(entry_logo, [("Image Files", "*.png;*.jpg;*.jpeg")])).grid(row=2, column=2, padx=5)

tk.Label(root, text="Excel File:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_excel = tk.Entry(root, width=30)
entry_excel.grid(row=3, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: browse_file(entry_excel, [("Excel Files", "*.xlsx")])).grid(row=3, column=2, padx=5)

tk.Label(root, text="Department Name").grid(row=4, column=0, padx=10, pady=5, sticky="w")
entry_dept = tk.Entry(root, width=40)
entry_dept.grid(row=4, column=1, padx=10, pady=5)
# Generate Button
tk.Button(root, text="Generate Reports", command=generate_reports, bg="green", fg="white").grid(row=5, columnspan=3, pady=15)

root.mainloop()
