#!/usr/bin/env python3
"""
Direct test of the backend app to verify it starts without errors.
"""

import sys
import os

# Set up paths
REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, REPO_ROOT)

print("=" * 70)
print(" " * 15 + "BACKEND DIRECT TEST")
print("=" * 70)
print()

# Test 1: Import data_sources
print("TEST 1: Import data_sources...")
try:
    from data_sources import get_supported_cities, is_city_supported, fetch_pois
    print("✓ data_sources imported successfully")

    # Test the function
    result = is_city_supported('Tokyo')
    print(f"✓ is_city_supported('Tokyo') = {result}")

    cities = get_supported_cities()
    print(f"✓ get_supported_cities() returned {len(cities)} cities")
except Exception as e:
    print(f"✗ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 2: Import backend app components
print("TEST 2: Import backend app components...")
sys.path.insert(0, os.path.join(REPO_ROOT, 'web_app/backend'))

try:
    print("  Importing Flask...")
    from flask import Flask
    print("  ✓ Flask imported")

    print("  Importing flask_cors...")
    from flask_cors import CORS
    print("  ✓ flask_cors imported")

    print("  Importing dotenv...")
    from dotenv import load_dotenv
    print("  ✓ dotenv imported")

except ImportError as e:
    print(f"  ✗ Missing dependency: {e}")
    print()
    print("To install:")
    print("  pip install flask flask-cors python-dotenv")
    sys.exit(1)

print()

# Test 3: Try to import the full app module
print("TEST 3: Import full app module...")
try:
    # Change to backend directory for proper import
    os.chdir(os.path.join(REPO_ROOT, 'web_app/backend'))
    sys.path.insert(0, REPO_ROOT)

    # Load .env
    env_path = os.path.join(REPO_ROOT, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print("  ✓ .env loaded")
    else:
        print("  ⚠️  No .env file (this is OK, will use fallback)")

    # Try importing the app
    import app as backend_app
    print("  ✓ Backend app module imported successfully")
    print()
    print("  Available routes:")
    for rule in backend_app.app.url_map.iter_rules():
        print(f"    {rule.rule} [{', '.join(rule.methods)}]")

except Exception as e:
    print(f"  ✗ Failed to import app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 4: Test the critical function
print("TEST 4: Test is_city_supported in backend context...")
try:
    # Import from the backend app's perspective
    from data_sources import is_city_supported as backend_is_city_supported

    test_cases = [
        'Tokyo',
        'tokyo',
        'tokyo.',
        'Paris',
        'new york',
    ]

    for city in test_cases:
        result = backend_is_city_supported(city)
        print(f"  ✓ is_city_supported('{city}') = {result}")

except Exception as e:
    print(f"  ✗ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 70)
print("SUCCESS! Backend app is ready to run.")
print("=" * 70)
print()
print("To start the backend:")
print("  python web_app/backend/app.py")
print()
print("Or use the start script:")
print("  ./start_web_app.sh")
print()
