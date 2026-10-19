# GTA 6 Production Automation & Stream Scene Director (Cut)

An AI-driven live production automation system and content orchestration pipeline built for technical live streaming workflows leading up to the Grand Theft Auto VI release. 

This repository bridges **Large Language Model (LLM) multi-agent orchestration** with real-time broadcasting tools. It features an automated multi-model research pipeline (`gta6_automation.py`) alongside an optimized desktop stream configuration framework (`Cut`).

---

## 🚀 Core Features

### 1. Multi-Model AI Research Pipeline (`gta6_automation.py`)
A data pipeline built using **LangChain Expression Language (LCEL)** that leverages the complementary strengths of two industry-leading LLMs:
* **Real-Time Data Aggregation (xAI Grok API):** Utilizes `grok-4-1-fast-non-reasoning` to query, extract, and sort the latest news, leak telemetry, and verified studio announcements into strict informational categories (`CONFIRMED`, `RUMOR`).
* **Structured Synthesis (Anthropic Claude API):** Orchestrates a downstream pass to `claude-sonnet-4-6` to parse the raw unstructured intelligence brief into a meticulously formatted markdown report.
* **Notification Webhooks:** Dispatches a structured automated operational notice to a target **Discord Webhook** immediately upon pipeline completion.

### 2. Stream Director Control Framework (Cut)
A structured control protocol engineered to reduce operational friction and cognitive load for content creators managing complex multi-source setups during live broadcasts.
* **OBS WebSocket Integration:** Interfaces directly with OBS Studio over local networks to execute automated scene transitions (`Starting Soon` ➔ `Live` ➔ `BRB` ➔ `Ending`).
* **Automated Countdowns & Overlays:** Dynamically pushes countdown timers and chat engagement prompts directly into video asset layers.
* **Show Running Logic:** Implements rigid segment boundaries (Hook, Resets, Segment A/B lanes) to ensure broadcast precision within a 90-minute runtime window.

---

## 🛠️ Architecture & Tech Stack

* **Language:** Python 3.11+
* **Frameworks:** LangChain Core, LangChain Anthropic, LangChain xAI
* **APIs & Protocols:** Anthropic Claude API, xAI Grok API, OBS WebSocket Server, Discord Webhooks API, REST / JSON Data Structures
[ Scheduled Event Trigger ]
│
▼
┌───────────────────────────────┐
│     gta6_automation.py        │
└───────────────┬───────────────┘
│
┌───────────────────────┴───────────────────────┐
▼                                               ▼
┌────────────────────┐                          ┌────────────────────┐
│   xAI Grok API     │                          │ Anthropic Claude   │
│ (Real-time Intel)  │ ───[ Concatenated Text ]➔│ (Markdown Design)  │
└────────────────────┘                          └──────────┬─────────┘
│
▼
┌────────────────────┐
│  Discord Webhook   │
│ (Uptime Warning)   │
└────────────────────┘
---

## ⚙️ Setup & Installation

### 1. Prerequisites
Ensure you have Python installed, clone this repository, and install the required dependencies:
```bash
git clone https://github.com/kspencercuny-coder/GTA-6-Automation-work-flow.git
cd GTA-6-Automation-work-flow
pip install -r requirements.txt 
export XAI_API_KEY="your_grok_api_key_here"
export ANTHROPIC_API_KEY="your_claude_api_key_here"
export DISCORD_WEBHOOK="your_optional_discord_webhook_url" # Optional
python gta6_automation.py
• [ ] Audio Loopback: Complete microphone isolation test (5-second echo validation).
• [ ] Scene Verification: Sequencing lock check (Starting Soon ➔ Live ➔ BRB ➔ Ending).
• [ ] Capture Validation: Native local recording active on designated isolation clip source.
• [ ] Metadata Deployment: Live stream title and index category updated in platform dashboards.
• 0:00 - 0:15 | The Hook: Stream introduction, host identity positioning, stating the night's structural value promise.
• 0:15 - 0:45 | Segment A: Focused single-lane analysis covering core topic tracking blocks.
• 0:45 - 0:50 | The Reset: Local system refresh, mid-show audience re-engagement prompt.
• 0:50 - 1:20 | Segment B: Format adjustments, context shifting without deviating from core thematic subject.
• 1:20 - 1:30 | The Outro: Extracting clip timestamps for short-form rendering pipelines, highlighting next broadcast schedule.
If engagement thresholds drop, the control panel triggers interactive dialogue hooks:
1. “What was the very first Grand Theft Auto installment you ever played?”
2. “Jason or Lucia — who do you predict becomes the main liability in the narrative?”
3. “What is your ultimate wild or chaotic Wanted-Level survival story?”
This project is an independent developer toolkit built for workflow simulation and production automation. It is not affiliated with, authorized, maintained, or endorsed by Rockstar Games, Take-Two Interactive, or any of their corporate affiliates.
