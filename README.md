# AgriRemediate-AI: Autonomous Crop Health Remediation

![Title Animation](https://raw.githubusercontent.com/aniket-work/agri-remediate-ai/main/images/title-animation.gif)

## Overview
**AgriRemediate-AI** is an experimental autonomous crop health management system built using **LangGraph**. It demonstrates a robust, transactional multi-agent architecture for high-stakes agricultural operations, such as precision spraying and irrigation.

The system incorporates a **Two-Phase Commit (2PC)** pattern (Prepare/Commit) combined with **Human-in-the-Loop (HITL)** interrupts and automated rollbacks to ensure that remediation is only executed when all safety and resource conditions are met and approved by a human operator.

## 🏗️ System Architecture

![Architecture](https://raw.githubusercontent.com/aniket-work/agri-remediate-ai/main/images/architecture-diagram.png)

The project consists of several specialized agents:
1.  **Scout Agent**: Interfaces with simulated drone/sensor data to detect anomalies and crop health scores.
2.  **Planner Agent**: Proposes treatment (e.g., Pesticide-A) and reserves inventory (Phase 1: Prepare).
3.  **Safety Agent**: Verifies real-time environmental conditions (e.g., wind speed) before execution.
4.  **Execution Agent**: Performs the physical remediation (Phase 2: Commit) and handles hardware feedback.

## 🔄 Workflow Logic

![Flow Diagram](https://raw.githubusercontent.com/aniket-work/agri-remediate-ai/main/images/flow-diagram.png)

### Transactional Guarantees:
-   **Prepare Phase**: Inventory is "reserved" and safety is checked. If wind speed exceeds 20 km/h, the system automatically rolls back.
-   **Human Interrupt**: The workflow pauses before the `Execution` node, requiring an explicit signal to proceed.
-   **Commit/Rollback**: If the hardware reports a failure during execution, the system triggers a rollback sequence to release reserved resources and log the failure.

## 🚀 Quick Start

### Prerequisites
-   Python 3.12+
-   `langgraph`, `langchain-openai`, `pillow`, `matplotlib`

### Installation
1.  Clone the repository:
    ```bash
    git clone https://github.com/aniket-work/agri-remediate-ai.git
    cd agri-remediate-ai
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Workflow
```bash
python main.py
```

## 📊 Visualizing the Sequence
![Sequence Diagram](https://raw.githubusercontent.com/aniket-work/agri-remediate-ai/main/images/sequence-diagram.png)

---
*Disclaimer: This is an experimental PoC. Hardware interactions are simulated.*
