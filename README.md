# O-IAxis by Vrilon

**Financial Intelligence Platform for Emerging Corporate Markets**

A quantum-ready, hybrid infrastructure system featuring 17 intelligent engines for comprehensive financial analysis, prediction, and corporate decision-making.

## Project Status

**Phase**: PHASE_0_SETUP (Day 1 - Initial Infrastructure)

## Quick Start

### Prerequisites
- Python 3.10+
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd O-IAxis
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

4. Start the API server:
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## Project Structure

```
O-IAxis/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration
│   │   ├── db/             # Database
│   │   ├── models/         # SQLAlchemy models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   └── tests/              # Unit & integration tests
├── frontend/               # React/Vue frontend
├── ml/                     # Machine Learning engines
├── quantum/                # Quantum computing modules
├── infrastructure/         # Docker, Kubernetes, Terraform
├── docs/                   # Documentation
└── .github/                # GitHub workflows
```

## Development Phases

1. **PHASE 0**: Setup & Infrastructure (Week 1)
2. **PHASE 1**: Backend Core & Database (Weeks 2-3)
3. **PHASE 2**: Financial Engines (Weeks 4-5)
4. **PHASE 3**: ML & Quantum (Weeks 6-7)
5. **PHASE 4**: Frontend & UI (Week 8)
6. **PHASE 5**: Testing & Launch (Week 9)

## Documentation

- [Architecture](docs/architecture/)
- [API Documentation](docs/api/)
- [Development Guide](docs/development/)

## Technology Stack

- **Backend**: Python, FastAPI, SQLAlchemy
- **Database**: MySQL/PostgreSQL
- **ML**: scikit-learn, TensorFlow
- **Quantum**: Qiskit, PennyLane
- **Frontend**: React/Vue (TBD)
- **Infrastructure**: Docker, Kubernetes, Terraform

## Team

- **CTO**: Rodolfo

## License

Confidential - Vrilon Corporation

---

**Created**: 2026-06-25  
**Version**: 0.1.0
