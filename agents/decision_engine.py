from agents.base_agent import BaseAgent


class DecisionEngine(BaseAgent):

    def __init__(self):
        super().__init__("Decision Engine")

    def evaluate(self, campaign, insights):

        decisions = []

        for pain_point in insights["pain_points"]:

            decisions.append({
                "issue": pain_point,
                "decision": "Address customer concerns about delivery safety.",
                "reason": "The market data identifies delivery damage as a potential customer concern.",
                "recommended_action": "Include packaging and delivery information in campaign messaging."
            })

        for factor in insights["decision_factors"]:

            decisions.append({
                "issue": factor,
                "decision": "Highlight important purchase factors.",
                "reason": "These factors may influence customer purchasing decisions.",
                "recommended_action": "Include product dimensions, visuals, pricing and available reviews in campaign content."
            })

        return {
            "campaign_objective": campaign["objective"],
            "total_decisions": len(decisions),
            "decisions": decisions,
            "status": "evaluation_completed"
        }
