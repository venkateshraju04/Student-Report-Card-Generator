import pandas as pd
from fpdf import FPDF
import os

# Load data
input_data="./src/student_scores.xlsx"
data =pd.read_excel(input_data)

#get college details from txt file
with open("./src/college_data.txt","r") as file:
    lines=file.readlines()
college_name=lines[0].strip()
college_logo=lines[1].strip()
college_address=lines[2].strip()


#course code to subject mapping
dict={
    "BMATS101":"MATHEMATICS I for CSE",
    "BPHYS102":"APPLIED PHYSICS",
    "BCS103":"OOP with JAVA",
    "BCS104":"PYTHON PROGRAMMING"
}

#create report card
class ReportCard(FPDF):
    def __init__(self,college_name,college_logo,college_address):
        super().__init__()
        self.college_name=college_name
        self.college_logo=college_logo
        self.college_address=college_address

    #adds college logo,name, address and dept
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.image(self.college_logo, 10, 8, 30)

        self.set_xy(45, 10)  
        self.set_font('Arial', 'B', 18)
        self.cell(0, 10, self.college_name, ln=True)
        
        self.set_xy(35, 18)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, self.college_address, 0,0,'C')
        self.ln(10)

        self.set_xy(20, 30)
        self.set_font('Arial', 'B', 13)
        self.cell(0, 10, "DEPARTMENT OF COMPUTER SCIENCE\n\n", ln=True, align="C")

        self.set_xy(20, 43)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, "PROGRESS REPORT", ln=True, align="C")
        
    #adds footer
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'ABC MANAGEMENT ', 0, 0, 'C')
    
    #adds intro message
    def add_intro_message(self, student_name, usn):
        self.set_y(66)
        self.set_x(10)
        self.set_font("Times", "", 12)
        intro_message = (
            "To\n"
            f"Parent of {student_name}\n"
            "Dear Sir/Madam,\n"
            f"     I am here with furnishing the progress report of your ward Mr./Ms. {student_name} "
            f"USN: {usn} for the Internal Assessment Examination as under. "
            "You are hereby requested to go through the report and give us your feedback.\n"
        )
        self.multi_cell(0, 10, intro_message)
        self.ln(10)
    
    #creates marks table
    def add_score_table(self, scores, subject_mapping):
        self.set_y(self.get_y() + 2)
        table_width = 160  
        margin = (self.w - table_width) / 2 # Center the table horizontally
        self.set_x(margin)
        self.set_font("Arial", "B", 11)
        self.cell(30, 10, "Subject Code", 1, 0, "C")
        self.cell(70, 10, "Subject", 1, 0, "C")
        self.cell(30, 10, "Marks Scored", 1, 0, "C")
        self.cell(30, 10, "Total Marks", 1, 1, "C")

        #table data
        self.set_font("Arial", size=11)
        for subject, score in scores.items():
            subject_name = subject_mapping.get(subject, "N/A")
            self.set_x(margin)
            self.cell(30, 10, subject, 1, 0, "C")      
            self.cell(70, 10, subject_name, 1, 0, "C")
            self.cell(30, 10, str(score), 1, 0, "C")    
            self.cell(30, 10, "50", 1, 1, "C")
    
    # Add Remarks section
    def add_remarks(self):
        self.ln(10)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Remarks:", ln=True)

        self.set_font("Arial", "", 12)
        self.cell(0, 10, "_" * 80, ln=True)
        self.cell(0, 10, "_" * 80, ln=True)  
        self.cell(0, 10, "_" * 50, ln=True)

        # Add signature section
        self.ln(15)
        self.cell(0, 10, "Signature of Parent", 0, 0, "L")     
        self.cell(0, 10, "Signature of Counselor", 0, 0, "R")

#creating output directory
output_directory = "generated_reports"
os.makedirs(output_directory)
output_path=os.path.join(os.getcwd(),output_directory)

# Generate report card for each student
for _, row in data.iterrows():
    usn=row["USN"]
    name=row["NAME"]
    scores=row[3:]

    
    pdf = ReportCard(
        college_name=college_name,
        college_logo=college_logo,
        college_address=college_address
    )

    pdf.add_page()
    # Add intro message
    pdf.add_intro_message(name, usn)
    #marks table
    pdf.add_score_table(scores, dict)
    # Add remarks section
    pdf.add_remarks()
    # Save the PDF to a file
    output_file = os.path.join(output_path,f"{usn}.pdf")
    pdf.output(output_file)
    print(f"Generated report card for {name}: {output_file}")