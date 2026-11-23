from math import isfinite
from datetime import datetime


def validate_distance(distance_m):
    """
    Validate the distance of a route or street segment.

    The distance must be a positive, finite number expressed
    in meters. Invalid values such as negative numbers, zero,
    booleans, NaN, and infinity are rejected.

    Args:
        distance_m: Distance value in meters.

    Returns:
        bool: True if the distance is valid, False otherwise.
    """

    # Ensure the distance is a numeric value.
    if not isinstance(distance_m, (int, float)):
        return False

    # Reject booleans, which Python considers a subtype of int.
    if isinstance(distance_m, bool):
        return False

    # Reject zero, negative distances, NaN, and infinite values.
    if not isfinite(distance_m) or distance_m <= 0:
        return False

    return True


def validate_duration(duration_seconds):
    """
    Validate the estimated travel duration of a route.

    Travel duration must be a positive, finite number
    expressed in seconds.

    Args:
        duration_seconds: Estimated travel time in seconds.

    Returns:
        bool: True if the duration is valid, False otherwise.
    """

    # Check that the duration is represented by a number.
    if not isinstance(duration_seconds, (int, float)):
        return False

    # Prevent boolean values from being accepted as numbers.
    if isinstance(duration_seconds, bool):
        return False

    # A valid duration cannot be zero, negative, or non-finite.
    if not isfinite(duration_seconds) or duration_seconds <= 0:
        return False

    return True


def validate_segments(segments):
    """
    Validate the structure of a route's street segments.

    Each route contains a list of street segments.
    Every segment must be represented as a dictionary
    containing a non-empty string identifier.

    An empty list is currently accepted because this
    function checks structure rather than route completeness.

    Args:
        segments: Collection of street segments.

    Returns:
        bool: True if the segment structure is valid,
              False otherwise.
    """

    # The segments field must contain a list.
    if not isinstance(segments, list):
        return False

    # Examine each segment individually.
    for segment in segments:

        # Each segment must be a dictionary.
        if not isinstance(segment, dict):
            return False

        # Retrieve the segment identifier.
        segment_id = segment.get("id")

        # Segment identifiers must be strings.
        if not isinstance(segment_id, str):
            return False

        # Reject empty identifiers or identifiers containing only spaces.
        if not segment_id.strip():
            return False

    return True


def validate_removal_status(status):
    """
    Validate a normalized snow-removal status.

    Snow-removal information helps the application describe
    street conditions and support route analysis.

    The accepted statuses are currently a provisional set
    and may be updated to match the backend data contract.

    Args:
        status: Snow-removal status to validate.

    Returns:
        bool: True if the status is recognized,
              False otherwise.
    """

    # Define the currently accepted normalized status values.
    valid_statuses = {
        "snowy",
        "cleared",
        "planned",
        "rescheduled",
        "to_be_rescheduled",
        "in_progress",
        "unknown"
    }

    # Status values must be represented as strings.
    if not isinstance(status, str):
        return False

    # Accept only statuses included in the allowed set.
    return status in valid_statuses


def validate_timestamp(timestamp):
    """
    Validate the format of a timestamp received from an API.

    Timestamps are important for identifying when snow-removal
    or weather information was last updated.

    This function accepts ISO 8601 datetime strings with
    timezone information, including timestamps ending in 'Z'.

    Note:
        This function checks the timestamp format only.
        It does not determine whether the information is recent.

    Args:
        timestamp: Datetime value represented as a string.

    Returns:
        bool: True if the timestamp is valid and timezone-aware,
              False otherwise.
    """

    # API timestamps must be provided as strings.
    if not isinstance(timestamp, str):
        return False

    try:
        # Convert the UTC indicator 'Z' into an explicit UTC offset
        # before parsing the datetime value.
        parsed_date = datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )

        # Require timezone information to avoid ambiguous timestamps.
        return parsed_date.tzinfo is not None

    except ValueError:
        # Reject strings that cannot be interpreted as valid datetimes.
        return False


def validate_route(route):
    """
    Validate the basic structure of a route.

    A valid route must contain:
        - A non-empty string identifier.
        - A positive distance in meters.
        - A positive estimated duration in seconds.
        - A structurally valid list of street segments.

    This function reuses the individual validation functions
    to ensure consistent checks across the application.

    Note:
        This is a structural validation only. It does not
        verify weather conditions, snow depth, ice risk,
        or the completeness of route segment data.

    Args:
        route: Dictionary containing route information.

    Returns:
        bool: True if the route passes all basic validation
              checks, False otherwise.
    """

    # Route data must be represented as a dictionary.
    if not isinstance(route, dict):
        return False

    # Retrieve the route identifier.
    route_id = route.get("id")

    # Reject missing, invalid, or empty route identifiers.
    if not isinstance(route_id, str) or not route_id.strip():
        return False

    # Validate the total route distance.
    if not validate_distance(route.get("distance_m")):
        return False

    # Validate the estimated travel duration.
    if not validate_duration(route.get("duration_seconds")):
        return False

    # Validate the structure of the route's street segments.
    if not validate_segments(route.get("segments")):
        return False

    # The route has passed all basic structural checks.
    return True

def validate_segment_distance(distance_m):
    """
    Validate the distance of an individual street segment.

    Missing values are accepted because some street segments
    may not have distance information available.

    A provided distance must be a positive, finite number.

    Args:
        distance_m: Segment distance in meters or None.

    Returns:
        bool: True if the distance is valid or missing,
              False if it contains an invalid value.
    """

    # Missing information is allowed for individual segments.
    if distance_m is None:
        return True

    # Reuse the existing distance validation rules.
    return validate_distance(distance_m)
