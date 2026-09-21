# 🏬 Store & Asset Management System (Desktop Application)

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-blue?style=for-the-badge)
![SQLite3](https://img.shields.io/badge/Database-SQLite3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-MVC-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A multi-module desktop management software developed in Python. Designed around the **Model-View-Controller (MVC)** architectural pattern, this application provides an integrated solution for managing personnel, customers, vehicle fleets, and real estate assets with transactional reliability and an intuitive GUI.

---

## 🧭 System Modules

| Section | Description |
| :--- | :--- |
| **👤 Admin Management** | Manage credentials, access levels, and suspension status. |
| **👥 Customer Relations** | Client profiling, contact tracking, and account statuses. |
| **🚗 Vehicle Fleet** | Specs, production year, formatted currency pricing, and availability. |
| **🏡 Real Estate** | Property profiling with tags for **Parking**, **Elevator**, and **Storage**. |

---

## 🌟 Core Features

- **MVC Architecture:** Strict decoupling between data models, repositories, business logic controllers, and Tkinter UI views.
- **Auto-Maximizing UI:** All application windows launch automatically in full-screen (`zoomed`) mode.
- **Dynamic Table Indicators:** Real-time color coding in `Treeview` tables:
  - 🟩 **Green Rows:** Active / Available
  - 🟥 **Red Rows:** Suspended / Sold
- **Financial Formatting:** Dynamic 3-digit comma separators for monetary entries with currency labels.
- **Persistent Routing:** Seamless navigation with unified return buttons to the main dashboard.
- **Zero-Setup Database:** Automated database and schema creation on initial startup.

---

## 📁 Repository Structure

```text
store-management-system/
│
├── controller/
│   ├── admin_controller.py
│   ├── customer_controller.py
│   ├── car_controller.py
│   └── house_controller.py
│
├── model/
│   ├── entity/
│   │   ├── admin.py
│   │   ├── customer.py
│   │   ├── car.py
│   │   └── house.py
│   │
│   └── repository/
│       ├── admin_repository.py
│       ├── customer_repository.py
│       ├── car_repository.py
│       └── house_repository.py
│
├── view/
│   ├── admin_view.py
│   ├── customer_view.py
│   ├── car_view.py
│   └── house_view.py
│
├── main.py
└── README.md
