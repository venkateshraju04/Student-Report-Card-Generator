import pandas as pd
from fpdf import FPDF

# Load data
input_data="Book1.xlsx"
data =pd.read_excel(input_data)

#gets college details
with open("college_data.txt","r") as file:
    lines=file.readlines()
college_name=lines[0].strip()
college_logo=lines[1].strip()
college_address=lines[2].strip()


#course code to subject mapping
dict={
    "BMATS101":"MATHS",
    "BPHYS102":"PHYSICS",
    "BCS103":"JAVA",
    "BCS104":"PYTHON"
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
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, self.college_name, ln=True)
        
        self.set_xy(45, 18)  # Position directly below the college name
        self.set_font('Arial', '', 10)
        self.cell(0, 10, self.college_address, ln=True)

        # Add a line break for separation
        self.ln(20)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'ABC MANAGEMENT ', 0, 0, 'C')
    
    #create marks table
    def add_score_table(self, scores, subject_mapping):
        table_width = 160  
        margin = (self.w - table_width) / 2  # Center the table horizontally
        self.set_y(80)  # Set vertical position for the table
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
    #marks table
    pdf.add_score_table(scores, dict)
    #creating pdf output
    
    output_file = f"{usn}.pdf"
    pdf.output(output_file)
    print(f"Generated report card for {name}: {output_file}")