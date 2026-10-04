from agents.base_agent import BaseAgent


class DecisionEngine(BaseAgent):

    def __init__(self):
        super().__init__("Decision Engine")

    def evaluate(self, campaign, insights):

        product = campaign.get("product", "the offering")
        decisions = []

        for pain_point in insights["pain_points"]:

            decisions.append({
                "issue": pain_point,
                "decision": "Address this customer concern directly in the campaign.",
                "reason": "Market research for this segment lists it as a customer concern.",
                "recommended_action": f"Add a message that shows how {product} handles this concern."
            })

        for factor in insights["decision_factors"]:

            decisions.append({
                "issue": factor,
                "decision": "Highlight the factors customers use to decide.",
                "reason": "These factors influence the purchase or hiring decision.",
                "recommended_action": f"Make these points visible in {product} content."
            })

        return {
            "campaign_objective": campaign["objective"],
            "total_decisions": len(decisions),
            "decisions": decisions,
            "status": "evaluation_completed"
        }