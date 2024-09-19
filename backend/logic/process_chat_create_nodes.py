"""Logic to process chat text data to generate knowledge graph representations."""
import spacy
from llm.graph_processing import get_nodes
from models.chat_reference import ChatReference
from models.graph.node import Node
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


def process_text_and_create_references(
    text: str, chat_id: int, user_id: int, db: Session, nlp: spacy.language.Language
) -> list[ChatReference]:
    """Process the text and create ChatReferences and Nodes in the database."""
    # Generate Spacy doc
    doc = nlp(text)

    # Get nodes from the doc
    node_data = get_nodes(doc)

    chat_references = []

    for node in node_data:
        try:
            # Try to find an existing node or create a new one
            db_node = db.query(Node).filter_by(label=node["label"], user_id=user_id).first()
            if not db_node:
                db_node = Node(label=node["label"], user_id=user_id)
                db.add(db_node)
                db.flush()  # This will populate the id of the new node

            # Create ChatReference
            for span in node["spans"]:
                chat_ref = ChatReference(
                    chat_id=chat_id,
                    node_id=db_node.id,
                    span_idx_start=span[0],
                    span_idx_end=span[-1],
                    character_idx_start=doc[span[0]].idx,
                    character_idx_end=doc[span[-1]].idx + len(doc[span[-1]]),
                )
                db.add(chat_ref)
                chat_references.append(chat_ref)

        except SQLAlchemyError as e:
            db.rollback()
            raise e

    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e

    return chat_references
