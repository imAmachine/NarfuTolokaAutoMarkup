@echo off
pip install -r requirements.txt
set /p ENV_USERNAME=Enter your username from TOLOKA: 
set /p ENV_PASSWORD=Enter your password from TOLOKA: 
python .\run.py
pause
