from agents.base_agent import BaseAgent


class CampaignAgent(BaseAgent):

    def __init__(self):
        super().__init__("Campaign Agent")

    def create_campaign(self, strategy):

        campaign = {
            "objective": strategy["marketing_goal"],
            "target_audience": strategy["target_market"],
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
            "Enquire now to explore available mirror designs."
        )

        campaign["content_ideas"].append(
            "Create a product showcase highlighting mirror designs, dimensions and delivery information."
        )

        return campaign