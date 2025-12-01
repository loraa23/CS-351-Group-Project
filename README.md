# UIC Commuter & Schedule Optimization App

A full stack web application designed to help UIC students better manage their academic schedules, optimize commute planning using CTA/Metra data, and connect with peers who have similar class times for potential study groups.

---

# Overview

UIC is a commuter campus, and students often struggle to choose class times that align with train schedules and find peers with matching free time. This application streamlines that experience by providing:

- Automatic schedule parsing from a `.ics` calendar file  
- Chronologically sorted class schedules  
- Customized CTA/Metra commute suggestions  
- Study group recommendations based on overlapping schedules  
- A clean and intuitive user interface built in React  

---

# Features

### Schedule Upload & Parsing
- Upload your UIC schedule as a `.ics` file  
- The backend parses class events and stores them in the database  
- Events are automatically sorted by time using a Red-Black Tree
- The backend uses a custom parser to read each VEVENT block from the .ics file and convert it into an Event model instance.


### Commute Optimization
- Integrates with **Metra GTFS API**  
- Integrates with **CTA API**  
- Suggests best train/bus options based on class start and end times  

### Study Partner Matching
- Uses a Union-Find (Disjoint Set) structure  
- Groups students with similar class schedules or overlapping free time  
- Frontend displays your matching study group cluster  

### Authentication
- Register and login securely  
- Each user manages their own schedule  
- Passwords are stored using hashing  

---

# Tech Stack

### Frontend
- React  
- JavaScript  
- CSS  

### Backend
- Django
- SQLite  

### APIs
- Metra GTFS API  
- CTA API  

### Advanced Data Structures
- **Red-Black Tree** for event ordering  
- **Union-Find (Disjoint Set)** for study group clustering  

---

# System Architecture
- frontend/    → React interface  
- backend/     → Django backend  
- api/         → REST API endpoints  
- models.py    → Schedule, Event, StudentSchedule  
- services.py  → Event sorting + study group logic  
- rbtree.py    → Red-Black Tree  
- unionfind.py → Union-Find  
- myproject/   → Django settings  

React communicates with Django via REST API calls.
Backend handles file processing, time sorting, commute logic, and study group clustering.

---

# Backend Setup (Django)
 1. Navigate to the backend directory
    - cd backend
 2. Create a virtual environment
    - python -m venv venv
 3. Activate it
    - Windows
        - venv\Scripts\activate
    - Linux
        - source venv/bin/activate
 4. Install dependencies
    - pip install -r requirements.txt
 5. Apply migrations
    - python manage.py migrate
 6. Run the backend server
    - python manage.py runserver

Backend runs at:
http://127.0.0.1:8000

# Frontend Setup (React)
 1. Go to the frontend directory
    - cd frontend
2. Install dependencies
   - npm install
3. Start React development server
   - npm start

Frontend runs at:
http://localhost:3000

---

# Running the Full Application

In two separate terminals:

### Terminal 1 — Backend
cd backend
venv\Scripts\activate
python manage.py runserver

### Terminal 2 — Frontend
cd frontend
npm start

The React frontend will communicate with Django through:
http://127.0.0.1:8000/api/

---

# Data Models

### **Schedule**
Stores uploaded `.ics` files and connects them to a user.

### **Event**
Represents individual class blocks parsed from a user’s schedule.

### **StudentSchedule**
Links a user to their parsed list of Event objects for analysis and matching.

---

# Advanced Data Structures

## Red-Black Tree (Event Ordering)
Used to keep all class events sorted chronologically.  
Every time an event is parsed, it is inserted into the Red-Black Tree.  
The tree ensures efficient sorting and retrieval for schedule display.

We selected Red-Black Tree because it guarantees O(log n) insertion and retrieval, which is ideal for sorting events as soon as they are parsed.

## Union-Find (Study Group Matching)
Used to group students who share similar schedules or overlapping free time.  
Each student is treated as a node; overlapping schedules trigger unions.  
The resulting sets represent study groups with compatible availability.

We selected Union-Find because it efficiently groups users with similar schedules using near-constant-time operations.

---

# API Endpoints

### **POST /api/upload-schedule/**
Uploads and parses a `.ics` schedule file for the authenticated user.

### **GET /api/events/**
Returns all parsed events sorted in chronological order.

### **GET /api/study-groups/**
Returns groups of students formed using the Union-Find data structure.

### **POST /api/register/**
Registers a new user account.

### **POST /api/login/**
Authenticates an existing user.

---

# How the Application Works

### 1. Upload a `.ics` schedule  
File is saved and parsed into individual Event objects.

### 2. Events inserted into a Red-Black Tree  
The tree sorts events by time to build a chronological schedule.

### 3. Frontend retrieves sorted events  
React displays the user’s full schedule.

### 4. Commute suggestions generated  
Using CTA and Metra APIs for real-time or scheduled data.

### 5. Study group matching  
Union-Find clusters students with similar schedules.

---

# Third-Party API Usage

### Metra GTFS API
Provides train schedules and real-time commuter rail data.

### CTA Bus/Train API
Provides transportation options from Union Station/Ogilvie to UIC.

Local fallback data ensures functionality during API downtime.

---

# Team Members

**Lora** — Project Lead
**Rishi** — Backend
**Hibatul** — Frontend 

---
