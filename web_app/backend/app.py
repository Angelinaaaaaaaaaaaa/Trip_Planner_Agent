#!/usr/bin/env python3
"""
Flask Backend API for Trip Planner Agent Web Platform
Provides REST API endpoints for the web frontend
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO
import sys
import os
from dotenv import load_dotenv

# Resolve repository root and ensure project modules are importable
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, REPO_ROOT)

# Load environment variables from repo root .env regardless of CWD
env_path = os.path.join(REPO_ROOT, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

from intent import parse_intent
from planner import build_itinerary
from llm_planner import create_intelligent_itinerary
from llm_config import is_llm_available
from exporters import itinerary_to_markdown, itinerary_to_ics, itinerary_to_ics_string
from data_sources import get_supported_cities, is_city_supported

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Store recent itineraries for download
recent_itineraries = {}


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Trip Planner Agent API',
        'version': '1.0.0'
    })


@app.route('/api/cities', methods=['GET'])
def get_cities():
    """Get list of supported cities and LLM status."""
    cities = get_supported_cities()
    llm_available = is_llm_available()
    
    return jsonify({
        'static_cities': cities,
        'static_count': len(cities),
        'llm_available': llm_available,
        'supports_any_city': llm_available,
        'message': 'Can plan trips to ANY city worldwide!' if llm_available else f'Limited to: {", ".join(cities)}'
    })


@app.route('/api/plan', methods=['POST'])
def plan_trip():
    """
    Main endpoint to plan a trip.

    Request body:
    {
        "message": "Plan a 3-day trip to Tokyo for food and culture"
    }

    Response:
    {
        "success": true,
        "intent": {...},
        "itinerary": {...},
        "markdown": "...",
        "itinerary_id": "..."
    }
    """
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing "message" in request body'
            }), 400

        user_message = data['message']

        # Parse intent
        intent = parse_intent(user_message)

        if not intent.destination:
            return jsonify({
                'success': False,
                'error': 'Could not identify destination. Please specify a city.',
                'llm_available': is_llm_available(),
                'message': 'You can ask for ANY city worldwide!' if is_llm_available() else f'Please choose from: {", ".join(get_supported_cities())}'
            }), 400

        # Default to 3 days if not specified
        if not intent.days:
            intent.days = 3

        # Build itinerary using LLM if available, fallback to static
        if is_llm_available():
            # LLM mode - can plan trips to ANY city worldwide
            itinerary = create_intelligent_itinerary(intent, use_llm=True)
        else:
            # Static mode - validate that the destination is in static database
            if not is_city_supported(intent.destination):
                return jsonify({
                    'success': False,
                    'error': f'City "{intent.destination}" is not supported yet. Please choose from the available cities.',
                    'supported_cities': get_supported_cities(),
                    'llm_available': False,
                    'message': f'To enable planning for ANY city, add ANTHROPIC_API_KEY to .env file'
                }), 400

            itinerary = build_itinerary(intent)

        # Convert to markdown
        markdown = itinerary_to_markdown(itinerary)

        # Generate unique ID for this itinerary
        import uuid
        itinerary_id = str(uuid.uuid4())

        # Store itinerary for later download
        recent_itineraries[itinerary_id] = itinerary

        # Convert itinerary items and day ranges to dict for JSON serialization
        items_dict = [
            {
                'day': item.day,
                'time': item.time,
                'name': item.name,
                'area': item.area,
                'tags': item.tags,
                'url': item.url
            }
            for item in itinerary.items
        ]

        day_ranges_dict = [
            {
                'start_day': dr.start_day,
                'end_day': dr.end_day,
                'description': dr.description,
                'activity_type': dr.activity_type,
                'num_days': dr.num_days
            }
            for dr in itinerary.day_ranges
        ] if itinerary.day_ranges else []

        return jsonify({
            'success': True,
            'llm_powered': is_llm_available(),
            'intent': {
                'destination': intent.destination,
                'days': intent.days,
                'preferences': intent.preferences
            },
            'itinerary': {
                'destination': itinerary.destination,
                'days': itinerary.days,
                'items': items_dict,
                'day_ranges': day_ranges_dict
            },
            'markdown': markdown,
            'itinerary_id': itinerary_id
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/download/<itinerary_id>', methods=['GET'])
def download_calendar(itinerary_id):
    """
    Download calendar file for a specific itinerary.
    Generates the ICS file in memory without saving to disk.

    Parameters:
        itinerary_id: UUID of the itinerary
    """
    try:
        if itinerary_id not in recent_itineraries:
            return jsonify({
                'success': False,
                'error': 'Itinerary not found. It may have expired.'
            }), 404

        itinerary = recent_itineraries[itinerary_id]

        # Generate ICS content in memory (no file saved to disk!)
        ics_content, filename = itinerary_to_ics_string(itinerary)

        if not ics_content:
            return jsonify({
                'success': False,
                'error': 'Failed to generate calendar file'
            }), 500

        # Convert string to bytes and create in-memory file
        ics_bytes = BytesIO(ics_content.encode('utf-8'))
        ics_bytes.seek(0)

        # Send file directly from memory
        return send_file(
            ics_bytes,
            mimetype='text/calendar',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get example prompts for users."""
    
    # Different examples based on LLM availability
    if is_llm_available():
        examples = [
            {
                'title': 'Cultural Tokyo',
                'prompt': 'Plan a 3-day trip to Tokyo for food and culture',
                'description': 'Explore temples, markets, and authentic cuisine'
            },
            {
                'title': 'Prague Architecture',
                'prompt': 'I want to visit Prague for 4 days, focus on architecture and history',
                'description': 'Discover stunning Gothic and Baroque buildings'
            },
            {
                'title': 'Mumbai Food Tour',
                'prompt': 'Plan a 5-day food-focused trip to Mumbai',
                'description': 'Street food, markets, and local restaurants'
            },
            {
                'title': 'Reykjavik Adventure',
                'prompt': 'Adventure trip to Reykjavik for 6 days with nature focus',
                'description': 'Northern lights, geysers, and outdoor activities'
            },
            {
                'title': 'Family Singapore',
                'prompt': 'Family trip to Singapore for 4 days, kid-friendly',
                'description': 'Zoo, aquarium, and family attractions'
            },
            {
                'title': 'Dubai Luxury',
                'prompt': 'Plan a luxurious 3-day trip to Dubai with shopping',
                'description': 'High-end experiences and world-class shopping'
            },
            {
                'title': 'Cape Town Nature',
                'prompt': 'Cape Town for 7 days focusing on nature and wine',
                'description': 'Table Mountain, penguins, and wine tastings'
            },
            {
                'title': 'Istanbul Culture',
                'prompt': 'Cultural exploration of Istanbul for 5 days',
                'description': 'Mosques, bazaars, and Turkish history'
            }
        ]
    else:
        # Static examples for limited cities
        examples = [
            {
                'title': 'Cultural Tokyo',
                'prompt': 'Plan a 3-day trip to Tokyo for food and culture',
                'description': 'Explore temples, markets, and authentic cuisine'
            },
            {
                'title': 'Architecture in Barcelona',
                'prompt': 'I want to visit Barcelona for 2 days, focus on architecture',
                'description': 'Discover Gaudí masterpieces and historic sites'
            },
            {
                'title': 'Family Singapore',
                'prompt': 'Family trip to Singapore for 4 days, kid-friendly',
                'description': 'Zoo, aquarium, and family attractions'
            },
            {
                'title': 'Paris Highlights',
                'prompt': 'Show me Paris highlights for 3 days',
                'description': 'Eiffel Tower, Louvre, and more'
            },
            {
                'title': 'New York Adventure',
                'prompt': 'Plan a 5-day trip to New York',
                'description': 'Explore the Big Apple from top to bottom'
            },
            {
                'title': 'London Culture',
                'prompt': 'London trip for 3 days, museums and history',
                'description': 'British Museum, palaces, and historic sites'
            }
        ]

    return jsonify({
        'examples': examples,
        'llm_powered': is_llm_available(),
        'note': 'AI can plan trips to ANY city worldwide!' if is_llm_available() else 'Limited to pre-configured cities'
    })


if __name__ == '__main__':
    print("🚀 Starting Trip Planner Agent API Server...")
    
    # Check LLM availability
    if is_llm_available():
        print("✅ LLM Integration: ENABLED (Claude AI)")
        print("🌍 Capability: Can plan trips to ANY city worldwide!")
    else:
        print("⚠️  LLM Integration: DISABLED (no ANTHROPIC_API_KEY)")
        print(f"📍 Capability: Limited to {len(get_supported_cities())} pre-configured cities")
        print("💡 Tip: Set ANTHROPIC_API_KEY environment variable to enable global planning")

    # Get port from environment variable (for production deployment)
    port = int(os.environ.get('PORT', 5000))

    # Determine if running in production or development
    debug_mode = os.environ.get('FLASK_ENV', 'production') == 'development'

    print(f"📍 API available at: http://localhost:{port}")
    print("📖 Endpoints:")
    print("   GET  /api/health       - Health check")
    print("   GET  /api/cities       - List supported cities")
    print("   POST /api/plan         - Plan a trip")
    print("   GET  /api/download/:id - Download calendar file")
    print("   GET  /api/examples     - Get example prompts")

    app.run(host='0.0.0.0', port=port, debug=debug_mode)
