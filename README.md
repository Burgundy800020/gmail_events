# Gmail Events

**Gmail Events** is an intelligent automation tool that scans your Gmail inbox, extracts event information from your emails using advanced AI, and seamlessly populates your calendar or exports structured event data. Never miss an important meeting, appointment, or social event buried in your inbox again!

---

## 🚀 Features

- **Automatic Event Extraction:** Uses OpenAI's GPT models to understand and extract event details (title, date, time, location, items to bring) from your emails.
- **Gmail Integration:** Securely connects to your Gmail account using OAuth2.
- **Structured Output:** Saves events in a machine-readable format (JSONL) for easy import into calendars or other tools.
- **API Server:** Built-in FastAPI server for real-time event access and integration.
- **Database Support:** Stores events in a PostgreSQL database for persistence and querying.
- **Customizable & Extensible:** Easily adapt polling intervals, output formats, and more.

---

## 🛠️ Technologies Used

- **Python 3.12+**
- **FastAPI** – High-performance web API framework
- **Uvicorn** – Lightning-fast ASGI server
- **OpenAI API** – Natural language event extraction
- **Google API Client** – Secure Gmail access
- **SQLAlchemy** – Database ORM for PostgreSQL
- **Pydantic** – Data validation and settings management
- **Structlog** – Structured logging
- **Conda** – Environment and dependency management

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/gmail_events.git
cd gmail_events
```

### 2. Set Up the Environment

Create and activate the Conda environment:

```bash
conda env create -f environment.yml
conda activate gmail_events
```

### 3. Configure Secrets

- Place your Gmail OAuth credentials in `secrets/credentials.json`.
- Generate a Gmail OAuth token using the provided Jupyter notebook (`get_oauth_token.ipynb`) or your preferred method. Save the token as `secrets/token.json`.
- Set your OpenAI API key in a `.env` file or as an environment variable (`OPENAI_API_KEY`).

### 4. Configure Database

Set your PostgreSQL connection string in a `.env` file:

```
DATABASE_URL=postgresql://user:password@localhost:5432/yourdb
```

### 5. Run the Application

#### As a Standalone Script

Extract events and save to a file:

```bash
python main.py --token secrets/token.json --output output/jiangjiang.jsonl
```

#### As an API Server

Start the FastAPI server:

```bash
python main.py
```

The API will be available at `http://localhost:8000`.

---

## ⚙️ Configuration

You can customize the behavior via environment variables or a `.env` file:

- `DATABASE_URL` – PostgreSQL connection string
- `OPENAI_API_KEY` – Your OpenAI API key
- `GMAIL_TOKEN_PATH` – Path to your Gmail OAuth token
- `OUTPUT` – Output file for events
- `POLLING_INTERVAL` – How often to check for new emails (in seconds)
- `ALL_TIME` – If true, processes all emails, not just new ones

---

## 📂 Output Example

Each extracted event is saved as a JSON object:

```json
{
  "name": "Movie night out",
  "datetime": "2025-06-10T00:00:00Z",
  "location": "Squirrel Hill Theatre",
  "items_to_bring": ["theatre coupons"]
}
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Please open an issue or submit a pull request.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## ✨ Acknowledgements

- [OpenAI](https://openai.com/)
- [Google Cloud](https://cloud.google.com/)
- [FastAPI](https://fastapi.tiangolo.com/)

```bash
python main.py --token secrets/token.json --output output.jsonl
``` 
