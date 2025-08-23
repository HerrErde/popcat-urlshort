@echo off

echo Setting up...
rmdir /s /q .venv
python -m venv .venv

call .venv\Scripts\activate
echo Upgrade Pip...
python.exe -m pip install --upgrade pip > nul
cd src
echo Installing packages...
pip install -r requirements.txt

echo Finished...

exit