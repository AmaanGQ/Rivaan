
from agents.base_agent import BaseAgent


class RecommendationAgent(BaseAgent):

    def __init__(self):
        super().__init__("Recommendation Agent")

    def generate_recommendations(self, performance):

        recommendations = []

        ctr = performance["ctr_percent"]
        conversion_rate = performance["conversion_rate_percent"]

        if ctr < 2:
            recommendations.append({
                "area": "Ad Creative",
                "issue": "Low click-through rate",
                "action": "Test different headlines, product visuals and ad messaging."
            })

        if conversion_rate < 5:
            recommendations.append({
                "area": "Landing Page",
                "issue": "Low enquiry conversion",
                "action": "Review page clarity, product information and enquiry process."
            })

        if not recommendations:
            recommendations.append({
                "area": "Campaign",
                "issue": "No threshold-based issue detected",
                "action": "Continue monitoring and test new campaign variations."
            })

        return {
            "total_recommendations": len(recommendations),
            "recommendations": recommendations,
            "status": "recommendations_generated"
        }