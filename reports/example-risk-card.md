# AI System Risk Card

## Candidate ranking assistant

**Tier:** High Risk · **Governance score:** 70/100

Assessment ID: 99ef3d84-7566-43cd-8eec-96d363d510a1  
Created (UTC): 2026-10-25T22:45:02.369952+00:00  
Engine: 1.0.0 · Status: Provisional / owner review required

## System profile

**Name:** Candidate ranking assistant

**Owner:** Demo governance team

**Purpose:** Rank job applicants by job-relevant evidence to support recruiter shortlisting decisions.

**Data Description:** Applicant CVs, employment history and job-relevant assessment results.

**Affected People:** Job applicants and recruiting staff.

**Domain:** Hiring / employment

**Data Type:** Personal

**Autonomy:** Human approves

**High Stakes:** False

**Vulnerable People:** False

**Public Facing:** False

**Generates Content:** False

**Consequential Decisions:** True

**Safety Component:** False

**Prohibited Practices:** \[\]

**Screening Complete:** True

**Eu Scope:** Unknown

**Limitations:** 

## Classification rationale

- **H01** (+35): Consequential decisions in Hiring / employment require enhanced governance.
- **S01** (+15): Outputs materially influence decisions about people.
- **S02** (+10): Data sensitivity: Personal.
- **S03** (+10): Decision autonomy: Human approves.

Raw points: 70. Final score: 70. Floors: High=60; transparency/limited=20; prohibited-practice override=100. Raw scores are capped at 100. Thresholds: Minimal <20, Limited 20–59, High ≥60; overrides take precedence.

## Recommended controls

### Accountability
Assign an accountable owner; document intended and excluded uses and review after material changes.

**Owner:** System owner · **Due:** Before deployment  
**Evidence:** Approved system inventory and change log

### Evaluation
Test representative cases and failure modes before release; define acceptance criteria.

**Owner:** Engineering lead · **Due:** Before deployment  
**Evidence:** Versioned test results and release decision

### Monitoring
Track errors, complaints and drift; define incident response and rollback thresholds.

**Owner:** Operations lead · **Due:** Before deployment  
**Evidence:** Monitoring plan and incident register

### Data protection
Minimise data, set retention and access controls; ask a privacy lead to assess lawful basis and DPIA necessity.

**Owner:** Privacy lead · **Due:** Before deployment  
**Evidence:** Data inventory, retention policy and privacy assessment

### Human oversight
Give trained reviewers authority to challenge, override and stop outputs; offer affected people a review route.

**Owner:** Governance lead · **Due:** Before deployment  
**Evidence:** Oversight procedure and reviewer training

### Fairness and robustness
Evaluate subgroup performance where lawful and appropriate, security threats, edge cases and harmful failure modes.

**Owner:** ML lead · **Due:** Before deployment  
**Evidence:** Disaggregated evaluation and security test report

### Traceability and approval
Keep proportionate decision logs and technical documentation; require independent governance approval before release.

**Owner:** Risk committee · **Due:** Before deployment  
**Evidence:** Risk register, technical file and approval record

## Limitations and review

- Provisional governance screening based on self-reported structured answers; not legal advice or compliance certification.
- The 0–100 score is a policy heuristic, not a probability of harm. Human oversight does not remove a high-stakes floor.
- EU classification requires jurisdiction, operator role, intended use, Article 6/Annex I/III conditions and exceptions. Sensitive data alone does not make a system legally high-risk.
- Free-text descriptions are documented, not semantically classified. Check them against every structured answer; contradictions are not automatically detected.
- EU territorial scope is unknown; obtain a scope review.

## Approval record

Reviewer: __________  Review date: __________  Decision: __________

Controls are recommendations; implementation and residual risk have not been verified.

## Reference framework

- [EU AI Act — official text (verify current consolidated version)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)
- [European Commission — regulatory framework](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
