# Online Store API

## Overview

The Online Store API is a FastAPI-based backend service that allows management of a catalog of games. It supports functionalities such as creating, reading, updating, and deleting game entries. The application is designed with modularity in mind, separating the service, database, and API layers for better maintainability and scalability.

## Features

- **Games Management:**

  - List all games
  - Retrieve a specific game by ID
  - Add a new game
  - Update game information
  - Delete a game

- **Dependency Injection:**

  - Uses FastAPI's dependency injection system to manage database sessions and services.

- **Database:**
  - SQLAlchemy ORM integration for database interactions.

## Project Structure

```
.
├── adapters
│   ├── api.py               # API routes and endpoints
│   ├── database
│   │   ├── database.py      # Database connection and session management
│   │   ├── models.py        # SQLAlchemy models
├── domain
│   ├── schemas.py           # Pydantic schemas for data validation
│   ├── services.py          # Business logic and services
├── main.py                  # Application entry point
├── settings.py              # Configuration settings
├── docker-compose.yaml      # Docker configuration for development
├── .env                     # Environment variables
```

## Prerequisites

- Python 3.9+
- PostgreSQL (or any supported SQL database)
- Docker (for containerized deployment)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/onlinestoreapi.git
   cd onlinestoreapi
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   - Copy `.env.example` to `.env` and update the database credentials.

5. Run the application:
   ```bash
   fastapi dev main.py
   ```

## Usage

- Access the API documentation at `http://localhost:8000/docs`.
- Use the interactive Swagger UI to test the endpoints.

### API Endpoints

| Method | Endpoint      | Description              |
| ------ | ------------- | ------------------------ |
| GET    | `/games/`     | List all games           |
| GET    | `/games/{id}` | Retrieve a specific game |
| POST   | `/games/`     | Add a new game           |
| PUT    | `/games/{id}` | Update game information  |
| DELETE | `/games/{id}` | Delete a game            |

## Running with Docker

1. Build and start the containers:

   ```bash
   docker-compose up --build
   ```

2. Access the application at `http://localhost:8000`.

## Testing

Run the tests with:

```bash
pytest
```

## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.
