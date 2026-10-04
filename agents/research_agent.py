import json
from pathlib import Path

from agents.base_agent import BaseAgent
from agents.insight_engine import InsightEngine


class ResearchAgent(BaseAgent):

    def __init__(self):
        super().__init__("Research Agent")
        self.insight_engine = InsightEngine()

    def load_market_data(self):
        file_path = Path(__file__).parent.parent / "data" / "market_data.json"

        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def research(self, product, target_market, goal):

        research_questions = [
            f"Who are the main customers for {product}?",
            f"What problems do customers have with {product}?",
            f"Who are the main competitors in {target_market}?",
            f"What alternatives do customers currently use?",
            f"What factors influence customers when choosing {product}?",
            f"What trends are affecting the {product} market?"
        ]

        market_data = self.load_market_data()

        insights = self.insight_engine.analyze(market_data)

        return {
            "product": product,
            "target_market": target_market,
            "marketing_goal": goal,
            "research_questions": research_questions,
            "market_data": market_data,
            "insights": insights,
            "status": "research_completed"
        }