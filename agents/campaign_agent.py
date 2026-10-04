from agents.base_agent import BaseAgent


class CampaignAgent(BaseAgent):

    def __init__(self):
        super().__init__("Campaign Agent")

    def build_cta(self, product, goal, market):
        goal_lower = goal.lower()
        is_service = market == "construction_services"

        if any(w in goal_lower for w in ["lead", "enquir", "inquir"]):
            return f"Enquire now about {product}."
        if "sales" in goal_lower:
            if is_service:
                return f"Get a quote for {product} today."
            return f"Shop {product} now."
        if "traffic" in goal_lower:
            return f"Visit our website to explore {product}."
        if "awareness" in goal_lower:
            return f"Discover more about {product}."
        if "engagement" in goal_lower:
            return f"Tell us what you think about {product}."

        return f"Learn more about {product}."

    def create_campaign(self, strategy):

        product = strategy.get("product", "this offering")
        market = strategy.get("matched_market", "general")
        audience = strategy["target_market"]

        campaign = {
            "product": product,
            "objective": strategy["marketing_goal"],
            "target_audience": audience,
            "core_message": [],
            "ad_angles": [],
            "call_to_action": [],
            "content_ideas": []
        }

        for message in strategy["key_messages"]:
            campaign["core_message"].append(message)

        for recommendation in strategy["recommendations"]:
            campaign["ad_angles"].append(recommendation)

        campaign["call_to_action"].append(
            self.build_cta(product, strategy["marketing_goal"], market)
        )

        campaign["content_ideas"].append(
            f"Create a showcase post that shows what {product} offers {audience}."
        )

        for idea in strategy["campaign_ideas"]:
            campaign["content_ideas"].append(idea)

        return campaign