# Dante - Email Alert Monitoring Dashboard

This project is a web application that connects to a Microsoft email account, monitors incoming notification emails, classifies them, and displays a real-time dashboard of unread emails by category.

## Project Structure

- `dante_backend/`: The FastAPI backend.
- `dante_frontend/`: The React frontend.
- `requirements.txt`: Python dependencies.
- `run_server.py`: A script to run the backend server.

## Setup and Installation

### 1. Configure Backend

- **Create an Azure App Registration:**
    - Go to the Azure portal and create a new App Registration.
    - Under "Authentication", add a new platform for "Web" and set the redirect URI to `http://localhost:8000/callback`.
    - Under "Certificates & secrets", create a new client secret.
    - Note down the Application (client) ID, Tenant ID, and the client secret value.

- **Set up Environment Variables:**
    - Rename `dante_backend/.env.example` to `dante_backend/.env` (or create it).
    - Fill in the values for `CLIENT_ID`, `CLIENT_SECRET`, and `TENANT_ID` with the credentials from your Azure App Registration.
    - The `ENCRYPTION_KEY` is generated automatically if not present.

- **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 2. Configure Frontend

- **Install Node.js Dependencies:**
    ```bash
    cd dante_frontend
    npm install
    ```

## Running the Application

1.  **Start the Backend Server:**
    - From the project root directory, run:
    ```bash
    python run_server.py
    ```
    - The backend will be running at `http://localhost:8000`.

2.  **Start the Frontend Development Server:**
    - In a new terminal, from the project root directory, run:
    ```bash
    cd dante_frontend
    npm start
    ```
    - The frontend will be running at `http://localhost:3000`.

## How to Use

1.  Open your browser to `http://localhost:3000`.
2.  Click "Connect with Microsoft" and log in with your Microsoft account.
3.  Grant the requested permissions.
4.  You will be redirected to the dashboard, which will show the categories of unread emails.
5.  Send emails that match the rules in `dante_backend/classifier.py` to see the dashboard update in real time.
6.  Click "Mark as Read" to mark all unread emails in a category as read.
