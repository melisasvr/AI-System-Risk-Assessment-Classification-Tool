"""Portable Markdown risk cards with complete input and rule trace."""
import re
from app.schemas import Assessment

SOURCES = [
    ("EU AI Act — official text (verify current consolidated version)", "https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng"),
    ("European Commission — regulatory framework", "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai"),
]

def safe_text(value: object) -> str:
    return re.sub(r"([\\`*_{}\[\]<>|#])", r"\\\1", str(value))

def generate_markdown(a: Assessment) -> str:
    s = a.system
    lines = ["# AI System Risk Card", "", f"## {safe_text(s.name)}", "", f"**Tier:** {a.tier.value} · **Governance score:** {a.score}/100", "", f"Assessment ID: {a.assessment_id}  ", f"Created (UTC): {a.created_at.isoformat()}  ", f"Engine: {a.engine_version} · Status: Provisional / owner review required", "", "## System profile", ""]
    for key,value in s.model_dump().items():
        lines.extend([f"**{key.replace('_',' ').title()}:** {safe_text(value)}", ""])
    lines += ["## Classification rationale", ""]
    lines += [f"- **{f.rule_id}** (+{f.points}): {safe_text(f.reason)}" for f in a.findings]
    lines += ["", f"Raw points: {a.raw_score}. Final score: {a.score}. Floors: High=60; transparency/limited=20; prohibited-practice override=100. Raw scores are capped at 100. Thresholds: Minimal <20, Limited 20–59, High ≥60; overrides take precedence.", "", "## Recommended controls", ""]
    for c in a.controls:
        lines += [f"### {c.title}", c.action, "", f"**Owner:** {c.owner} · **Due:** {c.priority}  ", f"**Evidence:** {c.evidence}", ""]
    lines += ["## Limitations and review", ""] + [f"- {safe_text(n)}" for n in a.review_notes]
    lines += ["", "## Approval record", "", "Reviewer: __________  Review date: __________  Decision: __________", "", "Controls are recommendations; implementation and residual risk have not been verified.", "", "## Reference framework", ""]
    lines += [f"- [{title}]({url})" for title,url in SOURCES]
    return "\n".join(lines) + "\n"
