# ML Tutor

Simple machine learning Q&A app built with FastAPI and a small HTML frontend.

The backend loads a PDF from `data/ml.pdf`, retrieves relevant chunks with Chroma, and uses Groq to generate an answer. The frontend is served by FastAPI from `Backend/static`.

## Project Structure

- `Backend/main.py` - FastAPI app with `GET /` and `POST /chat`
- `Backend/rag.py` - RAG pipeline and vector store setup
- `Backend/static/` - HTML, CSS, and JavaScript frontend
- `data/ml.pdf` - source study material
- `chroma_db/` - persisted Chroma vector database

## Requirements

- Python 3.10+ recommended
- A `.env` file with `GROQ_API_KEY`

Example:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Install

From the project root:

```powershell
.
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If you do not already have a virtual environment, create one first:

```powershell
python -m venv venv
```

## Run the App

Start the backend from the `Backend` folder:

```powershell
cd Backend
uvicorn main:app --reload
```

Open the app in your browser at:

```text
http://127.0.0.1:8000/
```

## How It Works

1. Type a question into the search box.
2. Click Search or press Enter.
3. The frontend sends the query to `POST /chat`.
4. The backend retrieves relevant context from the PDF and returns an answer.

## API

### `POST /chat`

Request body:

```json
{
  "question": "What is overfitting?"
}
```

Response:

```json
{
  "answer": "..."
}
```

## Notes

- The first run may take longer because the embeddings and Chroma store need to load.
- If `chroma_db/` is deleted, the vector store will be rebuilt from `data/ml.pdf`.
