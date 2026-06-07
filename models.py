# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

from openenv.core.env_server.types import Action, Observation
from pydantic import Field

class SreIncidentTriageAction(Action):
    """Action for the Sre Incident Triage environment."""
    command: str = Field(..., description="Command to execute: ANALYZE_LOGS, CHECK_METRICS, ISOLATE_SERVICE, RESTART_POOL, BLOCK_IP_RANGE")

class SreIncidentTriageObservation(Observation):
    """Observation from the Sre Incident Triage environment."""
    output: str = Field(default="", description="Command output")
    system_health: float = Field(default=100.0, description="System health score (0-100)")
    time_used: int = Field(default=0, description="Time used in the current incident")
    alert_summary: str = Field(default="", description="Summary of the active alert")
