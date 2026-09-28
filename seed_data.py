"""
seed_data.py - Populate the NexusCorp intelligence memory bank with 10 synthetic
               competitor updates spanning March-September 2026.

Run:  python seed_data.py
"""

import os
import sys
import time
from dotenv import load_dotenv
from hindsight_client import Hindsight

# Force UTF-8 output on Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

HINDSIGHT_API_KEY  = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
MEMORY_BANK        = "nexuscorp-intelligence-bank"

# 10 Synthetic NexusCorp Competitor Updates (March-September 2026)
SEED_UPDATES = [
    {
        "date": "2026-03-04",
        "content": (
            "[March 2026] NexusCorp's primary rival, Synthetix Corp, quietly hired "
            "Tomas Ibarra away from NexusCorp's VP of Product role. Ibarra brings deep "
            "knowledge of NexusCorp's three-year roadmap for AI-embedded enterprise "
            "dashboards. Intelligence sources confirm he is leading a stealth product "
            "team at Synthetix focused on replicating NexusCorp's workflow automation suite."
        ),
    },
    {
        "date": "2026-03-21",
        "content": (
            "[March 2026] OrbitEdge Technologies closed a $95M Series C round led by "
            "Andreessen Horowitz, with participation from Salesforce Ventures. The capital "
            "is earmarked for expanding their mid-market go-to-market motion and doubling "
            "their sales headcount in EMEA. This positions OrbitEdge as a direct threat to "
            "NexusCorp's European accounts in the manufacturing vertical."
        ),
    },
    {
        "date": "2026-04-08",
        "content": (
            "[April 2026] Synthetix Corp publicly launched 'Synth-AI Copilot', a generative "
            "AI layer integrated into their CRM product. Early reviews note it underperforms "
            "on complex multi-step reasoning tasks, but the marketing push is aggressive. "
            "Several NexusCorp enterprise prospects have requested a comparison demo, "
            "signalling growing awareness pressure in the market."
        ),
    },
    {
        "date": "2026-04-29",
        "content": (
            "[April 2026] DataVault Systems, a mid-tier competitor, announced a strategic "
            "partnership with Microsoft Azure to bundle their analytics platform with Azure "
            "Marketplace listings. The co-sell agreement grants DataVault access to Azure's "
            "200,000+ enterprise customer base. NexusCorp currently has no comparable "
            "cloud-marketplace co-sell arrangement."
        ),
    },
    {
        "date": "2026-05-15",
        "content": (
            "[May 2026] OrbitEdge Technologies poached NexusCorp's Regional Sales Director "
            "for APAC, Priya Mehta, offering a reported 40% salary increase and equity "
            "refresh. Mehta managed NexusCorp's three largest APAC accounts (combined ARR "
            "$8.2M). There is a 90-day non-compete clause, but relationship continuity "
            "risk with those accounts is high."
        ),
    },
    {
        "date": "2026-06-02",
        "content": (
            "[June 2026] Gartner published its 2026 Magic Quadrant for Enterprise Workflow "
            "Automation. NexusCorp was placed as a 'Challenger'. Synthetix Corp moved into "
            "the 'Leaders' quadrant for the first time, largely credited to Tomas Ibarra's "
            "product direction. OrbitEdge remained a 'Visionary'. This shift is already "
            "influencing procurement committee shortlists at Fortune 500 prospects."
        ),
    },
    {
        "date": "2026-06-20",
        "content": (
            "[June 2026] NexusCorp's intelligence team confirmed that Synthetix Corp is "
            "underpricing NexusCorp by an average of 23% in competitive deal cycles, "
            "funded by their recent $200M Series D war chest. Three mid-market deals "
            "were lost to Synthetix in Q2 on price alone. A fourth deal (a $1.4M ACV "
            "opportunity with a logistics firm) is currently at risk."
        ),
    },
    {
        "date": "2026-07-11",
        "content": (
            "[July 2026] DataVault Systems released an open-source version of their core "
            "ETL engine under an MIT licence, branded 'VaultCore'. The move is designed to "
            "build developer mindshare and create an inbound pipeline of SMB customers who "
            "eventually upgrade to paid tiers. GitHub traction reached 4,200 stars within "
            "two weeks of launch, suggesting strong developer community adoption."
        ),
    },
    {
        "date": "2026-08-18",
        "content": (
            "[August 2026] Synthetix Corp signed a preferred-vendor agreement with the UK "
            "Government's Central Digital & Data Office (CDDO), granting them access to "
            "framework contracts across 300+ public-sector bodies. NexusCorp had been in "
            "late-stage talks for the same framework. The loss eliminates a projected "
            "$12M public-sector pipeline for NexusCorp in the 2026-2027 fiscal year."
        ),
    },
    {
        "date": "2026-09-10",
        "content": (
            "[September 2026] Following the UK CDDO win, Synthetix Corp announced 'GovPods' "
            "- pre-configured, compliance-ready deployment bundles targeting public-sector "
            "IT teams. Each pod includes their AI Copilot, workflow engine, and audit trail "
            "modules pre-tuned to ISO 27001 and UK Government Security Classifications. "
            "Industry analysts predict GovPods will become a template replicated for EU "
            "and US federal markets in 2027, significantly widening Synthetix's addressable "
            "public-sector footprint at NexusCorp's expense."
        ),
    },
]


def main():
    client = Hindsight(base_url=HINDSIGHT_BASE_URL, api_key=HINDSIGHT_API_KEY)

    print(f"\n{'='*60}")
    print(f"  NexusCorp Intelligence Bank -- Seed Script")
    print(f"  Bank: {MEMORY_BANK}")
    print(f"  Base URL: {HINDSIGHT_BASE_URL}")
    print(f"  Updates to seed: {len(SEED_UPDATES)}")
    print(f"{'='*60}\n")

    success_count = 0
    fail_count    = 0

    for i, update in enumerate(SEED_UPDATES, start=1):
        label = f"[{i:02d}/{len(SEED_UPDATES)}] {update['date']}"
        try:
            client.retain(
                bank_id=MEMORY_BANK,
                content=update["content"],
                metadata={"date": update["date"], "source": "seed_data"},
            )
            print(f"  [OK] {label} -- stored successfully")
            success_count += 1
        except Exception as e:
            print(f"  [FAIL] {label} -- ERROR: {e}")
            fail_count += 1

        # Small delay to avoid rate-limiting
        if i < len(SEED_UPDATES):
            time.sleep(0.6)

    print(f"\n{'='*60}")
    print(f"  Seeding complete: {success_count} succeeded, {fail_count} failed")
    print(f"{'='*60}\n")

    if fail_count == 0:
        print(">> Memory bank fully populated. Run the app with:")
        print("     streamlit run app.py\n")
    else:
        print("[!] Some updates failed. Check HINDSIGHT_API_KEY and connectivity.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
