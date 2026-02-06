# 📦 StockFlow Pro

**StockFlow Pro** is a high-performance, asynchronous inventory management system designed to demonstrate robust backend engineering and modern UI/UX principles. Built with **FastAPI** and **SQLModel**, it features a decoupled architecture that separates business logic from data presentation.

---

## 🚀 Key Features

* **Full CRUD Lifecycle**: Optimized management for Products, Categories, and Suppliers with relational integrity.
* **Secure Authentication**: Imple  mentation of **OAuth2** with **JWT (JSON Web Tokens)** and password hashing via **Bcrypt** for secure access control.
* **Decoupled Frontend**: A modern, interactive dashboard built with **Streamlit** that communicates with the API via asynchronous requests.
* **Advanced Data Modeling**: Utilizes **SQLModel** to unify Pydantic validation and SQLAlchemy ORM mapping.
* **Clean Architecture**: Structured directory layout (Core, API, Models, Schemas, Services) for maximum maintainability and scalability.
* **Automated Testing**: Comprehensive test suite using **Pytest** to ensure stability across service layers.

---

## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python, FastAPI, SQLModel (SQLAlchemy + Pydantic) |
| **Security** | Passlib (Bcrypt), Jose (JWT) |
| **Frontend** | Streamlit, Pandas, Requests |
| **Database** | SQLite (Development) / PostgreSQL (Production) |
| **Testing** | Pytest, Asyncio |

---

## 🏗️ Project Structure

The project follows a modular design to ensure high cohesion and low coupling:

* **`api/`**: Contains versioned API routes (`v1`) and endpoint definitions.
* **`core/`**: Houses global configurations, security utilities, and database engine setups.
* **`models/`**: Defines database entities and relational mapping.
* **`schemas/`**: Pydantic models for data validation and API response serialization.
* **`services/`**: Encapsulated business logic and database transaction handling.
* **`tests/`**: Unit and integration tests for the service layer.

---

## ⚙️ Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/CarlosBusiness-exe/stockflow.git
    cd stockflow-pro
    ```

2.  **Environment Configuration**:
    Create a `.env` file in the root directory:
    ```env
    DB_URL=sqlite+aiosqlite:///stockflow.db
    JWT_SECRET=your_secure_random_key
    ALGORITHM=HS256
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the System**:
    * **Start Backend**: `uvicorn main:app --reload`
    * **Start Frontend**: `streamlit run app_frontend.py`

---

## 🧪 Running Tests

To execute the automated test suite and ensure all modules are functioning correctly:
```bash
python -m pytest
```

## 👤 Author
Carl Computer Science Student & Backend Developer

Passionate about crafting scalable backend architectures and integrating functional design into technical solutions. Currently exploring high-performance API development and martial arts as a lifestyle.