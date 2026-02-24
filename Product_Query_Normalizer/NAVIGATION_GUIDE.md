# Product Query Normalizer - Navigation Guide

## 📍 Start Here

This guide helps you navigate the Product Query Normalizer project efficiently.

---

## 🎯 By Use Case

### "I want a quick overview"
→ Read: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)  
→ Time: 5 minutes  
→ What you'll learn: What was built, what works, test results

### "I want to understand the architecture"
→ Read: [README.md](README.md) - Section "Architecture"  
→ Code: Review [normalizer.py](normalizer.py)  
→ Time: 10 minutes

### "I want to see it work"
→ Run: `python final_demo.py`  
→ Or: `python normalizer.py`  
→ Or: `streamlit run app.py`  
→ Time: 2 minutes

### "I want to run tests"
→ Run: `python tests.py`  
→ Time: 1 minute  
→ Expected: 7/7 tests passing

### "I want to learn how to use it"
→ Read: [usage_examples.py](usage_examples.py) (10 examples)  
→ Or: [README.md](README.md) - "Usage Examples" section  
→ Time: 15 minutes

### "I want to integrate it into my code"
→ Read: [usage_examples.py](usage_examples.py)  
→ Code: Start with basic_usage() example  
→ Time: 10 minutes

### "I want to understand the data model"
→ Read: [schemas.py](schemas.py)  
→ Documentation: [README.md](README.md) - "Schema Overview" section  
→ Time: 10 minutes

### "I want to extend the system"
→ Read: [README.md](README.md) - "Extending the System" section  
→ Code Examples: Review [parser.py](parser.py) for patterns  
→ Time: 20 minutes

---

## 📁 File Guide by Purpose

### Core System Files (Start here for understanding)
| File | Purpose | Lines | Type |
|------|---------|-------|------|
| [normalizer.py](normalizer.py) | Main orchestrator + API | 150 | Core |
| [parser.py](parser.py) | Parse queries into structured data | 260 | Core |
| [schemas.py](schemas.py) | Pydantic data models | 380 | Core |
| [validator.py](validator.py) | Validation + clarification | 300 | Core |
| [ambiguity_detector.py](ambiguity_detector.py) | Detect ambiguities | 190 | Core |

### Testing
| File | Purpose | Tests | Type |
|------|---------|-------|------|
| [tests.py](tests.py) | Unit tests (all passing) | 7 | Test |

### User Interface
| File | Purpose | Type |
|------|---------|------|
| [app.py](app.py) | Interactive Streamlit UI | UI |

### Examples & Usage
| File | Purpose | Examples | Type |
|------|---------|----------|------|
| [usage_examples.py](usage_examples.py) | 10 complete usage examples | 10 | Example |
| [final_demo.py](final_demo.py) | Quick demo script | 4 | Example |

### Documentation
| File | Purpose | Type |
|------|---------|------|
| [README.md](README.md) | Complete documentation | Docs |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | What was implemented | Docs |
| [PROJECT_DELIVERABLES.md](PROJECT_DELIVERABLES.md) | Complete deliverables list | Docs |

### Configuration
| File | Purpose | Type |
|------|---------|------|
| [requirements.txt](requirements.txt) | Python dependencies | Config |
| [__init__.py](__init__.py) | Package initialization | Config |

---

## 🗺️ Learning Path

### Path 1: Quick Start (15 min)
1. Read: IMPLEMENTATION_SUMMARY.md
2. Run: `python final_demo.py`
3. Explore: Try the Streamlit UI with `streamlit run app.py`

