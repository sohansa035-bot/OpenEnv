---
title: Sre Incident Triage Env
emoji: 🚨
colorFrom: red
colorTo: yellow
sdk: docker
pinned: false
---

# 🚨 SRE Incident Triage Environment (`sre-incident-triage-env`)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenEnv](https://img.shields.io/badge/OpenEnv-Compatible-brightgreen.svg)](https://github.com/openenv-project/openenv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An advanced, deterministic **OpenEnv** environment designed for evaluating AI Agents on real-world Site Reliability Engineering (SRE) tasks.

## 📖 Overview

The **SRE Incident Triage Environment** simulates a high-pressure on-call scenario for a cloud e-commerce platform. AI agents are tasked with receiving production alerts, investigating logs and metrics, identifying root causes, and deploying safe mitigations—all while the system's health decays under simulated time pressure.

This project was built to provide a **highly realistic, operational task benchmark** for agentic workflows, mirroring the day-to-day challenges faced by SREs at Meta and other top tech companies.

### ✨ Key Features
- **Deterministic Grading**: Consistent evaluation criteria across multiple agent runs.
- **Dynamic System Health**: The environment actively decays system health with each step if critical issues are ignored.
- **Multi-step Reasoning**: Agents must perform diagnostic steps before executing mitigations.
- **Priority Handling**: Hard scenarios require the agent to prioritize immediate threats (e.g., DDoS) over secondary issues (e.g., Memory Leaks) to prevent cascading failures.

---

## 🎯 Incident Scenarios

The environment supports 3 difficulty levels, randomly assigned or manually forced via the `reset` options:

1. 🟢 **Easy (Task 1)**: *High CPU Alert*
   - **Scenario**: A single microservice is experiencing unexplained CPU spikes.
   - **Optimal Path**: `ANALYZE_LOGS payment` -> `ISOLATE_SERVICE payment-service`

2. 🟡 **Medium (Task 2)**: *Database Connection Pool Exhaustion*
   - **Scenario**: The application is hanging due to stale connections holding the DB hostage.
   - **Optimal Path**: `CHECK_METRICS db` -> `RESTART_POOL db`

3. 🔴 **Hard (Task 3)**: *Cascading Failure (DDoS + Memory Leak)*
   - **Scenario**: A simultaneous memory leak and suspicious traffic spike are occurring. 
   - **Optimal Path**: The agent *must* prioritize blocking the traffic (`BLOCK_IP_RANGE suspicious`) before analyzing the memory (`ANALYZE_LOGS memory`). Doing the reverse results in immediate system failure.

---

## 🛠️ API & Agent Interfaces

### Actions
The agent interacts with the environment by executing specific command strings:
*   `ANALYZE_LOGS [type]`
*   `CHECK_METRICS [component]`
*   `ISOLATE_SERVICE [name]`
*   `RESTART_POOL [db]`
*   `BLOCK_IP_RANGE [range]`
*   `SUBMIT_REPORT`

### Observations
The environment returns detailed JSON observations to the agent:
*   `output`: The terminal output/result of the executed command.
*   `system_health`: Current system health score (0-100%).
*   `time_used`: Number of steps taken (ticks).
*   `alert_summary`: High-level summary of the active alert from PagerDuty.

---

## 🚀 Quick Start (Local Setup)

To run the OpenEnv environment locally for agent testing:

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Start the FastAPI server:**
   ```bash
   uv run uvicorn server.app:app --port 8000
   ```
   *Note: The server will host the OpenEnv HTTP interface. A visual API dashboard (Swagger) will be available at `http://127.0.0.1:8000/docs`.*

3. **Run the baseline agent test:**
   In a separate terminal window, run the inference baseline to verify the environment:
   ```bash
   uv run inference.py
   ```

---
*Built for the Open Source AI Agent Hackathon.*
