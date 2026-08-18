#!/bin/bash

python3.13 --version &> /dev/null

echo "Checking if Python 3.13 is installed..."
if [ $? -ne 0 ]; then
    echo "Python 3.13 wurde nicht gefunden! Bitte mit 'brew install python@3.13' installieren."
    echo "ODER HIER DOWNLOADEN: https://www.python.org/ftp/python/3.13.12/python-3.13.12-macos11.pkg"
    exit 1
fi

echo "Virtual Environment erstellen..."
python3.13 -m venv venv

echo "Virtual Environment aktivieren..."
source venv/bin/activate

echo "Pip aktualisieren..."
python3 -m pip install --upgrade pip

echo "Dependencies installieren..."
python3 -m pip install openai python-dotenv pydantic langchain_text_splitters langchain_openai langchain_community jinja2 pypdf faiss-cpu langgraph "langgraph-cli[inmem]" pipreqs

echo "Installation fertig!"
