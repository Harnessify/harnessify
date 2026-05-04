from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


DEFAULT_BASE_URL = "http://localhost:8080/v1"


def openai_compatible_status(base_url: str | None = None) -> dict[str, str | bool]:
    resolved_base_url = normalize_base_url(base_url or os.getenv("HFY_OPENAI_BASE_URL") or DEFAULT_BASE_URL)
    try:
        models = list_models(resolved_base_url)
    except Exception as exc:
        return {
            "available": False,
            "base_url": resolved_base_url,
            "message": f"OpenAI-compatible endpoint is unavailable: {exc}",
        }

    return {
        "available": True,
        "base_url": resolved_base_url,
        "message": "OpenAI-compatible endpoint is available.",
        "model": first_model_id(models) or "",
    }


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def post_json(url: str, payload: dict[str, Any], headers: dict[str, str] | None = None) -> dict[str, Any]:
    request_headers = {"Content-Type": "application/json", **(headers or {})}
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=request_headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {body}") from exc


def get_json(url: str, headers: dict[str, str] | None = None) -> dict[str, Any]:
    request = urllib.request.Request(url, headers=headers or {}, method="GET")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def auth_headers() -> dict[str, str]:
    api_key = os.getenv("HFY_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {}
    return {"Authorization": f"Bearer {api_key}"}


def list_models(base_url: str | None = None) -> dict[str, Any]:
    resolved_base_url = normalize_base_url(base_url or os.getenv("HFY_OPENAI_BASE_URL") or DEFAULT_BASE_URL)
    return get_json(f"{resolved_base_url}/models", headers=auth_headers())


def first_model_id(models_payload: dict[str, Any]) -> str | None:
    data = models_payload.get("data")
    if isinstance(data, list) and data:
        model_id = data[0].get("id")
        if isinstance(model_id, str):
            return model_id

    models = models_payload.get("models")
    if isinstance(models, list) and models:
        model_id = models[0].get("model") or models[0].get("name")
        if isinstance(model_id, str):
            return model_id

    return None


def resolve_model(base_url: str) -> str:
    configured_model = os.getenv("HFY_OPENAI_MODEL")
    if configured_model:
        return configured_model

    discovered_model = first_model_id(list_models(base_url))
    if discovered_model:
        return discovered_model

    raise RuntimeError("No model found. Set HFY_OPENAI_MODEL or expose /v1/models.")


def chat_completion(
    messages: list[dict[str, str]],
    *,
    base_url: str | None = None,
    model: str | None = None,
    temperature: float = 0.0,
    max_tokens: int = 512,
) -> dict[str, Any]:
    resolved_base_url = normalize_base_url(base_url or os.getenv("HFY_OPENAI_BASE_URL") or DEFAULT_BASE_URL)
    resolved_model = model or resolve_model(resolved_base_url)
    request_messages = apply_local_model_hints(messages, resolved_model)
    payload = {
        "model": resolved_model,
        "messages": request_messages,
        "temperature": temperature,
        "max_tokens": int(os.getenv("HFY_OPENAI_MAX_TOKENS", str(max_tokens))),
        "stream": False,
    }
    return post_json(
        f"{resolved_base_url}/chat/completions",
        payload,
        headers=auth_headers(),
    )


def extract_chat_content(response: dict[str, Any]) -> str:
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ValueError("OpenAI-compatible response did not include choices.")
    message = choices[0].get("message")
    if not isinstance(message, dict):
        raise ValueError("OpenAI-compatible response choice did not include message.")
    content = message.get("content")
    if not isinstance(content, str):
        raise ValueError("OpenAI-compatible response message did not include string content.")
    return content


def apply_local_model_hints(messages: list[dict[str, str]], model: str) -> list[dict[str, str]]:
    no_think = os.getenv("HFY_OPENAI_NO_THINK")
    should_disable_thinking = no_think == "1" or (no_think is None and "qwen3" in model.lower())
    if not should_disable_thinking:
        return messages

    hinted_messages = []
    for message in messages:
        content = message.get("content", "")
        if content.startswith("/no_think"):
            hinted_messages.append(message)
        else:
            hinted_messages.append({**message, "content": f"/no_think\n{content}"})
    return hinted_messages
