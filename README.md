# Project Setup Guide

## Prerequisites
- Python 3.x installed
- `venv` module available
- Docker & Docker Compose installed

---

## Setup Instructions

### 1. Create and Activate Virtual Environment
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # For Linux/MacOS
# OR
venv\Scripts\activate     # For Windows
```

---

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 3. Start the Services
Run the following command to start all required services (Grafana, Jaeger, etc.):

```bash
docker-compose up --build
```

---

### 4. Access Services
- **Grafana** → [http://localhost:3000](http://localhost:3000)  
- **Jaeger** → [http://localhost:16686](http://localhost:16686)

---

### 5. Stop Services
When you're done, stop the services with:

```bash
docker-compose down
```

---

## Notes
- Make sure to always **activate your virtual environment** before running any commands.
- Update `requirements.txt` if you add or modify Python packages.