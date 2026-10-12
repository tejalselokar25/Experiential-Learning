import os
import math
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

BOOKS_FILE = "books.csv"
EMPLOYEE_FILE = "employee.xlsx"
NAMES_FILE = "names.txt"
WORD_FILE = "sample.txt"
WORD_COUNT_FILE = "word_counts.txt"

def prepare_files():
    if not os.path.exists(BOOKS_FILE):
        pd.DataFrame([
            ["Python Basics", "A. Sharma", "2nd", 2023, "TechPress", 350],
            ["Data Science Intro", "R. Verma", "1st", 2024, "LearnWell", 520],
            ["C++ Made Easy", "A. Sharma", "3rd", 2021, "TechPress", 280],
            ["AI for Beginners", "M. Rao", "1st", 2025, "FutureBooks", 650],
            ["Web Development", "S. Patil", "2nd", 2022, "LearnWell", 430]
        ], columns=["Title", "Author", "Edition", "Year", "Publisher", "Price"]).to_csv(BOOKS_FILE, index=False)
    if not os.path.exists(EMPLOYEE_FILE):
        pd.DataFrame([
            [1001, "Aarav Patil", "Automotive", "Developer"],
            [1002, "Diya Sharma", "Finance", "Analyst"],
            [1003, "Kabir Joshi", "Automotive", "Developer"],
            [1004, "Anaya Rao", "Healthcare", "Tester"],
            [1005, "Ishaan Deshmukh", "Automotive", "Manager"]
        ], columns=["Employee ID", "Employee Name", "Department", "Designation"]).to_excel(EMPLOYEE_FILE, index=False)
    if not os.path.exists(WORD_FILE):
        with open(WORD_FILE, "w", encoding="utf-8") as f:
            f.write("Python makes programming simple. Python supports data analysis and file handling.")
    if not os.path.exists(NAMES_FILE):
        with open(NAMES_FILE, "w", encoding="utf-8") as f:
            f.write("Aarav\nDiya\nKabir\nAnaya\n")

def marksheet():
    name = input("Student name: ").strip()
    department = input("Department: ").strip()
    year = input("Year: ").strip()
    semester = input("Semester: ").strip()
    section = input("Section: ").strip()
    roll = input("Roll number: ").strip()
    subjects = ["Subject 1", "Subject 2", "Subject 3", "Subject 4", "Subject 5"]
    marks = []
    for subject in subjects:
        while True:
            try:
                mark = float(input(f"Marks for {subject} (0-100): "))
                if 0 <= mark <= 100:
                    marks.append(mark)
                    break
                print("Enter marks between 0 and 100.")
            except ValueError:
                print("Enter a valid number.")
    total = sum(marks)
    percentage = total / 5
    if min(marks) < 40:
        grade = "F (Fail)"
    elif percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "E"
    print("\n========== STUDENT MARKSHEET ==========")
    print(f"Name: {name} | Roll No: {roll}")
    print(f"Department: {department} | Year: {year} | Semester: {semester} | Section: {section}")
    for subject, mark in zip(subjects, marks):
        print(f"{subject}: {mark:g}/100")
    print(f"Total: {total:g}/500\nPercentage: {percentage:.2f}%\nGrade: {grade}")
    with open("marksheet.txt", "a", encoding="utf-8") as f:
        f.write(f"{name},{roll},{department},{year},{semester},{section},{marks},{total},{percentage:.2f},{grade}\n")
    print("Marksheet saved in marksheet.txt")

def temperature_checker():
    try:
        t = float(input("Enter water temperature in Celsius: "))
        if t < -273.15:
            print("Invalid: below absolute zero.")
        elif t == -273.15:
            print("Absolute zero.")
        elif t < 0:
            print("Below freezing.")
        elif t == 0:
            print("Freezing point.")
        elif t < 100:
            print("Normal range.")
        elif t == 100:
            print("Boiling point.")
        else:
            print("Above boiling point.")
    except ValueError:
        print("Please enter a valid temperature.")

def number_lab():
    try:
        a, b, c = [int(input(f"Enter integer {i}: ")) for i in range(1, 4)]
        print("Largest number:", max(a, b, c))
        print("\nHello Students using while loop:")
        i = 0
        while i < 20:
            print("Hello Students")
            i += 1
        print("\nHello Students using for loop:")
        for _ in range(20):
            print("Hello Students")
        n = int(input("\nEnter n to calculate sum from 1 to n: "))
        if n < 1:
            print("n should be at least 1.")
        else:
            print("Sum:", sum(range(1, n + 1)))
    except ValueError:
        print("Enter valid integers.")

