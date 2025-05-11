# IT Ticketing System

## Description

This is a Python-based IT ticketing system with an agentic AI component. It allows users to submit IT tickets, and the system uses LLM (Large Language Model) technology to suggest solutions. The backend is built using FastAPI.

## Features

* **Ticket Management:** Users can create, view, and update the status of tickets.
* **User Management:** Includes user registration, login, and role-based access control (user, support, admin).
* **LLM-Powered Assistance:** The system uses an LLM to suggest solutions for tickets.
* **Documentation Ingestion:** Support for ingesting documents (PDF, DOCX, MD) to enhance the LLM's knowledge base.
* **API-First Design:** The backend provides a RESTful API for interacting with the system.
* **Authentication and Authorization:** Secure user authentication and role-based authorization.

## Technical Architecture

* **Backend:** Python, FastAPI
* **Database:** SQLAlchemy (PostgreSQL - *Assumed from the vector extension, the code uses "DATABASE_URL"*)
* **LLM:** Google Gemini
* **Vector Storage:** pgvector (for storing and querying embeddings)
* **Embedding Model**: Nomic
* **Message Broker:** Redis (Not used in the provided code)

## Prerequisites

Before you begin, ensure you have the following installed:

* **Python:** (>= 3.10)
* **PostgreSQL:** (with the `pgvector` extension)
* **Poetry:** (for dependency management)
* **Google Cloud Account:** (for Gemini API access)
* **Nomic Account**: (for Nomic Embeddings)
* **Alembic:** (for database migrations)

## Setup

1.  **Clone the Repository:**

    ```bash
    git clone <your_repository_url>
    cd it-ticketing-system
    cd backend
    ```

2.  **Set up the Database:**

    * Ensure PostgreSQL is running.
    * Create a database.
    * Enable the `pgvector` extension in your database:

        ```sql
        CREATE EXTENSION IF NOT EXISTS vector;
        ```

    * Set the `DATABASE_URL` environment variable. For example:

        ```bash
        export DATABASE_URL="postgresql://your_user:your_password@your_host/your_database"
        ```

        (Replace with your actual database credentials.)
    * The application expects this environment variable.

3.  **Set up Environment Variables:**

    * Create a `.env` file in the `backend` directory.
    * Add the following environment variables to the `.env` file:

        ```
        JWT_SECRET_KEY=<your_secret_key> # Change this to a strong, random key
        JWT_ALGORITHM=HS256 # Or another supported algorithm
        ACCESS_TOKEN_EXPIRE_MINUTES=30 # Or your desired expiration time
        GEMINI_API_KEY=<your_gemini_api_key> # Get this from Google Cloud
        DATABASE_URL="postgresql://your_user:your_password@your_host/your_database" # If not set in the environment
        ```

        * Replace `<your_secret_key>` with a strong, random key.
        * Obtain a `GEMINI_API_KEY` from Google Cloud. You'll need to enable the Gemini API in your Google Cloud project.
        * Make sure the `DATABASE_URL` matches your PostgreSQL connection string.

4.  **Install Dependencies:**

    ```bash
    poetry install
    ```

5.  **Run Migrations (Create Tables with Alembic):**

    * Initialize Alembic:

        ```bash
        poetry run alembic init migrations
        ```

    * Edit the `alembic.ini` file to configure your database connection. Specifically, ensure the `sqlalchemy.url` setting points to your PostgreSQL database (using the `DATABASE_URL` environment variable is recommended). For example:

        ```ini
        sqlalchemy.url = postgresql://your_user:your_password@your_host/your_database
        # OR, to use the environment variable:
        # sqlalchemy.url = %(env)s/DATABASE_URL
        ```

    * Create a migration script:

        ```bash
        poetry run alembic revision -m "Create initial tables"
        ```

    * Apply the migration to create the tables in your database:

        ```bash
        poetry run alembic upgrade head
        ```

6.  **Run the Application:**

    ```bash
    poetry run uvicorn backend.app.main:app --reload
    ```

    * This will start the FastAPI server. The `--reload` flag enables hot reloading, so the server will automatically restart when you make changes to the code.

## Documentation Ingestion

To ingest documents (PDF, DOCX, MD) into the system:

1.  Send a POST request to the `/api/v1/llm/ingest_doc/` endpoint.
2.  Use the `multipart/form-data` content type.
3.  Include the file as a form field named `file`.

    \* Example using `curl`\*:

    ```bash
    curl -X POST \
      http://localhost:8000/api/v1/llm/ingest_doc/ \
      -H "Content-Type: multipart/form-data" \
      -F "file=@your_document.pdf"
    ```

## API Endpoints

### Auth

* `POST /api/v1/auth/register`: Register a new user.
* `POST /api/v1/auth/login`: Log in and get an access token.

### Users

* `GET /api/v1/users/`: List all users (admin only).
* `GET /api/v1/users/me`: Get the current user's information.
* `PATCH /api/v1/users/{user_id}/role`: Update a user's role (admin only).
* `DELETE /api/v1/users/{user_id}`: Delete a user (admin only)

### Tickets

* `POST /api/v1/tickets/`: Create a new ticket.
* `GET /api/v1/tickets/`: List user's tickets (or all tickets for support/admin).
* `PATCH /api/v1/tickets/{ticket_id}`: Update ticket status (support/admin only).

### LLM

* `POST /api/v1/llm/resolve_ticket/{ticket_id}`: Resolve a ticket using the LLM.
* `POST /api/v1/llm/ingest_doc/`: Ingest a document for the LLM.

## User Roles

The system has the following user roles:

* **user:** Can create and view their own tickets.
* **support:** Can view and update all tickets, and use the LLM to suggest solutions.
* **admin:** Can manage users and tickets, and use the LLM.

## Authentication

* The API uses JWT (JSON Web Token) authentication.
* Upon successful login, the user receives an access token.
* This token must be included in the `Authorization` header of subsequent requests:

    ```
    Authorization: Bearer <your_access_token>
    ```

## Error Handling

* The API returns JSON responses with appropriate HTTP status codes for errors.
* Common error scenarios include:

    * 401 Unauthorized (invalid credentials, missing token)
    * 403 Forbidden (insufficient permissions)
    * 404 Not Found
    * 400 Bad Request
    * 500 Internal Server Error
