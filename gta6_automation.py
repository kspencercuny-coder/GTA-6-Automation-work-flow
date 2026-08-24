"""
GTA 6 briefing pipeline
Grok drafts research notes → Claude formats a structured report → saves markdown.
Requires env: XAI_API_KEY, ANTHROPIC_API_KEY
Optional env: DISCORD_WEBHOOK (posts a short notice when done)
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone

from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_xai import ChatXAI


def require_keys() -> None:
    missing = [
        name
        for name in ("XAI_API_KEY", "ANTHROPIC_API_KEY")
        if not os.environ.get(name)
    ]
    if missing:
        raise SystemExit(
            f"Missing env vars: {', '.join(missing)}. "
            "Set them in Codespaces/Actions secrets or your shell."
        )


def build_agents() -> tuple[ChatXAI, ChatAnthropic]:
    grok = ChatXAI(
        model="grok-2",
        temperature=0.2,
    )
    claude = ChatAnthropic(
        model="claude-3-5-sonnet-latest",
        temperature=0.3,
    )
    return grok, claude


def research_with_grok(grok: ChatXAI) -> str:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You research Grand Theft Auto VI (GTA 6 / GTA VI). "
                    "Separate confirmed facts from rumors. "
                    "Prefer official Rockstar / Take-Two sources when possible. "
                    "If you are unsure or something is unverified, say so. "
                    "Cover: release timing, platforms, trailers, setting, "
                    "gameplay, map, online plans, and recent credible reporting. "
                    "Output a concise raw brief with bullet points."
                ),
            ),
            (
                "user",
                (
                    "Produce an up-to-date GTA 6 intelligence brief. "
                    "Label each item: CONFIRMED, RUMOR, or UNKNOWN."
                ),
            ),
        ]
    )
    chain = prompt | grok | StrOutputParser()
    print("Step 1/3 — Grok research…")
    return chain.invoke({})


def synthesize_with_claude(claude: ChatAnthropic, research: str) -> str:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are a careful games analyst. Rewrite the raw research into "
                    "a clean markdown report. Do not invent facts. "
                    "Use these headers exactly:\n"
                    "## Executive summary\n"
                    "## Confirmed\n"
                    "## Rumors and speculation\n"
                    "## Open questions\n"
                    "## Streamer notes\n"
                    "Under Streamer notes, suggest 3–5 on-stream talking points "
                    "that stay honest about what is unconfirmed."
                ),
            ),
            (
                "user",
                (
                    "Raw research:\n\n{research_data}\n\n"
                    "Build the structured GTA 6 briefing now."
                ),
            ),
        ]
    )
    chain = prompt | claude | StrOutputParser()
    print("Step 2/3 — Claude synthesis…")
    return chain.invoke({"research_data": research})


def save_report(report: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    path = f"gta6_intelligence_report_{stamp}.md"
    header = (
        f"# GTA 6 intelligence report\n\n"
        f"_Generated {stamp} UTC_\n\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(report.strip())
        f.write("\n")
    print(f"Step 3/3 — Saved {path}")
    return path


def maybe_notify_discord(path: str, report: str) -> None:
    url = os.environ.get("DISCORD_WEBHOOK")
    if not url:
        return
    try:
        import json
        import urllib.request

        preview = report.strip().replace("\n", " ")
        preview = (preview[:280] + "…") if len(preview) > 280 else preview
        body = {
            "content": (
                f"**GTA 6 briefing ready** → `{path}`\n"
                f"{preview}"
            )
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            resp.read()
        print("Discord notice sent.")
    except Exception as exc:  # noqa: BLE001 — best-effort notify
        print(f"Discord notify skipped: {exc}", file=sys.stderr)


def run_gta6_automation_pipeline() -> str:
    require_keys()
    print("Starting GTA 6 multi-agent pipeline\n")
    grok, claude = build_agents()
    research = research_with_grok(grok)
    report = synthesize_with_claude(claude, research)
    print("\n" + "=" * 60)
    print(report)
    print("=" * 60 + "\n")
    path = save_report(report)
    maybe_notify_discord(path, report)
    return path


if __name__ == "__main__":
    run_gta6_automation_pipeline()
