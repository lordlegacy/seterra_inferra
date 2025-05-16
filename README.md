# Seterra Inferra – AI-Powered IT Ticketing Backend

[![GitHub](https://img.shields.io/badge/repo-github-blue)](https://github.com/lordlegacy/seterra_inferra)

Seterra Inferra is a FastAPI-powered backend for an IT support ticketing system enhanced with an **AI agent** that uses **RAG (Retrieval-Augmented Generation)** to recommend solutions. It features automatic ticket embedding using `pgvector`, secure authentication, and role-based access control.

---

## 🚀 Features

- 📝 Users can register and create IT support tickets
- 🔐 JWT-based authentication
- 👤 Role-based access: `user`, `support`, `admin`
- 🧠 AI (LLM) integration for ticket resolution using:
  - Prompt engineering
  - Context retrieval from ticket history, docs, and web snippets
  - Embedding & semantic search with `pgvector`
- 📄 Document ingestion: PDF, DOCX, Markdown
- 📈 Full vector search RAG system
- 🪄 Admin APIs for managing users and ticket statuses

---

## 🔗 Key Routes

### 🧑‍💼 Auth (`/api/v1/auth`)
| Method | Route         | Description                  |
|--------|---------------|------------------------------|
| POST   | `/register`   | Register a new user          |
| POST   | `/login`      | Log in and receive JWT token |

---

### 🧾 Tickets (`/api/v1/tickets`)
| Method | Route               | Description                              |
|--------|---------------------|------------------------------------------|
| POST   | `/`                 | Create a ticket (auto-runs AI resolver)  |
| GET    | `/`                 | List your tickets (or all if admin)      |
| PATCH  | `/{ticket_id}`      | Update ticket status (admin/support)     |

---

### 🧠 LLM & RAG (`/api/v1/llm`)
| Method | Route                         | Description                    |
|--------|-------------------------------|--------------------------------|
| POST   | `/resolve_ticket/{ticket_id}` | Manually trigger AI resolution |

---

### 📚 Document Ingestion (`/api/v1/llm/ingest_doc/`)
| Method | Route                | Description                     |
|--------|----------------------|---------------------------------|
| POST   | `/ingest_doc/`       | Upload and embed documents      |

---

### 👤 Users (`/api/v1/users`)
| Method | Route                     | Description                        |
|--------|---------------------------|------------------------------------|
| GET    | `/`                       | List users (admin only)            |
| GET    | `/me`                     | Get your own user profile          |
| PATCH  | `/{user_id}/role`         | Update user role (admin only)      |
| DELETE | `/{user_id}`              | Delete a user (admin only)         |

---

## 🧠 How the AI Agent Works (RAG Flow)

1. 📝 Ticket is created (title + description)
2. 🧬 Text is embedded with LangChain and stored in `pgvector`
3. 🔎 Context is retrieved from:
   - Similar past tickets
   - Ingested documents
   - Web snippets
4. 🤖 A prompt is generated and sent to an LLM (e.g. Gemini)
5. 📥 LLM returns structured JSON with:
   - Summary
   - Diagnoses
   - Recommended solutions
6. 💾 Result is stored with the ticket and re-embedded

---

## 🧰 Tech Stack

- **FastAPI** – Modern Python API framework
- **PostgreSQL + pgvector** – Vector search database
- **LangChain** – Embedding, chunking, LLM orchestration
- **Gemini API** – Language model inference
- **JWT** – Authentication & session management
- **SQLAlchemy** – ORM layer for DB access

---

## 📂 Repository

**GitHub:** [https://github.com/lordlegacy/seterra_inferra](https://github.com/lordlegacy/seterra_inferra)

---

## 🧪 Development Notes

- Use `.env` to configure secrets like `JWT_SECRET_KEY`, `DATABASE_URL`, and `GEMINI_API_KEY`.
- To ingest documents, call `/api/v1/llm/ingest_doc/` with PDF/DOCX/MD.
- Embedding is done using NomicEmbedText via LangChain.
- RAG retrieval searches across:
  - Ticket embeddings
  - Document chunks
  - Web snippets

---

## 🛡️ Roles

| Role     | Capabilities                                     |
|----------|--------------------------------------------------|
| `user`   | Create/view tickets                              |
| `support`| View all tickets, update status, resolve         |
| `admin`  | Manage users, roles, view everything             |

---

## 📈 Future Ideas

- Live chat handoff to human support
- Feedback loop for AI accuracy
- Vector indexing for ticket comments
- Full frontend interface

---

MIT Licensed. Built for learning and exploration.


