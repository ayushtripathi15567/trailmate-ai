# TrailMate AI 🌿

TrailMate AI is a small open-source nature companion that helps people spend less time on their phones and more time noticing the world around them.

## Features
- Generate short outdoor nature missions with a locally running Gemma model.
- Ask beginner-friendly questions about nature.
- Includes a fallback message if Ollama is unavailable.
- Keeps this starter app's journal/session data in the browser only (localStorage).

## Stack
- React + Vite
- Flask + Flask-CORS
- Ollama running a Gemma open-weight model

## Requirements
- Node.js 18+ and npm
- Python 3.10+
- Ollama installed and running
- A Gemma model downloaded in Ollama

## Run locally

### 1. Get the model
Install Ollama from https://ollama.com, then in a terminal run:

```bash
ollama pull gemma3:1b
ollama serve
```

If your Ollama installation uses a different Gemma tag, update `OLLAMA_MODEL` in `backend/.env` or set it as an environment variable.

### 2. Start the Flask backend
Open a terminal in the project root:

```bash
cd backend
python -m venv .venv
```

Windows:
```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Then:
```bash
pip install -r requirements.txt
python app.py
```

The backend runs at http://127.0.0.1:5000.

### 3. Start the frontend
Open another terminal in the project root:

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, usually http://localhost:5173.

## Notes
- AI generation requires Ollama and a compatible local model. The app does not silently switch to a closed hosted AI API.
- The frontend includes a basic fallback when the backend/model is unavailable, but that fallback is not AI-generated.
- Model output can be inaccurate. Treat nature identification and safety-related suggestions cautiously; don't eat or handle plants, fungi, or wildlife based on AI advice.
- This is a starter project. Test it on your machine before claiming that all features work in your DEV submission.

## Project structure
```text
trailmate-ai/
├── backend/
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       └── style.css
├── .gitignore
└── README.md
```

## Hacktoberfest
Built for the Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass.
