"""
USF-2: Unified Superintelligence Framework
Core Execution Engine

A self-evolving methodology framework for AI reasoning that coordinates
multiple analytical perspectives and calibrates reasoning depth.

Version: 2.0.0
License: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import json
import logging
import re

logger = logging.getLogger(__name__)


class ComputeType(Enum):
    """Orchestration compute types for multi-agent coordination"""
    SEQUENTIAL = "sequential"      # Chains run one after another
    PARALLEL = "parallel"          # All chains run simultaneously
    SWARM = "swarm"               # Many agents, best answer wins
    HIVEMIND = "hivemind"         # Consensus voting across agents
    PIPELINE = "pipeline"         # Output of one feeds into next
    SUPERVISOR_WORKER = "supervisor_worker"  # Coordinator + workers
    HYBRID = "hybrid"             # Parallel exploration + sequential refinement
    MAP_REDUCE = "map_reduce"     # Split, parallel process, combine
    TOURNAMENT = "tournament"     # Agents compete, best wins
    CRITIC_LOOP = "critic_loop"   # Generate then critique
    ENSEMBLE = "ensemble"         # Multiple approaches combined
    MESH_DISTRIBUTED = "mesh_distributed"  # Spread across nodes
    MESH_OFFENSIVE = "mesh_offensive"      # Security-focused execution


@dataclass
class USFExecutionPlan:
    """Structured execution plan for USF tasks"""
    task: str
    engines: List[str]
    chains: List[str]
    compute_type: ComputeType
    precision_level: int
    profile: str
    template: Optional[str] = None
    mode: str = "omega"


@dataclass
class ChainResult:
    """Result from a verification chain execution"""
    chain_id: str
    result: str
    confidence: float
    agent_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SynthesizedPersona:
    """A domain-specific expert persona synthesized from archetype + domain"""
    archetype_id: str
    domain: str
    title: str
    expertise_prompt: str
    cognitive_patterns: List[str]


class ArchetypeLoader:
    """
    Loads and synthesizes expert personas from universal archetypes.

    5 Universal Archetypes:
    - ARC-TH: Theoretical (research, proofs, invariants)
    - ARC-AD: Adversarial (attack surface, red team)
    - ARC-IM: Implementation (engineering, optimization)
    - ARC-ST: Strategic (holistic synthesis, trade-offs)
    - ARC-QA: Quality Assurance (testing, compliance)
    """

    ARCHETYPES = {
        "ARC-TH": {
            "name": "Theoretical",
            "primary_mode": "constructive_analysis",
            "cognitive_patterns": [
                "first_principles_decomposition",
                "formal_verification",
                "completeness_checking",
                "invariant_identification",
                "proof_construction"
            ],
            "domains": {
                "security": "Security Researcher",
                "crypto": "Cryptographer",
                "software": "Software Architect",
                "legal": "Legal Theorist",
                "default": "Domain Theorist"
            }
        },
        "ARC-AD": {
            "name": "Adversarial",
            "primary_mode": "destructive_analysis",
            "cognitive_patterns": [
                "attack_surface_mapping",
                "assumption_violation",
                "edge_case_exploitation",
                "failure_mode_analysis",
                "threat_modeling"
            ],
            "domains": {
                "security": "Red Team Operator",
                "crypto": "Cryptanalyst",
                "software": "Bug Hunter",
                "legal": "Opposing Counsel",
                "default": "Adversarial Analyst"
            }
        },
        "ARC-IM": {
            "name": "Implementation",
            "primary_mode": "constructive_engineering",
            "cognitive_patterns": [
                "practical_constraints",
                "optimization_focus",
                "scalability_analysis",
                "integration_planning",
                "resource_estimation"
            ],
            "domains": {
                "security": "Security Engineer",
                "crypto": "Cryptographic Engineer",
                "software": "Senior Developer",
                "legal": "Compliance Officer",
                "default": "Implementation Specialist"
            }
        },
        "ARC-ST": {
            "name": "Strategic",
            "primary_mode": "holistic_synthesis",
            "cognitive_patterns": [
                "stakeholder_analysis",
                "risk_assessment",
                "timeline_planning",
                "trade_off_evaluation",
                "big_picture_integration"
            ],
            "domains": {
                "security": "Security Strategist",
                "crypto": "Protocol Architect",
                "software": "Technical Lead",
                "legal": "General Counsel",
                "default": "Strategic Planner"
            }
        },
        "ARC-QA": {
            "name": "Quality Assurance",
            "primary_mode": "verification_validation",
            "cognitive_patterns": [
                "test_coverage_analysis",
                "regression_detection",
                "compliance_verification",
                "documentation_review",
                "acceptance_criteria"
            ],
            "domains": {
                "security": "Security Auditor",
                "crypto": "Protocol Auditor",
                "software": "QA Engineer",
                "legal": "Legal Reviewer",
                "default": "Quality Analyst"
            }
        }
    }

    DOMAIN_KEYWORDS = {
        "security": ["security", "vulnerability", "exploit", "attack", "defense", "pentest", "audit"],
        "crypto": ["cryptograph", "encrypt", "cipher", "hash", "signature", "key", "protocol"],
        "software": ["code", "function", "class", "api", "refactor", "bug", "feature"],
        "legal": ["legal", "compliance", "regulation", "contract", "liability", "policy"]
    }

    def __init__(self):
        self.archetypes = self.ARCHETYPES

    def detect_domain(self, task: str) -> str:
        """Auto-detect domain from task description"""
        task_lower = task.lower()

        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            if any(kw in task_lower for kw in keywords):
                return domain

        return "default"

    def synthesize_persona(
        self,
        archetype_id: str,
        domain: str,
        task_context: str = ""
    ) -> SynthesizedPersona:
        """Synthesize a domain-specific expert persona from archetype + domain"""

        archetype = self.archetypes.get(archetype_id)
        if not archetype:
            raise ValueError(f"Unknown archetype: {archetype_id}")

        title = archetype["domains"].get(domain, archetype["domains"]["default"])

        expertise_prompt = f"""You are a {title} with deep expertise in {domain} analysis.

