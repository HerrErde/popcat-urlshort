@echo off
call .venv\Scripts\activate
::start /B python main.py
cd src
python main.py
::start http://localhost:5000
pause