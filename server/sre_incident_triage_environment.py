# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

import random
from uuid import uuid4
from typing import Dict, Any, Optional

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from ..models import SreIncidentTriageAction, SreIncidentTriageObservation
except ImportError:
    from models import SreIncidentTriageAction, SreIncidentTriageObservation

class SreIncidentTriageEnvironment(Environment):
    """
    SRE Incident Triage Environment where the agent must diagnose and fix issues.
    """
    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._env_state: Dict[str, Any] = {}
        # Initial reset handles populating self._env_state
        self.reset()

    def reset(self, options: Optional[Dict] = None) -> SreIncidentTriageObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)
        
        scenario = options.get("scenario", random.randint(1, 3)) if options else random.randint(1, 3)
        
        self._env_state = {
            "scenario": scenario,
            "system_health": 100.0,
            "time_used": 0,
            "resolved": False,
            "blocked_ddos": False,
            "alert_summary": self._get_initial_alert(scenario)
        }
        
        return SreIncidentTriageObservation(
            output="Incident started. Use commands to investigate.",
            system_health=100.0,
            time_used=0,
            alert_summary=self._env_state["alert_summary"],
            reward=0.0,
            done=False
        )

    def _get_initial_alert(self, scenario: int) -> str:
        if scenario == 1:
            return "High CPU alert on payment-service. Possible config issue."
        elif scenario == 2:
            return "Database connection pool exhaustion detected."
        else:
            return "Multiple alerts: Memory leak + suspicious traffic spike. Prioritize carefully!"

    def step(self, action: SreIncidentTriageAction) -> SreIncidentTriageObservation:
        self._state.step_count += 1
        self._env_state["time_used"] += 1
        
        cmd = action.command.strip().upper()
        reward = 0.0
        done = False
        output = "Command received."
        
        scenario = self._env_state["scenario"]
        
        # Task 1 - Easy: High CPU / Config
        if scenario == 1:
            if "ANALYZE_LOGS" in cmd and "PAYMENT" in cmd:
                reward = 0.4
                output = "Found port mapping error in logs."
            elif "ISOLATE_SERVICE" in cmd and "PAYMENT" in cmd:
                reward = 1.0
                done = True
                output = "SUCCESS: Payment service isolated. Incident resolved."
        
        # Task 2 - Medium: DB Pool
        elif scenario == 2:
            if "CHECK_METRICS" in cmd and "DB" in cmd:
                reward = 0.5
                output = "Stale connections detected in pool."
            elif "RESTART_POOL" in cmd:
                reward = 1.0
                done = True
                output = "SUCCESS: Connection pool restarted safely."
        
        # Task 3 - Hard: Multi-issue
        else:
            if "BLOCK_IP" in cmd or "BLOCK" in cmd:
                reward = 0.6
                output = "DDoS traffic blocked. Now address memory leak."
                self._env_state["blocked_ddos"] = True
            elif "MEMORY" in cmd or "LEAK" in cmd:
                if self._env_state.get("blocked_ddos", False):
                    reward = 1.0
                    done = True
                    output = "SUCCESS: All issues mitigated. System stable."
                else:
                    reward = -0.5
                    output = "CRITICAL: Wrong priority - DDoS not blocked first."
        
        # Time pressure & health decay
        if self._env_state["time_used"] > 8:
            self._env_state["system_health"] = max(0, self._env_state["system_health"] - 15)
            
        if self._env_state["system_health"] <= 0:
            done = True
            reward = min(reward, 0.0)
            
        self._env_state["resolved"] = done
        
        return SreIncidentTriageObservation(
            output=output,
            system_health=self._env_state["system_health"],
            time_used=self._env_state["time_used"],
            alert_summary=self._env_state["alert_summary"],
            reward=reward,
            done=done,
            metadata=self._env_state.copy()
        )

    @property
    def state(self) -> State:
        return self._state
