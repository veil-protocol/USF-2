<p align="center">
  <img src="https://img.shields.io/badge/v2.0.0-OMEGA-0a0a0a?style=flat-square&labelColor=1a1a2e" alt="version"/>
  <img src="https://img.shields.io/badge/status-production-10b981?style=flat-square" alt="status"/>
  <img src="https://img.shields.io/badge/tests-43%2F43-10b981?style=flat-square" alt="tests"/>
  <img src="https://img.shields.io/badge/license-MIT-6366f1?style=flat-square" alt="license"/>
</p>

<h1 align="center">
  <br>
  <code>U S F - 2</code>
  <br>
</h1>

<p align="center">
  <strong>Unified Superintelligence Framework</strong><br>
  <sub>Multi-agent orchestration for recursive verification</sub>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#compute-types">Compute Types</a> •
  <a href="#verification-chains">Verification</a> •
  <a href="CLAUDE.md">Claude Integration</a>
</p>

---

USF-2 orchestrates parallel verification agents with calibrated analytical depth. It spawns independent chains that validate conclusions through adversarial, formal, and consensus-based methods, then aggregates results using weighted confidence scoring.

The framework evolved from USF 4.1.1 through 6 development cycles. Version 2.0 introduces 13 compute orchestration patterns, 9 verification chains, and native integration with Claude Code's Task tool for zero-configuration agent spawning.

## Quick Start

Generate an execution plan:

```bash
python3 src/usf.py "Analyze authentication system security" --json
```

USF-2 auto-detects optimal parameters from task semantics:

| Keywords | Compute | Precision | Agents |
|:---------|:--------|:----------|:-------|
| security, audit, vulnerability | hivemind | PL5 | 16 |
| comprehensive, thorough | swarm | PL5 | 16 |
| compare, evaluate, benchmark | tournament | PL3 | 8 |
| quick, simple, basic | sequential | PL1 | 4 |
| analyze, research | parallel | PL3 | 8 |

Override with explicit flags:

```bash
python3 src/usf.py "task" --compute hivemind --precision 5 --json
```

## Architecture

```
                              ┌─────────────────────────────────────┐
                              │         ORCHESTRATION LAYER         │
                              │   13 compute patterns coordinate    │
                              │        agent execution              │
                              └──────────────┬──────────────────────┘
                                             │
                    ┌────────────────────────┼────────────────────────┐
                    │                        │                        │
                    ▼                        ▼                        ▼
        ┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
        │  DOMAIN ADAPTER   │    │ PRECISION ENGINE  │    │   VERIFICATION    │
        │                   │    │                   │    │                   │
        │  Auto-detects     │    │  Calibrates depth │    │  9 independent    │
        │  domain context   │───▶│  Maps to PL1-PL5  │───▶│  chains validate  │
        │  Synthesizes      │    │  Scales agents    │    │  conclusions      │
        │  expert personas  │    │                   │    │                   │
        └───────────────────┘    └───────────────────┘    └───────────────────┘
                    │                                                 │
                    │              ┌───────────────────┐              │
                    └─────────────▶│  ARCHETYPE PANEL  │◀─────────────┘
                                   │                   │
                                   │  5 universal      │
                                   │  archetypes       │
                                   │  synthesized to   │
                                   │  domain experts   │
                                   └───────────────────┘
```

**Precision levels** determine verification chain count:

| Level | Chains | Confidence Target | Resource Cost |
|:------|:-------|:------------------|:--------------|
| PL1 | 1 | 80% | 1× |
| PL2 | 2 | 90% | 2× |
| PL3 | 3 | 95% | 3× |
| PL4 | 6 | 99% | 6× |
| PL5 | 9 | 99.9%+ | 9× |

PL5 achieves up to 12× speedup through parallel execution with early-exit consensus.

## Compute Types

USF-2 supports 13 orchestration patterns:

| Type | Execution Model | Aggregation |
|:-----|:----------------|:------------|
| `sequential` | Chains execute in order | Last result |
| `parallel` | All chains simultaneously | Confidence-weighted average |
| `swarm` | Maximum agent coverage | Best-of-N selection |
| `hivemind` | Consensus voting | Majority vote (60% quorum) |
| `pipeline` | Each output feeds next | Chain refinement |
| `tournament` | Competitive elimination | Winner takes all |
| `critic_loop` | Generate then critique | Refined output |
| `ensemble` | Multiple analytical approaches | Weighted combination |
| `supervisor_worker` | Coordinator + parallel workers | Supervised aggregation |
| `map_reduce` | Split, parallel process, combine | Reducer synthesis |
| `hybrid` | Parallel exploration + sequential refinement | Two-phase synthesis |
| `mesh_distributed` | Spread across compute nodes | Distributed consensus |
| `mesh_offensive` | Security-focused execution | Threat-weighted aggregation |

Subagent type selection:

```
Explore        → Research, codebase navigation, information gathering
Plan           → Coordination, task decomposition, synthesis
general-purpose → Execution, verification, analysis
```

