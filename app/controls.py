"""Actionable controls; recommendations do not demonstrate compliance."""
from app.schemas import Control, SystemInput, Tier

def recommend_controls(system: SystemInput, tier: Tier) -> list[Control]:
    rows = [
        ("Accountability", "Assign an accountable owner; document intended and excluded uses and review after material changes.", "System owner", "Approved system inventory and change log"),
        ("Evaluation", "Test representative cases and failure modes before release; define acceptance criteria.", "Engineering lead", "Versioned test results and release decision"),
        ("Monitoring", "Track errors, complaints and drift; define incident response and rollback thresholds.", "Operations lead", "Monitoring plan and incident register"),
    ]
    if system.data_type != "Non-personal":
        rows.append(("Data protection", "Minimise data, set retention and access controls; ask a privacy lead to assess lawful basis and DPIA necessity.", "Privacy lead", "Data inventory, retention policy and privacy assessment"))
    if system.public_facing or system.generates_content:
        rows.append(("Transparency", "Provide clear AI interaction or generated-content notices where applicable, explain limitations and offer escalation.", "Product owner", "Notice screenshots and escalation procedure"))
    if tier in (Tier.HIGH, Tier.UNACCEPTABLE):
        rows.extend([
            ("Human oversight", "Give trained reviewers authority to challenge, override and stop outputs; offer affected people a review route.", "Governance lead", "Oversight procedure and reviewer training"),
            ("Fairness and robustness", "Evaluate subgroup performance where lawful and appropriate, security threats, edge cases and harmful failure modes.", "ML lead", "Disaggregated evaluation and security test report"),
            ("Traceability and approval", "Keep proportionate decision logs and technical documentation; require independent governance approval before release.", "Risk committee", "Risk register, technical file and approval record"),
        ])
    if tier == Tier.UNACCEPTABLE:
        rows.insert(0, ("Stop and review", "Pause the flagged use. Obtain specialist review of scope, legal conditions and exceptions; redesign or abandon prohibited functionality.", "Legal and executive owner", "Written legal review and documented go/no-go decision"))
    return [Control(title=t, action=a, owner=o, evidence=e) for t,a,o,e in rows]
