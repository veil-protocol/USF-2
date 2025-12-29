"""
USF-2: Unified Superintelligence Framework

A self-evolving methodology framework for AI reasoning.
"""

from .usf_executor import (
    USFExecutor,
    ComputeType,
    USFExecutionPlan,
    ChainResult,
    SynthesizedPersona,
    ArchetypeLoader,
    auto_detect_compute,
    auto_detect_precision,
    auto_detect_parameters
)

from .usf_runner import (
    USFRunner,
    USFPreparedPlan
)

__version__ = "2.0.0"
__all__ = [
    "USFExecutor",
    "USFRunner",
    "ComputeType",
    "USFExecutionPlan",
    "USFPreparedPlan",
    "ChainResult",
    "SynthesizedPersona",
    "ArchetypeLoader",
    "auto_detect_compute",
    "auto_detect_precision",
    "auto_detect_parameters"
]
