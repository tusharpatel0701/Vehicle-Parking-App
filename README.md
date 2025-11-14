# 🚗 Vehicle Parking Management System  
### A Web-Based Real-Time Parking Slot Booking & Management Application

![Flask](https://img.shields.io/badge/Flask-black?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-blue?logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap5-purple?logo=bootstrap&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-lightgrey?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Full_Stack_Project-green)

---

## 🎥 Live Demo / Video  
🔗 **[Watch the Project Demo]**  

---

## 🎯 Project Objective  
The **Vehicle Parking Management System** is a full-stack web application designed to **automate parking slot booking, monitoring, and management**.

It allows:  
- Users to **book, release, and view parking slots** in real-time  
- Admins to **manage parking lots, track user activity, and access visual analytics**  

The system is built using **Flask**, **SQLAlchemy**, **Bootstrap**, and **Matplotlib**, following an MVC-style architecture for clean, modular development.

---

## 🧠 Key Features  

### 👤 User Features  
- 🔐 **User Registration & Login** (secured via Flask-Login)  
- 🅿️ **Book Parking Slots** with real-time status  
- 📄 **View Active & Past Bookings**  
- 🔓 **Release Parking Slots** instantly  
- 📊 **User-Level Pie Charts** summarizing booking activity  

### 🛠️ Admin Features  
- 🧑‍💼 **Registered User Management**  
- 🗂️ **Add/Edit Parking Lots & Slots**  
- 🚦 **Monitor Spot Availability & Status**  
- 📊 **Admin Dashboard** with Matplotlib charts  
- 🗃️ **Slot-Level Status Overview**  

### 🌟 Additional Highlights  
- 🎨 **Responsive UI** (Bootstrap 5)  
- 🗂️ **MVC Folder Structure**  
- 📈 **Integrated Analytics** (Matplotlib)  
- ⚡ **Lightweight Flask Backend**  

---

## 🧩 Technologies Used  
- **Backend:** Flask  
- **Database:** SQLite (via SQLAlchemy ORM)  
- **Templating:** Jinja2  
- **Frontend:** HTML, CSS, Bootstrap 5  
- **Charts:** Matplotlib  
- **Auth:** Flask-Login  

---

## 🏗️ Architecture Overview  
The project follows an MVC-inspired structure:

- **Controllers:** `controllers.py` – route handling & logic  
- **Models:** `models.py` – SQLAlchemy models  
- **Templates:** HTML + Jinja2 templates (`/templates`)  
- **Static Files:** CSS, JS, and chart images (`/static`)  

---

## ⚙️ Development Process  

### 1. Planning & Design  
- Identified modules for **User**, **Admin**, **Lot**, and **Slot** operations  
- Designed a relational database schema linking **ParkingSpot**, **User**, and **Lot**  
- Implemented real-time tracking with `status` fields  

### 2. Backend Development  
- Created secure authentication using Flask-Login  
- Implemented all CRUD and booking operations  
- Generated analytics using Matplotlib  

### 3. Frontend & UI  
- Built responsive pages using Bootstrap 5  
- Designed clean tables, forms, navigation, and dashboards  
- Optimized layout for smooth user/admin experience  

### 4. Testing & Improvements  
- Verified booking, release, and status updates  
- Ensured admin controls work properly  
- Improved UI for readability and responsiveness  

---

## 💡 Project Insights  
- **SQLAlchemy ORM** made complex relationships simple and clean  
- **Matplotlib visualizations** provide helpful usage insights  
- **Bootstrap 5** ensures a modern and responsive UI  
- Flask's flexibility makes this system scalable for future features  

---

## 📌 Future Improvements  
- Real-time updates using WebSockets  
- Payment integration for paid parking  
- QR-based entry/exit  
- Mobile app support  

---

## 👨‍💻 Developed By  
**Tushar Patel**  
Diploma Student – IIT Madras BS Degree Program  
📧 *23f3001555@ds.study.iitm.ac.in*  