## Your Analytical Approach
You employ {archetype['primary_mode']} methodology with these cognitive patterns:
{chr(10).join(f'- {p.replace("_", " ").title()}' for p in archetype['cognitive_patterns'])}

## Your Role
As the {title}, your analysis should reflect:
- Deep domain expertise in {domain}
- {archetype['name']} perspective on problems
- Rigorous application of your cognitive patterns

## Task Context
{task_context}

Provide your expert analysis with a confidence score (0.0-1.0) and clear reasoning."""

        return SynthesizedPersona(
            archetype_id=archetype_id,
            domain=domain,
            title=title,
            expertise_prompt=expertise_prompt,
            cognitive_patterns=archetype["cognitive_patterns"]
        )

    def compose_panel(
        self,
        domain: str,
        panel_size: int = 5,
        required_archetypes: Optional[List[str]] = None
    ) -> List[str]:
        """Compose a balanced expert panel for the domain"""

        if required_archetypes:
            panel = list(required_archetypes)
        else:
            panel = []

        # Fill remaining slots with balanced selection
        all_archetypes = list(self.archetypes.keys())
        for arc_id in all_archetypes:
            if arc_id not in panel and len(panel) < panel_size:
                panel.append(arc_id)

        return panel[:panel_size]


class USFExecutor:
    """
    Core USF execution engine.

    Orchestrates multi-agent verification with:
    - 9 verification chains (A through I)
    - 13 compute types
    - 5 precision levels
    - 5 universal archetypes
    """

    # Verification chain templates
    CHAIN_PROMPTS = {
        "A_SINGLE_SOURCE": """## Chain A: Single Source Verification

TASK: {task}

Analyze this task using a single authoritative source approach.
Provide your findings with confidence score (0.0-1.0).

Output format:
```json
{{
  "chain": "A",
  "confidence": 0.0-1.0,
  "result": "your analysis",
  "sources": ["source1"]
}}
```""",

        "B_DUAL_SOURCE": """## Chain B: Dual Source Cross-Reference

TASK: {task}

Analyze using two independent sources and cross-reference findings.
Identify agreements and conflicts between sources.

Output format:
```json
{{
  "chain": "B",
  "confidence": 0.0-1.0,
  "result": "your analysis",
  "sources": ["source1", "source2"],
  "agreements": [],
  "conflicts": []
}}
```""",

        "C_TRIPLE_SOURCE": """## Chain C: Triple Source Consensus

TASK: {task}

Use three independent sources to establish consensus.
Require 2/3 agreement for high-confidence claims.

