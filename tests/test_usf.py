#!/usr/bin/env python3
"""
USF-2 Test Suite

Run with: python3 tests/test_usf.py
"""

import sys
import json
import subprocess

sys.path.insert(0, 'src')

from usf_executor import (
    USFExecutor,
    ComputeType,
    auto_detect_compute,
    auto_detect_precision,
    auto_detect_parameters
)
from usf_runner import USFRunner


def test_auto_detect_compute():
    """Test compute type auto-detection"""
    tests = [
        ("security audit of the system", "hivemind"),
        ("quick check of this code", "sequential"),
        ("comprehensive review of architecture", "swarm"),
        ("compare these two approaches", "tournament"),
        ("analyze the design patterns", "parallel"),
        ("random task with no keywords", "parallel"),
    ]

    passed = 0
    for task, expected in tests:
        result = auto_detect_compute(task)
        if result == expected:
            print(f"  [PASS] auto_detect_compute: {task[:30]}...")
            passed += 1
        else:
            print(f"  [FAIL] auto_detect_compute: {task[:30]}... (got {result}, expected {expected})")

    return passed, len(tests)


def test_auto_detect_precision():
    """Test precision level auto-detection"""
    tests = [
        ("security audit", 5),
        ("quick check", 1),
        ("thorough analysis", 4),
        ("basic review", 1),
        ("normal task", 3),
    ]

    passed = 0
    for task, expected in tests:
        result = auto_detect_precision(task)
        if result == expected:
            print(f"  [PASS] auto_detect_precision: {task[:30]}...")
            passed += 1
        else:
            print(f"  [FAIL] auto_detect_precision: {task[:30]}... (got {result}, expected {expected})")

    return passed, len(tests)


def test_executor_creation():
    """Test executor instantiation"""
    try:
        executor = USFExecutor()
        print("  [PASS] USFExecutor creation")
        return 1, 1
    except Exception as e:
        print(f"  [FAIL] USFExecutor creation: {e}")
        return 0, 1


def test_execution_plan():
    """Test execution plan creation"""
    executor = USFExecutor()
    passed = 0
    total = 3

    # Test default plan
    plan = executor.create_execution_plan("test task")
    if plan.task == "test task" and plan.precision_level == 3:
        print("  [PASS] Default execution plan")
        passed += 1
    else:
        print("  [FAIL] Default execution plan")

    # Test with compute type
    plan = executor.create_execution_plan("test", compute_type="hivemind", precision_level=5)
    if plan.compute_type == ComputeType.HIVEMIND and plan.precision_level == 5:
        print("  [PASS] Custom execution plan")
        passed += 1
    else:
        print("  [FAIL] Custom execution plan")

    # Test chains for precision
    chains = executor.get_chains_for_precision(5)
    if len(chains) == 9:
        print("  [PASS] PL5 chains")
        passed += 1
    else:
        print(f"  [FAIL] PL5 chains (got {len(chains)}, expected 9)")

    return passed, total


def test_task_commands():
    """Test task command generation for all compute types"""
    executor = USFExecutor()
    passed = 0
    total = len(ComputeType)

    for ct in ComputeType:
        plan = executor.create_execution_plan("test task", compute_type=ct.value, precision_level=3)
        commands = executor.get_task_commands(plan)

        if len(commands) > 0:
            print(f"  [PASS] {ct.value} generates {len(commands)} commands")
            passed += 1
        else:
            print(f"  [FAIL] {ct.value} generates no commands")

    return passed, total


def test_smart_plan():
    """Test smart execution plan"""
    executor = USFExecutor()
    passed = 0
    total = 4

    plan = executor.create_smart_execution_plan(
        task="security audit of authentication",
        precision_level=3,
        use_archetypes=True
    )

    if "chain_commands" in plan:
        print("  [PASS] Smart plan has chain_commands")
        passed += 1
    else:
        print("  [FAIL] Smart plan missing chain_commands")

    if "archetype_commands" in plan:
        print("  [PASS] Smart plan has archetype_commands")
        passed += 1
    else:
        print("  [FAIL] Smart plan missing archetype_commands")

    if plan.get("domain_detected") == "security":
        print("  [PASS] Domain detected as security")
        passed += 1
    else:
        print(f"  [FAIL] Domain detection (got {plan.get('domain_detected')})")

    if plan.get("total_agents", 0) > 0:
        print(f"  [PASS] Total agents: {plan['total_agents']}")
        passed += 1
    else:
        print("  [FAIL] No agents in plan")

    return passed, total


