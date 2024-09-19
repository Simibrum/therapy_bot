"""Test the get edges function."""


import pytest
from llm.graph_processing import get_edges  # Replace 'your_module' with the actual module name


class TestGetEdges:
    @pytest.fixture()
    def mock_api_request(self, mocker):
        return mocker.patch("llm.graph_processing.api_request")

    def test_generates_edges_correctly(self, mock_api_request, test_nlp):
        existing_nodes = [{"label": "Alice", "spans": [[0]]}, {"label": "London", "spans": [[3]]}]
        api_response = """{
            "edges": [
                {"label": "went to", "spans": [[1, 2]], "source": "Alice", "target": "London"}
            ]
        }"""
        mock_api_request.return_value = api_response
        doc = test_nlp("Alice went to London.")
        result = get_edges(doc, existing_nodes)
        assert result == [{"label": "went to", "spans": [[1, 2]], "source": "Alice", "target": "London"}]

    def test_handles_empty_input_text(self, mock_api_request, test_nlp):
        mock_api_request.return_value = '{"edges": []}'
        doc = test_nlp("")
        result = get_edges(doc, [])
        assert result == []

    def test_handles_multiple_edges(self, mock_api_request, test_nlp):
        existing_nodes = [
            {"label": "John", "spans": [[0]]},
            {"label": "Mary", "spans": [[2]]},
            {"label": "park", "spans": [[6]]},
        ]
        api_response = """{
            "edges": [
                {"label": "met", "spans": [[1]], "source": "John", "target": "Mary"},
                {"label": "at", "spans": [[3]], "source": "John", "target": "park"},
                {"label": "at", "spans": [[3]], "source": "Mary", "target": "park"}
            ]
        }"""
        mock_api_request.return_value = api_response
        doc = test_nlp("John met Mary at the park.")
        result = get_edges(doc, existing_nodes)
        assert result == [
            {"label": "met", "spans": [[1]], "source": "John", "target": "Mary"},
            {"label": "at", "spans": [[3]], "source": "John", "target": "park"},
            {"label": "at", "spans": [[3]], "source": "Mary", "target": "park"},
        ]

    def test_handles_api_error(self, mock_api_request, test_nlp):
        mock_api_request.side_effect = Exception("API Error")
        doc = test_nlp("This should cause an error.")
        with pytest.raises(Exception, match="API Error"):
            get_edges(doc, [])

    def test_correct_prompts_used(self, mock_api_request, test_nlp):
        existing_nodes = [{"label": "Alice", "spans": [[0]]}]
        mock_api_request.return_value = '{"edges": []}'
        doc = test_nlp("Alice went to London.")
        get_edges(doc, existing_nodes)

        called_messages = mock_api_request.call_args[1]["messages"]
        assert any(
            "You are an AI expert specializing in knowledge graph creation" in msg["content"] for msg in called_messages
        )
        assert any(
            "Please provide the edges for the knowledge graph based on the following input text." in msg["content"]
            for msg in called_messages
        )
        assert any("Alice went to London." in msg["content"] for msg in called_messages)
        assert any("Token Indexes:" in msg["content"] for msg in called_messages)
        assert any(str(existing_nodes) in msg["content"] for msg in called_messages)

    def test_respects_token_indexes(self, mock_api_request, test_nlp):
        existing_nodes = [{"label": "Alice", "spans": [[0]]}, {"label": "London", "spans": [[3]]}]
        api_response = """{
            "edges": [
                {"label": "went to", "spans": [[1, 2]], "source": "Alice", "target": "London"}
            ]
        }"""
        mock_api_request.return_value = api_response
        doc = test_nlp("Alice went to London.")
        result = get_edges(doc, existing_nodes)
        assert result[0]["spans"] == [[1, 2]]
        assert doc[result[0]["spans"][0][0]].text == "went"
        assert doc[result[0]["spans"][0][1]].text == "to"

    def test_handles_json_decode_error(self, mock_api_request, test_nlp):
        mock_api_request.return_value = "Invalid JSON"
        doc = test_nlp("This should cause a JSON decode error.")
        result = get_edges(doc, [])
        assert result == {}

    def test_removes_stray_backticks(self, mock_api_request, test_nlp):
        api_response = """```
        {
            "edges": [
                {"label": "went to", "spans": [[1, 2]], "source": "Alice", "target": "London"}
            ]
        }
        ```"""
        mock_api_request.return_value = api_response
        doc = test_nlp("Alice went to London.")
        result = get_edges(doc, [{"label": "Alice", "spans": [[0]]}, {"label": "London", "spans": [[3]]}])
        assert result == [{"label": "went to", "spans": [[1, 2]], "source": "Alice", "target": "London"}]
