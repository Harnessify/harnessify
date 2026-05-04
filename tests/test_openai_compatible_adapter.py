from __future__ import annotations

import json

from harnessify.adapters import openai_compatible


def test_first_model_id_handles_llama_cpp_payload() -> None:
    payload = {
        "models": [{"name": "Qwen3-14B-Q4_K_M.gguf", "model": "Qwen3-14B-Q4_K_M.gguf"}],
        "data": [{"id": "Qwen3-14B-Q4_K_M.gguf"}],
    }

    assert openai_compatible.first_model_id(payload) == "Qwen3-14B-Q4_K_M.gguf"


def test_chat_completion_posts_to_local_openai_compatible_endpoint(monkeypatch) -> None:
    calls = []

    def fake_post_json(url, payload, headers=None):
        calls.append((url, payload, headers))
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "decision": "approve",
                                "refund_amount": 25,
                                "needs_human_review": False,
                                "reason": "This damaged-item request qualifies for a refund.",
                            }
                        )
                    }
                }
            ]
        }

    monkeypatch.setattr(openai_compatible, "post_json", fake_post_json)
    response = openai_compatible.chat_completion(
        [{"role": "user", "content": "hello"}],
        base_url="http://localhost:8080/v1",
        model="local-model",
    )

    assert calls[0][0] == "http://localhost:8080/v1/chat/completions"
    assert calls[0][1]["model"] == "local-model"
    assert openai_compatible.extract_chat_content(response).startswith("{")


def test_qwen3_model_gets_no_think_hint_by_default() -> None:
    messages = [{"role": "user", "content": "Return JSON."}]

    hinted = openai_compatible.apply_local_model_hints(messages, "Qwen3-14B-Q4_K_M.gguf")

    assert hinted[0]["content"].startswith("/no_think")
