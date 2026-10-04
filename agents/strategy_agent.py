from agents.base_agent import BaseAgent


class StrategyAgent(BaseAgent):

    def __init__(self):
        super().__init__("Strategy Agent")

    def create_strategy(self, research_result):

        strategy = {
            "marketing_goal": research_result["marketing_goal"],
            "target_market": research_result["target_market"],
            "key_messages": [],
            "campaign_ideas": [],
            "recommendations": []
        }

        insights = research_result["insights"]

        for pain_point in insights["pain_points"]:
            strategy["key_messages"].append(
                f"Address customer concern: {pain_point}"
            )

        for factor in insights["decision_factors"]:
            strategy["recommendations"].append(
                f"Highlight: {factor}"
            )

        for trend in insights["trends"]:
            strategy["campaign_ideas"].append(
                f"Use this market trend: {trend}"
            )

        return strategy