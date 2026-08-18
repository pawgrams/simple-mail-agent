@echo off
echo Checking if Python 3.13 is installed...
py -3.13 -m venv venv
if %errorlevel% neq 0 (
    echo Python 3.13 wurde nicht gefunden! Bitte installieren.
    echo HIER DOWNLOADEN: https://www.python.org/ftp/python/3.13.12/python-3.13.12-amd64.exe
    pause
    exit /b
)

echo Virtual Environment aktivieren...
call venv\Scripts\activate

echo Pip aktualisieren...
python -m pip install --upgrade pip

echo Dependencies installieren...
python -m pip install openai python-dotenv pydantic langchain_text_splitters langchain_openai langchain_community jinja2 pypdf faiss-cpu langgraph "langgraph-cli[inmem]" pipreqs

echo Installation fertig!
pause
