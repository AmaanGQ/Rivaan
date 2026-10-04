
class TemplateAgent:

    def __init__(self):
        self.platform_sizes = {
            "instagram_post": "1080x1080",
            "instagram_story": "1080x1920",
            "instagram_carousel": "1080x1080"
        }

        self.style_profiles = {
            "minimal": {
                "colors": ["#F8FAFC", "#1E293B", "#64748B"],
                "layout": {
                    "top": "Small brand name with generous spacing",
                    "center": "Large clear headline with one dominant visual",
                    "bottom": "Short supporting copy and subtle CTA"
                },
                "direction": "Minimal editorial composition, generous whitespace, restrained typography and a single focal point"
            },
            "bold": {
                "colors": ["#111827", "#F97316", "#FFFFFF"],
                "layout": {
                    "top": "Prominent brand name and campaign label",
                    "center": "Large high-impact headline with dominant visual",
                    "bottom": "Strong benefit statement and high-contrast CTA"
                },
                "direction": "Bold commercial composition, strong contrast, large typography and energetic visual hierarchy"
            },
            "premium": {
                "colors": ["#172033", "#C6A875", "#F8F5EF"],
                "layout": {
                    "top": "Discreet brand identity",
                    "center": "Elegant headline with refined hero visual",
                    "bottom": "Concise benefit copy and understated CTA"
                },
                "direction": "Premium editorial composition, refined spacing, elegant typography and sophisticated product or service imagery"
            }
        }

    def generate_template(
        self,
        product_name,
        product_description,
        target_audience,
        marketing_goal,
        platform="instagram_post",
        design_style="modern"
    ):

        product = (product_name or "").strip()
        description = (product_description or "").strip()
        audience = (target_audience or "").strip()
        goal = (marketing_goal or "").strip()

        if not product:
            raise ValueError("Product name is required")

        if platform not in self.platform_sizes:
            platform = "instagram_post"

        style_key = (design_style or "modern").strip().lower()

        style_aliases = {
            "modern": "minimal",
            "clean": "minimal",
            "minimal": "minimal",
            "bold": "bold",
            "vibrant": "bold",
            "premium": "premium",
            "luxury": "premium"
        }

        style_key = style_aliases.get(style_key, "minimal")
        style = self.style_profiles[style_key]

        product_lower = product.lower()
        description_lower = description.lower()
        combined = f"{product_lower} {description_lower}"

        service_keywords = [
            "service",
            "core cutting",
            "core cut",
            "wall cutting",
            "drilling",
            "construction",
            "contractor",
            "fabrication",
            "installation",
            "repair",
            "plumbing",
            "electrical",
            "civil work",
            "builder"
        ]

        is_service = any(
            keyword in combined
            for keyword in service_keywords
        )

        if is_service:
            profile = {
                "headline": f"Precision {product}",
                "benefit": (
                    description
                    if description
                    else "Professional solutions delivered with precision and care"
                ),
                "visual": (
                    f"Professional real-world photography showing {product}, "
                    "the work process, equipment and completed result"
                ),
                "cta": "Get a Quote"
            }

        else:
            profiles = {
                "mirror": {
                    "headline": f"Reflect Your Style with {product}",
                    "benefit": "A stylish addition to your living space",
                    "visual": "Premium mirror photography in an elegant interior",
                    "cta": "Explore the Collection"
                },
                "air conditioner": {
                    "headline": f"Comfort Starts with {product}",
                    "benefit": "Comfort-focused cooling for your space",
                    "visual": "Modern home interior with a clear product focus",
                    "cta": "Discover More"
                },
                "coffee": {
                    "headline": f"Make Every Moment Better with {product}",
                    "benefit": "Bring a little more enjoyment to your routine",
                    "visual": "Warm coffee photography with natural textures",
                    "cta": "Try It Today"
                },
                "headphones": {
                    "headline": f"Find Your Sound with {product}",
                    "benefit": "Designed for your everyday listening",
                    "visual": "Minimal product photography with a music-inspired background",
                    "cta": "Explore Now"
                }
            }

            profile_key = next(
                (
                    key for key in profiles
                    if key in product_lower
                ),
                None
            )

            profile = profiles.get(profile_key, {
                "headline": f"Discover {product}",
                "benefit": (
                    description
                    if description
                    else "Discover what makes this product useful"
                ),
                "visual": "Clean product-focused promotional photography",
                "cta": "Learn More"
            })

        goal_lower = goal.lower()

        if is_service:
            if any(word in goal_lower for word in ["lead", "enquiry", "inquiry"]):
                profile["cta"] = "Enquire Now"
            elif "awareness" in goal_lower:
                profile["cta"] = "Discover Our Services"
            elif "engagement" in goal_lower:
                profile["cta"] = "Contact Us"
            elif "sales" in goal_lower:
                profile["cta"] = "Get a Quote"

        else:
            goal_ctas = {
                "sales": "Shop Now",
                "awareness": "Discover More",
                "leads": "Get in Touch",
                "engagement": "Share Your Thoughts"
            }

            for key, cta in goal_ctas.items():
                if key in goal_lower:
                    profile["cta"] = cta
                    break

        if platform == "instagram_story":
            layout = {
                "top": "Brand identity in the upper safe area",
                "center": "Vertical hero visual with headline",
                "bottom": "Supporting copy and prominent CTA above the lower safe area"
            }

        elif platform == "instagram_carousel":
            layout = {
                "top": "Brand identity and slide label",
                "center": "Main visual and headline",
                "bottom": "Supporting message and continuation cue"
            }

        else:
            layout = style["layout"].copy()

        return {
            "status": "success",
            "template": {
                "name": f"{product} — Instagram Creative",
                "platform": platform,
                "dimensions": self.platform_sizes[platform],
                "design_style": style_key,
                "product": product,
                "target_audience": audience,
                "marketing_goal": goal,
                "headline": profile["headline"],
                "description": profile["benefit"],
                "product_description": description,
                "call_to_action": profile["cta"],
                "color_palette": style["colors"].copy(),
                "visual_direction": (
                    f"{style['direction']}. {profile['visual']}"
                ),
                "layout": layout
            },
            "engine": "Rule-based creative layout prototype"
        }