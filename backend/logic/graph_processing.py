"""Logic for processing chat text data to generate knowledge graph representations."""
from __future__ import annotations

from hashlib import sha256
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import Doc


def generate_candidate_nodes(doc: Doc) -> list[dict]:
    """Generate candidate nodes from the input text."""
    nodes = []

    for ent in doc.ents:
        node = {
            "text": ent.text,
            "start_char": ent.start_char,
            "end_char": ent.end_char,
            "start_token": ent.start,
            "end_token": ent.end,
            "sentence_index": list(doc.sents).index(ent.sent),
            "label": ent.label_,
        }
        nodes.append(node)

    return nodes


def generate_candidate_node_ids(nodes: list[dict]) -> dict:
    """Generate candidate node IDs from the input nodes."""
    node_ids = {}

    for node in nodes:
        salted_node_text = f"{node['text']}_{node['start_char']}_{node['end_char']}"
        node_id = sha256(salted_node_text.encode("utf-8")).hexdigest()
        node_ids[node["start_token"]] = node_id

    return node_ids
