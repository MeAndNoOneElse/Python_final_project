# Architecture Overview

## System Components

SplitChek consists of three main components:

### 1. FastAPI Server (Backend)
- **Location**: `programm/server/`
- **Purpose**: RESTful API for data management
- **Key Modules**:
  - `api/` - API endpoints
  - `db/` - Database models and repositories
  - `services/` - Business logic
  - `schemas/` - Pydantic models

### 2. Telegram Bot
- **Location**: `programm/bot/`
- **Purpose**: User interface via Telegram
- **Features**:
  - Private commands
  - Group management
  - NLU message processing

### 3. React Frontend
- **Location**: `programm/web/`
- **Purpose**: Web interface for the application
- **Built with**: Vite + React

## Data Flow

```
User -> Telegram Bot -> FastAPI Server <-> Database
     -> Web Frontend ----
```

## Authors

- **andrey** - Server and Web Frontend
- **habib** - Telegram Bot