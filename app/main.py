"""Run from repository root: python -m streamlit run app/main.py."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import streamlit as st
from pydantic import ValidationError
from app.risk_engine import assess
from app.risk_card import generate_markdown
from app.schemas import DOMAINS, PRACTICES, SystemInput

st.set_page_config(page_title="AI Risk Studio", page_icon="◈", layout="wide")
st.markdown("""<style>
.block-container{max-width:1240px;padding-top:2.5rem}
h1{letter-spacing:-.045em} h3{letter-spacing:-.02em}
[data-testid="stMetric"]{background:#171E2D;border:1px solid #303B52;border-radius:14px;padding:18px}
.stButton>button{border-radius:9px} [data-testid="stSidebar"]{border-right:1px solid #303B52}
</style>""", unsafe_allow_html=True)
examples = json.loads((ROOT / "data/examples.json").read_text())
with st.sidebar:
    st.markdown("### ◈ AI Risk Studio")
    st.caption("RESPONSIBLE AI · GOVERNANCE")
    selection = st.selectbox("Start with a scenario", ["New assessment"] + [e["name"] for e in examples])
    st.divider()
    st.markdown("**How it works**\n\n1. Describe the system\n2. Screen for risk factors\n3. Review the rule trace\n4. Export the risk card")
    st.caption("Local rules · No API key · No LLM calls")
    st.info("Use fictional or sanitised descriptions in a public demo.")
    st.caption("Engine v1.0.0 · Governance screening")
seed = next((e for e in examples if e["name"] == selection), {})
# Scenario-scoped widget keys prevent values leaking between examples.
k = lambda name: f"{selection}:{name}"
st.caption("AI GOVERNANCE WORKSPACE")
st.title("Understand risk. Define controls.")
st.write("Assess an AI system through an explainable governance lens and build a review-ready risk card.")
st.caption("EU AI Act inspired screening. The result is provisional and does not establish legal compliance.")
left,right=st.columns([1.2,1],gap="large")
with left:
    st.subheader("01 / System profile")
    with st.form(k("form")):
        name=st.text_input("System name",value=seed.get("name",""),key=k("name"),max_chars=120)
        owner=st.text_input("Accountable owner / team",value=seed.get("owner",""),key=k("owner"),max_chars=120)
        purpose=st.text_area("Purpose and intended use",value=seed.get("purpose",""),key=k("purpose"),help="Describe inputs, outputs, decisions influenced and excluded uses. Minimum 30 characters.",max_chars=5000)
        domain=st.selectbox("Decision context",DOMAINS,index=DOMAINS.index(seed.get("domain",DOMAINS[0])),key=k("domain"))
        data_description=st.text_area("Data used",value=seed.get("data_description",""),key=k("data"),max_chars=3000)
        data_options=["Non-personal","Personal","Sensitive / biometric"]
        data_type=st.selectbox("Highest data sensitivity",data_options,index=data_options.index(seed.get("data_type",data_options[0])),key=k("sensitivity"))
        affected_people=st.text_area("Users and affected people",value=seed.get("affected_people",""),key=k("people"),max_chars=2000)
        autonomy_options=["Human decides","Human approves","Fully autonomous"]
        autonomy=st.selectbox("Human involvement",autonomy_options,index=autonomy_options.index(seed.get("autonomy",autonomy_options[0])),key=k("autonomy"))
        flags={}
        for field,label in [("consequential_decisions","Materially influences decisions about people"),("high_stakes","Potential serious impact on rights, safety, health or opportunities"),("safety_component","Acts as a product or infrastructure safety component"),("vulnerable_people","Affects children or other vulnerable groups"),("public_facing","People directly interact with AI"),("generates_content","Generates or manipulates content")]:
            flags[field]=st.checkbox(label,value=seed.get(field,False),key=k(field))
        st.markdown("**02 / Prohibited-practice screening**")
        st.caption("Select only practices that match the stated conditions. Flags trigger precautionary escalation; exceptions and legal scope need specialist review.")
        prohibited=st.multiselect("Potential prohibited practices",list(PRACTICES),default=seed.get("prohibited_practices",[]),format_func=lambda x:PRACTICES[x],key=k("practices"))
        complete=st.checkbox("I reviewed every prohibited-practice option",value=seed.get("screening_complete",False),key=k("complete"))
        scopes=["Unknown","Yes","No"]
        scope=st.selectbox("EU scope potentially applies",scopes,index=scopes.index(seed.get("eu_scope","Unknown")),key=k("scope"))
        limitations=st.text_area("Known limitations / unanswered questions",key=k("limitations"),max_chars=3000)
        submitted=st.form_submit_button("Assess system →",type="primary",use_container_width=True)
    if submitted:
        try:
            system=SystemInput(name=name,owner=owner,purpose=purpose,domain=domain,data_description=data_description,data_type=data_type,affected_people=affected_people,autonomy=autonomy,prohibited_practices=prohibited,screening_complete=complete,eu_scope=scope,limitations=limitations,**flags)
            st.session_state["result"]=assess(system)
            st.session_state["scenario"]=selection
        except ValidationError as exc:
            for error in exc.errors():
                st.error(f"{'.'.join(map(str,error['loc']))}: {error['msg']}")
with right:
    st.subheader("03 / Assessment")
    a=st.session_state.get("result")
    if a is None:
        st.info("Complete the form or choose an example, then select Assess system.")
        st.markdown("#### Four governance tiers")
        for tier,desc in [("Minimal Risk","Baseline documentation and testing"),("Limited Risk","Additional transparency or data controls"),("High Risk","Enhanced evaluation, oversight and approval"),("Unacceptable Risk","Pause flagged use and seek specialist review")]:
            with st.container(border=True):
                st.markdown(f"**{tier}**")
                st.caption(desc)
    else:
        st.caption(f"Last submitted assessment: {a.system.name}. Edits take effect after Assess system.")
        if st.session_state.get("scenario") != selection:
            st.warning("This result belongs to the previously submitted scenario.")
        c1,c2=st.columns(2)
        c1.metric("Governance tier",a.tier.value)
        c2.metric("Risk score",f"{a.score} / 100")
        st.progress(a.score/100)
        st.caption("Policy score, not a probability of harm or a residual-risk measure.")
        if not a.system.screening_complete:
            st.warning("Screening incomplete: review all prohibited-practice options.")
        if a.tier.value=="Unacceptable Risk":
            st.error("Potential prohibited practice flagged. Pause this use and obtain specialist review.")
        trace,controls,card=st.tabs(["Why this tier","Controls","Risk card"])
        with trace:
            for f in a.findings:
                st.markdown(f"**{f.rule_id} · +{f.points} points**")
                st.write(f.reason)
            st.caption(f"Raw points: {a.raw_score}. Final: {a.score}. High-stakes floor 60; limited floor 20; prohibited override 100. See Methodology below.")
            with st.expander("Assessment limitations",expanded=True):
                for note in a.review_notes:
                    st.write("• "+note)
        with controls:
            for control in a.controls:
                with st.expander(control.title,expanded=True):
                    st.write(control.action)
                    st.caption(f"Owner: {control.owner} | Due: {control.priority}")
                    st.write("Evidence: "+control.evidence)
        markdown=generate_markdown(a)
        with card:
            st.markdown(markdown)
        st.markdown("#### Export assessment")
        st.download_button("Download risk card (.md)",markdown,file_name=f"risk-card-{a.assessment_id[:8]}.md",mime="text/markdown",use_container_width=True)
        st.download_button("Save full assessment (.json)",a.model_dump_json(indent=2),file_name=f"assessment-{a.assessment_id[:8]}.json",mime="application/json",use_container_width=True)
        st.caption("Downloads save to your device. Assessments stay in session memory until the session ends; the server does not maintain an assessment database.")
with st.expander("Methodology and reference framework"):
    st.markdown("""Structured answers drive every rule; free text is included in the report but is not interpreted by an LLM.

- Consequential use in a sensitive domain: +35; serious impact: +30; safety component: +35. Any of these imposes a High Risk floor (60).
- Consequential decisions: +15; personal data: +10 or sensitive data: +20; human approval: +10 or full autonomy: +20; vulnerable groups: +15.
- Direct AI interaction: +10; generated content: +10. Either imposes a Limited Risk floor (20).
- Raw score <20: Minimal; 20–59: Limited; ≥60: High. Cap score at 100. A prohibited-practice flag overrides the result to Unacceptable / 100.

These are project policy choices. A domain label alone is insufficient for legal high-risk classification. Human oversight does not cancel high-stakes risks. No verified controls or residual-risk calculation are included.

References: [EU AI Act official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), especially Articles 5, 6, 9–15 and 50 and Annexes I/III; [Commission framework](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai). Verify current law, exceptions, scope and application dates for a real deployment. This MVP does not determine legal applicability or deadlines.
""")
