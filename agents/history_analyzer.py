
from agents.base_agent import BaseAgent


class HistoryAnalyzer(BaseAgent):

    def __init__(self):
        super().__init__("History Analyzer")

    def analyze_history(self, campaign_history):

        if len(campaign_history) == 0:
            return {
                "total_campaigns": 0,
                "message": "No previous campaigns found.",
                "status": "analysis_completed"
            }

        total_campaigns = len(campaign_history)

        total_impressions = 0
        total_clicks = 0
        total_enquiries = 0

        for record in campaign_history:

            performance = record.get("performance", {})

            total_impressions += performance.get("impressions", 0)
            total_clicks += performance.get("clicks", 0)
            total_enquiries += performance.get("enquiries", 0)

        overall_ctr = (
            total_clicks / total_impressions * 100
            if total_impressions > 0 else 0
        )

        overall_conversion = (
            total_enquiries / total_clicks * 100
            if total_clicks > 0 else 0
        )

        return {
            "total_campaigns": total_campaigns,
            "total_impressions": total_impressions,
            "total_clicks": total_clicks,
            "total_enquiries": total_enquiries,
            "overall_ctr_percent": round(overall_ctr, 2),
            "overall_conversion_percent": round(overall_conversion, 2),
            "status": "analysis_completed"
        }