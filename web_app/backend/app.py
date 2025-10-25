#!/usr/bin/env python3
"""
Flask Backend API for Trip Planner Agent Web Platform
Provides REST API endpoints for the web frontend
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import agent modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from intent import parse_intent
from planner import build_itinerary
from exporters import itinerary_to_markdown, itinerary_to_ics
from data_sources import get_supported_cities

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
    """Get list of supported cities."""
    cities = get_supported_cities()
    return jsonify({
        'cities': cities,
        'count': len(cities)
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
                'supported_cities': get_supported_cities()
            }), 400

        # Default to 3 days if not specified
        if not intent.days:
            intent.days = 3

        # Build itinerary
        itinerary = build_itinerary(intent)

        # Convert to markdown
        markdown = itinerary_to_markdown(itinerary)

        # Generate unique ID for this itinerary
        import uuid
        itinerary_id = str(uuid.uuid4())

        # Store itinerary for later download
        recent_itineraries[itinerary_id] = itinerary

        # Convert itinerary items to dict for JSON serialization
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

        return jsonify({
            'success': True,
            'intent': {
                'destination': intent.destination,
                'days': intent.days,
                'preferences': intent.preferences
            },
            'itinerary': {
                'destination': itinerary.destination,
                'days': itinerary.days,
                'items': items_dict
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

        # Generate ICS file
        ics_path = itinerary_to_ics(itinerary)

        if not ics_path or not os.path.exists(ics_path):
            return jsonify({
                'success': False,
                'error': 'Failed to generate calendar file'
            }), 500

        # Send file for download
        return send_file(
            ics_path,
            mimetype='text/calendar',
            as_attachment=True,
            download_name=f'{itinerary.destination.lower()}_trip.ics'
        )

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get example prompts for users."""
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
        'examples': examples
    })


if __name__ == '__main__':
    print("🚀 Starting Trip Planner Agent API Server...")

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
