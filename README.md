---
title: Sre Incident Triage Env
emoji: 🚨
colorFrom: red
colorTo: yellow
sdk: docker
pinned: false
---

# SRE Incident Triage Environment (`sre-incident-triage-env`)

An OpenEnv environment simulating an on-call SRE triage scenario. The agent acts as an SRE responding to production incidents in a cloud e-commerce platform. It receives alerts, must investigate root causes, prioritize issues, and apply safe mitigations under time pressure.

## Scenarios

The environment supports 3 difficulty levels:

1. **Easy (Task 1)**: High CPU alert on a service.
   - **Goal**: Analyze logs, identify the culprit, and isolate the service.
   - **Commands**: `ANALYZE_LOGS payment`, `ISOLATE_SERVICE payment-service`

2. **Medium (Task 2)**: Database connection pool exhaustion.
   - **Goal**: Spot stale connections and safely restart the pool.
   - **Commands**: `CHECK_METRICS db`, `RESTART_POOL db`

3. **Hard (Task 3)**: Simultaneous memory leak + DDoS-like traffic spike.
   - **Goal**: Prioritize blocking the DDoS first, then fix the memory leak. Wrong order causes a cascading outage.
   - **Commands**: `BLOCK_IP_RANGE suspicious`, `ANALYZE_LOGS memory`

## Actions

The agent interacts with the environment by executing specific commands as strings:
- `ANALYZE_LOGS [type]`
- `CHECK_METRICS [component]`
- `ISOLATE_SERVICE [name]`
- `RESTART_POOL [db]`
- `BLOCK_IP_RANGE [range]`
- `SUBMIT_REPORT`

## Observations

The environment returns observations containing:
- `output`: Result of the executed command.
- `system_health`: Current system health score (0-100). Decays over time if issues are not resolved.
- `time_used`: Number of steps taken.
- `alert_summary`: Summary of the active alert.

## Running Locally

1. Install dependencies:
   ```bash
   cd sre_incident_triage
   uv sync
   ```

2. Start the local server:
   ```bash
   uv run uvicorn server.app:app --port 8000
   ```

3. Run the baseline inference script:
   ```bash
   uv run inference.py
   ```
