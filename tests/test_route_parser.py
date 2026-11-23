
"""
Unit tests for the SnowHeightTracker route parser.

These tests verify that API route data is correctly
converted into Python Route and StreetSegment objects.

The tests cover:
- Valid route conversion.
- Invalid route rejection.
- Routes with empty segment lists.
- Conversion of multiple routes from a JSON file.
"""

import json
from pathlib import Path

from app.route_parser import parse_route


def test_parse_valid_route():
    """
    Verify that valid route data is converted correctly.

    The parser should convert distances from meters to
    kilometers and durations from seconds to minutes.
    """

    route_data = {
        "id": "A",
        "distance_m": 6400,
        "duration_seconds": 1080,
        "segments": [
            {
                "id": "A-segment-1",
                "street_name": "Côte-des-Neiges",
                "distance_m": 500
            }
        ]
    }

    # Convert the dictionary into a Route object.
    route = parse_route(route_data)

    # Verify the route identifier and transportation mode.
    assert route.route_id == "A"
    assert route.travel_mode == "driving"

    # Verify the conversion of distance and duration.
    assert route.distance_km == 6.4
    assert route.duration_min == 18

    # Verify the street segment information.
    assert len(route.segments) == 1
    assert route.segments[0].segment_id == "A-segment-1"
    assert route.segments[0].street_name == "Côte-des-Neiges"
    assert route.segments[0].length_m == 500


def test_parse_invalid_route():
    """
    Verify that invalid route data is rejected.

    A route containing a negative distance should not
    be converted into a Route object.
    """

    route_data = {
        "id": "B",
        "distance_m": -500,
        "duration_seconds": 1200,
        "segments": []
    }

    # Invalid data should return None.
    assert parse_route(route_data) is None


def test_parse_empty_segments():
    """
    Verify that a route with no segments can be converted.

    An empty segment list is currently accepted by the
    structural validation rules.
    """

    route_data = {
        "id": "C",
        "distance_m": 5600,
        "duration_seconds": 1260,
        "segments": []
    }

    route = parse_route(route_data)

    # Verify that the route exists and has no segments.
    assert route.route_id == "C"
    assert route.segments == []


def test_parse_demo_routes():
    """
    Verify that all four routes from the demonstration JSON
    can be converted into Python Route objects.

    This test uses simplified local demonstration data,
    not live weather or snow-removal API responses.
    """

    # Locate the demonstration JSON file.
    file_path = Path("fixtures/demo_response.json")

    # Read and load the JSON data.
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Store the converted Route objects.
    routes = []

    # Convert each route from the JSON response.
    for route_data in data["routes"]:
        route = parse_route(route_data)

        # Ensure that the route was converted successfully.
        assert route is not None

        routes.append(route)

    # Verify that all four routes were converted.
    assert len(routes) == 4

    # Verify the route identifiers.
    assert [route.route_id for route in routes] == [
        "A", "B", "C", "D"
    ]

    # Verify the first route's unit conversions.
    assert routes[0].distance_km == 6.4
    assert routes[0].duration_min == 18


def test_parse_missing_segment_distance():
    """
    Verify that a missing segment distance is stored as None.

    Missing distance information should not be interpreted
    as an actual distance of zero meters.
    """

    route_data = {
        "id": "D",
        "distance_m": 7200,
        "duration_seconds": 1560,
        "segments": [
            {
                "id": "D-segment-1",
                "street_name": "Sherbrooke"
            }
        ]
    }

    # Convert the route into a Python object.
    route = parse_route(route_data)

    # Verify that the route was created successfully.
    assert route is not None

    # The segment exists, but its distance is unknown.
    assert len(route.segments) == 1
    assert route.segments[0].length_m is None


def test_parse_invalid_segment_distance():
    """
    Verify that routes containing an invalid segment
    distance are rejected by the parser.
    """

    route_data = {
        "id": "E",
        "distance_m": 6400,
        "duration_seconds": 1080,
        "segments": [
            {
                "id": "E-segment-1",
                "street_name": "Sherbrooke",
                "distance_m": -500
            }
        ]
    }

    # A negative segment distance should invalidate the route.
    assert parse_route(route_data) is None
