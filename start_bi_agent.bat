@echo off
echo Starting Business Intelligence Agent...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo Warning: .env file not found
    echo Please create .env file with your GROQ API key
    echo See env_example.txt for reference
    echo.
)

REM Install dependencies if requirements.txt exists
if exist requirements.txt (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Start the application
echo Starting BI Agent web interface...
echo Open your browser and go to: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

python run.py

pause
