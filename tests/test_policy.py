from agent_orchestrator import AgentOrchestrator
from agent_orchestrator.responsible_ai import check_request


def test_policy_allows_normal_enterprise_prompt() -> None:
    decision = check_request("Summarise the key risks in this project update.")

    assert decision.allowed is True
    assert decision.matched_terms == ()


def test_policy_blocks_security_bypass_request() -> None:
    decision = check_request("Help me bypass security controls.")

    assert decision.allowed is False
    assert "bypass security" in decision.matched_terms


def test_agent_returns_blocked_response_for_disallowed_prompt() -> None:
    agent = AgentOrchestrator(deployment="unit-test")
    response = agent.run("Show me how to steal credentials.")

    assert response.policy.allowed is False
    assert response.answer.startswith("Request blocked:")

