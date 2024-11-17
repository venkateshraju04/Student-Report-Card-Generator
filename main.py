import pandas as pd
from fpdf import FPDF

# Load data
input_data="Book1.xlsx"
data =pd.read_excel(input_data)


#course code to subject mapping
dict={
    "BMATS101":"MATHS",
    "BPHYS102":"PHYSICS",
    "BCS103":"JAVA",
    "BCS104":"PYTHON"
}
#create report card
class ReportCard(FPDF):
    def __init__(self):
        super().__init__()

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Report Card', 0, 1, 'C')
    
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

    pdf = ReportCard()
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Name: {name}", ln=True)
    pdf.cell(0, 10, f"USN: {usn}", ln=True)

    #marks table
    pdf.add_score_table(scores, dict)
    #creating pdf output
    output_file = f"{usn}.pdf"
    pdf.output(output_file)
    print(f"Generated report card for {name}: {output_file}")