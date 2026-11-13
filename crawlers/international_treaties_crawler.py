"""
================================================================================
LexGlobal-OS: Complete Integrated Open-Source Platform
Includes:
1. Terrestrial, Special (Aviation, Submarine, Space/ISS) & International Treaties Crawlers
2. Backend RAG & Legislative Drafting Engine
3. Static Web Portal Generator (Multi-domain ready: .com / .org / .net)

License: CC0-1.0 / MIT
================================================================================
"""

import os
import json
from datetime import datetime, timezone

# Directory Configuration
DATA_DIR = "data/json"
SITE_DIR = "frontend_site"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SITE_DIR, exist_ok=True)


# ==============================================================================
# MODULE 1: GLOBAL & SPECIAL JURISDICTIONS CRAWLER
# ==============================================================================
class GlobalJurisdictionIngestor:
    def __init__(self):
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def ingest_all(self):
        """Ingests terrestrial, special (aviation, submarine, ISS), and treaty frameworks."""
        datasets = [
            # 1. Terrestrial Sample
            {
                "jurisdiction_code": "RO",
                "domain": "terrestrial",
                "name": "Romania - National Legislative Framework",
                "scope": "Sovereign terrestrial law, civil and administrative codes, EU directives transposition.",
                "sample_rule": "Law No. 24/2000 on legislative drafting rules and normative acts."
            },
            # 2. International Aviation
            {
                "jurisdiction_code": "INT_AVIATION",
                "domain": "aviation",
                "name": "International Civil Aviation Organization (ICAO) & Chicago Convention",
                "scope": "Applies to aircraft in international airspace. Governed by the law of the state of registry and Tokyo Convention (1963).",
                "sample_rule": "Article 12 (Chicago Convention): Rules of the air over the high seas shall be established by ICAO."
            },
            # 3. Private Submersibles & High Seas
            {
                "jurisdiction_code": "INT_SUB_PRIVATE",
                "domain": "submarine",
                "name": "Private Submersibles & Deep-Sea Vessels (UNCLOS / NEMO Class)",
                "scope": "Governed by Flag State jurisdiction on the high seas (UNCLOS Art. 87) and marine environmental protection treaties (London Convention).",
                "sample_rule": "Deep-submergence vehicles operating beyond territorial waters remain under the exclusive jurisdiction of their registry state."
            },
            # 4. Extraterrestrial / International Space Station
            {
                "jurisdiction_code": "EXT_ISS",
                "domain": "space",
                "name": "International Space Station (ISS) Intergovernmental Agreement (IGA)",
                "scope": "Extraterrestrial orbital jurisdiction. Partner states retain criminal and civil jurisdiction over their respective flight elements and nationals.",
                "sample_rule": "Article 22 (IGA): Partner States exercise criminal jurisdiction over personnel in or on any flight element who are their respective nationals."
            },
            # 5. International Litigation Treaties
            {
                "jurisdiction_code": "TREATY_ECHR_1950",
                "domain": "international_treaty",
                "name": "European Convention on Human Rights (ECHR)",
                "scope": "Direct application in domestic courts and the European Court of Human Rights for civil, administrative, and property disputes.",
                "sample_rule": "Article 6: Right to a fair trial within a reasonable time by an independent and impartial tribunal."
            },
            {
                "jurisdiction_code": "TREATY_NYC_1958",
                "domain": "international_treaty",
                "name": "New York Arbitration Convention (1958)",
                "scope": "Recognition and enforcement of foreign arbitral awards in international commercial disputes.",
                "sample_rule": "Article II: Each Contracting State shall recognize an agreement in writing under which the parties undertake to submit to arbitration."
            },
            {
                "jurisdiction_code": "TREATY_AARHUS_1998",
                "domain": "international_treaty",
                "name": "Aarhus Convention on Environmental Justice",
                "scope": "Access to information, public participation in decision-making, and access to justice in environmental litigation.",
                "sample_rule": "Article 9: Members of the public have access to administrative or judicial procedures to challenge acts contravening environmental law."
            }
        ]

        for item in datasets:
            item["metadata"] = {
                "ingested_at": self.timestamp,
                "schema_standard": "Akoma-Ntoso-Compatible-JSON",
                "status": "active"
            }
            filename = f"{item['jurisdiction_code']}.json"
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(item, f, ensure_ascii=False, indent=4)
            print(f"[Ingestor] Saved: {filepath}")


