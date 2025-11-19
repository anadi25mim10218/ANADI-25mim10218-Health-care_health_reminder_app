# ANADI-25mim10218-Health-care_health_reminder_app

Project Overview:
This project is a Django REST API for managing users, doctors, patients, staff members, treatments, exercises, records, and notifications.
The API supports token-based authentication and allows different types of users to interact with the system based on their roles.
Features
User & Authentication
User registration
Token-based login
Automatic profile creation for every user
Role support: Doctor, Patient, Staff Member
Doctors
Create doctor profile
Create and manage exercises
View list of treatments assigned to them
Patients
Get personal treatments
View exercises and medicine details
View notifications
View relatives linked to their profile
Staff Members
Create staff profile
Assigned to treatments
Treatments
Create treatment records
Add exercises
Assign doctor and staff
Track start and end dates
Records
Save daily treatment progress
Mark completion statuses
Notifications
Create notifications for patients
Retrieve notification history
Tech Stack
Python 3
Django 3+
Django REST Framework
Token Authentication
SQLite / PostgreSQL



Notes
Every user automatically gets a Profile created through signals.
Every new user also gets a Token for authentication.
Doctor, Patient, and Staff tables are connected through OneToOneField.
Treatments link doctor, patient, staff, and exercises.