
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.agents.template_agent import TemplateAgent


app = FastAPI(
    title="RIVAAN AI Marketing Assistant",
    description="AI-powered marketing campaign and template generation",
    version="0.2.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


template_agent = TemplateAgent()


# -----------------------------
# REQUEST MODELS
# -----------------------------

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


# -----------------------------
# BASIC ROUTES
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to RIVAAN AI Marketing Assistant",
        "status": "running",
        "version": "0.2.0"
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
        "available_modules": [
            "Campaign Generator",
            "Template Generator"
        ]
    }


# -----------------------------
# CAMPAIGN GENERATOR
# -----------------------------

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

    product_lower = product.lower()

    profiles = {
        "mirror": {
            "concerns": [
                "Product safety during delivery",
                "Packaging protection",
                "Interior design compatibility"
            ],
            "angles": [
                "Transform your living space",
                "A stylish addition to modern interiors",
                "Discover functional design"
            ]
        },
        "air conditioner": {
            "concerns": [
                "Cooling performance",
                "Electricity consumption",
                "Installation requirements"
            ],
            "angles": [
                "Comfort for everyday living",
                "Explore cooling solutions",
                "Find comfort for your space"
            ]
        },
        "coffee": {
            "concerns": [
                "Taste preferences",
                "Product quality",
                "Convenience"
            ],
            "angles": [
                "Make your everyday coffee moment special",
                "Discover your next favorite cup",
                "Bring warmth to your routine"
            ]
        },
        "headphones": {
            "concerns": [
                "Sound quality",
                "Comfort during use",
                "Device compatibility"
            ],
            "angles": [
                "Find your sound",
                "Make every listening moment count",
                "Explore your audio experience"
            ]
        }
    }

    detected_profile = next(
        (
            key for key in profiles
            if key in product_lower
        ),
        None
    )

    profile = profiles.get(
        detected_profile,
        {
            "concerns": [
                "Product value",
                "Customer requirements",
                "Ease of use"
            ],
            "angles": [
                f"Discover {product}",
                f"Explore what {product} offers",
                "Find a solution for your needs"
            ]
        }
    )

    return {
        "status": "success",
        "product": product,
        "product_category": detected_profile or "general",
        "audience": audience,
        "goal": goal,
        "budget": request.budget,
        "research": {
            "product_category": detected_profile or "general",
            "market_context": (
                f"Marketing considerations for {product}"
            )
        },
        "insights": {
            "customer_insights": [
                f"Understand the needs of {audience}",
                f"Evaluate customer expectations for {product}"
            ],
            "pain_points": profile["concerns"],
            "competitor_insights": [
                "Compare product value propositions",
                "Review competitor messaging before launch"
            ],
            "decision_factors": [
                "Product value",
                "Customer trust",
                "Purchase convenience"
            ],
            "trends": [
                "Clear product communication",
                "Relevant audience messaging"
            ]
        },
        "strategy": {
            "marketing_goal": goal,
            "target_market": audience,
            "key_messages": profile["angles"],
            "campaign_ideas": [
                f"Create a product-focused campaign for {product}",
                "Highlight relevant customer benefits",
                "Use a clear call to action"
            ],
            "recommendations": [
                "Test different creative approaches",
                "Track engagement and conversions"
            ]
        },
        "campaign": {
            "objective": goal,
            "target_audience": audience,
            "core_message": f"Discover {product}",
            "ad_angles": profile["angles"],
            "call_to_action": "Learn More",
            "content_ideas": [
                "Product showcase",
                "Customer benefit post",
                "Promotional creative"
            ]
        },
        "decisions": {
            "status": "evaluation_completed",
            "recommendation": "Review campaign before publishing"
        },
        "note": "Prototype uses local rule-based product profiles."
    }


# -----------------------------
# TEMPLATE GENERATOR
# -----------------------------

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