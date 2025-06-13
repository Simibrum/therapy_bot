"""Class to process Chat objects and create/update a knowledge graph."""

import asyncio
from typing import Dict, List, Union

import spacy
from llm.graph_processing import get_edges, get_nodes
from models.chat import Chat
from models.graph.edge import Edge
from models.graph.node import Node
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


class KnowledgeGraphProcessor:
    """Class to process Chat objects and create/update a knowledge graph."""
    def __init__(self, db: Union[Session, AsyncSession], nlp: spacy.language.Language) -> None:
        self.db = db
        self.nlp = nlp

    async def process_chat(self, chat: Chat) -> None:
        """Process a Chat object and update the knowledge graph asynchronously."""
        entities = self.extract_entities(chat.text)
        nodes = await self.create_or_update_nodes(entities, chat.user_id)
        edges = await self.create_edges(nodes, chat)
        await self.update_graph(nodes, edges)

    def extract_entities(self, text: str) -> List[Dict]:
        """Extract entities from the given text using NLP."""
        doc = self.nlp(text)
        return get_nodes(doc)

    @staticmethod
    def _match_node_by_string(label: str, candidate_nodes: List[Node]) -> Node:
        """Match a node to an existing node in a list of nodes."""
        return next((n for n in candidate_nodes if n.label == label), None)

    async def _find_node_by_string(self, label: str, user_id: int) -> Node:
        """Find a node in the DB by its label."""
        statement = select(Node).where(Node.label == label, Node.user_id == user_id)
        result = await self.db.execute(statement)
        return result.scalars().first()

    async def create_or_update_nodes(self, entities: List[Dict], user_id: int) -> List[Node]:
        """Create new nodes or update existing ones based on extracted entities."""
        nodes = []
        for entity in entities:
            # Check if node exists
            node = await self._find_node_by_string(entity["label"], user_id)
            if not node:
                # Create new node
                node = Node(label=entity["label"], user_id=user_id, node_type=entity["type"])
                self.db.add(node)
            # You might want to update node properties here
            nodes.append(node)
        await self.db.commit()
        return nodes

    async def create_edges(self, nodes: List[Node], chat: Chat) -> List[Edge]:
        """Create edges between nodes based on their relationships in the chat."""
        # Convert nodes to the format expected by get_edges
        node_dicts = [{"label": node.label, "id": node.id} for node in nodes]

        # Create doc - is this needed?
        doc = self.nlp(chat.text)

        # Get edge candidates using the get_edges function
        edge_candidates = get_edges(doc, node_dicts)

        edges = []
        for edge_data in edge_candidates:
            # This is a simple matching algorithm, you might want to improve it
            source_node = await self.db.get(Node, edge_data["source"])
            target_node = await self.db.get(Node, edge_data["target"])

            if source_node and target_node:
                edge = Edge(
                    user_id=chat.user_id,
                    from_node_id=source_node.id,
                    to_node_id=target_node.id,
                    type=edge_data["label"],
                    description=f"{edge_data['source']} {edge_data['label']} {edge_data['target']}",
                )
                self.db.add(edge)
                edges.append(edge)

        await self.db.commit()
        return edges

    async def update_graph(self, nodes: List[Node], edges: List[Edge]) -> None:
        """Update the knowledge graph with new nodes and edges."""
        # This method might involve updating global graph statistics,
        # triggering any graph-wide computations, etc.
        # For now, we'll just ensure all changes are committed to the database
        await self.db.commit()


class GraphProcessingQueue:
    def __init__(self) -> None:
        """Create a new processing queue."""
        self.queue = asyncio.Queue()

    async def add_task(self, chat: Chat) -> None:
        """Add a chat to the processing queue."""
        await self.queue.put(chat)

    async def process_queue(self, processor: KnowledgeGraphProcessor) -> None:
        """Process the queue of chat messages."""
        while True:
            chat = await self.queue.get()
            await processor.process_chat(chat)
            self.queue.task_done()


# Usage example (you would typically do this in your main application code):
# async def setup_graph_processing(db_session, nlp_model):
#     processor = KnowledgeGraphProcessor(db_session, nlp_model)
#     queue = GraphProcessingQueue()
#     asyncio.create_task(queue.process_queue(processor))
#     return queue

# Then in your application code:
# graph_queue = await setup_graph_processing(db_session, nlp_model)
#
# # When you receive a new chat message:
# asyncio.create_task(graph_queue.add_task(chat_message))
