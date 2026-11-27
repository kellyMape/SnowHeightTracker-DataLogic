
"""
Unit tests for the SnowHeightTracker data validation module.

These tests verify that route information is correctly validated
before being used by the application.

The test cases cover:
- Route distances and travel durations.
- Street segment structures.
- Snow-removal status values.
- Timestamp formats.
- Complete route structures.
- Integration with a simplified demonstration JSON file.

All tests use pytest and Python's assert statements.
"""

import json
from pathlib import Path

from app.data_validator import (
    validate_distance,
    validate_duration,
    validate_segments,
    validate_removal_status,
    validate_timestamp,
    validate_route,
    validate_segment_distance,
    validate_snow_depth,
    validate_ice_risk
)


# ---------------------------------------------------------
# DISTANCE VALIDATION TESTS
# ---------------------------------------------------------

def test_valid_distance():
    """Verify that positive distances are accepted."""

    # Test a whole-number distance and a decimal distance.
    assert validate_distance(6400) is True
    assert validate_distance(150.5) is True


def test_invalid_distance():
    """Verify that negative and zero distances are rejected."""

    # A route cannot have a negative or zero travel distance.
    assert validate_distance(-500) is False
    assert validate_distance(0) is False


def test_invalid_data_types():
    """Verify that non-numeric distance values are rejected."""

    # Strings, missing values, and booleans are not valid distances.
    assert validate_distance("abc") is False
    assert validate_distance(None) is False
    assert validate_distance(True) is False


def test_non_finite_distance():
    """Verify that NaN and infinite distances are rejected."""

    # Non-finite values cannot represent measurable route distances.
    assert validate_distance(float("nan")) is False
    assert validate_distance(float("inf")) is False


# ---------------------------------------------------------
# TRAVEL DURATION VALIDATION TESTS
# ---------------------------------------------------------

def test_valid_duration():
    """Verify that positive travel durations are accepted."""

    # Travel duration is measured in seconds.
    assert validate_duration(1080) is True
    assert validate_duration(300.5) is True


def test_invalid_duration():
    """Verify that negative and zero durations are rejected."""

    # Estimated travel time must be greater than zero.
    assert validate_duration(-100) is False
    assert validate_duration(0) is False


def test_invalid_duration_types():
    """Verify that invalid duration values are rejected."""

    # Reject strings, missing values, booleans, and non-finite numbers.
    assert validate_duration("fifteen") is False
    assert validate_duration(None) is False
    assert validate_duration(True) is False
    assert validate_duration(float("nan")) is False
    assert validate_duration(float("inf")) is False


# ---------------------------------------------------------
# STREET SEGMENT VALIDATION TESTS
# ---------------------------------------------------------

def test_valid_segments():
    """Verify that a list of segments with valid IDs is accepted."""

    # A route may contain multiple street segments.
    segments = [
        {"id": "A-segment-1"},
        {"id": "A-segment-2"}
    ]

    assert validate_segments(segments) is True


def test_invalid_segments_type():
    """Verify that the segments field must be a list."""

    # Strings and missing values are not valid segment collections.
    assert validate_segments("segments") is False
    assert validate_segments(None) is False


def test_invalid_segment_id():
    """Verify that segments with empty identifiers are rejected."""

    segments = [
        {"id": "A-segment-1"},
        {"id": ""}
    ]

    # Every segment must have a non-empty string identifier.
    assert validate_segments(segments) is False


def test_empty_segments():
    """Verify that an empty segment list is structurally accepted."""

    # Structural validation currently allows an empty list.
    # Route completeness can be checked separately.
    assert validate_segments([]) is True


# ---------------------------------------------------------
# SNOW-REMOVAL STATUS VALIDATION TESTS
# ---------------------------------------------------------

def test_valid_removal_status():
    """Verify that recognized snow-removal statuses are accepted."""

    # These values belong to the provisional normalized status set.
    assert validate_removal_status("planned") is True
    assert validate_removal_status("cleared") is True
    assert validate_removal_status("in_progress") is True
    assert validate_removal_status("unknown") is True


def test_invalid_removal_status():
    """Verify that unrecognized status values are rejected."""

    # Only explicitly supported status values should be accepted.
    assert validate_removal_status("banana") is False
    assert validate_removal_status("finished") is False
    assert validate_removal_status("") is False


def test_invalid_removal_status_type():
    """Verify that snow-removal statuses must be strings."""

    # Reject missing values, numbers, and booleans.
    assert validate_removal_status(None) is False
    assert validate_removal_status(2) is False
    assert validate_removal_status(True) is False


# ---------------------------------------------------------
# TIMESTAMP VALIDATION TESTS
# ---------------------------------------------------------

def test_valid_timestamp():
    """Verify that valid timezone-aware ISO timestamps are accepted."""

    # Accept UTC timestamps using either 'Z' or an explicit offset.
    assert validate_timestamp("2026-11-19T19:30:41Z") is True
    assert validate_timestamp("2026-11-19T19:30:41+00:00") is True


