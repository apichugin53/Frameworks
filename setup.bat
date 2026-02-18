@echo off

set PYTHON_EXE=python.exe

%PYTHON_EXE% --version >NUL 2>&1
if %errorlevel% neq 0 set PYTHON_EXE=py.exe

%PYTHON_EXE% --version >NUL 2>&1
if %errorlevel% neq 0 goto ERROR

%PYTHON_EXE% -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -U -r requirements.txt
goto END

:ERROR
echo "No python found"

:END