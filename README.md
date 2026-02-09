# Student Management System (Flask + Python + JSON)

A simple Student Management System web application built using **Python**, **Flask**, and **JSON** for data storage. This project allows users to add, view, update, and delete student records through a web interface.

---

## 🔹 Project Description

This project is created to manage student details such as name, roll number, class, and other information. It uses Flask as a backend framework and stores data in a JSON file instead of a database.

This project is suitable for beginners who are learning Flask and backend development.

---

## 🔹 Features

* Add new student
* View all students
* View single student details
* Update student information
* Delete student record
* Data stored using JSON file

---

## 🔹 Technologies Used

* Python
* Flask
* HTML
* CSS 
* JSON (for data storage)

---

## 🔹 Project Structure


student-management-system/
│
├── app.py
├── students.json
├── templates/
│   ├── index.html
│   ├── add_student.html
│   ├── edit_student.html
│   └── view_students.html
└── static/
    └── style.css

---

## 🔹 How to Run This Project

### Step 1 : Clone the repository

git clone https://github.com/Premlata-code/STUDENT_MANAGEMENT SYSTEM.git

### Step 2 : Open project folder

cd STUDENT_MANAGEMENT SYSTEM

### Step 3 : Create virtual environment 

```
python -m venv venv
```

### Step 4 : Activate environment

Windows

```
venv\Scripts\activate
```

Mac / Linux

```
source venv/bin/activate
```

### Step 5 : Install dependencies

```
pip install flask
```

### Step 6 : Run the application

```
python app.py
```

### Step 7 : Open in browser

```
http://127.0.0.1:5000/
```

---

## 🔹 Main Routes

| Route        | Method    | Description       |
| ------------ | --------- | ----------------- |
| /            | GET       | Home page         |
| /add         | GET, POST | Add new student   |
| /students    | GET       | View all students |
| /edit/<id>   | GET, POST | Edit student      |
| /delete/<id> | GET       | Delete student    |

(Note: Route names may change based on your implementation.)

---

## 🔹 Data Storage

All student data is stored in a JSON file named:

```
students.json
```

---

## 🔹 Purpose of This Project

This project is created for learning and practice of:

* Flask framework
* CRUD operations
* File handling using JSON
* Backend development basics

---

## 🔹 Future Improvements

* Add authentication (login / signup)
* Use database (MySQL / SQLite)
* Add search and filter option
* Improve UI

---

## 🔹 Author

Premlata
Email: premlatarajput0001@gmail.com

GitHub : [https://github.com/Premlata-code]
---

## 🔹 Note

This is a beginner-friendly academic project developed for practice and learning purpose.
