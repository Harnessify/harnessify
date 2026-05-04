# Adapters

Harnessify does not try to own the runtime. It wraps existing agent runtimes and evaluation tools behind thin adapters and open local formats.

## Runtime Adapters

- `callable`: wrap a Python callable directly
- `shell`: wrap a local shell-invoked agent process
- `OpenAI-compatible`: target local or remote OpenAI-style endpoints
- `PyFlue`: future thin adapter
- `LangGraph`: future thin adapter
- `Hermes`: future thin adapter
- `OpenClaw`: future thin adapter

## Tooling Integrations

- `Promptfoo`: future red-team and eval orchestration adapter
- `DeepEval`: optional evaluation adapter
- `Inspect AI`: optional agent-eval adapter
- `Guardrails AI`: optional validation adapter
- `OpenTelemetry`: optional trace export path
- `MLflow`: optional tracking adapter
- `Docker`: optional sandbox runner
- `GitPython`: optional git metadata lookup

## Milestone 1 Strategy

- Keep every adapter thin.
- Do not make optional tools mandatory.
- Fail gracefully with a clear `not installed` message when a dependency is unavailable.
- Keep the local deterministic support agent as the only built-in runtime for this milestone.
