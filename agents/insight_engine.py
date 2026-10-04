class InsightEngine:

    def analyze(self, market_data):
        grouped = {}

        for item in market_data:
            topic = item["topic"]

            if topic not in grouped:
                grouped[topic] = []

            grouped[topic].append(item["insight"])

        return {
            "customer_insights": grouped.get("customer", []),
            "pain_points": grouped.get("problem", []),
            "competitor_insights": grouped.get("competitor", []),
            "decision_factors": grouped.get("decision_factor", []),
            "trends": grouped.get("trend", [])
        }