# OpenAI-Compatible Endpoints

Harnessify can run the support refund domain pack against local or remote OpenAI-compatible chat completion APIs.

This is useful for local inference servers such as llama.cpp.

## llama.cpp

Start llama.cpp with its OpenAI-compatible server enabled, then point Harnessify at it:

```bash
export HFY_OPENAI_BASE_URL="http://localhost:8080/v1"
```

If `HFY_OPENAI_MODEL` is unset, Harnessify discovers the first model from:

```text
GET /v1/models
```

Run the support readiness flow:

```bash
hfy init
hfy support eval --agent-version llama-v1 --agent-impl openai_compatible_support_refund --adapter openai-compatible
hfy support redteam --agent-version llama-v1 --agent-impl openai_compatible_support_refund --adapter openai-compatible
hfy support readiness --agent-version llama-v1
```

## Environment

- `HFY_OPENAI_BASE_URL`: defaults to `http://localhost:8080/v1`
- `HFY_OPENAI_MODEL`: optional model override
- `HFY_OPENAI_API_KEY`: optional bearer token
- `HFY_OPENAI_MAX_TOKENS`: optional response token budget, defaults to `512`
- `HFY_OPENAI_NO_THINK`: set to `1` to prepend `/no_think` to prompts for reasoning models

For Qwen3 models, Harnessify prepends `/no_think` by default so the model returns JSON in `message.content` instead of spending the response budget on hidden reasoning.

## Boundary

The model server owns inference. Harnessify owns the readiness artifacts:

- `input.json`
- `output.json`
- `score.json`
- `trace.jsonl`
- readiness reports
- compare output
