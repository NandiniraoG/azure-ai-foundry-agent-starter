from dataclasses import dataclass


BLOCKED_TERMS = {
    "ignore all policies",
    "exfiltrate",
    "steal credentials",
    "bypass security",
}


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str
    matched_terms: tuple[str, ...]


def check_request(text: str) -> PolicyDecision:
    normalized = text.lower()
    matches = tuple(term for term in BLOCKED_TERMS if term in normalized)

    if matches:
        return PolicyDecision(
            allowed=False,
            reason="The request appears to conflict with enterprise AI safety policy.",
            matched_terms=matches,
        )

    return PolicyDecision(
        allowed=True,
        reason="No blocking policy terms detected.",
        matched_terms=(),
    )