# ==============================================================================
# MODULE 2: BACKEND RAG & LEGISLATIVE DRAFTING ENGINE
# ==============================================================================
class LegislativeRAGEngine:
    def __init__(self, data_path: str = DATA_DIR):
        self.data_path = data_path
        self.knowledge_base = self._load_knowledge_base()

    def _load_knowledge_base(self) -> list:
        kb = []
        if not os.path.exists(self.data_path):
            return kb
        for filename in os.listdir(self.data_path):
            if filename.endswith(".json"):
                filepath = os.path.join(self.data_path, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    kb.append(json.load(f))
        print(f"[RAG Engine] Loaded {len(kb)} jurisdictional frameworks into memory.")
        return kb

    def retrieve_context(self, jurisdiction_code: str) -> dict:
        code = jurisdiction_code.upper()
        for doc in self.knowledge_base:
            if doc.get("jurisdiction_code") == code:
                return doc
        return {"error": f"Jurisdiction '{code}' not found in indexed database."}

    def generate_draft_bill(self, jurisdiction_code: str, user_request: str) -> str:
        context = self.retrieve_context(jurisdiction_code)
        if "error" in context:
            return f"Generation Error: {context['error']}"

        draft = f"""================================================================================
DRAFT LEGISLATIVE ACT / LEGAL BRIEF (GENERATED BY LexGlobal-OS)
================================================================================
JURISDICTION CODE : {context['jurisdiction_code']}
DOMAIN CATEGORY   : {context['domain'].upper()}
FRAMEWORK TITLE   : {context['name']}
GENERATED AT (UTC): {datetime.now(timezone.utc).isoformat()}
--------------------------------------------------------------------------------

EXPLANATORY MEMORANDUM:
In response to the user inquiry: "{user_request}", this draft instrument is 
structured in accordance with applicable normative standards, international 
treaties, and jurisdictional hierarchies.

APPLICABLE LEGAL BASIS & PRECEDENT:
- Scope: {context['scope']}
- Key Provision: {context['sample_rule']}

ARTICLE 1 (Subject Matter):
This instrument establishes the regulatory and procedural framework governing 
the requested matter, ensuring full compliance with terrestrial statutes, 
flag-state maritime/aviation rules, or extraterrestrial agreements.

ARTICLE 2 (Jurisdictional Application):
The provisions herein apply to all natural persons, legal entities, vessels, 
aircraft, or orbital habitats operating under {context['jurisdiction_code']}.

ARTICLE 3 (Open-Source Governance & Amendment):
This draft is released into the public domain for peer review and legislative 
refinement via the LexGlobal-OS version control repository.
================================================================================
"""
        return draft


# ==============================================================================
# MODULE 3: STATIC WEB PORTAL GENERATOR (.COM / .ORG / .NET)
# ==============================================================================
class WebPortalGenerator:
    def __init__(self, data_path: str = DATA_DIR, output_dir: str = SITE_DIR):
        self.data_path = data_path
        self.output_dir = output_dir

    def build_site(self):
        records = []
        for filename in sorted(os.listdir(self.data_path)):
            if filename.endswith(".json"):
                with open(os.path.join(self.data_path, filename), "r", encoding="utf-8") as f:
                    records.append(json.load(f))

        cards_html = ""
        options_html = ""
        for rec in records:
            code = rec["jurisdiction_code"]
            name = rec["name"]
            domain = rec["domain"].replace("_", " ").title()
            scope = rec["scope"]
            rule = rec["sample_rule"]

            options_html += f'<option value="{code}">{code} — {name}</option>\n'
            cards_html += f"""
            <div class="card">
                <span class="badge">{domain}</span>
                <h3>{code}: {name}</h3>
                <p><strong>Scope:</strong> {scope}</p>
                <p class="rule"><strong>Key Rule:</strong> {rule}</p>
            </div>
            """

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LexGlobal-OS | Open-Source Global & Extraterrestrial Legal Aggregator</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #e2e8f0; margin: 0; padding: 0; }}
        header {{ background: #1e293b; padding: 2rem; text-align: center; border-bottom: 1px solid #334155; }}
        header h1 {{ margin: 0; color: #38bdf8; font-size: 2.2rem; }}
        header p {{ color: #94a3b8; max-width: 700px; margin: 0.5rem auto 0; }}
        .domains {{ font-size: 0.85rem; color: #64748b; margin-top: 0.5rem; }}
        .container {{ max-width: 1100px; margin: 2rem auto; padding: 0 1rem; }}
        .ad-banner {{ background: #1e293b; border: 1px dashed #475569; padding: 1rem; text-align: center; color: #94a3b8; margin-bottom: 2rem; border-radius: 8px; }}
        .drafting-box {{ background: #1e293b; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; border: 1px solid #334155; }}
        .drafting-box h2 {{ margin-top: 0; color: #f8fafc; }}
        select, textarea, button {{ width: 100%; padding: 0.75rem; margin-top: 0.5rem; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: #f8fafc; font-size: 1rem; box-sizing: border-box; }}
        button {{ background: #0284c7; border: none; font-weight: bold; cursor: pointer; margin-top: 1rem; }}
        button:hover {{ background: #0369a1; }}
        pre {{ background: #020617; padding: 1rem; border-radius: 6px; overflow-x: auto; color: #38bdf8; white-space: pre-wrap; display: none; margin-top: 1rem; border: 1px solid #1e293b; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; }}
        .card {{ background: #1e293b; padding: 1.5rem; border-radius: 8px; border: 1px solid #334155; }}
        .badge {{ background: #0369a1; color: #e0f2fe; padding: 0.25rem 0.6rem; border-radius: 4px; font-size: 0.75rem; text-transform: uppercase; font-weight: bold; }}
        .card h3 {{ margin: 0.75rem 0 0.5rem; color: #f8fafc; }}
        .rule {{ font-size: 0.9rem; color: #94a3b8; border-left: 3px solid #38bdf8; padding-left: 0.75rem; }}
        footer {{ text-align: center; padding: 2rem; color: #64748b; font-size: 0.9rem; border-top: 1px solid #1e293b; margin-top: 3rem; }}
    </style>
</head>
<body>
    <header>
        <h1>LexGlobal-OS</h1>
        <p>Open-Source Global Legislative Aggregator, International Treaties Index & Extraterrestrial Legal Drafting Engine</p>
        <div class="domains">Official Mirrors: lexglobal-os.org | lexglobal-os.net | lexglobal-os.com</div>
    </header>

    <div class="container">
        <div class="ad-banner">
            [Public Access Infrastructure — Supported by Open-Source Sponsors & Ethical Legal-Tech Ads]
        </div>

        <div class="drafting-box">
            <h2>Automated Legislative & Litigation Brief Generator</h2>
            <label for="jurisdiction">Select Jurisdiction or International Treaty:</label>
            <select id="jurisdiction">
                {options_html}
            </select>
            <label for="query">Describe your legal objective, draft bill requirement, or litigation context:</label>
            <textarea id="query" rows="3" placeholder="e.g., Draft a data protection and jurisdictional liability clause for private orbital equipment..."></textarea>
            <button onclick="generateDraft()">Generate Legal Draft</button>
            <pre id="output"></pre>
        </div>

        <h2>Indexed Jurisdictions & International Frameworks ({len(records)})</h2>
        <div class="grid">
            {cards_html}
        </div>
    </div>

    <footer>
        Released under CC0-1.0 / MIT Public Domain License. Contribute via GitHub Pull Requests.
    </footer>

    <script>
        const legalData = {json.dumps(records)};

        function generateDraft() {{
            const code = document.getElementById('jurisdiction').value;
            const query = document.getElementById('query').value || "General regulatory compliance framework";
            const item = legalData.find(d => d.jurisdiction_code === code);
            const output = document.getElementById('output');

            if (!item) return;

            const now = new Date().toISOString();
            output.style.display = 'block';
            output.textContent = `================================================================================
DRAFT LEGISLATIVE ACT / LEGAL BRIEF (GENERATED BY LexGlobal-OS)
================================================================================
JURISDICTION CODE : ${{item.jurisdiction_code}}
DOMAIN CATEGORY   : ${{item.domain.toUpperCase()}}
FRAMEWORK TITLE   : ${{item.name}}
GENERATED AT (UTC): ${{now}}
--------------------------------------------------------------------------------

EXPLANATORY MEMORANDUM:
In response to the inquiry: "${{query}}", this draft instrument is structured 
in accordance with applicable normative standards and international hierarchies.

APPLICABLE LEGAL BASIS:
- Scope: ${{item.scope}}
- Key Provision: ${{item.sample_rule}}

ARTICLE 1 (Subject Matter):
Establishes the legal framework governing the requested matter in compliance 
with sovereign statutes, flag-state maritime/aviation rules, or space treaties.

ARTICLE 2 (Jurisdictional Application):
Applies to all entities, vessels, aircraft, or orbital elements operating under 
${{item.jurisdiction_code}}.

ARTICLE 3 (Open-Source Governance):
Published under CC0-1.0 / MIT for public review and GitHub Pull Request refinement.
================================================================================`;
        }}
    </script>
</body>
</html>
"""
        index_path = os.path.join(self.output_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[Site Generator] Web portal generated successfully at: {index_path}")


# ==============================================================================
# MAIN EXECUTION PIPELINE
# ==============================================================================
if __name__ == "__main__":
    print("--- Starting LexGlobal-OS Full Pipeline ---")
    
    # Step 1: Ingest all terrestrial, special, and international treaty frameworks
    ingestor = GlobalJurisdictionIngestor()
    ingestor.ingest_all()
    
    # Step 2: Initialize Backend RAG Engine and run a verification test
    rag_engine = LegislativeRAGEngine()
    sample_output = rag_engine.generate_draft_bill(
        jurisdiction_code="EXT_ISS",
        user_request="Criminal and data jurisdiction protocol for private commercial modules"
    )
    print("\n" + sample_output)
    
    # Step 3: Build the static web portal ready for GitHub Pages / .com / .org / .net
    portal = WebPortalGenerator()
    portal.build_site()
    
    print("--- Pipeline Execution Complete ---")