## Verification Chains

Nine independent chains validate conclusions. Chain selection is automatic based on precision level:

```
Chain A  Single Source       ████████████  PL1+
Chain B  Dual Source         ████████████  PL2+
Chain C  Triple Consensus    ████████████  PL4+
Chain D  Adversarial         ████████████  PL3+
Chain E  Formal Methods      ████████████  PL4+
Chain F  Domain Expert       ████████████  PL4+
Chain G  Temporal Validity   ████████████  PL5
Chain H  Multi-Agent         ████████████  PL5
Chain I  Streaming Early-Exit ███████████  PL5
```

Early-exit (Chain I) terminates when consensus exceeds 85% confidence threshold, reducing latency without sacrificing accuracy.

## Expert Archetypes

Five universal archetypes synthesize into domain-specific personas:

| ID | Archetype | Primary Mode | Domain Synthesis |
|:---|:----------|:-------------|:-----------------|
| **TH** | Theoretical | First principles, proofs | Security Researcher, Cryptographer |
| **AD** | Adversarial | Attack surface, failure modes | Red Team Operator, Cryptanalyst |
| **IM** | Implementation | Practical constraints | Security Engineer, Developer |
| **ST** | Strategic | Long-term implications | Security Strategist, Architect |
| **QA** | Quality Assurance | Edge cases, compliance | Security Auditor, QA Engineer |

Panel size scales with precision: `min(precision_level + 2, 7)` archetypes per analysis.

Aggregation weighting: `0.6 × chain_confidence + 0.4 × archetype_confidence`

## Claude Code Integration

Copy `CLAUDE.md` to project root. Invoke with natural language:

```
use USF                    → Auto-detect parameters, execute
use USF max                → swarm + PL5, maximum rigor
use USF quick              → sequential + PL1, fast check
use USF manual             → Step-by-step guided execution
```

Zero-prompt mode infers task from conversation context and spawns agents without confirmation.

## Limitations

USF-2 is an orchestration framework, not a knowledge base. It improves *how* analysis is coordinated, not *what* is known.

Known constraints:

- Parallel speedup requires tasks decomposable into independent subtasks
- PL5 analysis incurs 9× compute cost; reserve for security-critical work
- Consensus-based methods assume good-faith agent outputs
- Cross-session state requires external persistence layer
- Maximum context scales with agent count; circuit breaker auto-reduces at limits

## Files

| Path | Contents |
|:-----|:---------|
| [`CLAUDE.md`](CLAUDE.md) | Claude Code memory file and invocation patterns |
| [`src/usf.py`](src/usf.py) | CLI interface |
| [`src/usf_executor.py`](src/usf_executor.py) | Core execution engine |
| [`src/usf_runner.py`](src/usf_runner.py) | High-level runner class |
| [`tests/test_usf.py`](tests/test_usf.py) | Test suite (43 tests) |
| [`docs/PROMPTS.md`](docs/PROMPTS.md) | Ready-to-use invocation prompts |

<details>
<summary><strong>Python API</strong></summary>

```python
from src.usf_runner import USFRunner

runner = USFRunner()
plan = runner.prepare("Analyze security of auth system", auto=True)

print(f"Agents: {plan.total_agents}")
print(f"Chains: {plan.chain_count}")
print(f"Experts: {plan.archetype_count}")

# Spawn agents via Claude Task tool
# Collect outputs
# Aggregate results

result = runner.aggregate(outputs, plan.plan_dict)
print(f"Confidence: {result['confidence']:.0%}")
```

</details>

<details>
<summary><strong>CLI reference</strong></summary>

```bash
# Show full interface specification
python3 src/usf.py --show-interface

# Human-readable output
python3 src/usf.py "task"

# JSON for Task tool integration
python3 src/usf.py "task" --json

# Auto-detect compute type and precision
python3 src/usf.py "task" --auto --json

# Override parameters
python3 src/usf.py "task" --compute hivemind --precision 5 --json

# Disable archetype panel
python3 src/usf.py "task" --no-archetypes --json
```

</details>

## Development

USF-2 evolved through 6 development cycles from USF 4.1.1:

| Version | Changes | Status |
|:--------|:--------|:-------|
| 4.1.1 | SKYNET-Hardened specification | Baseline |
| 5.0 | PROMETHEUS layer (5 engines) | Complete |
| 5.1 | TITAN layer (3 engines) | Complete |
| 5.2 | FORGE layer (1 engine) | Complete |
| 5.3 | APEX security hardening | Complete |
| 6.0 | OMEGA superintelligence layer | Complete |
| **2.0** | Production release, sanitized | **Current** |

Total: 15 engines implemented across 4 architectural layers.

## Contributing

Submit issues and pull requests via GitHub. Changes are validated through the USF test suite before merge.

## License

MIT. See [`LICENSE`](LICENSE).

---

<sub>USF-2 builds on USF 4.1.1 patterns. Previous version: <a href="https://github.com/veil-protocol/usf">veil-protocol/usf</a></sub>
