# AI System Risk Assessment & Classification Tool

An explainable AI governance portfolio project built with **Python, Streamlit and Pydantic**. Describe a system, review a transparent risk assessment, and download a professional Markdown risk card or a full JSON assessment.

## Features

- Dark interface with guided system profile and prohibited-practice screening
- Four provisional governance tiers: Minimal, Limited, High and Unacceptable Risk
- Deterministic, versioned rules with individual point contributions and tier overrides
- Actionable controls with suggested owners, due dates and required evidence
- Markdown risk cards with assessment IDs, UTC timestamps, complete inputs and approval fields
- JSON export for saving the complete assessment
- Four built-in examples; no API keys, model downloads or external inference services

## Quick start

Use Python **3.11–3.13** (3.12 recommended).

```bash
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Then, from the project root:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app/main.py
```

Open the local URL printed by Streamlit. Choose an example or fill in the form, review all prohibited-practice options, and click **Assess system**. Edits do not replace the last submitted assessment until resubmission. Download Markdown or JSON to keep a record.

## Project structure

```text
ai-risk-assessment/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── risk_engine.py
│   ├── controls.py
│   └── risk_card.py
├── .streamlit/config.toml
├── data/examples.json
├── reports/example-risk-card.md
├── tests/test_risk_engine.py
├── tests/test_app.py
├── requirements.txt
└── README.md
```

## Classification methodology

This is **inherent governance screening**, based on self-reported structured answers. Free text is preserved in the card but is not interpreted or checked for contradictions. It is not a legal applicability engine, compliance certificate, probability estimate or residual-risk calculation.

| Rule | Points | Override |
| --- | ---: | --- |
| Consequential decisions in a sensitive domain | 35 | High floor |
| Owner declares serious impact | 30 | High floor |
| Safety component | 35 | High floor |
| Consequential decisions about people | 15 | — |
| Personal / sensitive data | 10 / 20 | — |
| Human approval / full autonomy | 10 / 20 | — |
| Vulnerable affected groups | 15 | — |
| Direct AI interaction | 10 | Limited floor |
| Generated or manipulated content | 10 | Limited floor |
| Potential prohibited-practice flag | 0 | Unacceptable / 100 |

Raw points are summed. Below 20 is Minimal, 20–59 is Limited, and 60 or above is High. High floors set a minimum score of 60; Limited floors set 20. Scores are capped at 100. A prohibited-practice flag takes precedence and sets 100. High scores without a prohibited flag remain High. Duplicate prohibited flags are counted once.

Sensitive domains include hiring, lending/essential services, healthcare, education access/assessment, law enforcement/justice and critical infrastructure. A domain alone does not trigger High: the consequential-decision flag must also be selected, or another high-floor rule must apply. This deliberately simplified policy can understate risk when answers are incomplete; independent review is essential. Human oversight never cancels a high floor.

Incomplete prohibited-practice screening is prominently marked, while the result stays provisional. “Unacceptable” means precautionary escalation of a declared potentially prohibited practice, not a definitive finding of illegality. Each practice has specific legal conditions and may have exceptions. The screening list is not exhaustive and does not encode application dates.

These thresholds and weights are project policy choices, not thresholds supplied by the EU AI Act. EU transparency obligations can coexist with high-risk obligations; this MVP uses one overall tier while recommending controls for all declared factors.

## Example assessments

| Example | Result | Score | Why |
| --- | --- | ---: | --- |
| Documentation organiser | Minimal Risk | 0 | No elevated factors declared |
| Customer support assistant | Limited Risk | 30 | Personal data, direct interaction, generated content |
| Candidate ranking assistant | High Risk | 70 | Consequential employment use, personal data and human approval |
| Workplace emotion surveillance | Unacceptable Risk | 100 | Workplace emotion-inference flag outside medical/safety exceptions |

## Verify

```bash
python -m unittest discover -s tests -v
```

The tests cover example tiers, floors, overrides, score caps, invalid inputs, incomplete screening, JSON round trips, risk-card traceability and Streamlit form submission/download rendering.

## Deployment on Streamlit Community Cloud

Push this folder's contents to your GitHub repository. Select `app/main.py` as the main file and **Python 3.12** in advanced settings. Dependencies install from `requirements.txt`; the theme is in `.streamlit/config.toml`. No secrets are needed. Runtime dependency ranges are bounded but not a reproducible lockfile; freeze a tested environment for production use.

## Data and reporting

The application does not intentionally send assessments to third-party AI APIs or write them to server-side report files. Inputs/results live in Streamlit session memory; downloads are saved by the user's browser. Hosting infrastructure still processes the submitted data. Do not enter confidential or identifiable data into a public demo.

The reports directory contains a generated example card. JSON export saves the full assessment, but JSON import and persistent multi-user storage are not part of this MVP. Markdown is the supported report format; PDF export is a future enhancement.

## Framework and limits

Inspired by [Regulation (EU) 2024/1689 — official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), particularly Articles 5, 6, 9–15, 50 and Annexes I/III, and the [European Commission regulatory framework](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai).

For actual deployment, verify the current consolidated law, territorial scope, provider/deployer role, intended use, exceptions and application dates with qualified reviewers. This version does not determine whether a product is an AI system under the Act, whether an Annex I conformity pathway applies, or whether an Article 6 exception applies. It does not replace privacy, security, sectoral or fundamental-rights assessment. Controls are recommendations; no implementation evidence or legal compliance is verified.

## Potential extensions
- PDF rendering from the existing Markdown report
- Versioned assessments, reviewer sign-off and evidence attachments
- Separate inherent and residual risk after control verification
- Broader jurisdiction and role-specific screening
- Evaluation dataset reviewed by AI governance specialists

## Contributing
- Contributions are welcome! You can help improve the tool by reporting bugs,
suggesting features, refining governance controls, or adding example assessments.

### Report bugs or suggest improvements
- Open a GitHub issue describing:
- The problem or proposed improvement
- Steps to reproduce the issue, if applicable
- Expected and actual behaviour
- Screenshots or fictional example inputs, where helpful

- Do not include personal data, confidential system descriptions, or credentials.

### Submit a pull request
1. Fork the repository.
2. Create a branch for your change:
   ```
   git checkout -b feature/your-improvement
3. Make your changes using clear code and type hints.
4. Run the test suite from the project root:
- `python -m unittest discover -s tests -v`
5. Update tests and documentation when your change affects behaviour.
6. Open a pull request explaining what changed, why, and how you tested it.

## License
- This project is licensed under the MIT License.
- MIT License
```
Copyright (c) 2026 Melisa Sever

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```