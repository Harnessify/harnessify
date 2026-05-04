# Adapters

Harnessify does not try to own the runtime. It wraps existing agent runtimes and evaluation tools behind thin adapters and open local formats.

The adapter story only works if the repo also includes reference agents for real workflows. Reference agents prove the harness contract. Adapters make that contract portable to customer-owned runtimes.

## Runtime Adapters

- `callable`: wrap a Python callable directly
- `shell`: wrap a local shell-invoked agent process
- `OpenAI-compatible`: target local or remote OpenAI-style endpoints
- `PyFlue`: future thin adapter
- `LangGraph`: future thin adapter
- `Hermes`: future thin adapter
- `OpenClaw`: future thin adapter

Today, the support refund domain can already run through:

- `callable` with the in-process deterministic reference agent
- `shell` with the same reference agent executed as an external process

## Reference Agents vs Bring-Your-Own Agents

- Reference agents are maintained in-repo for concrete domain workflows
- Bring-your-own agents stay in the customer's runtime and are wrapped through adapters
- The goal is to keep the readiness contract stable while the runtime varies

Examples:

- `support/refunds` deterministic local reference agent
- future `support/refunds` OpenAI-compatible reference agent
- future `support/refunds` LangGraph reference agent

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
- Keep the local deterministic support agent as the default built-in runtime for this milestone.
- Prove portability by running the same domain pack through more than one adapter path.
