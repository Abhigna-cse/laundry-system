# 🧺 Laundry Order Management System

A lightweight dry cleaning store management system built with Python (Flask) and a simple HTML frontend.

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation & Run

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/laundry-system.git
cd laundry-system

# 2. Install dependencies
pip install flask

# 3. Run the app
python app.py

# 4. Open in browser
# Go to: http://localhost:5000
```

That's it! No database setup needed — uses in-memory storage.

---

## ✅ Features Implemented

### Core Features
| Feature | Status |
|---|---|
| Create Order (name, phone, garments, quantity, price) | ✅ Done |
| Auto-calculate total bill | ✅ Done |
| Unique Order ID generation | ✅ Done |
| Order Status Management (RECEIVED → PROCESSING → READY → DELIVERED) | ✅ Done |
| Update order status | ✅ Done |
| View all orders | ✅ Done |
| Filter by status | ✅ Done |
| Filter by customer name / phone | ✅ Done |
| Dashboard (total orders, revenue, orders per status) | ✅ Done |

### Bonus Features
| Feature | Status |
|---|---|
| Simple HTML + JS Frontend | ✅ Done |
| Estimated delivery date (+2 days) | ✅ Done |
| Filter by garment type | ✅ Done |
| Delete order | ✅ Done |
| Price list (hardcoded, configurable) | ✅ Done |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Frontend UI |
| POST | `/orders` | Create new order |
| GET | `/orders` | List all orders (with filters) |
| GET | `/orders/<id>` | Get single order |
| PATCH | `/orders/<id>/status` | Update order status |
| DELETE | `/orders/<id>` | Delete order |
| GET | `/dashboard` | Dashboard stats |

### Sample API Requests

**Create Order:**
```json
POST /orders
{
  "customer_name": "Priya Sharma",
  "phone": "9876543210",
  "garments": [
    { "name": "saree", "quantity": 2 },
    { "name": "shirt", "quantity": 3 }
  ]
}
```

**Response:**
```json
{
  "order_id": "ORD-AB12CD34",
  "total_bill": 390,
  "estimated_delivery": "2025-04-22",
  "message": "Order created successfully"
}
```

**Update Status:**
```json
PATCH /orders/ORD-AB12CD34/status
{ "status": "PROCESSING" }
```

**Filter Orders:**
```
GET /orders?status=READY
GET /orders?search=Priya
GET /orders?garment=saree
```

---

## 🤖 AI Usage Report

### Tools Used
- **ChatGPT** — Used for generating initial code structure, API logic, and HTML frontend
- **Claude (Anthropic)** — Used for refining code, fixing bugs, and improving UI

---

### Sample Prompts Used

**Prompt 1 — Project scaffold:**
> "Build a Flask REST API for a dry cleaning laundry management system. It should allow creating orders with customer name, phone number, garments (name, quantity, price), auto-calculate total bill, generate a unique order ID, and store orders in memory."

**Prompt 2 — Status management:**
> "Add an endpoint to update order status. Valid statuses are RECEIVED, PROCESSING, READY, DELIVERED. Validate the status before updating."

**Prompt 3 — View and filter orders:**
> "Add a GET /orders endpoint that returns all orders. Add optional query parameters to filter by status, customer name/phone search, and garment type."

**Prompt 4 — Dashboard:**
> "Create a GET /dashboard endpoint that returns total orders, total revenue, and count of orders per status."

**Prompt 5 — Frontend:**
> "Build a clean HTML + JavaScript frontend for this Flask app. It should have a dashboard with stats, a form to create orders with dynamic garment rows, and an orders table with filters and status update modal. Use a blue color theme."

**Prompt 6 — Bonus features:**
> "Add estimated delivery date (2 days from order creation) and a garment filter to the orders endpoint. Also add a price list endpoint."

---

### What AI Got Wrong / What I Fixed

| Issue | What AI Did | What I Fixed |
|---|---|---|
| Order ID format | AI used plain UUID which was too long | Changed to `ORD-` prefix with 8 character short UUID for readability |
| Price auto-fill | AI didn't auto-fill price when garment type changed | Added `onchange` handler to auto-populate price from price list |
| Status validation | AI didn't validate status values | Added `VALID_STATUSES` list and proper error messages |
| Garment filter | AI missed garment type filter in orders endpoint | Added `garment` query param filter that searches inside garments array |
| Frontend alerts | AI showed alerts as browser `alert()` popups | Replaced with styled inline alert boxes that auto-hide after 5 seconds |
| Bill calculation | AI used fixed prices only | Made it accept custom price per garment OR fall back to price list |
| Phone filter | AI only filtered by name | Extended search to also match phone number |

---

## ⚖️ Tradeoffs

### What I Skipped
- **Database** — Used in-memory storage. Data resets on server restart. Would use SQLite or MongoDB with more time.
- **Authentication** — No login system. Would add JWT-based auth for production.
- **Input validation** — Basic validation only. Would add phone number format check, garment name sanitization.
- **Pagination** — Orders list loads all at once. Would add pagination for large datasets.

### What I'd Improve With More Time
- Add SQLite/MongoDB for persistent storage
- Deploy on Render or Railway (free hosting)
- Add SMS notification when order is READY
- Add print receipt feature
- Add date range filter for orders
- Add customer order history view

---

## 💰 Price List (Default)

| Garment | Price |
|---|---|
| Shirt | ₹50 |
| Pants | ₹60 |
| Saree | ₹120 |
| Jacket | ₹150 |
| Kurta | ₹70 |
| Suit | ₹200 |
| Bedsheet | ₹100 |
| Blanket | ₹180 |
| Towel | ₹40 |

---

## 📁 Project Structure

```
laundry-system/
├── app.py              # Flask backend — all API logic
├── templates/
│   └── index.html      # Frontend UI
└── README.md           # This file
```
