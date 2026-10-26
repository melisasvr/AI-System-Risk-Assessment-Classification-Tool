"""Deterministic governance screening, not an EU legal classification engine."""
from app.controls import recommend_controls
from app.schemas import Assessment, Finding, PRACTICES, SystemInput, Tier

HIGH_DOMAINS = {"Hiring / employment", "Lending / essential services", "Healthcare", "Education access / assessment", "Law enforcement / justice", "Critical infrastructure"}

def assess(system: SystemInput) -> Assessment:
    findings: list[Finding] = []
    def add(key: str, reason: str, points: int) -> None:
        findings.append(Finding(rule_id=key, reason=reason, points=points))
    if system.domain in HIGH_DOMAINS and system.consequential_decisions:
        add("H01", f"Consequential decisions in {system.domain} require enhanced governance.", 35)
    if system.high_stakes:
        add("H02", "The owner reports potential serious effects on rights, health, safety or access to opportunities.", 30)
    if system.safety_component:
        add("H03", "The system is a safety component; failure may cause physical harm.", 35)
    if system.consequential_decisions:
        add("S01", "Outputs materially influence decisions about people.", 15)
    if system.data_type != "Non-personal":
        add("S02", f"Data sensitivity: {system.data_type}.", 20 if system.data_type == "Sensitive / biometric" else 10)
    if system.autonomy != "Human decides":
        add("S03", f"Decision autonomy: {system.autonomy}.", 20 if system.autonomy == "Fully autonomous" else 10)
    if system.vulnerable_people:
        add("S04", "Children or other vulnerable people may be affected.", 15)
    if system.public_facing:
        add("T01", "People interact directly with AI; transparency review is needed.", 10)
    if system.generates_content:
        add("T02", "Generated content introduces disclosure and misinformation considerations.", 10)
    for key in sorted(set(system.prohibited_practices)):
        add("P_" + key, "Potential prohibited-practice flag: " + PRACTICES[key] + ". Confirm exact legal conditions and exceptions.", 0)
    raw = sum(f.points for f in findings)
    high_floor = any(f.rule_id.startswith("H") for f in findings)
    tier = Tier.HIGH if high_floor or raw >= 60 else Tier.LIMITED if raw >= 20 or system.public_facing or system.generates_content else Tier.MINIMAL
    score = min(100, max(raw, 60 if high_floor else 20 if tier == Tier.LIMITED else 0))
    if system.prohibited_practices:
        tier, score = Tier.UNACCEPTABLE, 100
    if not findings:
        add("B01", "No elevated factors were declared in the structured answers. This is not evidence that the system is safe.", 0)
    notes = ["Provisional governance screening based on self-reported structured answers; not legal advice or compliance certification.", "The 0–100 score is a policy heuristic, not a probability of harm. Human oversight does not remove a high-stakes floor.", "EU classification requires jurisdiction, operator role, intended use, Article 6/Annex I/III conditions and exceptions. Sensitive data alone does not make a system legally high-risk.", "Free-text descriptions are documented, not semantically classified. Check them against every structured answer; contradictions are not automatically detected."]
    if not system.screening_complete:
        notes.append("INCOMPLETE: prohibited-practice screening has not been confirmed; resolve before deployment.")
    if system.eu_scope == "Unknown":
        notes.append("EU territorial scope is unknown; obtain a scope review.")
    if system.eu_scope == "No":
        notes.append("EU scope was declared absent; governance tiers still apply, while EU obligations may not.")
    return Assessment(system=system, tier=tier, score=score, raw_score=raw, findings=findings, controls=recommend_controls(system,tier), review_notes=notes)
