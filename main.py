import pandas as pd
from fpdf import FPDF

# Load data
input_data="./src/student_scores.xlsx"
data =pd.read_excel(input_data)

#gets college details
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

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.image(self.college_logo, 10, 8, 30)

        self.set_xy(45, 10)  # Position next to the logo
        self.set_font('Arial', 'B', 18)
        self.cell(0, 10, self.college_name, ln=True)
        
        self.set_xy(35, 18)  # Position directly below the college name
        self.set_font('Arial', '', 12)
        self.cell(0, 10, self.college_address, 0,0,'C')
        self.ln(10)


        #add department name
        self.set_xy(20, 30)
        self.set_font('Arial', 'B', 13)
        self.cell(0, 10, "DEPARTMENT OF COMPUTER SCIENCE\n\n", ln=True, align="C")

        self.set_xy(20, 43)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, "PROGRESS REPORT", ln=True, align="C")
        # Add a line break for separation
        
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'ABC MANAGEMENT ', 0, 0, 'C')
    
    def add_intro_message(self, student_name, usn):
        # Position message under header
        self.set_y(66)
        self.set_x(10)
        
        # Add introductory message
        self.set_font("Times", "", 12)
        intro_message = (
            "To\n"
            f"Parent of {student_name}\n"
            "Dear Sir/Madam,\n"
            f"     I am here with furnishing the progress report of your ward Mr./Ms. {student_name} "
            f"USN: {usn} for the Internal Assessment Examination as under. "
            "You are hereby requested to go through the report and give us your feedback.\n"
        )
        
        # Multicell allows for line breaks and paragraph formatting
        self.multi_cell(0, 10, intro_message)
        self.ln(10)
    
    #create marks table
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
        self.ln(10)  # Add some space after the marks table
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Remarks:", ln=True)

        self.set_font("Arial", "", 12)
        self.cell(0, 10, "_" * 80, ln=True)  # Empty line for remarks
        self.cell(0, 10, "_" * 80, ln=True)  # Additional line for longer remarks if needed
        self.cell(0, 10, "_" * 50, ln=True)  # Additional line for longer remarks if needed

# Add signature section
        self.ln(15)  # Space before the signatures

        self.cell(0, 10, "Signature of Parent", 0, 0, "L")  # Left-aligned for Parent signature
        self.cell(0, 10, "Signature of Counselor", 0, 0, "R")  # Right-aligned for Counselor signature


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
    pdf.add_remarks()
    #creating pdf output
    output_directory = "./generated_pdf/"
    output_file = f"{output_directory}{usn}.pdf"
    pdf.output(output_file)
    print(f"Generated report card for {name}: {output_file}")