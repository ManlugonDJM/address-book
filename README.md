# FastAPI Address Book Application

This is a simple address book application built with FastAPI. The application allows users to create, update, delete, and retrieve addresses. Each address includes coordinates (latitude and longitude) and is saved to an SQLite database. The application also ensures that the combination of latitude and longitude is unique.

## Requirements

- Python 3.7+
- FastAPI
- SQLAlchemy
- SQLite (included with Python)
- Geopy

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/ManlugonDJM/address-book.git
    cd address-book
    ```

2. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source venv/bin/activate
        ```

4. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the FastAPI server:

    ```sh
    uvicorn app.app:app --reload
    ```
    or
    ```sh
    py main.py
    ```

2. Open your browser and go to `http://127.0.0.1:8000/docs` to see the interactive API documentation.

## Project Structure

```plaintext
fastapi-address book/
│
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
|
├── README.md             # This file
├── requirements.txt      # Project dependencies
├── app.log               # Log file for errors (generated after running the app)
└── venv/                 # Virtual environment directory
