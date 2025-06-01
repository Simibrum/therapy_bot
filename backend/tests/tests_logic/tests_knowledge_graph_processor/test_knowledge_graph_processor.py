"""Tests for the knowledge graph processor."""

import pytest
from models import Edge, Node
from sqlalchemy import select

# Mock data for get_nodes
mock_nodes = [
    {"label": "John", "spans": [[0]], "type": "person"},
    {"label": "pizza", "spans": [[2]], "type": "object"},
    {"label": "New York", "spans": [[6, 7]], "type": "place"},
]


def mock_get_nodes(doc):
    return mock_nodes


# Mock data for get_edges
mock_edges = [{"label": "lives in", "source": 1, "spans": [[1, 2]], "target": 2}]


def mock_get_edges(doc, nodes):
    return mock_edges


@pytest.mark.asyncio()
def test_extract_entities(async_knowledge_graph_processor, monkeypatch):
    text = "John loves pizza and lives in New York."
    monkeypatch.setattr("logic.knowledge_graph_processor.knowledge_graph_processor.get_nodes", mock_get_nodes)
    entities = async_knowledge_graph_processor.extract_entities(text)
    assert len(entities) == 3
    assert any(e["label"] == "John" for e in entities)
    assert any(e["label"] == "pizza" for e in entities)
    assert any(e["label"] == "New York" for e in entities)


# Asynchronous tests
@pytest.mark.asyncio()
async def test_create_or_update_nodes_async(async_knowledge_graph_processor, async_user_instance):
    entities = mock_nodes
    nodes = await async_knowledge_graph_processor.create_or_update_nodes(entities, async_user_instance.id)
    assert len(nodes) == 3
    assert any(n.label == "John" and n.type == "person" for n in nodes)
    assert any(n.label == "pizza" and n.type == "object" for n in nodes)
    assert any(n.label == "New York" and n.type == "place" for n in nodes)


@pytest.mark.asyncio()
async def test_create_edges_async(
    async_knowledge_graph_processor, async_user_instance, async_chat_instance, async_shared_session, monkeypatch
):
    # Monkey patch get_edges
    monkeypatch.setattr("logic.knowledge_graph_processor.knowledge_graph_processor.get_edges", mock_get_edges)
    nodes = [
        Node(label="Emily", user_id=async_user_instance.id, node_type="person"),
        Node(label="London", user_id=async_user_instance.id, node_type="place"),
    ]
    async_shared_session.add_all(nodes)
    async_chat_instance.text = "Emily lives in London."
    await async_shared_session.commit()
    edges = await async_knowledge_graph_processor.create_edges(nodes, async_chat_instance)
    assert len(edges) == 1
    assert edges[0].from_node_id == 1
    assert edges[0].to_node_id == 2
    assert edges[0].type == "lives in"


@pytest.mark.asyncio()
async def test_process_chat_async(
    async_knowledge_graph_processor, async_chat_instance, async_shared_session, monkeypatch
):
    async_chat_instance.text = "Bob works at Microsoft in Seattle"
    await async_shared_session.commit()

    def mock_get_nodes(doc):
        return [
            {"label": "Bob", "spans": [[0]], "type": "person"},
            {"label": "Microsoft", "spans": [[3]], "type": "organisation"},
            {"label": "Seattle", "spans": [[5]], "type": "place"},
        ]

    def mock_get_edges(doc, nodes):
        return [
            {"label": "works at", "source": 1, "spans": [[1, 2]], "target": 2},
            {"label": "in", "source": 1, "spans": [[4]], "target": 3},
        ]

    monkeypatch.setattr("logic.knowledge_graph_processor.knowledge_graph_processor.get_nodes", mock_get_nodes)
    monkeypatch.setattr("logic.knowledge_graph_processor.knowledge_graph_processor.get_edges", mock_get_edges)

    await async_knowledge_graph_processor.process_chat(async_chat_instance)

    # Check if nodes were created
    statement = select(Node)
    result = await async_knowledge_graph_processor.db.execute(statement)
    nodes = result.scalars().all()
    assert len(nodes) == 3
    assert any(n.label == "Bob" for n in nodes)
    assert any(n.label == "Microsoft" for n in nodes)
    assert any(n.label == "Seattle" for n in nodes)

    # Check if edges were created
    statement = select(Edge)
    result = await async_knowledge_graph_processor.db.execute(statement)
    edges = result.scalars().all()
    assert len(edges) == 2  # 'works at' and 'in'
