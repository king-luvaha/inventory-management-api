# 📦 Inventory Management API

A comprehensive RESTful API for inventory management built with Django and Django REST Framework. This system provides secure user authentication, complete CRUD operations for inventory items, category management, and detailed change tracking with advanced filtering capabilities.

## 🚀 Features

- **User Authentication**: JWT-based secure authentication system
- **Inventory Management**: Full CRUD operations for inventory items
- **Category System**: Organize items with customizable categories
- **Change Tracking**: Automatic logging of all inventory modifications
- **Advanced Filtering**: Filter by category, stock levels, price ranges
- **Search Functionality**: Search items by name and description
- **Stock Adjustment**: Dedicated endpoint for inventory adjustments
- **Admin Interface**: Django admin for comprehensive data management
- **RESTful Design**: Clean, predictable API endpoints

## 📁 Project Structure

```bash
inventory-management-api/
│── inventory/               # Django project root
│   ├── settings.py          # Project settings
│   ├── urls.py              # Project-level routes
│   └── ...
│
│── inventory_api/           # Core app
│   ├── models.py            # Database models
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API views
│   ├── urls.py              # App routes
│   ├── admin.py             # Admin panel customization
│   └── ...
│
│── manage.py
│── README.md
│── requirements.txt
```

## 💻Technology Stack

- **Backend Framework**: Django 4.2+
- **REST API**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: SQLite (default, can be configured for PostgreSQL/MySQL)
- **Filtering**: Django Filter for complex query operations

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/inventory-management-api.git
   cd inventory-management-api
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

## 📖 API Documentation

### 🔑 Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/token/` | Obtain JWT tokens (access & refresh) |
| POST | `/api/token/refresh/` | Refresh access token |

### 📦 Inventory Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/inventory/` | List all inventory items |
| POST | `/api/inventory/` | Create new inventory item |
| GET | `/api/inventory/{id}/` | Retrieve specific item |
| PUT | `/api/inventory/{id}/` | Update item details |
| PATCH | `/api/inventory/{id}/` | Partial update |
| DELETE | `/api/inventory/{id}/` | Delete item |
| POST | `/api/inventory/{id}/adjust_stock/` | Adjust item quantity |
| GET | `/api/inventory/{id}/history/` | View item change history |

### 🗃Category Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories/` | List all categories |
| POST | `/api/categories/` | Create new category |
| GET | `/api/categories/{id}/` | Retrieve specific category |
| PUT | `/api/categories/{id}/` | Update category |
| DELETE | `/api/categories/{id}/` | Delete category |

### 👥 User Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/` | List users (admin only) |
| POST | `/api/users/` | Create new user |
| GET | `/api/users/{id}/` | Retrieve user details |
| PUT | `/api/users/{id}/` | Update user |
| DELETE | `/api/users/{id}/` | Delete user |

## 🛠️ Admin Interface

Access the Django admin interface at `http://localhost:8000/admin/` to:

- Manage users and permissions
- View and edit all inventory data
- Monitor inventory changes and history
- Manage categories and product details

## 🗄Database Models

### 👤 User
Extended Django's default user model with additional fields.

### 🏷️ Category
- `name`: Category name (unique)
- `description`: Optional description

### 📦 InventoryItem
- `name`: Item name
- `description`: Item description
- `quantity`: Current stock quantity
- `price`: Item price
- `category`: ForeignKey to Category
- `created_by`: ForeignKey to User
- `date_added`: Auto-generated timestamp
- `last_updated`: Auto-updated timestamp

### 📜 InventoryChange
- `item`: ForeignKey to InventoryItem
- `user`: User who made the change
- `action`: Type of change (ADD, REMOVE, UPDATE, CREATE, DELETE)
- `quantity_change`: Difference in quantity
- `previous_quantity`: Quantity before change
- `new_quantity`: Quantity after change
- `timestamp`: When change occurred
- `notes`: Additional notes

## 🔒 Security Features

- JWT authentication for all API endpoints
- User-specific data isolation (users only see their own items)
- Password hashing using Django's secure password hashers
- Token expiration for enhanced security
- Input validation and sanitization
## 🧪 Testing

Run the test suite with:

```bash
python manage.py test
```

## 🚢 Deployment

For production deployment:

1. Set `DEBUG = False` in `settings.py`
2. Configure a production database (PostgreSQL recommended)
3. Set up a proper WSGI server (Gunicorn)
4. Configure a reverse proxy (Nginx)
5. Set up SSL certificates
6. Configure environment variables for sensitive data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
_If this project helped you, please consider giving it a ⭐ on GitHub!_