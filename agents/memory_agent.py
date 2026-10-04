import json
from pathlib import Path

from agents.base_agent import BaseAgent


class MemoryAgent(BaseAgent):

    def __init__(self):
        super().__init__("Memory Agent")

        self.file_path = (
            Path(__file__).parent.parent
            / "data"
            / "campaign_history.json"
        )

    def load_history(self):

        if not self.file_path.exists():
            return []

        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_campaign(self, campaign_data):

        history = self.load_history()

        history.append(campaign_data)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4)

        return {
            "saved": True,
            "total_campaigns": len(history),
            "message": "Campaign saved successfully."
        }