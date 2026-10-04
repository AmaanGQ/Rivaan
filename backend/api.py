from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.template_agent import TemplateAgent
from agents.research_agent import ResearchAgent
from agents.strategy_agent import StrategyAgent
from agents.campaign_agent import CampaignAgent
from agents.decision_engine import DecisionEngine


# =====================================
# RIVAAN APPLICATION
# =====================================

app = FastAPI(
    title="RIVAAN AI Marketing Assistant",
    description="Rule-based marketing intelligence and creative generation",
    version="0.4.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

template_agent = TemplateAgent()
research_agent = ResearchAgent()
strategy_agent = StrategyAgent()
campaign_agent = CampaignAgent()
decision_engine = DecisionEngine()


# =====================================
# REQUEST MODELS
# =====================================

class CampaignRequest(BaseModel):
    product_name: str
    target_audience: str
    marketing_goal: str
    budget: float = 0


class TemplateRequest(BaseModel):
    product_name: str
    product_description: str = ""
    target_audience: str
    marketing_goal: str
    platform: str = "instagram_post"
    design_style: str = "modern"


# =====================================
# BASIC ROUTES
# =====================================

@app.get("/")
def home():
    return {
        "message": "Welcome to RIVAAN AI Marketing Assistant",
        "status": "running",
        "version": "0.4.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "RIVAAN Backend"
    }


@app.get("/dashboard")
def dashboard():
    return {
        "message": "RIVAAN Dashboard API",
        "modules": [
            "Campaign Generator",
            "Template Generator",
            "Research Agent",
            "Strategy Agent",
            "Decision Engine"
        ]
    }


# =====================================
# CAMPAIGN GENERATOR (agent pipeline)
# =====================================

@app.post("/generate-campaign")
def generate_campaign(request: CampaignRequest):

    product = request.product_name.strip()
    audience = request.target_audience.strip()
    goal = request.marketing_goal.strip()

    if not product or not audience or not goal:
        raise HTTPException(
            status_code=400,
            detail="Product, audience and marketing goal are required"
        )

    try:
        # Step 1: Research
        research = research_agent.research(product, audience, goal)

        # Step 2: Strategy
        strategy = strategy_agent.create_strategy(research)

        # Step 3: Campaign
        campaign = campaign_agent.create_campaign(strategy)

        # Step 4: Decisions
        decisions = decision_engine.evaluate(campaign, research["insights"])

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Campaign generation failed: {str(error)}"
        )

    matched_market = research["matched_market"]

    # Keep the same response shape the dashboard already expects
    core_messages = campaign["core_message"]
    ctas = campaign["call_to_action"]

    return {
        "status": "success",
        "product": product,
        "product_category": matched_market,
        "audience": audience,
        "goal": goal,
        "budget": request.budget,

        "research": {
            "product_category": matched_market,
            "market_context": f"Marketing considerations for {product}"
        },

        "insights": research["insights"],

        "strategy": {
            "marketing_goal": strategy["marketing_goal"],
            "target_market": strategy["target_market"],
            "key_messages": strategy["key_messages"],
            "campaign_ideas": strategy["campaign_ideas"],
            "recommendations": strategy["recommendations"]
        },

        "campaign": {
            "objective": campaign["objective"],
            "target_audience": campaign["target_audience"],
            "core_message": core_messages[0] if core_messages else f"Discover {product}",
            "ad_angles": campaign["ad_angles"],
            "call_to_action": ctas[0] if ctas else "Learn More",
            "content_ideas": campaign["content_ideas"]
        },

        "decisions": {
            "status": decisions["status"],
            "total_decisions": decisions["total_decisions"],
            "recommendation": "Review campaign before publishing",
            "decisions": decisions["decisions"]
        },

        "note": "Rule-based agent pipeline: Research, Strategy, Campaign, Decision."
    }


# =====================================
# TEMPLATE GENERATOR
# =====================================

@app.post("/generate-template")
def generate_template(request: TemplateRequest):

    try:
        result = template_agent.generate_template(
            product_name=request.product_name,
            product_description=request.product_description,
            target_audience=request.target_audience,
            marketing_goal=request.marketing_goal,
            platform=request.platform,
            design_style=request.design_style
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Template generation failed: {str(error)}"
        )