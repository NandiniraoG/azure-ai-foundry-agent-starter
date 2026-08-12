from dataclasses import dataclass
from datetime import datetime, timezone
import os

from .responsible_ai import PolicyDecision, check_request


@dataclass(frozen=True)
class AgentResponse:
    answer: str
    policy: PolicyDecision
    deployment: str
    created_at: str


class AgentOrchestrator:
    def __init__(self, deployment: str | None = None) -> None:
        self.deployment = deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT", "local-demo")

    def run(self, user_request: str) -> AgentResponse:
        policy = check_request(user_request)
        if not policy.allowed:
            return AgentResponse(
                answer=f"Request blocked: {policy.reason}",
                policy=policy,
                deployment=self.deployment,
                created_at=self._timestamp(),
            )

        prompt = self._build_prompt(user_request)
        answer = self._call_model(prompt)

        return AgentResponse(
            answer=answer,
            policy=policy,
            deployment=self.deployment,
            created_at=self._timestamp(),
        )

    def _build_prompt(self, user_request: str) -> str:
        return (
            "You are an enterprise AI assistant. Answer with concise, grounded, "
            "auditable guidance. If information is missing, state assumptions.\n\n"
            f"User request: {user_request}"
        )

    def _call_model(self, prompt: str) -> str:
        return (
            "Demo response generated from the agent prompt. "
            f"Prompt length: {len(prompt)} characters."
        )

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).isoformat()

