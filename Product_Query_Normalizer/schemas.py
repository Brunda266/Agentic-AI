"""
Data schemas for Product Query Normalizer using Pydantic.
Enforces strict validation of parsed product queries.
"""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ValidationError


class ProductTypeEnum(str, Enum):
    """Enum of supported product types."""
    HEADPHONES = "headphones"
    EARBUDS = "earbuds"
    SPEAKERS = "speakers"
    MICROPHONE = "microphone"
    CAMERA = "camera"
    LAPTOP = "laptop"
    PHONE = "phone"
    TABLET = "tablet"
    WATCH = "watch"
    UNKNOWN = "unknown"


class UsageContextEnum(str, Enum):
    """Enum of common usage contexts."""
    GYM = "gym"
    OFFICE = "office"
    HOME = "home"
    OUTDOOR = "outdoor"
    TRAVEL = "travel"
    GAMING = "gaming"
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    UNKNOWN = "unknown"


class PriceRange(BaseModel):
    """Represents a price range in numeric currency units."""
    min_price: float = Field(ge=0, description="Minimum price in currency units")
    max_price: float = Field(ge=0, description="Maximum price in currency units")

    @field_validator("max_price")
    @classmethod
    def validate_max_price(cls, v: float, info) -> float:
        """Ensure max_price >= min_price."""
        if "min_price" in info.data and v < info.data["min_price"]:
            raise ValueError("max_price must be >= min_price")
        return v

    def __str__(self) -> str:
        return f"₹{self.min_price:.2f} - ₹{self.max_price:.2f}"


class ParsedQuery(BaseModel):
    """Core data model for a parsed product query."""
    product_type: ProductTypeEnum = Field(description="Type of product being searched")
    price_range: Optional[PriceRange] = Field(
        default=None, description="Budget constraints"
    )
    usage_context: List[UsageContextEnum] = Field(
        default_factory=list, description="Contexts where product will be used"
    )
    feature_preferences: List[str] = Field(
        default_factory=list, description="Desired features (e.g., 'waterproof', 'noise-cancelling')"
    )
    original_query: str = Field(description="Original user query")
    confidence_score: float = Field(
        ge=0.0, le=1.0, default=0.5, description="Confidence in parse (0-1)"
    )
    is_complete: bool = Field(
        default=False, description="True if all required fields are present"
    )
    missing_fields: List[str] = Field(
        default_factory=list, description="Fields that need clarification"
    )


class ClarificationRequest(BaseModel):
    """Request for user clarification on ambiguous fields."""
    field_name: str = Field(description="Field requiring clarification")
    field_label: str = Field(description="Human-readable field name")
    current_value: Optional[str] = Field(
        default=None, description="Current extracted/guessed value"
    )
    options: Optional[List[str]] = Field(
        default=None, description="Suggested options for user to choose from"
    )
    question: str = Field(description="Question to ask the user")


class NormalizedResult(BaseModel):
    """Final normalized result after clarification."""
    parsed_query: ParsedQuery = Field(description="Validated parsed query")
    clarifications_made: List[ClarificationRequest] = Field(
        default_factory=list, description="List of clarifications performed"
    )
    is_valid: bool = Field(description="True if query passes all validation rules")
    validation_errors: List[str] = Field(
        default_factory=list, description="Any validation errors encountered"
    )


if __name__ == "__main__":
    # Quick schema validation example
    price = PriceRange(min_price=1000, max_price=5000)
    print(f"Price Range: {price}")

    # Test ParsedQuery
    query = ParsedQuery(
        product_type=ProductTypeEnum.HEADPHONES,
        price_range=price,
        usage_context=[UsageContextEnum.GYM],
        feature_preferences=["noise-cancelling", "waterproof"],
        original_query="Best headphones around 4k for gym",
    )
    print(f"\nParsed Query:\n{query}")