def dataframe_lab():
    df = pd.DataFrame({
        "name": ["Ajay", "Vijay", "Vivek", "Atharv", "Apurva", "Rupal", "Priyal", "Shrushti", "Vishal", "Pranay"],
        "score": [12.5, 9, 16.5, np.nan, 9, 20, 14.5, np.nan, 8, 19],
        "attempts": [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
        "qualify": ["yes", "no", "yes", "no", "no", "yes", "yes", "no", "no", "yes"]
    }, index=list("abcdefghij"))
    print("\nName and score columns:\n", df[["name", "score"]].to_string())
    print("\nScores from 15 to 20:\n", df[df["score"].between(15, 20)].to_string())
    print("\nRows with missing scores:\n", df[df["score"].isna()].to_string())
    df.loc["d", "score"] = 11.5
    print("\nAfter changing row d score to 11.5:\n", df.to_string())
    print("\nTotal examination attempts:", df["attempts"].sum())

def tuple_lab():
    try:
        values = tuple(map(int, input("Enter integers separated by spaces: ").split()))
        print("Tuple:", values)
        print("Number of items:", len(values))
        if values:
            print("Last item:", values[-1])
        print("Reverse order:", values[::-1])
        print("Contains 5:", "Yes" if 5 in values else "No")
        print("Sorted middle items:", tuple(sorted(values[1:-1])) if len(values) > 2 else ())
    except ValueError:
        print("Enter integers only.")

def functions_lab():
    def add(x, y=0):
        return x + y
    def circle_area(radius=1):
        return math.pi * radius * radius
    def reverse_string(value):
        return value[::-1]
    def square_and_root(value):
        return value * value, math.sqrt(value) if value >= 0 else None
    try:
        x = float(input("First number: "))
        y = float(input("Second number: "))
        r = float(input("Circle radius: "))
        word = input("Enter a string to reverse: ")
        n = int(input("Enter a non-negative integer for square/root: "))
        print("Sum:", add(x, y))
        print("Sum using default argument (one value):", add(x))
        print(f"Area of circle (keyword argument): {circle_area(radius=r):.2f}")
        print("Reversed string:", reverse_string(word))
        if n < 0:
            print("Square:", n*n, "| Square root is not real for a negative number.")
        else:
            sq, root = square_and_root(n)
            print("Square:", sq, "| Square root:", root)
    except ValueError:
        print("Enter valid numeric values.")

def bank_lab():
    balance = 25000.0
    today = datetime.now()
    transactions = [
        (today - timedelta(days=5), "Deposit", 5000.0),
        (today - timedelta(days=20), "Withdrawal", 1200.0),
        (today - timedelta(days=50), "Deposit", 3000.0),
        (today - timedelta(days=100), "Withdrawal", 800.0)
    ]
    while True:
        print("\n--- Demo Bank Account ---\n1. Current balance\n2. Last 1 month statement\n3. Last 3 months statement\n4. Current financial year statement\n5. Back to main menu")
        choice = input("Choose: ")
        if choice == "1":
            print(f"Current demo balance: Rs. {balance:.2f}")
        elif choice in ("2", "3", "4"):
            if choice == "2":
                cutoff = today - timedelta(days=30)
            elif choice == "3":
                cutoff = today - timedelta(days=90)
            else:
                cutoff = datetime(today.year if today.month >= 4 else today.year - 1, 4, 1)
            print("Date          Type        Amount (Rs.)")
            found = False
            for date, kind, amount in transactions:
                if date >= cutoff:
                    print(f"{date:%Y-%m-%d}  {kind:<10}  {amount:.2f}")
                    found = True
            if not found:
                print("No transactions in this period.")
            print("Note: This is sample/demo data.")
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def numpy_lab():
    try:
        values = list(map(int, input("Enter 9 integers separated by spaces: ").split()))
        if len(values) != 9:
            print("Exactly 9 integers are required.")
            return
        print(np.array(values).reshape(3, 3))
    except ValueError:
        print("Enter integers only.")

def books_lab():
    df = pd.read_csv(BOOKS_FILE)
    while True:
        print("\n--- Books CSV Report ---\n1. All books\n2. Search by author\n3. Search by publisher\n4. Cheapest and costliest book\n5. Sort by year and price\n6. Back")
        choice = input("Choose: ")
        if choice == "1":
            print(df.to_string(index=False))
        elif choice == "2":
            author = input("Author name: ").strip()
            result = df[df["Author"].str.contains(author, case=False, na=False)]
            print(result.to_string(index=False) if not result.empty else "No books found.")
        elif choice == "3":
            publisher = input("Publisher name: ").strip()
            result = df[df["Publisher"].str.contains(publisher, case=False, na=False)]
            print(result.to_string(index=False) if not result.empty else "No books found.")
        elif choice == "4":
            print("Cheapest book:\n", df.loc[[df["Price"].idxmin()]].to_string(index=False))
            print("Costliest book:\n", df.loc[[df["Price"].idxmax()]].to_string(index=False))
        elif choice == "5":
            print(df.sort_values(["Year", "Price"]).to_string(index=False))
        elif choice == "6":
            break
        else:
            print("Invalid choice.")

def file_lab():
    while True:
        print("\n--- File Handling ---\n1. Read text file\n2. Write names to file\n3. Count words and save counts\n4. Demonstrate file modes\n5. Back")
        choice = input("Choose: ")
        if choice == "1":
            with open(WORD_FILE, "r", encoding="utf-8") as f:
                print(f.read())
        elif choice == "2":
            names = input("Enter names separated by commas: ").split(",")
            with open(NAMES_FILE, "w", encoding="utf-8") as f:
                f.write("\n".join(name.strip() for name in names if name.strip()))
            print("Names saved to", NAMES_FILE)
        elif choice == "3":
            with open(WORD_FILE, "r", encoding="utf-8") as f:
                words = f.read().lower().split()
            counts = {}
            for word in words:
                clean = word.strip(".,!?;:\"'()")
                counts[clean] = counts.get(clean, 0) + 1
            with open(WORD_COUNT_FILE, "w", encoding="utf-8") as f:
                for word, count in sorted(counts.items()):
                    f.write(f"{word}: {count}\n")
            print("Word counts saved to", WORD_COUNT_FILE)
            print(open(WORD_COUNT_FILE, encoding="utf-8").read())
        elif choice == "4":
            with open("mode_demo.txt", "w", encoding="utf-8") as f:
                f.write("Created using w mode.\n")
            with open("mode_demo.txt", "a", encoding="utf-8") as f:
                f.write("Added using a mode.\n")
            with open("mode_demo.txt", "r", encoding="utf-8") as f:
                print("r mode:\n" + f.read())
            with open("mode_demo.txt", "r+", encoding="utf-8") as f:
                old = f.read()
                f.seek(0)
                f.write("Updated with r+ mode.\n" + old)
            print("Demonstrated r, w, a and r+ in mode_demo.txt")
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def employee_lab():
    df = pd.read_excel(EMPLOYEE_FILE)
    while True:
        print("\n--- Employee Excel Reports ---\n1. Automotive domain employees\n2. Search by employee ID\n3. All developers\n4. Show complete employee list\n5. Back")
        choice = input("Choose: ")
        if choice == "1":
            result = df[df["Department"].str.contains("Automotive", case=False, na=False)]
            print(result.to_string(index=False))
        elif choice == "2":
            try:
                emp_id = int(input("Employee ID: "))
                result = df[df["Employee ID"] == emp_id]
                print(result.to_string(index=False) if not result.empty else "Employee not found.")
            except ValueError:
                print("Enter a valid employee ID.")
        elif choice == "3":
            result = df[df["Designation"].str.contains("Developer", case=False, na=False)]
            print(result.to_string(index=False))
        elif choice == "4":
            print(df.to_string(index=False))
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def main():
    prepare_files()
    while True:
        print("""
========== PYTHON LAB TOOLKIT ==========
1. Student Marksheet
2. Water Temperature Checker
3. Number Problems and Loops
4. Pandas DataFrame Operations
5. Tuple Operations
6. Functions and Arguments
7. Bank Account Statement (Demo)
8. NumPy 3x3 Array
9. Books CSV Management
10. File Handling
11. Employee Excel Reports
0. Exit
""")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            marksheet()
        elif choice == "2":
            temperature_checker()
        elif choice == "3":
            number_lab()
        elif choice == "4":
            dataframe_lab()
        elif choice == "5":
            tuple_lab()
        elif choice == "6":
            functions_lab()
        elif choice == "7":
            bank_lab()
        elif choice == "8":
            numpy_lab()
        elif choice == "9":
            books_lab()
        elif choice == "10":
            file_lab()
        elif choice == "11":
            employee_lab()
        elif choice == "0":
            print("Thank you for using Python Lab Toolkit!")
            break
        else:
            print("Invalid choice. Select 0-11.")

if __name__ == "__main__":
    main()