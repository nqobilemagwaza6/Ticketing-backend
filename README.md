# Ticketing-backend

# Admin login creditials
email = tms@gmail.com password = TMS#5

# 🎫 Ticket Management System (TMS)

A full-stack, role-based Ticket Management System built using Django REST Framework and Vue 3.

The system allows organizations to manage support tickets efficiently with structured roles for Admin, Support, and Users.

# 🚀 Live Application

https://ticket-management-system-aw70.onrender.com

Database: PostgreSQL (Render Hosted)

# 🏗 System Overview

The Ticket Management System enables structured communication between users and support staff through a secure and role-based platform.

# 👥 User Roles 👤 User

Registers and logs into the system

Creates support tickets

Views ticket status updates

Adds comments to tickets

Receives email notifications

Can reset password via secure email link

# 🛠 Support

Assigned tickets by Admin

Updates ticket status

Resolves user issues

Communicates through ticket comments

# 👩‍💼 Admin

Full system control

Create / update / deactivate users

Assign tickets to Support staff

Manage user roles (Admin / Support / User)

Monitor all tickets

Sends automated password setup emails

# ✨ Features

Role-Based Access Control (Admin / Support / User)

Token Authentication (DRF)

Ticket creation & assignment

Ticket status tracking

Ticket comments system

Admin dashboard

User management (Create / Update / Deactivate)

Email notifications via Brevo API

Secure password reset (Token + UID)

PostgreSQL database integration

Fully deployed frontend & backend

# 🛠 Tech Stack Backend

Django 5

Django REST Framework

PostgreSQL (Render)

Brevo Email API

TokenAuthentication

Deployed on Render

Frontend

Vue 3

Vue Router

Vue CLI

# 🔐 Authentication & Security

Token-based authentication

Role-based permission control

Secure password validation

Email-based password reset system

CSRF & CORS properly configured

Custom User model with role field

🗄 Database Design

Custom User model

Role field: Admin, Support, User

Foreign key relationships:

Users → Tickets

Tickets → Comments

PostgreSQL production database (Render)

# 🧠 Challenges Solved

Email delivery on Render (SMTP blocked → switched to Brevo API)

Duplicate email handling in PostgreSQL

Token authentication configuration

Role-based permission enforcement

Password reset token validation

CORS & CSRF production configuration

Background email sending to prevent worker timeout

# 🔮 Future Improvements

File attachments for tickets

Ticket priority levels

SLA tracking

Real-time updates (WebSockets)

Dashboard analytics

HTML email templates

Unit and integration testing

# 💼 Portfolio Value

This project demonstrates:

Full-stack development

REST API design

Authentication & authorization

Role-based access control

Email API integration

PostgreSQL database management

Production deployment on Render

Real-world debugging & deployment troubleshooting
