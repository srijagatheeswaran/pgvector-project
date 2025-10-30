from app.tasks import compute_and_store_embedding

def test_dummy_embedding(monkeypatch):
    """Unit test example with mock embedding generation."""
    def fake_grok_call(*args, **kwargs):
        # return the same structure our get_embedding helper returns
        return {"data": [{"embedding": [0.1] * 1536}]}

    # Patch the helper used by tasks to fetch embeddings
    monkeypatch.setattr("app.tasks.get_embedding", fake_grok_call)
    result = compute_and_store_embedding(1)
    assert "Success" in result
