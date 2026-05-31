# How to Run the Project

## Prerequisites
- Python 3.8 or higher installed
- Internet connection (for first run to download models if needed, though they are likely included)

## Setup and Run

1.  **Open Terminal**:
    Open a terminal or command prompt in the project folder:
    `c:\Users\harin\OneDrive\Documents\autism_learning_platform`

2.  **Install Dependencies**:
    Run the following command to install required libraries:
    > [!IMPORTANT]
    > Please ensure you are using a stable Python version (3.10, 3.11, or 3.12). Python 3.14+ is experimental and may cause hangs.

    ```bash
    # If using Git Bash (recommended):
    source .venv/Scripts/activate
    
    # Then install:
    pip install -r requirements.txt
    ```

3.  **Run the Application**:
    Start the Flask server:
    ```bash
    python app.py
    ```

4.  **Access the App**:
    Open your web browser and go to:
    `http://127.0.0.1:5000`

## Using the New Features

### 1. Register Your Face
1.  Log in (or register a new account).
2.  Go to the **Dashboard**.
3.  Click on **Face ID Settings**.
4.  Button: **Register New Face**.
5.  Allow camera access.
6.  Click **Capture Sample** 5 times moving your head slightly between captures.
7.  Once complete, you will be redirected to the dashboard.

### 2. Login with Face ID
1.  Log out of the application.
2.  On the Login page, click the **Login with Face ID** button.
3.  Look at the camera.
4.  The system will recognize you and log you in automatically!

### 3. Emotion Recognition
1.  Go to **AI Friend** -> **AI Emotion**.
2.  The system will now display your name when it detects your emotion (e.g., "John - You look Happy!").

## Troubleshooting
- **Database Error**: If you see database errors, delete the `instance/db.sqlite` file and restart the application.
- **Camera Not Working**: Ensure your browser has permission to access the camera.
- **Models Not Loading**: Ensure the `static/models` directory exists and contains the model files.