def test_invalid_timestamp():
    """Verify that malformed or impossible timestamps are rejected."""

    # Reject informal dates, invalid calendar values, and empty strings.
    assert validate_timestamp("yesterday") is False
    assert validate_timestamp("2026-99-19T19:30:41Z") is False
    assert validate_timestamp("") is False


def test_invalid_timestamp_type():
    """Verify that timestamps must be strings."""

    # Reject missing values, numbers, and booleans.
    assert validate_timestamp(None) is False
    assert validate_timestamp(12345) is False
    assert validate_timestamp(True) is False


# ---------------------------------------------------------
# COMPLETE ROUTE VALIDATION TESTS
# ---------------------------------------------------------

def test_valid_route():
    """Verify that a route with valid required fields is accepted."""

    # Create a simplified route matching the expected data structure.
    route = {
        "id": "A",
        "distance_m": 6400,
        "duration_seconds": 1080,
        "segments": [
            {"id": "A-segment-1"}
        ]
    }

    # All required fields should pass structural validation.
    assert validate_route(route) is True


def test_invalid_route_distance():
    """Verify that a route with an invalid distance is rejected."""

    route = {
        "id": "B",
        "distance_m": -500,
        "duration_seconds": 1200,
        "segments": []
    }

    # A negative distance invalidates the entire route.
    assert validate_route(route) is False


def test_invalid_route_structure():
    """Verify that unsupported route structures and IDs are rejected."""

    # Route data must be represented as a dictionary.
    assert validate_route(None) is False
    assert validate_route("Route A") is False

    route = {
        "id": "",
        "distance_m": 6400,
        "duration_seconds": 1080,
        "segments": []
    }

    # An empty route identifier is not allowed.
    assert validate_route(route) is False


# ---------------------------------------------------------
# JSON DEMONSTRATION INTEGRATION TEST
# ---------------------------------------------------------

def test_demo_routes():
    """
    Verify that the simplified demonstration JSON can be loaded
    and that all four routes pass structural validation.

    This test checks compatibility with our local sample data.
    It does not validate live API responses or real road conditions.
    """

    # Locate the JSON fixture containing the demonstration routes.
    file_path = Path("fixtures/demo_response.json")

    # Read the file and deserialize its JSON content into Python data.
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Confirm that the response is demonstration data.
    assert data["mode"] == "demo"

    # Confirm that the response reports four routes.
    assert data["returned_route_count"] == 4

    # Retrieve the collection of routes from the JSON response.
    routes = data["routes"]

    # Verify that the expected number of routes was received.
    assert len(routes) == 4

    # Validate each route using the existing validation module.
    for route in routes:
        assert validate_route(route) is True


def test_valid_segment_distance():
    """
    Verify that positive segment distances are accepted.
    """

    assert validate_segment_distance(500) is True
    assert validate_segment_distance(150.5) is True


def test_missing_segment_distance():
    """
    Verify that missing segment distances are accepted.

    Missing information should remain unknown rather
    than being interpreted as zero meters.
    """

    assert validate_segment_distance(None) is True


def test_invalid_segment_distance():
    """
    Verify that invalid segment distances are rejected.
    """

    assert validate_segment_distance(-500) is False
    assert validate_segment_distance(0) is False
    assert validate_segment_distance("unknown") is False
    assert validate_segment_distance(True) is False
    assert validate_segment_distance(float("nan")) is False


def test_valid_snow_depth():
    """
    Verify that valid snow depth measurements are accepted.
    """

    # Zero is valid because a station may report no snow.
    assert validate_snow_depth(0) is True
    assert validate_snow_depth(8) is True
    assert validate_snow_depth(15.5) is True


def test_missing_snow_depth():
    """
    Verify that missing snow depth data is accepted as unknown.
    """

    assert validate_snow_depth(None) is True


def test_invalid_snow_depth():
    """
    Verify that invalid snow depth values are rejected.
    """

    assert validate_snow_depth(-5) is False
    assert validate_snow_depth("much snow") is False
    assert validate_snow_depth(True) is False
    assert validate_snow_depth(float("nan")) is False
    assert validate_snow_depth(float("inf")) is False


def test_valid_ice_risk():
    """
    Verify that recognized ice risk categories are accepted.
    """

    assert validate_ice_risk("Low") is True
    assert validate_ice_risk("Medium") is True
    assert validate_ice_risk("High") is True


def test_missing_ice_risk():
    """
    Verify that missing ice risk information is accepted
    as unknown.
    """

    assert validate_ice_risk(None) is True


def test_invalid_ice_risk():
    """
    Verify that unsupported ice risk values are rejected.
    """

    assert validate_ice_risk("Extreme") is False
    assert validate_ice_risk("low") is False
    assert validate_ice_risk("") is False
    assert validate_ice_risk(10) is False
    assert validate_ice_risk(True) is False
