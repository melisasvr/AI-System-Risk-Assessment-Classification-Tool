"""Validated inputs and auditable assessment records."""
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
from pydantic import BaseModel, ConfigDict, Field, model_validator

class Tier(str, Enum):
    MINIMAL = "Minimal Risk"
    LIMITED = "Limited Risk"
    HIGH = "High Risk"
    UNACCEPTABLE = "Unacceptable Risk"

DOMAINS = ["Internal productivity", "Customer support", "Content moderation", "Hiring / employment", "Lending / essential services", "Healthcare", "Education access / assessment", "Law enforcement / justice", "Critical infrastructure", "Other"]
PRACTICES = {
    "manipulation": "Manipulation or deception likely to cause significant harm",
    "exploitation": "Exploiting vulnerabilities likely to cause significant harm",
    "social_scoring": "Social scoring causing unrelated or disproportionate detrimental treatment",
    "crime_profiling": "Predicting individual criminal offending solely from profiling or personality",
    "face_scraping": "Untargeted internet or CCTV scraping to build facial recognition databases",
    "emotion": "Emotion inference in workplaces or education outside medical/safety exceptions",
    "biometric": "Biometric inference of protected sensitive characteristics",
    "remote_id": "Real-time remote biometric identification for law enforcement in public spaces",
    "intimate": "Generating non-consensual intimate imagery or child sexual abuse material",
}
class SystemInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=3, max_length=120)
    owner: str = Field(min_length=2, max_length=120)
    purpose: str = Field(min_length=30, max_length=5000)
    data_description: str = Field(min_length=10, max_length=3000)
    affected_people: str = Field(min_length=10, max_length=2000)
    domain: str
    data_type: str = "Non-personal"
    autonomy: str = "Human decides"
    high_stakes: bool = False
    vulnerable_people: bool = False
    public_facing: bool = False
    generates_content: bool = False
    consequential_decisions: bool = False
    safety_component: bool = False
    prohibited_practices: list[str] = Field(default_factory=list)
    screening_complete: bool = False
    eu_scope: str = "Unknown"
    limitations: str = Field(default="", max_length=3000)

    @model_validator(mode="after")
    def validate_choices(self) -> "SystemInput":
        choices = {"domain": DOMAINS, "data_type": ["Non-personal", "Personal", "Sensitive / biometric"], "autonomy": ["Human decides", "Human approves", "Fully autonomous"], "eu_scope": ["Yes", "No", "Unknown"]}
        for field, allowed in choices.items():
            if getattr(self, field) not in allowed:
                raise ValueError(f"Invalid {field}")
        if set(self.prohibited_practices) - PRACTICES.keys():
            raise ValueError("Unknown prohibited practice identifier")
        return self

class Finding(BaseModel):
    rule_id: str
    reason: str
    points: int = 0

class Control(BaseModel):
    title: str
    action: str
    owner: str
    evidence: str
    priority: str = "Before deployment"

class Assessment(BaseModel):
    assessment_id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    engine_version: str = "1.0.0"
    system: SystemInput
    tier: Tier
    score: int = Field(ge=0, le=100)
    raw_score: int
    findings: list[Finding]
    controls: list[Control]
    review_notes: list[str]
