# Ropolitiko

A FastAPI application that scrapes Romanian political news, classifies them using AI, and summarizes them with LLMs.

## Setup

1. Clone the repository
2. Create a virtual environment with `uv`:
   ```
   uv venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```
   uv pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example` and add your OpenAI API key

## Usage

1. Start the server:
   ```
   python main.py
   ```
2. The API will be available at http://localhost:8000
3. Visit http://localhost:8000/docs for the interactive API documentation

## Adding dependencies

Use the `./scripts/install.sh` script to install a package and update the `requirements.txt` file with the locked version.

```
./scripts/install.sh PACKAGE_NAME
```