### Path 2: Deep Dive (1 hour)
1. Read: README.md (full)
2. Review: schemas.py (understand data model)
3. Review: normalizer.py (understand flow)
4. Run: tests.py (see what's being tested)
5. Try: usage_examples.py (10 examples)

### Path 3: Developer (2 hours)
1. Study: All core system files (normalizer, parser, schemas, validator, detector)
2. Run: tests.py (understand test patterns)
3. Review: usage_examples.py (integration patterns)
4. Try: Extend the parser with new keywords
5. Try: Add a new product type

### Path 4: Full Understanding (3+ hours)
1. Deep read: All Python files in order
   - schemas.py (understand data model)
   - parser.py (understand parsing logic)
   - ambiguity_detector.py (understand detection)
   - validator.py (understand validation)
   - normalizer.py (understand orchestration)
2. Review: app.py (understand UI)
3. Review: tests.py (understand testing)
4. Try: Modify and test features
5. Create: Integration examples

---

## 🚀 Quick Commands

```bash
# Install
pip install -r requirements.txt

# Test
python tests.py

# Demo
python final_demo.py
python normalizer.py
python usage_examples.py

# UI
streamlit run app.py

# Python usage
python -c "from Product_Query_Normalizer import ProductQueryNormalizer; \
normalizer = ProductQueryNormalizer(); \
result = normalizer.normalize('Best headphones around 4k'); \
print(result.parsed_query.product_type)"
```

---

## 📊 File Relationships

```
normalizer.py (Main API)
    ├── parser.py → QueryParser
    ├── ambiguity_detector.py → AmbiguityDetector
    ├── validator.py → QueryValidator, InteractiveClarifier
    └── schemas.py → All data models

app.py (UI)
    └── normalizer.py

tests.py (Verification)
    ├── parser.py
    ├── ambiguity_detector.py
    ├── validator.py
    └── normalizer.py

usage_examples.py (Learning)
    └── normalizer.py + components
```

---

## 🎓 Code Structure by Complexity

### Level 1: Beginner (Start here)
- Read: IMPLEMENTATION_SUMMARY.md
- Run: final_demo.py
- Try: Basic usage in usage_examples.py

### Level 2: Intermediate
- Read: README.md
- Study: schemas.py (data models)
- Study: normalizer.py (main flow)
- Try: Use it in your code

### Level 3: Advanced
- Study: parser.py (extraction logic)
- Study: ambiguity_detector.py (detection logic)
- Study: validator.py (validation logic)
- Try: Extend with new features

### Level 4: Expert
- Study: All code files
- Run: tests.py
- Try: Modify test cases
- Create: Custom extensions

---

## 🔍 Finding Specific Information

### "How do I use this?"
→ [usage_examples.py](usage_examples.py) - basic_usage()

### "What data structures are used?"
→ [schemas.py](schemas.py)

### "How does parsing work?"
→ [parser.py](parser.py) - read QueryParser class

### "How are ambiguities detected?"
→ [ambiguity_detector.py](ambiguity_detector.py) - read AmbiguityDetector class

### "How is validation done?"
→ [validator.py](validator.py) - read QueryValidator class

### "How is the UI built?"
→ [app.py](app.py) - read from top to bottom

### "What are the test cases?"
→ [tests.py](tests.py) - each test function

### "How do I extend this?"
→ [README.md](README.md) - "Extending the System" section

### "What was the task?"
→ [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - "Requirements Met"

### "What files exist and why?"
→ [PROJECT_DELIVERABLES.md](PROJECT_DELIVERABLES.md)

---

## 📈 Module Dependencies

```
schemas.py (No dependencies)
    ↓
parser.py (depends on schemas)
    ↓
ambiguity_detector.py (depends on schemas, parser)
    ↓
validator.py (depends on schemas, ambiguity_detector)
    ↓
normalizer.py (depends on all above)
    ↓
app.py (depends on normalizer)
tests.py (depends on all)
usage_examples.py (depends on normalizer and components)
```

---

## ✅ Verification Checklist

To verify everything is working:

- [ ] Run `python tests.py` → All 7 tests should pass
- [ ] Run `python final_demo.py` → Should show 4 test scenarios
- [ ] Run `streamlit run app.py` → Should open UI at localhost:8501
- [ ] Try: `python -c "from Product_Query_Normalizer import ProductQueryNormalizer"`
- [ ] Try: `python usage_examples.py`

---

## 🎯 Common Tasks

### Task: Parse a query
```python
from Product_Query_Normalizer import ProductQueryNormalizer
normalizer = ProductQueryNormalizer()
result = normalizer.normalize("Your query here")
```

### Task: Get ambiguities
```python
ambiguities = normalizer.get_ambiguities("Your query")
```

### Task: Get clarifications
```python
result = normalizer.normalize(query, user_responses={...})
```

### Task: Understand data model
1. Read: schemas.py
2. Look at: ParsedQuery class
3. See: All field types and validations

### Task: Add new product type
1. Update: ProductTypeEnum in schemas.py
2. Add keywords: In parser.py → PRODUCT_KEYWORDS
3. Set budget: In validator.py

### Task: Test your changes
1. Write: New test in tests.py
2. Run: `python tests.py`

---

## 📞 Help Resources

| Question | Answer Location |
|----------|-----------------|
| "What is this project?" | IMPLEMENTATION_SUMMARY.md |
| "How do I use it?" | usage_examples.py or README.md |
| "What files are there?" | PROJECT_DELIVERABLES.md |
| "How does it work?" | README.md - Architecture section |
| "How do I extend it?" | README.md - Extending section |
| "What's the API?" | normalizer.py docstrings |
| "Are there tests?" | tests.py (all 7 passing) |
| "Can I see examples?" | usage_examples.py (10 examples) |
| "What's the data model?" | schemas.py and README.md |

---

## 🚪 Entry Points

### As a User
→ Start: [usage_examples.py](usage_examples.py)  
→ Then: [app.py](app.py) for UI  
→ Reference: [README.md](README.md)

### As a Developer
→ Start: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)  
→ Then: [README.md](README.md)  
→ Code: [normalizer.py](normalizer.py)

### As a Tester
→ Run: [tests.py](tests.py)  
→ Review: Each test function  
→ Extend: Add your own tests

### As a Learner
→ Read: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)  
→ Study: [schemas.py](schemas.py)  
→ Explore: [normalizer.py](normalizer.py)  
→ Practice: [usage_examples.py](usage_examples.py)

---

**Last Updated**: February 24, 2026  
**Project Status**: ✅ Complete & Tested  
**All Tests**: ✅ Passing (7/7)

Navigate using this guide for the best learning experience!
