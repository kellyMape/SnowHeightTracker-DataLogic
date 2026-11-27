"""
Snow condition analysis for SnowHeightTracker.

This module extracts and validates winter condition data
from street segments.

Missing information is preserved as unknown.
Weather station measurements are not treated as actual
snow depth on the road.
"""

from datetime import datetime, timezone, timedelta

from app.data_validator import (
    validate_snow_depth,
    validate_ice_risk,
    validate_removal_status,
    validate_timestamp,
    validate_route
)


def analyze_segment(segment_data):
    """
    Extract and validate winter conditions for a street segment.

    Args:
        segment_data: Dictionary containing segment information.

    Returns:
        dict: Validated winter condition information.
        None: If the segment data is invalid.
    """

    # Verify that the segment is a dictionary.
    if not isinstance(segment_data, dict):
        return None
        

    # Retrieve and validate the segment identifier.
    segment_id = segment_data.get("id")

    if not isinstance(segment_id, str) or not segment_id.strip():
        return None

    # Extract winter condition information.
    removal_status = segment_data.get("removal_status")
    station_snow_depth = segment_data.get("station_snow_depth_cm")
    ice_risk = segment_data.get("ice_risk")

    # Retrieve the latest snow-removal update timestamp.
    removal_updated_at = segment_data.get("removal_updated_at")

    # Validate the snow-removal status when one is provided.
    # Missing information is preserved as unknown.
    if removal_status is not None:
        if not validate_removal_status(removal_status):
            return None


    # Reject invalid snow depth measurements.
    if not validate_snow_depth(station_snow_depth):
        return None

    # Reject unsupported ice risk categories.
    if not validate_ice_risk(ice_risk):
        return None

     # Check whether the snow-removal information is recent.
    # Missing timestamps are treated as unverified.
    removal_data_recent = is_data_recent(removal_updated_at)

    # Return the validated winter condition information.
    return {
        "segment_id": segment_id,
        "removal_status": removal_status,
        "station_snow_depth_cm": station_snow_depth,
        "ice_risk": ice_risk,
        "removal_updated_at": removal_updated_at,
        "removal_data_recent": removal_data_recent
    }

def is_data_recent(timestamp, max_age_hours=24, current_time=None):
    """
    Check whether a timestamp is within an allowed age.

    Args:
        timestamp: ISO 8601 timestamp from the API.
        max_age_hours: Maximum accepted age in hours.
        current_time: Optional reference time for testing.

    Returns:
        bool: True if the timestamp is recent,
              False if it is invalid, missing, old, or in the future.
    """

    # Missing or invalid timestamp formats cannot be verified.
    if not validate_timestamp(timestamp):
        return False

    # The maximum age must be a positive number.
    if not isinstance(max_age_hours, (int, float)):
        return False

    if isinstance(max_age_hours, bool) or not 0 < max_age_hours < float("inf"):
        return False

    # Convert the API timestamp into a datetime object.
    updated_at = datetime.fromisoformat(
        timestamp.replace("Z", "+00:00")
    )

    # Use the current UTC time unless a reference time is provided.
    now = current_time if current_time is not None else datetime.now(timezone.utc)

    # Both timestamps must contain timezone information.
    if not isinstance(now, datetime) or now.tzinfo is None:
        return False

    # Calculate how old the information is.
    age = now - updated_at

    # Reject future timestamps and data older than the allowed limit.
    return timedelta(0) <= age <= timedelta(hours=max_age_hours)


def test_recent_data():
    """
    Verify that data updated recently is accepted.
    """

    current_time = datetime(
        2026, 11, 26, 18, 0, tzinfo=timezone.utc
    )

    timestamp = "2026-11-26T16:00:00Z"

    # Data updated two hours ago should be recent.
    assert is_data_recent(timestamp, current_time=current_time) is True


def test_outdated_data():
    """
    Verify that data older than 24 hours is rejected.
    """

    current_time = datetime(
        2026, 11, 26, 18, 0, tzinfo=timezone.utc
    )

    timestamp = "2026-11-23T18:00:00Z"

    # Data updated three days ago is considered outdated.
    assert is_data_recent(timestamp, current_time=current_time) is False


def test_future_timestamp():
    """
    Verify that future timestamps are rejected.
    """

    current_time = datetime(
        2026, 11, 26, 18, 0, tzinfo=timezone.utc
    )

    timestamp = "2026-11-27T18:00:00Z"

    # Future timestamps should not be considered recent.
    assert is_data_recent(timestamp, current_time=current_time) is False


def test_missing_timestamp():
    """
    Verify that missing or invalid timestamps are rejected.
    """

    assert is_data_recent(None) is False
    assert is_data_recent("invalid date") is False


def analyze_route(route_data):
    """
    Analyze winter conditions for all segments in a route.

    Each street segment is analyzed individually using
    the existing analyze_segment() function.

    Args:
        route_data: Dictionary containing route information.

    Returns:
        dict: Route identifier and analyzed street segments.
        None: If the route or any segment is invalid.
    """

    # Validate the basic structure of the route.
    if not validate_route(route_data):
        return None

    # Store the winter condition analysis for each segment.
    analyzed_segments = []

    for segment_data in route_data["segments"]:

        # Reuse the existing segment analysis function.
        result = analyze_segment(segment_data)

        # Reject the route if a segment contains invalid data.
        if result is None:
            return None

        analyzed_segments.append(result)

    # Return the route identifier and its analyzed segments.
    return {
        "route_id": route_data["id"],
        "segments": analyzed_segments
    }
