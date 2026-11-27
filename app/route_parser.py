"""
Convert validated API route data into Python models.

The backend provides distances in meters and durations
in seconds. This module converts those values into the
units used by the application's Route model.
"""

from app.models import Route, StreetSegment
from app.data_validator import validate_route, validate_segment_distance


def parse_route(route_data, travel_mode="driving"):
    """
    Convert a valid API route dictionary into a Route object.

    Args:
        route_data: Dictionary containing route information.
        travel_mode: Transportation mode for the route.

    Returns:
        Route: A Route object containing converted values.
        None: If the route data is invalid.
    """

    # Reject invalid route data before processing it.
    if not validate_route(route_data):
        return None

    # Convert the route's street segments into model objects.
    segments = []

    for segment_data in route_data["segments"]:
                # Reject routes containing invalid segment distances.
        if not validate_segment_distance(segment_data.get("distance_m")):
            return None
        segment = StreetSegment(
            segment_id=segment_data["id"],
            street_name=segment_data.get("street_name"),
            length_m=segment_data.get("distance_m")
        )

        segments.append(segment)

    # Convert meters to kilometers and seconds to minutes.
    return Route(
        route_id=route_data["id"],
        travel_mode=travel_mode,
        distance_km=route_data["distance_m"] / 1000,
        duration_min=route_data["duration_seconds"] / 60,
        segments=segments
    )
