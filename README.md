# therapy_bot
This is a proof of concept for a GPT-4 powered chatbot. The project explores how GPT models work with mental health dialogues and plays with chat memory and user profiling.

# Therapy-Bot Project Resurrection - June 2025

## Current State Summary
- **Branch**: dev_graph_building (main development branch)
- **Last active**: ~8 months ago
- **Status**: Mid-migration from sync to async database operations

## Test Results (June 1, 2025)
- **62 tests failing, 72 passed, 2 ignored** (136 total)
- **Primary issue**: SQLAlchemy async greenlet context errors
- **Root cause**: Tests not updated for async database operations

## Architecture Changes in Progress
- ✅ Async database engine setup
- ✅ Knowledge graph processor foundation
- ✅ Chat processor and vector processor modules
- ❌ Test suite async context migration (incomplete)
- ❌ Async route handlers (partially complete)

## Next Session Priorities
1. Fix async test context setup in conftest.py
2. Update failing tests to use async database sessions
3. Focus on knowledge graph extraction functionality

## Languages and Frameworks
- Python
- JavaScript
- React

## Python Libraries
- SQLAlchemy
- Pydantic

## Installation
For Python dependencies, use pip:
pip install -r requirements.txt
For JavaScript dependencies, use npm:
npm install

## Folder Structure
- backend: FastAPI backend
    - app: FastAPI application
        - crud: CRUD operations
        - routes: FastAPI routes
        - schemas: Pydantic schemas
        - main.py: FastAPI application instance
    - database: SQLAlchemy ORM with SQLite database
    - models: SQLAlchemy models
    - tests: tests
    - migrations: Alembic migrations
    - logic: logic for the chatbot
    - llm: functions to generate content
    - utils: utility functions
- frontend: React frontend
  - node_modules: node modules 
  - public: public files
  - src: source files
    - components: React components
    - images: images
    - App.js: main React component
    - index.js: React entry point
    - ...

## Database
The project uses SQLAlchemy ORM for database interactions. The declarative base for SQLAlchemy models is defined in backend/database/__init__.py.

## Schemas
Pydantic models for data validation and serialization are defined in backend/app/schemas.

## CRUD Operations
CRUD operations for users are defined in backend/app/crud/users.py.

## Usage
This project is experimental and is intended for research purposes only.

## Disclaimer
DO NOT USE THIS FOR ANY PURPOSE OTHER THAN RESEARCH.# therapy_bot

# Development Plan

Current Priorities:
- [X] Create a basic chatbot with GPT-4
- [X] Implement user account
- [X] Implement chat memory
- [ ] Add graph memory for people, places, and things