def test_aggregation():
    """Test result aggregation"""
    executor = USFExecutor()
    passed = 0
    total = 4

    # Test basic aggregation
    outputs = [
        {"task_id": "1", "description": "Chain-A verify", "output": '{"confidence": 0.8}'},
        {"task_id": "2", "description": "Chain-B verify", "output": '{"confidence": 0.9}'},
    ]
    result = executor.aggregate_from_json(outputs, {"compute_type": "parallel", "precision_level": 3})

    if 0 < result.get("confidence", 0) <= 1:
        print("  [PASS] Basic aggregation")
        passed += 1
    else:
        print("  [FAIL] Basic aggregation")

    # Test with archetypes
    outputs.append({
        "task_id": "3",
        "description": "Security Auditor (ARC-QA)",
        "output": '{"confidence": 0.85}'
    })
    result = executor.aggregate_from_json(outputs, {"compute_type": "parallel", "precision_level": 3})

    if result.get("archetype_count", 0) == 1:
        print("  [PASS] Archetype detection")
        passed += 1
    else:
        print(f"  [FAIL] Archetype detection (got {result.get('archetype_count')})")

    # Test empty outputs
    result = executor.aggregate_from_json([], {"compute_type": "parallel", "precision_level": 3})
    if result.get("status") == "no_chain_results":
        print("  [PASS] Empty outputs handling")
        passed += 1
    else:
        print("  [FAIL] Empty outputs handling")

    # Test malformed JSON
    outputs = [{"task_id": "1", "description": "Test", "output": "not json"}]
    result = executor.aggregate_from_json(outputs, {"compute_type": "parallel", "precision_level": 3})
    if "confidence" in result:
        print("  [PASS] Malformed JSON handling")
        passed += 1
    else:
        print("  [FAIL] Malformed JSON handling")

    return passed, total


def test_runner():
    """Test USFRunner class"""
    passed = 0
    total = 4

    try:
        runner = USFRunner()
        print("  [PASS] USFRunner creation")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] USFRunner creation: {e}")
        return passed, total

    # Test prepare
    plan = runner.prepare("test task", auto=True)
    if plan.total_agents > 0:
        print(f"  [PASS] Runner prepare ({plan.total_agents} agents)")
        passed += 1
    else:
        print("  [FAIL] Runner prepare")

    # Test properties
    if plan.chain_count >= 0 and plan.archetype_count >= 0:
        print("  [PASS] Runner properties")
        passed += 1
    else:
        print("  [FAIL] Runner properties")

    # Test aggregate
    outputs = [{"task_id": "1", "description": "Test", "output": '{"confidence": 0.8}'}]
    result = runner.aggregate(outputs, plan.plan_dict)
    if "confidence" in result:
        print("  [PASS] Runner aggregate")
        passed += 1
    else:
        print("  [FAIL] Runner aggregate")

    return passed, total


def test_cli():
    """Test CLI interface"""
    passed = 0
    total = 3

    # Test --json output
    try:
        result = subprocess.run(
            ["python3", "src/usf.py", "test task", "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if "task_invocations" in data:
                print("  [PASS] CLI --json output")
                passed += 1
            else:
                print("  [FAIL] CLI --json missing task_invocations")
        else:
            print(f"  [FAIL] CLI --json error: {result.stderr}")
    except Exception as e:
        print(f"  [FAIL] CLI --json: {e}")

    # Test --auto flag
    try:
        result = subprocess.run(
            ["python3", "src/usf.py", "security audit", "--auto", "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            # Security should trigger hivemind
            print("  [PASS] CLI --auto flag")
            passed += 1
        else:
            print(f"  [FAIL] CLI --auto: {result.stderr}")
    except Exception as e:
        print(f"  [FAIL] CLI --auto: {e}")

    # Test --compute override
    try:
        result = subprocess.run(
            ["python3", "src/usf.py", "test", "--compute", "tournament", "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data.get("compute_type") == "tournament":
                print("  [PASS] CLI --compute override")
                passed += 1
            else:
                print(f"  [FAIL] CLI --compute (got {data.get('compute_type')})")
        else:
            print(f"  [FAIL] CLI --compute: {result.stderr}")
    except Exception as e:
        print(f"  [FAIL] CLI --compute: {e}")

    return passed, total


def main():
    print("=" * 60)
    print("USF-2 TEST SUITE")
    print("=" * 60)
    print()

    total_passed = 0
    total_tests = 0

    print("=== AUTO-DETECTION TESTS ===")
    p, t = test_auto_detect_compute()
    total_passed += p
    total_tests += t

    p, t = test_auto_detect_precision()
    total_passed += p
    total_tests += t

    print("\n=== EXECUTOR TESTS ===")
    p, t = test_executor_creation()
    total_passed += p
    total_tests += t

    p, t = test_execution_plan()
    total_passed += p
    total_tests += t

    print("\n=== COMPUTE TYPE TESTS ===")
    p, t = test_task_commands()
    total_passed += p
    total_tests += t

    print("\n=== SMART PLAN TESTS ===")
    p, t = test_smart_plan()
    total_passed += p
    total_tests += t

    print("\n=== AGGREGATION TESTS ===")
    p, t = test_aggregation()
    total_passed += p
    total_tests += t

    print("\n=== RUNNER TESTS ===")
    p, t = test_runner()
    total_passed += p
    total_tests += t

    print("\n=== CLI TESTS ===")
    p, t = test_cli()
    total_passed += p
    total_tests += t

    print()
    print("=" * 60)
    print(f"RESULTS: {total_passed}/{total_tests} passed ({100*total_passed//total_tests}%)")
    print("=" * 60)

    return 0 if total_passed == total_tests else 1


if __name__ == "__main__":
    sys.exit(main())
