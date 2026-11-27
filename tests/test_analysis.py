"""
Unit tests for the SnowHeightTracker analysis module.

These tests verify that winter condition data is
extracted correctly from street segments.
"""

from datetime import datetime, timezone

from app.analysis import analyze_segment, is_data_recent, analyze_route


def test_valid_segment_analysis():
    """
    Verify that winter condition data is extracted
    correctly from a valid street segment.
    """

    segment_data = {
        "id": "A-segment-1",
        "removal_status": "planned",
        "station_snow_depth_cm": 8,
        "ice_risk": "High"
    }

    result = analyze_segment(segment_data)

    assert result["segment_id"] == "A-segment-1"
    assert result["removal_status"] == "planned"
    assert result["station_snow_depth_cm"] == 8
    assert result["ice_risk"] == "High"


def test_missing_weather_data():
    """
    Verify that missing weather information remains
    unknown instead of being replaced with zero.
    """

    segment_data = {
        "id": "B-segment-1",
        "removal_status": "unknown"
    }

    result = analyze_segment(segment_data)

    assert result["segment_id"] == "B-segment-1"
    assert result["removal_status"] == "unknown"
    assert result["station_snow_depth_cm"] is None
    assert result["ice_risk"] is None


def test_invalid_segment_analysis():
    """
    Verify that invalid segment structures are rejected.
    """

    assert analyze_segment(None) is None
    assert analyze_segment("segment") is None
    assert analyze_segment({}) is None
    assert analyze_segment({"id": ""}) is None


def test_invalid_snow_depth_analysis():
    """
    Verify that the analysis rejects invalid snow depth values.

    Negative snow measurements should not be accepted
    as valid weather information.
    """

    segment_data = {
        "id": "A-segment-2",
        "removal_status": "planned",
        "station_snow_depth_cm": -5,
        "ice_risk": "High"
    }

    # Invalid snow depth should prevent segment analysis.
    assert analyze_segment(segment_data) is None


def test_invalid_ice_risk_analysis():
    """
    Verify that unsupported ice risk categories
    are rejected during segment analysis.
    """

    segment_data = {
        "id": "A-segment-3",
        "removal_status": "planned",
        "station_snow_depth_cm": 8,
        "ice_risk": "Extreme"
    }

    # Unsupported ice risk values should invalidate the analysis.
    assert analyze_segment(segment_data) is None


def test_invalid_removal_status_analysis():
    """
    Verify that unsupported snow-removal statuses
    are rejected during segment analysis.
    """

    segment_data = {
        "id": "A-segment-4",
        "removal_status": "banana",
        "station_snow_depth_cm": 8,
        "ice_risk": "Medium"
    }

    # An unsupported removal status should invalidate the analysis.
    assert analyze_segment(segment_data) is None

def test_recent_data():
    current_time = datetime(2026, 11, 26, 18, 0, tzinfo=timezone.utc)
    timestamp = "2026-11-26T16:00:00Z"

    assert is_data_recent(timestamp, current_time=current_time) is True


def test_outdated_data():
    current_time = datetime(2026, 11, 26, 18, 0, tzinfo=timezone.utc)
    timestamp = "2026-11-23T18:00:00Z"

    assert is_data_recent(timestamp, current_time=current_time) is False


def test_future_timestamp():
    current_time = datetime(2026, 11, 26, 18, 0, tzinfo=timezone.utc)
    timestamp = "2026-11-27T18:00:00Z"

    assert is_data_recent(timestamp, current_time=current_time) is False


def test_missing_timestamp():
    assert is_data_recent(None) is False
    assert is_data_recent("invalid date") is False


def test_missing_removal_timestamp():
    """
    Verify that missing snow-removal timestamps
    are treated as unverified information.
    """

    segment_data = {
        "id": "A-segment-5",
        "removal_status": "planned",
        "station_snow_depth_cm": 8,
        "ice_risk": "Medium"
    }

    result = analyze_segment(segment_data)

    assert result is not None
    assert result["removal_updated_at"] is None
    assert result["removal_data_recent"] is False


def test_invalid_removal_timestamp():
    """
    Verify that invalid timestamps are not
    considered recent snow-removal information.
    """

    segment_data = {
        "id": "A-segment-6",
        "removal_status": "planned",
        "station_snow_depth_cm": 8,
        "ice_risk": "High",
        "removal_updated_at": "invalid date"
    }

    result = analyze_segment(segment_data)

    assert result is not None
    assert result["removal_data_recent"] is False


def test_valid_route_analysis():
    """
    Verify that all segments in a valid route
    are analyzed correctly.
    """

    route_data = {
        "id": "A",
        "distance_m": 6400,
        "duration_seconds": 1080,
        "segments": [
            {
                "id": "A-segment-1",
                "removal_status": "planned",
                "station_snow_depth_cm": 8,
                "ice_risk": "High"
            },
            {
                "id": "A-segment-2",
                "removal_status": "cleared",
                "station_snow_depth_cm": 3,
                "ice_risk": "Low"
            }
        ]
    }

    # Analyze every street segment in the route.
    result = analyze_route(route_data)

    # Verify the route and its analyzed segments.
    assert result is not None
    assert result["route_id"] == "A"
    assert len(result["segments"]) == 2

    assert result["segments"][0]["ice_risk"] == "High"
    assert result["segments"][1]["removal_status"] == "cleared"


def test_invalid_route_analysis():
    """
    Verify that a route is rejected when one
    of its segments contains invalid weather data.
    """

    route_data = {
        "id": "B",
        "distance_m": 5900,
        "duration_seconds": 1200,
        "segments": [
            {
                "id": "B-segment-1",
                "removal_status": "planned",
                "station_snow_depth_cm": -5,
                "ice_risk": "Medium"
            }
        ]
    }

    # Negative snow depth should invalidate the analysis.
    assert analyze_route(route_data) is None
