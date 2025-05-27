# 🌀 Voice Vortex

**Voice Vortex** is a powerful voice-enabled chatbot application that leverages the capabilities of FastAPI, Google Generative AI, and modern frontend technologies. It allows users to interact with the bot using voice commands and get intelligent responses in real-time.

---

## 🚀 Features

- 🎤 **Voice Recognition**: Supports real-time speech recognition using `react-speech-recognition`.
- 🤖 **AI-Powered Chat**: Integrates with Google Generative AI for intelligent responses.
- 🌐 **Full-stack Application**: Backend with FastAPI and PostgreSQL, frontend with React and Vite.
- 🧠 **NLP Support**: Uses spaCy for natural language processing.
- 🔄 **State Management**: Redux Toolkit for managing app state.
- ⚡ **Fast Performance**: Vite for blazing-fast frontend development.
- 🧾 **Excel & Data Handling**: Supports `.xlsx` file parsing and uses Pandas for data operations.
- 🧠 **Search Memory**: Redis integration for caching and fast retrieval.

---

## 🧰 Tech Stack

### 🔙 Backend

- **FastAPI** – Python web framework
- **PostgreSQL** – Relational database
- **Redis** – In-memory cache
- **spaCy** – NLP library (with `en_core_web_sm`)
- **Google Generative AI** – For AI-generated responses
- **pandas**, **openpyxl**, **psycopg2-binary**, **python-dotenv**

### 🔜 Frontend

- **React 19**
- **Vite**
- **Redux Toolkit**
- **Material-UI (MUI)**
- **React Speech Recognition**
- **TypeScript**
- **SASS**

---

## 📦 Backend Setup

### 🔧 Requirements

- Python 3.10+
- PostgreSQL
- Redis
- `.env` file with necessary secrets

### 📥 Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/voice-vortex.git
cd voice-vortex/backend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate 
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Run the backend:

```bash
uvicorn main:app --reload
```

## 📦 Frontend Setup

1. Go to the frontend directory:

```bash
cd ../frontend
```

2. Install Node.js dependencies:

```bash
npm install
```

3. Run the frontend:

```bash
npm start
```

4. Access the app at:

```bash
http://localhost:3000/chatbot
```


## 📦 Project Structure


```
voice-vortex/
├── backend/
│ ├── Configuration/
│ │ └── config.py
│ ├── data/
│ │ └── chatbot_data.py
│ ├── data_preprocess/
│ │ └── prepare_data.py
│ ├── gemini_function/
│ │ └── prompt.py
│ ├── models/
│ │ └── pydantic.py
│ ├── utils/
│ │ └── nlp_utils.py
│ ├── main.py
│ ├── requirements.txt
│ └── ...
├── frontend/
│ ├── src/
│ │ ├── assets/
│ │ ├── common/
│ │ ├── components/
│ │ ├── pages/
│ │ ├── redux/
│ │ ├── services/
│ │ ├── utils/
│ │ ├── app.tsx
│ │ ├── environment.ts
│ │ ├── global.scss
│ │ └── main.tsx
│ ├── env
│ └── package.json
├── requirements.txt
├── README.md
└── .env.example
```


## 🙌 Acknowledgements

- [spaCy](https://spacy.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Generative AI](https://ai.google.dev/)
- [React Speech Recognition](https://www.npmjs.com/package/react-speech-recognition)
- [Material UI (MUI)](https://mui.com/)
