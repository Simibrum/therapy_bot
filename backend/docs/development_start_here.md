# Development Start Here - Therapy Bot Knowledge Graph Integration

*Last updated: June 1, 2025*  
*Branch: dev_knowledge_graph_sync*  
*Status: Ready for knowledge graph integration*

## Project Overview

This is a therapy chatbot that uses GPT-4 to conduct therapy sessions via websocket connections. The system includes user authentication, persistent chat history, and vector-based similarity search for retrieving relevant past conversations.

## Current Architecture

### Core Flow
1. **Session Creation**: `/sessions/new` creates a new `TherapySession` 
2. **Websocket Connection**: `/ws/session/{therapy_session_id}` handles real-time chat
3. **Message Processing**: `TherapySessionLogic` manages conversation flow and responses
4. **Vector Search**: Each chat message gets embedded and stored for similarity search

### Key Components

**Models:**
- `TherapySession` - Links user, therapist, and chat messages
- `Chat` - Individual messages with encrypted text and vector embeddings
- `User` / `Therapist` - Authentication and profiling
- `Node` / `Edge` - Knowledge graph entities (ready but not integrated)

**Logic Layer:**
- `TherapySessionLogic` - Main session management and conversation flow
- `get_nodes()` / `get_edges()` - LLM-powered entity extraction (tested, working)
- `process_text_and_create_references()` - Database integration for graph entities

**API Layer:**
- FastAPI routes with websocket support
- Token-based authentication
- RESTful session management

## Knowledge Graph Status

### ✅ Working Components
- **Entity Extraction**: `llm/graph_processing.py` with `get_nodes()` and `get_edges()`
- **Graph Models**: `Node`, `Edge`, `ChatReference` models ready
- **SpaCy Integration**: Token-level entity mapping with spans
- **Database Layer**: User-scoped nodes with SQLAlchemy integration
- **Tests**: Full test coverage for core extraction functions

### 🚧 Integration Points Identified
1. **Real-time Processing**: Extract entities during `generate_response()` 
2. **Batch Processing**: Process existing chat history for graph building
3. **Graph Querying**: Expose entities via API endpoints for visualization

### 🎯 Next Steps (Pomodoro 5)

**Option A: Real-time Integration** (Recommended)
- Hook `process_text_and_create_references()` into `add_chat_message()`
- Extract entities from both user input and therapist responses
- Start building graph incrementally as conversations happen

**Option B: Batch Processing**
- Create script to process existing `Chat` messages
- Build historical knowledge graph from past sessions
- Good for testing and seeing immediate results

**Option C: API Endpoint**
- Add `/sessions/{id}/entities` endpoint
- Show extracted entities for a given therapy session
- Useful for debugging and development

## File Locations

```
backend/
├── docs/                          # Documentation (this file)
├── app/routes/therapy_sessions.py # Websocket and session routes
├── logic/therapy_session_logic.py # Core session management
├── llm/graph_processing.py        # Entity extraction (LLM calls)
├── logic/process_chat_create_nodes.py # DB integration for entities
├── models/
│   ├── chat.py                    # Chat messages with vectors
│   ├── graph/node.py              # Knowledge graph nodes
│   └── graph/edge.py              # Knowledge graph relationships
└── tests/tests_llm/               # Entity extraction tests
```

## Development Environment

- **Python**: 3.13.3 in fresh virtual environment
- **Tests**: All passing except 1 GPU test (SpaCy/CuPy issue - can ignore)
- **Database**: SQLite with SQLAlchemy ORM
- **LLM**: GPT-4o for entity extraction
- **NLP**: SpaCy for tokenization and spans

## Integration Decision

The cleanest integration point appears to be in `TherapySessionLogic.add_chat_message()`:

```python
def add_chat_message(self, sender, text) -> ChatOut:
    # ... existing code ...
    session.commit()
    
    # NEW: Extract entities and create graph references
    if hasattr(self, 'nlp'):  # Add nlp to __init__
        chat_refs = process_text_and_create_references(
            text, new_chat.therapy_session_id, self.user_id, session, self.nlp
        )
    
    # ... rest of method ...
```

This would create knowledge graph entries for every message (both user and therapist) as they're added to the database.

## Questions for Next Session

1. **Entity Focus**: What entities are most valuable? People mentioned, emotional states, therapy topics, or something else?
2. **Performance**: Should extraction be async/background, or is real-time acceptable?
3. **Visualization**: How do you want to expose/view the knowledge graph data?
4. **Privacy**: Any special considerations for therapy data in knowledge graphs?