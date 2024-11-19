# Student Progress Report Generator
This Python-based **Student Progress Report Generator** allows educators and administrators to generate progress reports for students based on their scores, attendance, and other performance metrics. The tool processes data input in a structured format (e.g., CSV or Excel files) and outputs comprehensive reports for each student.
[![YouTube](http://i.ytimg.com/vi/fuCqdW8Zimk/hqdefault.jpg)](https://www.youtube.com/watch?v=fuCqdW8Zimk)
## Requirements

- Python 3.6 or above
- - Libraries:
  - `pandas` for data manipulation
  - `fpdf` for creating PDFs
    
## Steps To Run
- You can install the required libraries using the following command:
```bash 
pip install requirements.txt
```
- Add location of excel sheet containing marks in main.py
```bash
input_data="/your_excel_sheet.xlsx"
```
- Make required changes to college_data.txt such that  the firstt line contains the college name , 2nd line contains college logo location and last line should contain address of college
- run main.py
```bash
python main.py
```

## Implemenations yet to do
- Improve overall design of report card
- Develop simple GUI to make the process easy
- Add student attendance details