Output format:
```json
{{
  "chain": "C",
  "confidence": 0.0-1.0,
  "result": "your analysis",
  "consensus_items": [],
  "disputed_items": []
}}
```""",

        "D_ADVERSARIAL": """## Chain D: Adversarial Verification

TASK: {task}

Apply adversarial thinking: actively try to disprove claims.
Identify weaknesses, edge cases, and potential failures.

Output format:
```json
{{
  "chain": "D",
  "confidence": 0.0-1.0,
  "result": "your analysis",
  "attack_vectors": [],
  "weaknesses_found": [],
  "surviving_claims": []
}}
```""",

        "E_MATHEMATICAL": """## Chain E: Formal/Mathematical Verification

TASK: {task}

Apply formal reasoning and mathematical rigor.
Use logical proofs, invariants, and formal methods where applicable.

Output format:
```json
{{
  "chain": "E",
  "confidence": 0.0-1.0,
  "result": "your analysis",
  "formal_claims": [],
  "proof_sketches": []
}}
```""",

        "F_DOMAIN_EXPERT": """## Chain F: Domain Expert Analysis

TASK: {task}

Analyze as a domain expert with deep specialized knowledge.
Apply domain-specific best practices and patterns.

Output format:
```json
{{
  "chain": "F",
  "confidence": 0.0-1.0,
  "result": "your analysis",
  "domain_insights": [],
  "best_practices_applied": []
}}
```""",

        "G_TEMPORAL": """## Chain G: Temporal Validity Check

TASK: {task}

Verify temporal validity: are claims still current?
Check for outdated information, version changes, deprecations.

Output format:
```json
{{
  "chain": "G",
  "confidence": 0.0-1.0,
  "result": "your analysis",
  "temporal_issues": [],
  "freshness_score": 0.0-1.0
}}
```""",

        "H_CONSENSUS": """## Chain H: Multi-Agent Consensus

TASK: {task}

Synthesize findings across multiple perspectives.
Build consensus from diverse analytical approaches.

Output format:
```json
{{
  "chain": "H",
  "confidence": 0.0-1.0,
  "result": "your analysis",
  "consensus_points": [],
  "minority_views": []
}}
```""",

        "I_STREAMING": """## Chain I: Streaming Early-Exit

TASK: {task}

Provide analysis with early-exit capability.
If high confidence (>0.85) reached early, indicate completion.

