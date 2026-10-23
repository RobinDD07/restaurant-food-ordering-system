# Restaurant Food Ordering System — DBMS Course Project

A full-stack **Restaurant Food Ordering System** developed for an academic **Database Management Systems (DBMS)** course project. Built with Python Django, MySQL, Django REST Framework, HTML5, CSS3, and Bootstrap 5.

---

## 📌 Project Overview

This application manages multi-restaurant food operations, suppliers, delivery agents, customer orders, and customer feedback while strictly adhering to relational database design principles:
- **Primary Keys** for unique tuple identification.
- **Foreign Keys** with cascading referential integrity (`ON DELETE CASCADE`).
- **Data Validation** at both form and database levels.
- **Relational Aggregations & Joins** for operational insights.

---

## 🏗 Relational Database Schema

The system implements the **7 core relational tables** specified in the course schema document, plus an intuitive **`order_items`** bridge table:

```
+----------------------------------------------------------------------------------------------------+
|                                    RELATIONAL SCHEMA ARCHITECTURE                                 |
+----------------------------------------------------------------------------------------------------+
| 1. SUPPLIER       (supplier_id [PK], supplier_name)                                                |
| 2. RESTAURANT     (restaurant_id [PK], restaurant_name, restaurant_ph_no, restaurant_adrs, rating, |
|                    supplier_id [FK -> SUPPLIER])                                                   |
| 3. FOOD           (food_id [PK], food_name, food_price, food_rating, restaurant_id [FK -> RESTAURANT]) |
| 4. AGENTS         (agent_id [PK], agent_name, agent_ph_number, supplier_id [FK -> SUPPLIER])       |
| 5. CUSTOMER       (cust_id [PK], cust_name, cust_adrs, cust_ph_no)                                 |
| 6. ORDER_DETAILS  (order_id [PK], cust_id [FK -> CUSTOMER], supplier_id [FK -> SUPPLIER],          |
|                    order_date, quantity, price)                                                    |
| 7. FEEDBACK       (feedback_id [PK], cust_id [FK -> CUSTOMER], rating, message, feedback_date)     |
+----------------------------------------------------------------------------------------------------+
| *  ORDER_ITEMS    (order_item_id [PK], order_id [FK -> ORDER_DETAILS],                             |
|    (Extension)     food_id [FK -> FOOD], quantity, item_price)                                     |
+----------------------------------------------------------------------------------------------------+
```

### Note on `ORDER_ITEMS` Table Extension:
As specified in the requirements, the original `ORDER_DETAILS` table tracks total quantities and amounts per order. To allow an order to contain specific menu dishes, the supplementary table `ORDER_ITEMS` was added. This preserves the 7 core tables untouched while providing itemized billing and menu breakdown.

---

## 💻 Tech Stack

- **Frontend:** HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons
- **Backend:** Python 3.14+, Django 5/6
- **Database:** MySQL 8.0 (connected via PyMySQL & Django MySQL backend)
- **API:** Django REST Framework (DRF)
- **Version Control:** Git & GitHub

---

## 🚀 Step-by-Step Setup & Run Instructions (Windows / VS Code)

### 1. Clone or Open the Project
Open the project directory in **Visual Studio Code** or terminal:
```bash
cd "c:\Users\viren\OneDrive\Desktop\DBMS _ PROJECT"
```

### 2. Install Required Python Dependencies
Ensure Python 3.10+ is installed and run:
```bash
pip install -r requirements.txt
```
*(Dependencies: Django, djangorestframework, pymysql, cryptography, python-dotenv)*

### 3. Verify MySQL Database
Ensure MySQL Server 8.0 is running. Open MySQL Command Line Client or Workbench and verify the database:
```sql
CREATE DATABASE IF NOT EXISTS restaurant_food_ordering;
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` (if not already created) and update your MySQL credentials:
```ini
SECRET_KEY=django-insecure-restaurant-food-ordering-system-key-2026
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# MySQL Database Settings
DB_NAME=restaurant_food_ordering
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 5. Apply Database Migrations
Create all 7 relational tables + `order_items` directly inside MySQL:
```bash
python manage.py makemigrations ordering
python manage.py migrate
```

### 6. Populate Realistic Sample Records
Insert pre-configured sample data into all tables with one command:
```bash
python manage.py load_sample_data
```
*(Alternatively: `python load_sample_data.py`)*

### 7. (Optional) Create Django Admin Account
```bash
python manage.py createsuperuser
```

### 8. Run the Server
Launch the development server:
```bash
python manage.py runserver
```
*Or simply double-click **`run_server.bat`** on Windows!*

Open your browser and navigate to:
👉 **`http://127.0.0.1:8000/`**

---

## 🌐 Web Application Pages & Features

