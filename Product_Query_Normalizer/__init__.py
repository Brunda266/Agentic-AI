"""
Product Query Normalizer Package
E-commerce product search query normalization with ambiguity detection.

Main exports:
    ProductQueryNormalizer: Main orchestrator for the full pipeline
    QueryParser: Query parsing and feature extraction
    AmbiguityDetector: Ambiguity detection and clarification generation
    QueryValidator: Business rules validation
    InteractiveClarifier: Interactive clarification loop
"""

from normalizer import ProductQueryNormalizer
from parser import QueryParser
from ambiguity_detector import AmbiguityDetector
from validator import QueryValidator, InteractiveClarifier
from schemas import (
    ProductTypeEnum,
    UsageContextEnum,
    PriceRange,
    ParsedQuery,
    ClarificationRequest,
    NormalizedResult,
)

__version__ = "1.0.0"
__author__ = "Agentic AI Team"

__all__ = [
    "ProductQueryNormalizer",
    "QueryParser",
    "AmbiguityDetector",
    "QueryValidator",
    "InteractiveClarifier",
    "ProductTypeEnum",
    "UsageContextEnum",
    "PriceRange",
    "ParsedQuery",
    "ClarificationRequest",
    "NormalizedResult",
]
