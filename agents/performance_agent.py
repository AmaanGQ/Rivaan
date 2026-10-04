
from agents.base_agent import BaseAgent


class PerformanceAgent(BaseAgent):

    def __init__(self):
        super().__init__("Performance Agent")

    def evaluate(self, metrics):

        impressions = metrics["impressions"]
        clicks = metrics["clicks"]
        enquiries = metrics["enquiries"]

        ctr = (clicks / impressions * 100) if impressions > 0 else 0

        conversion_rate = (
            enquiries / clicks * 100
            if clicks > 0 else 0
        )

        observations = []

        if ctr < 2:
            observations.append(
                "CTR is below the illustrative demo threshold. Review ad messaging and creative."
            )
        else:
            observations.append(
                "CTR meets the illustrative demo threshold."
            )

        if conversion_rate < 5:
            observations.append(
                "Enquiry conversion is below the illustrative demo threshold. Review the landing page and enquiry process."
            )
        else:
            observations.append(
                "Enquiry conversion meets the illustrative demo threshold."
            )

        return {
            "impressions": impressions,
            "clicks": clicks,
            "enquiries": enquiries,
            "ctr_percent": round(ctr, 2),
            "conversion_rate_percent": round(conversion_rate, 2),
            "observations": observations,
            "status": "evaluation_completed"
        }