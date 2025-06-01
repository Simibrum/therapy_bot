"""LLM functions for graph processing."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING

from config import logger

if TYPE_CHECKING:
    from spacy.tokens import Doc

from models.knowledge import VALID_TYPES

from llm.common import api_request

MODEL = "gpt-4o"

GRAPH_PROCESSOR_SYSTEM_PROMPT = (
    "You are an AI expert specializing in knowledge graph creation with the "
    "goal of capturing relationships based on a given input or request.\n"
    "* Based on the user input in various forms such as chat messages, paragraph, "
    "email, text files, and more.\n"
    "* Your task is to create a knowledge graph based on the input.\n"
    "* You will be asked to provide nodes and edges for the knowledge graph.\n"
    "* Nodes relate to entities such as people, places, and events.\n"
    "* Nodes must have a label parameter. where the label is a direct word or phrase from the input.\n"
    "* Nodes must have a spans parameter that is a list of spans associated with the node label, each span being a "
    "list of the indexes of the tokens that make up the label. The token indexes are indicated "
    "in square brackets in the input.\n"
    "* Edges relate to the information that connects nodes. They are typically a set of tokens.\n"
    "* Edges must also have a label parameter, where the label is a direct word or phrase from the input, and a spans "
    "parameter that is a list of spans associated with the node label, where each span is a list of "
    "token indexes for the label.\n"
    "* Respond only with JSON in a format where we can jsonify in python.\n"
    "* Make sure the target and source of edges match an existing node.\n"
    "* Do not include the markdown triple quotes above and below the JSON, jump straight into it "
    "with a curly bracket.\n"
)

TYPE_STRING = ", ".join([f'"{TYPE}"' for TYPE in VALID_TYPES])

GP_NODE_JSON_PROMPT = (
    "Here an example of the JSON format for the nodes in the knowledge graph.\n"
    "{\n"
    '  "nodes": [\n'
    "    {\n"
    '      "label": "Apple",\n'
    '      "spans": [[0]],\n'
    f'      "type": one of {TYPE_STRING},\n'
    "    },\n"
    "    {\n"
    '      "label": "Steve Jobs",\n'
    '      "spans": [[4, 5]],\n'
    f'      "type": one of {TYPE_STRING},\n'
    "    }\n"
    "  ]\n"
    "}"
)

GP_NODE_PROMPT = (
    "Please provide the nodes for the knowledge graph based on the following input text.\n"
    "\n"
    "Input Text: \n"
    "{}\n\n"
    "Token Indexes: {}"
)

GP_EDGE_JSON_PROMPT = (
    "Here an example of the JSON format for the edges in the knowledge graph.\n"
    "{\n"
    '  "edges": [\n'
    "    {\n"
    '      "label": "was run by",\n'
    '      "source": 1,\n'
    '      "target": 2,\n'
    '      "spans": [[1, 3]],\n'
    "    }\n"
    "  ]\n"
    "}"
)

GP_EDGE_PROMPT = (
    "Please provide the edges for the knowledge graph based on the following input text.\n"
    "\n"
    "Input Text: \n"
    "{}\n\n"
    "Token Indexes: {}"
)

GP_EXISTING_NODES_PROMPT = (
    "Here are the extracted nodes for the knowledge graph. Please provide the edges based on these nodes.\n" "{}"
)


def get_nodes(doc: Doc) -> list[dict]:
    """Generate candidate nodes from the input text."""
    text = doc.text
    tokens_and_indexes = [(token.text, token.i) for token in doc]

    messages = [
        {"role": "system", "content": GRAPH_PROCESSOR_SYSTEM_PROMPT},
        {"role": "user", "content": GP_NODE_JSON_PROMPT + "\n\n" + GP_NODE_PROMPT.format(text, tokens_and_indexes)},
    ]

    response = api_request(messages=messages, model=MODEL, temperature=0.1)
    # Parse the response as JSON
    try:
        # First replace any stray triple backticks
        clean_response = response.replace("```", "")
        nodes = json.loads(clean_response)
    except json.JSONDecodeError:
        logger.error(f"Error parsing JSON response: {response}")
        nodes = {}
    # If the response is nested, extract the nodes
    if "nodes" in nodes:
        nodes = nodes["nodes"]
    return nodes


def get_edges(doc: Doc, existing_nodes: list[dict]) -> list[dict]:
    """Generate candidate edges from the input text."""
    text = doc.text
    tokens_and_indexes = [(token.text, token.i) for token in doc]

    messages = [
        {"role": "system", "content": GRAPH_PROCESSOR_SYSTEM_PROMPT},
        {"role": "user", "content": GP_EDGE_JSON_PROMPT},
        {"role": "user", "content": GP_EDGE_PROMPT.format(text, tokens_and_indexes)},
        {"role": "user", "content": GP_EXISTING_NODES_PROMPT.format(existing_nodes)},
    ]

    response = api_request(messages=messages, model=MODEL, temperature=0.1)
    # Parse the response as JSON
    try:
        # First replace any stray triple backticks
        clean_response = response.replace("```", "")
        edges = json.loads(clean_response)
    except json.JSONDecodeError:
        logger.error(f"Error parsing JSON response: {response}")
        edges = {}
    # If the response is nested, extract the edges
    if "edges" in edges:
        edges = edges["edges"]
    return edges
