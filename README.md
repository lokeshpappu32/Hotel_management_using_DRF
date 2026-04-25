# 🏨 Hotel Management REST API

A Django REST Framework backend for a hotel booking platform with JWT authentication, user profiles, booking management, and admin controls.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.12, Django, Django REST Framework (DRF)
- **Database:** PostgreSQL
- **Auth:** JWT (djangorestframework-simplejwt)
- **Others:** Pillow, django-cors-headers

---

## ⚙️ Project Setup (Ubuntu)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd idbooks_hotel
```

### 2. Create and Activate Virtual Environment

```bash
sudo apt install python3.12-venv
python -m venv plugins
source plugins/bin/activate
```

### 3. Install Dependencies

```bash
pip install django djangorestframework psycopg2-binary djangorestframework-simplejwt Pillow django-cors-headers
pip freeze > requirements.txt
```

### 4. PostgreSQL Setup

```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo -u postgres psql
```

Run the following inside the PostgreSQL shell:

```sql
CREATE DATABASE hotel_booking;
CREATE USER hotel_user WITH PASSWORD 'your_password';
ALTER ROLE hotel_user SET client_encoding TO 'utf8';
ALTER ROLE hotel_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE hotel_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE hotel_booking TO hotel_user;
GRANT USAGE ON SCHEMA public TO hotel_user;
GRANT CREATE ON SCHEMA public TO hotel_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hotel_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO hotel_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO hotel_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO hotel_user;
\q
```

### 5. Run Migrations and Start Server

```bash
python manage.py makemigrations api
python manage.py migrate
python manage.py runserver
```

---

## 📁 Project Structure

```
hotel_booking/
├── hotel_booking/        # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/                  # Main app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── manage.py
└── requirements.txt
```

---

## 📡 API Endpoints

### 🔐 Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/` | Sign up with name, email, password |
| POST | `/api/token/` | Login — returns JWT access token |

---

### 👤 Profile

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/profile/` | Get logged-in user's profile |
| PUT | `/api/users/profile/` | Update profile (address, photo, gender) |
| GET | `/api/users/booking_count/` | Get total bookings in a date range |

---

### 📅 Bookings

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/bookings/` | Create a new hotel booking |
| GET | `/api/bookings/` | List all bookings for the user |
| GET | `/api/bookings/{id}/` | Get a single booking by ID |
| GET | `/api/bookings/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` | Filter bookings by date range |

> ⚠️ All booking endpoints require a valid JWT access token in the request header.

---

### 🛡️ Admin

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/users_list/` | List all registered users |
| GET | `/api/admin/booking_stats/` | Booking count per user in a date range |

---

## 🔑 Authentication — How to Use JWT

1. Sign up via `POST /api/users/`
2. Login via `POST /api/token/` to get your access token
3. Include the token in all protected requests:

```
Authorization: Bearer <your_access_token>
```

---

## 📋 Task Requirements Covered

- [x] User signup and JWT login
- [x] User profile with address, photo, gender
- [x] Booking count by date range
- [x] Hotel booking with check-in/out dates and number of persons
- [x] List all bookings / single booking by ID
- [x] Date range filter on bookings
- [x] Admin: list users
- [x] Admin: booking stats per user
- [x] Class-based ViewSets and Routers (DRF)
- [x] PostgreSQL database
- [x] Proper error messages on all endpoints

---

## 🧪 Testing

APIs tested using **Postman**. Import the collection or test manually using the endpoints above.

---

## 📄 License

This project is for demonstration and interview assessment purposes.
