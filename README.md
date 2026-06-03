📄 data_cleaning_visualization.py
The main Python script with 8 steps:
Step
What it does
Step 1
Creates raw dataset (200 students) with missing values, duplicates, outliers
Step 2
Explores raw data — shape, missing count, duplicates
Step 3
Removes 10 duplicate rows
Step 4
Fixes outlier ages (999, -5) → replaced with median
Step 5
Fills missing values with median/mode
Step 6
Standardizes Gender (male→Male, FEMALE→Female)
Step 7
Adds TotalScore & Percentage columns
Step 8
Creates 9 charts and saves dashboard
🖼️ dashboard.png
A 9-chart visual dashboard showing:
Chart
Purpose
Score Distribution
Histogram of Math, Science, English
Boxplot
Detect outliers in scores
Gender Distribution
Male vs Female count
Grade Pie Chart
% of A, B, C, D, F grades
Correlation Heatmap
Relationship between all scores
Attendance vs %
Scatter plot — more attendance = better %
Avg Score by Gender
Compare male vs female performance
Avg % by Grade
Which grade has highest percentage
Age Distribution
Age spread of students
📊 cleaned_student_data.csv
The cleaned dataset with 200 rows and 10 columns:
Column
Description
StudentID
Unique ID (1–200)
Age
Student age (outliers fixed)
Gender
Male / Female (standardized)
MathScore
30–100 (missing filled)
ScienceScore
30–100 (missing filled)
EnglishScore
30–100 (missing filled)
Attendance
50–100% (missing filled)
Grade
A / B / C / D / F
TotalScore
Math + Science + English
Percentage
TotalScore / 300 × 100
