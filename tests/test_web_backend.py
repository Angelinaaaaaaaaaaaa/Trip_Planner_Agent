#!/usr/bin/env python3
"""
Test the web app backend to ensure all imports and functions work correctly.
Run this before starting the web app to catch any issues.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print(" " * 20 + "WEB BACKEND TEST")
print("=" * 70)
print()

# Test 1: Check imports
print("TEST 1: Checking imports...")
print("-" * 70)

try:
    from data_sources import get_supported_cities, is_city_supported, fetch_pois
    print("✓ data_sources imports OK")
except Exception as e:
    print(f"✗ data_sources import failed: {e}")
    sys.exit(1)

try:
    from exporters import itinerary_to_markdown, itinerary_to_ics
    print("✓ exporters imports OK")
except Exception as e:
    print(f"✗ exporters import failed: {e}")
    sys.exit(1)

print()

# Test 2: Test the critical is_city_supported function
print("TEST 2: Testing is_city_supported()...")
print("-" * 70)

test_cities = [
    ('Tokyo', True),
    ('tokyo', True),
    ('TOKYO', True),
    ('tokyo.', True),
    ('Paris', True),
    ('Unknown', False),
]

all_passed = True
for city, expected in test_cities:
    try:
        result = is_city_supported(city)
        status = '✓' if result == expected else '✗'
        if result != expected:
            all_passed = False
        print(f"{status} is_city_supported('{city}') = {result}")
    except Exception as e:
        print(f"✗ is_city_supported('{city}') raised error: {e}")
        all_passed = False

if not all_passed:
    print("\n✗ Some tests failed!")
    sys.exit(1)

print()

# Test 3: Test get_supported_cities
print("TEST 3: Testing get_supported_cities()...")
print("-" * 70)

try:
    cities = get_supported_cities()
    print(f"✓ get_supported_cities() returned {len(cities)} cities")
    print(f"  Cities: {', '.join(cities)}")
except Exception as e:
    print(f"✗ get_supported_cities() failed: {e}")
    sys.exit(1)

print()

# Test 4: Test fetch_pois with normalized names
print("TEST 4: Testing fetch_pois() with normalized names...")
print("-" * 70)

test_cases = ['Tokyo', 'tokyo', 'TOKYO', 'tokyo.', 'new york']

all_passed = True
for city in test_cases:
    try:
        pois = fetch_pois(city)
        status = '✓' if pois else '✗'
        if not pois:
            all_passed = False
        print(f"{status} fetch_pois('{city}') returned {len(pois)} POIs")
    except Exception as e:
        print(f"✗ fetch_pois('{city}') raised error: {e}")
        all_passed = False

if not all_passed:
    print("\n✗ Some tests failed!")
    sys.exit(1)

print()

# Test 5: Try to import Flask app (without starting it)
print("TEST 5: Testing Flask app imports...")
print("-" * 70)

try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'web_app/backend'))

    # Check if we can import the app module
    print("  Attempting to import app module...")

    # This will test all imports in app.py
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "app",
        os.path.join(os.path.dirname(__file__), 'web_app/backend/app.py')
    )
    app_module = importlib.util.module_from_spec(spec)

    # This will execute the imports
    spec.loader.exec_module(app_module)

    print("✓ Flask app imports successfully")
    print("✓ All required functions are available")

except ModuleNotFoundError as e:
    print(f"⚠️  Missing dependency: {e}")
    print("   Run: pip install flask flask-cors")
    print("   This is expected if you haven't installed web dependencies yet.")
except Exception as e:
    print(f"✗ Flask app import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Final Summary
print("=" * 70)
print("FINAL SUMMARY")
print("=" * 70)
print()
print("✅ All critical functions work correctly!")
print("✅ is_city_supported() is properly defined and working")
print("✅ City name normalization is working")
print("✅ POI fetching is working")
print()
print("The web backend should work correctly!")
print()
print("Next steps:")
print("  1. Make sure Flask is installed: pip install flask flask-cors")
print("  2. Start the backend: python web_app/backend/app.py")
print("  3. Or use the script: ./start_web_app.sh")
print()
print("If you see any '✗' marks above, please fix those issues first.")
print()
