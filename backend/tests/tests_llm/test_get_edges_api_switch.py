"""Testing get edges but with switches to use the real API."""

import os

import pytest
from llm.graph_processing import api_request, get_edges, get_nodes


# This is a simple test double that can switch between mocked and real API calls
class APITestDouble:
    def __init__(self, use_real_api=False) -> None:
        self.use_real_api = use_real_api

    def request(self, *args, **kwargs):
        if self.use_real_api:
            return api_request(*args, **kwargs)
        else:
            # Return a mocked response
            return """{"edges": [{"label": "went to", "spans": [[1, 2]], "source": "Alice", "target": "London"}]}"""


@pytest.fixture()
def api_double(request):
    # Check if we should use the real API (e.g., from an environment variable)
    use_real_api = os.environ.get("USE_REAL_API", "false").lower() == "true"
    return APITestDouble(use_real_api)


class TestGetEdgesSwitch:
    def test_get_edges_switch(self, api_double, monkeypatch, test_nlp):
        # Monkeypatch the api_request function to use our test double
        monkeypatch.setattr("llm.graph_processing.api_request", api_double.request)

        existing_nodes = [{"label": "Alice", "spans": [[0]]}, {"label": "London", "spans": [[3]]}]
        doc = test_nlp("Alice went to London.")
        result = get_edges(doc, existing_nodes)

        # Our assertion remains the same whether we're using mocked or real data
        assert result == [{"label": "went to", "spans": [[1, 2]], "source": "Alice", "target": "London"}]

    @pytest.mark.skipif(
        os.environ.get("USE_REAL_API", "false").lower() != "true", reason="Skipped when not using real API"
    )
    def test_get_edges_real_api(self, api_double, monkeypatch, test_nlp):
        # This test will only run when USE_REAL_API is set to 'true'
        monkeypatch.setattr("llm.graph_processing.api_request", api_double.request)

        existing_nodes = [{"label": "Alice", "spans": [[0]]}, {"label": "London", "spans": [[3]]}]
        doc = test_nlp("Alice went to London.")
        result = get_edges(doc, existing_nodes)

        # Here you might want to make more specific assertions based on what you expect from the real API
        assert isinstance(result, list)
        assert all(isinstance(edge, dict) for edge in result)
        assert all("label" in edge and "spans" in edge and "source" in edge and "target" in edge for edge in result)

    @pytest.mark.skipif(
        os.environ.get("USE_REAL_API", "false").lower() != "true", reason="Skipped when not using real API"
    )
    def test_complex_example(self, api_double, monkeypatch, test_nlp):
        """Test both get nodes and get edges with the real API for a complex example."""
        # This test will only run when USE_REAL_API is set to 'true'
        monkeypatch.setattr("llm.graph_processing.api_request", api_double.request)

        # Create a complex input text with multiple sentences and multiple nodes
        text = (
            "At eight o'clock Kutuzov rode to Pratz at the head of Miloradovich's fourth column, the one which was "
            "to take the place of the columns of Przebyszewski and Langeron, which had already gone down. He "
            "greeted the men of the head regiment and gave the order to move, thus showing that he intended to "
            "lead the column himself. Having ridden to the village of Pratz, he halted. Prince Andrei, "
            "one of the enormous number of persons constituting the commander in chief's suite, stood behind him. "
            "Prince Andrei felt excited, irritated, and at the same time restrainedly calm, as a man usually is "
            "when a long-desired moment comes. He was firmly convinced that this was the day of his Toulon or his "
            "bridge of Arcole.[1] How it would happen, he did not know, but he was firmly convinced that it would "
            "be so. The locality and position of our troops were known to him, as far as they could be known to "
            "anyone in our army. His own strategic plan, which there obviously could be no thought of carrying "
            "out now, was forgotten. Now, entering into Weyrother's plan, Prince Andrei pondered the possible "
            "happenstances and came up with new considerations, such as might call for his swiftness of "
            "reflection and decisiveness."
        )

        doc = test_nlp(text)
        nodes = get_nodes(doc)
        # Tests on the nodes
        assert isinstance(nodes, list)

        edges = get_edges(doc, nodes)

        # Tests on the edges
        assert isinstance(edges, list)

        # Fuzzy assertions for nodes
        assert isinstance(nodes, list)
        assert len(nodes) > 10, "Expected at least 10 nodes to be extracted"

        expected_node_labels = ["Kutuzov", "Pratz", "Miloradovich", "Prince Andrei", "Toulon"]
        for label in expected_node_labels:
            assert any(node["label"] == label for node in nodes), f"Expected to find a node with label '{label}'"

        assert all("spans" in node and isinstance(node["spans"], list) for node in nodes)

        # Check for multi-token nodes
        assert any(len(node["spans"][0]) > 1 for node in nodes), "Expected to find at least one multi-token node"

        # Fuzzy assertions for edges
        assert isinstance(edges, list)
        assert len(edges) > 5, "Expected at least 5 edges to be extracted"

        expected_edge_labels = ["rode to", "at the head of", "greeted", "stood behind"]
        for label in expected_edge_labels:
            assert any(
                edge["label"].lower().startswith(label.lower()) for edge in edges
            ), f"Expected to find an edge with label starting with '{label}'"

        assert all("source" in edge and "target" in edge for edge in edges)

        # Check for consistency between nodes and edges
        node_labels = {node["label"] for node in nodes}
        edge_sources = {edge["source"] for edge in edges}
        edge_targets = {edge["target"] for edge in edges}
        assert edge_sources.issubset(node_labels), "All edge sources should correspond to node labels"
        assert edge_targets.issubset(node_labels), "All edge targets should correspond to node labels"

        # Check for specific relationships
        kutuzov_edges = [edge for edge in edges if edge["source"] == "Kutuzov"]
        assert len(kutuzov_edges) >= 2, "Expected at least 2 edges with Kutuzov as the source"

        prince_andrei_edges = [
            edge for edge in edges if edge["source"] == "Prince Andrei" or edge["target"] == "Prince Andrei"
        ]
        assert len(prince_andrei_edges) >= 1, "Expected at least 1 edge involving Prince Andrei"

        # Check for reasonable span values
        assert all(all(0 <= span < len(doc) for span_list in node["spans"] for span in span_list) for node in nodes)
        assert all(all(0 <= span < len(doc) for span in edge["spans"][0]) for edge in edges)
