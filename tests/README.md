# Tests & Demos

This directory contains all test files and demo scripts for the Trip Planner Agent.

## Running Tests

### Core Functionality Test (Recommended)

Tests all main features without requiring API key:

```bash
python3 tests/test_core_functionality.py
```

Expected: `28/28 tests passed`

### Individual Component Tests

```bash
# Intent parser
python3 tests/test_parser_only.py

# Itinerary planner
python3 tests/test_planner.py

# City name handling
python3 tests/test_city_names.py

# LLM planner (requires API key)
python3 tests/test_llm_planner.py

# Web backend
python3 tests/test_web_backend.py

# End-to-end
python3 tests/test_end_to_end.py
```

### Local Testing

Quick test of the system:

```bash
python3 tests/test_local.py
```

This will:
- Show supported cities
- Test intent parsing
- Generate a sample itinerary
- Create a calendar file

## Demo Scripts

### Day Ranges Demo

Shows how to use day ranges for multi-day activities:

```bash
python3 tests/demo_day_ranges.py
```

### LLM Integration Demo

Demonstrates AI-powered planning (requires API key):

```bash
python3 tests/demo_llm_integration.py
```

## Test Files

| File | Purpose |
|------|---------|
| `test_core_functionality.py` | Main test suite (28 tests) |
| `test_parser_only.py` | Intent parsing tests |
| `test_planner.py` | Itinerary generation tests |
| `test_city_names.py` | City name normalization tests |
| `test_llm_planner.py` | AI planner tests |
| `test_web_backend.py` | Web API tests |
| `test_backend_direct.py` | Direct backend tests |
| `test_end_to_end.py` | Full workflow tests |
| `test_and_fix.py` | Debug/fix utility |
| `test_local.py` | Quick local test |
| `demo_day_ranges.py` | Day ranges demo |
| `demo_llm_integration.py` | LLM demo |

## Notes

- Most tests work without API key
- Tests requiring API key will skip if not configured
- All tests automatically add parent directory to Python path
- Run tests from project root: `python3 tests/test_name.py`
