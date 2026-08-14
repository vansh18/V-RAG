from pydantic import BaseModel, Field
from typing import Literal, Optional

# ---------- Responder Schema ----------

class EvidenceReference(BaseModel):
    source: str = Field(
        description="Source filename of the retrieved document chunk."
    )

    chunk_id: int = Field(
        description="Identifier of the specific chunk within the source document."
    )


class Claim(BaseModel):
    claim_text: str = Field(
        description="A meaningful factual or legal claim made by the responder."
    )

    evidence_references: list[EvidenceReference] = Field(
        description=(
            "Retrieved document chunks that the responder relied on to support "
            "this claim. Use an empty list when no retrieved evidence supports "
            "the claim."
        )
    )


class ResponderOutput(BaseModel):
    answer: str = Field(
        description=(
            "The best answer to the user's question based only on the "
            "retrieved evidence."
        )
    )

    claims: list[Claim] = Field(
        description=(
            "The meaningful factual or legal claims made in the answer. "
            "Each claim should identify the retrieved evidence it relies on."
        )
    )

# ---------- Prosecutor Schema ----------

class ClaimRiskAssessment(BaseModel):
    claim_text: str = Field(
        description=(
            "The exact meaningful claim from the Responder's output being assessed."
        )
    )

    risk: Literal["Low", "Medium", "High"] = Field(
        description=(
            "The level of risk that the claim is unsupported, inaccurate, "
            "contradicted, or requires further verification."
        )
    )

    reason: str = Field(
        description=(
            "A concise explanation of why the claim was assigned this risk level."
        )
    )

class ProsecutorFinding(BaseModel):
    claim_text: str = Field(
        description=(
            "The specific claim from the Responder's output that was investigated."
        )
    )

    status: Literal["Supported", "Unsupported", "Contradicted", "Outdated"] = Field(
        description=(
            "The Prosecutor's assessment of the claim after examining the Responder's evidence and any additional evidence retrieved during the investigation."
        )
    )

    explanation: str = Field(
        description=(
            "A concise explanation of why the claim was assigned this status, including how the available evidence supports, fails to support, contradicts, or supersedes the claim."
        )
    )

    evidence_references: list[EvidenceReference] = Field(
        description=(
            "References to the retrieved document chunks that support the Prosecutor's finding. Include evidence from the original retrieval or from additional targeted retrieval performed during the investigation. Use an empty list when no relevant evidence was found."
        )
    )

class InvestigationRequest(BaseModel):
    claim_texts: list[str] = Field(
        description=(
            "The claims from the Responder's output that require further "
            "investigation."
        )
    )

    search_query: str = Field(
        description=(
            "A single concise search query that combines the information "
            "needed to investigate all of the identified claims."
        )
    )

class ProsecutorOutput(BaseModel):
    risk_assessments: list[ClaimRiskAssessment] = Field(
        description=(
            "Risk assessments for every claim made by the Responder. Each claim must be assessed as Low, Medium, or High risk."
        )
    )

    investigation_request: Optional[InvestigationRequest] = Field(
        default=None,
        description=(
            "Investigation requests generated for claims that the Prosecutor determines require further verification. Each request contains the claims requiring investigation and a combined search query for retrieving additional evidence."
        )
    )

    findings: list[ProsecutorFinding] = Field(
        description=(
            "Detailed findings for claims that the Prosecutor determined required further investigation. Claims that were not investigated should not appear here."
        )
    )