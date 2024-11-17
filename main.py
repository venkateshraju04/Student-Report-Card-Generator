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
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

for _, row in data.iterrows():
    usn=row["USN"]
    name=row["NAME"]
    scores=row[3:]
    total=scores.sum()
    pdf = ReportCard()
    pdf.add_page()

    # Student name
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Name: {name}", ln=True)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"USN: {usn}", ln=True)

    # Subject scores
    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    pdf.cell(0, 10, "Scores:", ln=True)
    for subject, score in scores.items():
        pdf.cell(0, 10, f"  {subject}: {score}", ln=True)

    # Total and average
    pdf.ln(5)
    pdf.cell(0, 10, f"Total: {total}", ln=True)

    # Save the report card
    output_file = f"{usn}.pdf"
    pdf.output(output_file)
    print(f"Generated report card for {name}: {output_file}")