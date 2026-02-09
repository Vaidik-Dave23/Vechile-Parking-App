# 🚗 Vehicle Parking Management System

A **full-stack web application** designed to manage vehicle parking operations efficiently.  
Built using **Flask** for the backend and **Vue.js** for the frontend, the system provides secure authentication, parking lot and spot management, and reservation handling through RESTful APIs.

---

## 🧠 Project Overview

The Vehicle Parking Management System is designed with a **backend-first, scalable architecture**.  
It separates frontend and backend concerns while enabling smooth communication through REST APIs.

- Backend handles business logic, authentication, database operations, caching, and background tasks
- Frontend provides a responsive and reactive user interface using Vue.js
- Asynchronous processing improves performance and scalability

---

## ✨ Key Features

- 🔐 JWT-based user authentication and authorization  
- 🚘 Parking lot and parking spot management  
- 📅 Vehicle reservation system  
- ⚡ Asynchronous background task processing using Celery  
- 🧠 Redis-based caching and message brokering  
- 🧩 Modular and scalable backend architecture  
- 🌐 RESTful API design  
- 🖥️ Reactive frontend built with Vue.js  

---

## 🛠️ Tech Stack

### Backend
- Flask
- Flask-SQLAlchemy (ORM)
- Flask-JWT-Extended
- Celery
- Redis

### Frontend
- Vue.js
- HTML, CSS, JavaScript

### Database
- SQLite / PostgreSQL (configurable)

---

## ⚙️ Backend Architecture

- **Application Factory Pattern** for scalable Flask app creation  
- **Blueprints** for modular routing  
- **SQLAlchemy ORM** for relational database modeling  
- **Celery + Redis** for background jobs and async processing  
- **JWT Authentication** for secure API access  

This architecture ensures maintainability, scalability, and clean separation of concerns.

---

## 🚀 How to Run the Project

### 1️⃣ Clone the repository

git clone https://github.com/Vaidik-Dave23/vehicle-parking-app.git
cd vehicle-parking-app

### 2️⃣ Install dependencies
pip install -r requirements.txt

### 3️⃣ Set Python path
export PYTHONPATH=$PWD

### 4️⃣ Run the backend
python app.py

### 5️⃣ Run Frontend
npm run dev

## 📡 API Design

The backend exposes RESTful APIs that are consumed by the Vue.js frontend.

- Authentication APIs (Login / Register)

- Parking lot APIs

- Parking spot APIs

- Reservation APIs

All protected routes use JWT-based authentication.

🧠 What I Learned

- Designing scalable backend systems using Flask

- Structuring Python projects using packages and relative imports

- Implementing secure authentication with JWT

- Handling asynchronous tasks with Celery and Redis

- Integrating a Vue.js frontend with a Flask backend

- Writing clean, maintainable, and production-style code

🎯 Use Case

This project can be extended for:

Smart parking systems

Campus or office parking management

Real-time parking availability tracking

Admin dashboards and analytics

📌 Future Improvements

Role-based access control (Admin / User)

Real-time updates using WebSockets

Payment gateway integration

Dockerization for deployment

Cloud deployment (AWS / GCP)

👤 Author

Vaidik Dave
Backend & Full-Stack Developer
Focused on scalable systems, clean architecture, and real-world applications.