| Page | URL | Key Features |
| :--- | :--- | :--- |
| **Dashboard** | `/` | Total entity counters, aggregate metrics (SUM, AVG), quick navigation, recent orders & reviews. |
| **Restaurants** | `/restaurants/` | View all restaurants, supplier links, star ratings, search filter, full Create/Edit/Delete. |
| **Food Menu** | `/food/` | Dish listings, price tags, ratings, filter by restaurant dropdown, full CRUD. |
| **Suppliers** | `/suppliers/` | Vendor management with counts of linked restaurants and employed agents. |
| **Agents** | `/agents/` | Delivery agents directory, contact numbers, and assigned supplier associations. |
| **Customers** | `/customers/` | Customer directory with addresses, phone numbers, and past order counts. |
| **Orders** | `/orders/` | Order creation with dynamic food dish selection and auto-computed total prices. |
| **Order Details** | `/orders/<id>/` | Itemized invoice showing dish breakdown, unit prices, subtotals, and customer info. |
| **Feedback** | `/feedback/` | Customer review ratings (1 to 5 stars) and message submission. |
| **SQL Demo** | `/queries-demo/` | **Interactive viva tool:** executes raw MySQL queries live on the database with rendered result tables. |

---

## 📡 REST API Endpoints (Django REST Framework)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/dashboard-stats/` | Live aggregate statistics (counts, revenue, averages) |
| `GET` | `/api/food-by-restaurant/<id>/` | Dynamic menu items for a selected restaurant |
| `GET, POST` | `/api/restaurants/` | Restaurant resources |
| `GET, POST` | `/api/food/` | Food menu resources |
| `GET, POST` | `/api/suppliers/` | Supplier vendor resources |
| `GET, POST` | `/api/agents/` | Delivery agent resources |
| `GET, POST` | `/api/customers/` | Customer resources |
| `GET, POST` | `/api/orders/` | Order details resources |
| `GET, POST` | `/api/feedback/` | Feedback and rating resources |

---

## 📊 SQL Demonstration Queries (DBMS Lab / Viva)

The included file **`database_queries.sql`** contains complete SQL scripts:
1. **`CREATE TABLE`** DDL scripts with Primary Keys and Foreign Keys.
2. **`INSERT`** DML scripts for realistic sample datasets.
3. **`SELECT` with `WHERE`, `LIKE`, `BETWEEN`** filtering.
4. **`INNER JOIN` & `LEFT JOIN`** queries across 2, 3, and 4 related tables.
5. **Aggregate functions:** `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`.
6. **Grouping:** `GROUP BY` and `HAVING` clauses.
7. **Nested Queries:** Subqueries with `IN` and scalar comparisons.
8. **`UPDATE` and `DELETE`** queries.

---

## 📁 Project Directory Structure

```
DBMS _ PROJECT/
│
├── food_ordering_system/          # Core Django project settings
│   ├── __init__.py                # PyMySQL initialization
│   ├── settings.py                # Database & app configurations
│   ├── urls.py                    # Master URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── ordering/                      # Main application
│   ├── management/
│   │   └── commands/
│   │       └── load_sample_data.py # Sample data CLI command
│   ├── templates/ordering/        # Responsive HTML5 + Bootstrap templates
│   │   ├── base.html              # Master layout & navbar
│   │   ├── dashboard.html         # Stat cards & metric dashboard
│   │   ├── restaurant_list.html
│   │   ├── restaurant_form.html
│   │   ├── food_list.html
│   │   ├── food_form.html
│   │   ├── supplier_list.html
│   │   ├── supplier_form.html
│   │   ├── agent_list.html
│   │   ├── agent_form.html
│   │   ├── customer_list.html
│   │   ├── customer_form.html
│   │   ├── order_list.html
│   │   ├── order_form.html        # Interactive order creator
│   │   ├── order_edit_form.html
│   │   ├── order_detail.html      # Itemized order invoice
│   │   ├── feedback_list.html
│   │   ├── feedback_form.html
│   │   ├── confirm_delete.html    # Safe deletion dialog
│   │   └── dbms_queries.html      # Live SQL query demonstration page
│   ├── admin.py                   # Django admin registrations
│   ├── api_views.py               # DRF API endpoints
│   ├── forms.py                   # ModelForms with validation
│   ├── models.py                  # 7 relational schema models + OrderItem
│   ├── serializers.py             # DRF ModelSerializers
│   ├── tests.py                   # Unit & integration test cases
│   ├── urls.py                    # App URLs & API routing
│   └── views.py                   # Server-side CRUD views
│
├── static/
│   └── css/
│       └── custom.css             # Custom UI polish
│
├── database_queries.sql           # Complete SQL schema & viva demo queries
├── load_sample_data.py            # Standalone sample data loader
├── run_server.bat                 # 1-click Windows server launcher
├── requirements.txt               # Dependencies
├── .env.example                   # Template environment configuration
├── .gitignore                     # Git exclusions (credentials, caches)
├── ER_DIAGRAM.jpeg                # Source ER Diagram reference
├── RELATIONAL DATABASE SCHEMA.docx# Source schema document reference
└── README.md                      # Documentation
```

---

## 👨‍🎓 Academic Presentation Notes

- **Database Engine Verification:** All tables are created in native MySQL with InnoDB storage engine ensuring ACID compliance.
- **Foreign Key Integrity:** Child records reference their parent tables via verified constraints. Cascading deletes are enforced.
- **Course Viva Readiness:** Navigate to `/queries-demo/` during your demonstration to showcase live SQL queries executing on MySQL.