Output format:
```json
{{
  "chain": "I",
  "confidence": 0.0-1.0,
  "result": "your analysis",
  "early_exit": true/false,
  "exit_reason": "confidence_threshold" or "complete_analysis"
}}
```"""
    }

    def __init__(self):
        self.archetype_loader = ArchetypeLoader()

    def detect_domain(self, task: str) -> str:
        """Auto-detect domain from task"""
        return self.archetype_loader.detect_domain(task)

    def get_chains_for_precision(self, precision_level: int) -> List[str]:
        """Get verification chains based on precision level"""
        all_chains = list(self.CHAIN_PROMPTS.keys())

        if precision_level >= 5:
            return all_chains  # All 9 chains
        elif precision_level == 4:
            return all_chains[:6]  # A through F
        elif precision_level == 3:
            return ["A_SINGLE_SOURCE", "B_DUAL_SOURCE", "D_ADVERSARIAL"]
        elif precision_level == 2:
            return ["A_SINGLE_SOURCE", "B_DUAL_SOURCE"]
        else:
            return ["A_SINGLE_SOURCE"]

    def create_execution_plan(
        self,
        task: str,
        compute_type: str = "parallel",
        precision_level: int = 3,
        profile: str = "autonomous"
    ) -> USFExecutionPlan:
        """Create an execution plan for the task"""

        chains = self.get_chains_for_precision(precision_level)

        engines = ["ENGINE_4_VERIFICATION", "ENGINE_10_PARALLEL_VERIFICATION"]
        if profile == "fire_and_forget":
            engines.append("ENGINE_12_FULL_AUTONOMY")

        return USFExecutionPlan(
            task=task,
            engines=engines,
            chains=chains,
            compute_type=ComputeType(compute_type),
            precision_level=precision_level,
            profile=profile
        )

    def get_task_commands(
        self,
        plan: USFExecutionPlan,
        domain: Optional[str] = None,
        use_persona: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Generate Task tool invocation commands for the execution plan.

        Returns a list of dicts ready for Claude's Task tool:
        {description, prompt, subagent_type, run_in_background}
        """
        commands = []

        if domain is None:
            domain = self.detect_domain(plan.task)

        # Generate commands based on compute type
        if plan.compute_type == ComputeType.SEQUENTIAL:
            for chain_id in plan.chains:
                commands.append(self._create_chain_command(
                    chain_id, plan.task, background=False, domain=domain
                ))

        elif plan.compute_type in [ComputeType.PARALLEL, ComputeType.SWARM]:
            for chain_id in plan.chains:
                commands.append(self._create_chain_command(
                    chain_id, plan.task, background=True, domain=domain
                ))

        elif plan.compute_type == ComputeType.HIVEMIND:
            for chain_id in plan.chains:
                commands.append(self._create_chain_command(
                    chain_id, plan.task, background=True, domain=domain
                ))

        elif plan.compute_type == ComputeType.PIPELINE:
            for i, chain_id in enumerate(plan.chains):
                cmd = self._create_chain_command(
                    chain_id, plan.task, background=False, domain=domain
                )
                if i > 0:
                    cmd["prompt"] = f"Previous chain results will be provided.\n\n{cmd['prompt']}"
                commands.append(cmd)

        elif plan.compute_type == ComputeType.TOURNAMENT:
            for chain_id in plan.chains:
                cmd = self._create_chain_command(
                    chain_id, plan.task, background=True, domain=domain
                )
                cmd["prompt"] = f"TOURNAMENT MODE: Compete to provide the best answer.\n\n{cmd['prompt']}"
                commands.append(cmd)

        elif plan.compute_type == ComputeType.CRITIC_LOOP:
            commands.append({
                "description": "Initial analysis",
                "prompt": f"Analyze this task thoroughly:\n\n{plan.task}",
                "subagent_type": "Explore",
                "run_in_background": False
            })
            commands.append({
                "description": "Critic review",
                "prompt": f"Critically review the previous analysis. Find flaws, gaps, and improvements for:\n\n{plan.task}",
                "subagent_type": "general-purpose",
                "run_in_background": False
            })

        elif plan.compute_type == ComputeType.ENSEMBLE:
            approaches = [
                ("analytical", "Explore"),
                ("creative", "general-purpose"),
                ("skeptical", "general-purpose")
            ]
            for approach, agent_type in approaches:
                commands.append({
                    "description": f"Ensemble {approach}",
                    "prompt": f"Using a {approach} approach, analyze:\n\n{plan.task}",
                    "subagent_type": agent_type,
                    "run_in_background": True
                })

        elif plan.compute_type == ComputeType.SUPERVISOR_WORKER:
            commands.append({
                "description": "Supervisor coordinator",
                "prompt": f"""You are the SUPERVISOR agent coordinating a team of workers.

TASK: {plan.task}

Decompose this task into {len(plan.chains)} subtasks.
Define clear success criteria for each.

Output format:
```json
{{
  "subtasks": [{{"id": 1, "description": "...", "success_criteria": "..."}}],
  "combination_strategy": "..."
}}
```""",
                "subagent_type": "Plan",
                "run_in_background": False
            })

            for i, chain_id in enumerate(plan.chains):
                commands.append({
                    "description": f"Worker {i+1} ({chain_id.split('_')[0]})",
                    "prompt": f"""You are WORKER {i+1} in a supervisor-worker system.

MAIN TASK: {plan.task}

Execute your assigned portion thoroughly.
Chain perspective: {chain_id}

Provide analysis with confidence score (0-1).""",
                    "subagent_type": "general-purpose",
                    "run_in_background": True
                })

        elif plan.compute_type == ComputeType.MAP_REDUCE:
            for i, chain_id in enumerate(plan.chains):
                commands.append({
                    "description": f"Map worker {i+1}",
                    "prompt": f"""MAP PHASE - Worker {i+1}/{len(plan.chains)}

TASK: {plan.task}

Analyze aspect {i+1} of {len(plan.chains)}.
Chain focus: {chain_id}

Output:
```json
{{
  "worker_id": {i+1},
  "partial_result": "...",
  "confidence": 0.0-1.0,
  "key_findings": []
}}
```""",
                    "subagent_type": "general-purpose",
                    "run_in_background": True
                })

            commands.append({
                "description": "Reduce aggregator",
                "prompt": f"""REDUCE PHASE - Result Aggregator

ORIGINAL TASK: {plan.task}

Combine results from {len(plan.chains)} map workers into coherent final answer.
Merge findings, resolve conflicts, calculate overall confidence.""",
                "subagent_type": "Plan",
                "run_in_background": False
            })

        elif plan.compute_type == ComputeType.HYBRID:
            for chain_id in plan.chains:
                commands.append(self._create_chain_command(
                    chain_id, plan.task, background=True, domain=domain
                ))

            commands.append({
                "description": "Hybrid synthesizer",
                "prompt": f"""HYBRID SYNTHESIS PHASE

TASK: {plan.task}

You are the final synthesizer. Previous phase: {len(plan.chains)} parallel chains.

1. Review all parallel chain outputs
2. Identify consensus and conflicts
3. Deep analysis on uncertain areas
4. Produce refined final answer

Include confidence score and reasoning chain.""",
                "subagent_type": "Plan",
                "run_in_background": False
            })

        elif plan.compute_type == ComputeType.MESH_DISTRIBUTED:
            for i, chain_id in enumerate(plan.chains):
                commands.append({
                    "description": f"Mesh node {i+1} ({chain_id.split('_')[0]})",
                    "prompt": f"""MESH DISTRIBUTED - Node {i+1}

TASK: {plan.task}

You are mesh node {i+1} with chain perspective: {chain_id}

Execute analysis independently. Include:
- node_id: {i+1}
- chain_id: {chain_id}
- confidence: 0.0-1.0
- result: your analysis""",
                    "subagent_type": "Explore",
                    "run_in_background": True,
                    "mesh_node": i
                })

        elif plan.compute_type == ComputeType.MESH_OFFENSIVE:
            for i, chain_id in enumerate(plan.chains):
                commands.append({
                    "description": f"Offensive node {i+1} ({chain_id.split('_')[0]})",
                    "prompt": f"""MESH OFFENSIVE - Security Node {i+1}

TARGET TASK: {plan.task}

You are on an OFFENSIVE SECURITY node.
Chain perspective: {chain_id}

Focus on:
- Attack surface analysis
- Vulnerability identification
- Exploitation paths
- Defense considerations

Output:
```json
{{
  "node_id": {i+1},
  "chain_id": "{chain_id}",
  "security_findings": [],
  "risk_level": "low|medium|high|critical",
  "confidence": 0.0-1.0
}}
```""",
                    "subagent_type": "general-purpose",
                    "run_in_background": True,
                    "mesh_type": "offensive"
                })

        else:
            # Default to parallel
            for chain_id in plan.chains:
                commands.append(self._create_chain_command(
                    chain_id, plan.task, background=True, domain=domain
                ))

        return commands

    def _create_chain_command(
        self,
        chain_id: str,
        task: str,
        background: bool,
        domain: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a Task command for a specific verification chain"""

        prompt_template = self.CHAIN_PROMPTS.get(chain_id, self.CHAIN_PROMPTS["A_SINGLE_SOURCE"])
        prompt = prompt_template.format(task=task)

        return {
            "description": f"Chain-{chain_id.split('_')[0]} verify",
            "prompt": prompt,
            "subagent_type": "general-purpose",
            "run_in_background": background
        }

    def create_archetype_panel_commands(
        self,
        task: str,
        domain: Optional[str] = None,
        panel_size: int = 5,
        required_archetypes: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Generate Task commands for an expert archetype panel"""

        if domain is None:
            domain = self.detect_domain(task)

        panel = self.archetype_loader.compose_panel(
            domain=domain,
            panel_size=panel_size,
            required_archetypes=required_archetypes
        )

        commands = []
        for archetype_id in panel:
            persona = self.archetype_loader.synthesize_persona(
                archetype_id=archetype_id,
                domain=domain,
                task_context=task
            )

            commands.append({
                "description": f"{persona.title} ({archetype_id})",
                "prompt": persona.expertise_prompt,
                "subagent_type": "general-purpose",
                "run_in_background": True
            })

        return commands

    def create_smart_execution_plan(
        self,
        task: str,
        precision_level: int = 3,
        use_archetypes: bool = True
    ) -> Dict[str, Any]:
        """
        Create a complete execution plan with chains and archetypes.

        Returns a dict suitable for JSON serialization with:
        - chain_commands: Verification chain Task invocations
        - archetype_commands: Expert panel Task invocations
        - execution_mode: How to run (parallel, etc.)
        - aggregation: How to combine results
        """

        domain = self.detect_domain(task)
        plan = self.create_execution_plan(task, precision_level=precision_level)

        chain_commands = self.get_task_commands(plan, domain=domain)

        archetype_commands = []
        if use_archetypes:
            panel_size = min(precision_level + 2, 7)
            archetype_commands = self.create_archetype_panel_commands(
                task=task,
                domain=domain,
                panel_size=panel_size
            )

        return {
            "task": task,
            "domain_detected": domain,
            "precision_level": precision_level,
            "compute_type": plan.compute_type.value,
            "chain_commands": chain_commands,
            "archetype_commands": archetype_commands,
            "execution_mode": "parallel" if plan.compute_type in [
                ComputeType.PARALLEL, ComputeType.SWARM, ComputeType.HIVEMIND
            ] else "sequential",
            "aggregation": {
                "method": self._get_aggregation_method(plan.compute_type),
                "chain_weight": 0.6,
                "archetype_weight": 0.4
            },
            "total_agents": len(chain_commands) + len(archetype_commands)
        }

    def _get_aggregation_method(self, compute_type: ComputeType) -> str:
        """Get aggregation method for compute type"""
        mapping = {
            ComputeType.PARALLEL: "confidence_weighted_average",
            ComputeType.HIVEMIND: "majority_vote",
            ComputeType.SWARM: "best_of_n",
            ComputeType.TOURNAMENT: "elimination",
            ComputeType.SEQUENTIAL: "last_result",
            ComputeType.PIPELINE: "chain_refinement",
            ComputeType.ENSEMBLE: "weighted_combination"
        }
        return mapping.get(compute_type, "confidence_weighted_average")

    def parse_task_output(self, raw_output: str, chain_id: str = "unknown") -> ChainResult:
        """Parse raw task output into structured ChainResult"""

        confidence = 0.5
        result = raw_output

        # Try to extract JSON
        json_match = re.search(r'```json\s*(.*?)\s*```', raw_output, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                confidence = float(data.get("confidence", 0.5))
                result = data.get("result", raw_output)
            except (json.JSONDecodeError, ValueError):
                pass

        # Look for confidence patterns
        conf_match = re.search(r'confidence[:\s]+([0-9.]+)', raw_output.lower())
        if conf_match:
            try:
                confidence = float(conf_match.group(1))
                if confidence > 1:
                    confidence = confidence / 100
            except ValueError:
                pass

        return ChainResult(
            chain_id=chain_id,
            result=result,
            confidence=min(1.0, max(0.0, confidence))
        )

    def aggregate_results(
        self,
        results: List[ChainResult],
        compute_type: ComputeType = ComputeType.PARALLEL
    ) -> Dict[str, Any]:
        """Aggregate multiple chain results into final output"""

        if not results:
            return {"confidence": 0, "result": "", "status": "no_results"}

        method = self._get_aggregation_method(compute_type)

        if method == "confidence_weighted_average":
            total_weight = sum(r.confidence for r in results)
            if total_weight == 0:
                return {"confidence": 0, "result": results[0].result, "status": "zero_confidence"}

            weighted_conf = sum(r.confidence ** 2 for r in results) / total_weight
            best = max(results, key=lambda r: r.confidence)

            return {
                "confidence": weighted_conf,
                "result": best.result,
                "method": method,
                "chain_count": len(results),
                "status": "success"
            }

        elif method == "majority_vote":
            if len(results) < 3:
                return self.aggregate_results(results, ComputeType.PARALLEL)

            high_conf = [r for r in results if r.confidence >= 0.6]
            if len(high_conf) >= len(results) * 0.6:
                best = max(high_conf, key=lambda r: r.confidence)
                return {
                    "confidence": sum(r.confidence for r in high_conf) / len(high_conf),
                    "result": best.result,
                    "method": method,
                    "votes": len(high_conf),
                    "status": "consensus"
                }
            return {"confidence": 0.5, "result": results[0].result, "status": "no_consensus"}

        elif method == "best_of_n":
            best = max(results, key=lambda r: r.confidence)
            return {
                "confidence": best.confidence,
                "result": best.result,
                "method": method,
                "chain_id": best.chain_id,
                "status": "success"
            }

        elif method == "elimination":
            sorted_results = sorted(results, key=lambda r: r.confidence, reverse=True)
            winner = sorted_results[0]
            return {
                "confidence": winner.confidence,
                "result": winner.result,
                "method": method,
                "winner": winner.chain_id,
                "status": "success"
            }

        else:
            # Default: last result
            return {
                "confidence": results[-1].confidence,
                "result": results[-1].result,
                "method": "last_result",
                "status": "success"
            }

    def aggregate_from_json(
        self,
        task_outputs: List[Dict[str, Any]],
        plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Aggregate results from JSON plan output.

        Args:
            task_outputs: List of {task_id, output, description} dicts
            plan: The execution plan dict from create_smart_execution_plan
        """

        compute_type_str = plan.get("compute_type", "parallel")
        precision_level = plan.get("precision_level", 3)

        try:
            compute_type = ComputeType(compute_type_str)
        except ValueError:
            compute_type = ComputeType.PARALLEL

        chain_results = []
        archetype_results = []

        for output in task_outputs:
            chain_id = output.get("description", output.get("task_id", "unknown"))
            raw_output = output.get("output", "")

            chain_result = self.parse_task_output(raw_output, chain_id)
            chain_result.agent_id = output.get("task_id")

            # Separate archetype results from chain results
            if "archetype" in chain_id.lower() or "ARC-" in chain_id or "ARC-" in raw_output:
                archetype_results.append(chain_result)
            else:
                chain_results.append(chain_result)

        # Aggregate chain results
        if chain_results:
            aggregated = self.aggregate_results(chain_results, compute_type)
        else:
            aggregated = {"confidence": 0, "status": "no_chain_results"}

        # Add archetype results
        aggregated["chain_results"] = [
            {"id": r.chain_id, "confidence": r.confidence, "result": r.result[:500]}
            for r in chain_results
        ]
        aggregated["archetype_results"] = [
            {"id": r.chain_id, "confidence": r.confidence, "result": r.result[:500]}
            for r in archetype_results
        ]

        # Combine confidences: 60% chains, 40% archetypes
        if archetype_results:
            archetype_confidence = sum(r.confidence for r in archetype_results) / len(archetype_results)
            chain_confidence = aggregated.get("confidence", 0)
            if chain_results:
                aggregated["confidence"] = (chain_confidence * 0.6) + (archetype_confidence * 0.4)
            else:
                aggregated["confidence"] = archetype_confidence

        aggregated["chain_count"] = len(chain_results)
        aggregated["archetype_count"] = len(archetype_results)
        aggregated["total_agents"] = len(task_outputs)
        aggregated["compute_type"] = compute_type_str
        aggregated["precision_level"] = precision_level
        aggregated["aggregation_method"] = self._get_aggregation_method(compute_type)

        return aggregated


# Auto-detection functions
def auto_detect_compute(task: str) -> str:
    """Auto-detect optimal compute type from task description"""
    task_lower = task.lower()

    if any(kw in task_lower for kw in ["security", "audit", "vulnerability", "attack"]):
        return "hivemind"
    elif any(kw in task_lower for kw in ["max", "comprehensive", "thorough", "exhaustive"]):
        return "swarm"
    elif any(kw in task_lower for kw in ["compare", "evaluate", "test", "benchmark"]):
        return "tournament"
    elif any(kw in task_lower for kw in ["quick", "simple", "check", "basic"]):
        return "sequential"
    else:
        return "parallel"


def auto_detect_precision(task: str) -> int:
    """Auto-detect optimal precision level from task description"""
    task_lower = task.lower()

    if any(kw in task_lower for kw in ["security", "critical", "production", "audit"]):
        return 5
    elif any(kw in task_lower for kw in ["thorough", "comprehensive", "detailed"]):
        return 4
    elif any(kw in task_lower for kw in ["quick", "simple", "basic", "fast"]):
        return 1
    else:
        return 3


def auto_detect_parameters(task: str) -> Dict[str, Any]:
    """Auto-detect all parameters from task description"""
    return {
        "compute_type": auto_detect_compute(task),
        "precision_level": auto_detect_precision(task)
    }
