# Central Command Hub

Foundational repository scaffolding for the **Central Command Hub**—a dashboard used to orchestrate a multi-agent digital conglomerate.

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, Uvicorn, Pydantic
- **Frontend**: React (initialized via Vite), Tailwind CSS, Lucide React (icons)

## Repository Structure

```text
.
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── routers/
│       ├── __init__.py
│       ├── agents.py
│       └── memory.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── index.css
│       ├── main.jsx
│       └── components/
│           ├── DashboardPanel.jsx
│           ├── Sidebar.jsx
│           └── TopNav.jsx
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js (v18+) and npm/yarn

---

### Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI backend server**:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```
   The API will be accessible at `http://localhost:8000`. Interactive documentation is available at `http://localhost:8000/docs`.

---

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the Vite development server**:
   ```bash
   npm run dev
   ```
   The frontend application will be running at `http://localhost:3000`.

4. **Build for production**:
   ```bash
   npm run build
   ```

---

## API Endpoints Summary

- `GET /` - Root status check.
- `GET /api/health` - Health check.
- `GET /api/agents` - List all managed agents.
- `GET /api/agents/{agent_id}` - Retrieve specific agent info.
- `GET /api/memory` - Retrieve shared memory and context logs.
