
from app.models import Route, StreetSegment


def create_sample_routes() -> list[Route]:
    """
    Create four fictional routes for testing.
    These are not real-time snow conditions.
    """

    route_a = Route(
        route_id="A",
        travel_mode="driving",
        distance_km=6.4,
        duration_min=18.0,
        segments=[
            StreetSegment(
                segment_id="A1",
                street_name="Côte-des-Neiges",
                length_m=500.0,
                snow_removal_code=2
            ),
            StreetSegment(
                segment_id="A2",
                street_name="Queen Mary",
                length_m=700.0,
                snow_removal_code=1
            )
        ]
    )

    route_b = Route(
        route_id="B",
        travel_mode="driving",
        distance_km=5.9,
        duration_min=20.0,
        segments=[
            StreetSegment(
                segment_id="B1",
                street_name="Sherbrooke",
                length_m=900.0,
                snow_removal_code=0
            )
        ]
    )

    route_c = Route(
        route_id="C",
        travel_mode="driving",
        distance_km=5.6,
        duration_min=21.0,
        segments=[
            StreetSegment(
                segment_id="C1",
                street_name="Saint-Denis",
                length_m=800.0,
                snow_removal_code=1
            )
        ]
    )

    route_d = Route(
        route_id="D",
        travel_mode="driving",
        distance_km=7.2,
        duration_min=26.0,
        segments=[
            StreetSegment(
                segment_id="D1",
                street_name="Papineau",
                length_m=600.0,
                snow_removal_code=None
            )
        ]
    )

    return [route_a, route_b, route_c, route_d]

from app.models import Route, StreetSegment


def create_sample_routes() -> list[Route]:
    """
    Create four fictional routes for testing.
    These are not real-time snow conditions.
    """

    route_a = Route(
        route_id="A",
        travel_mode="driving",
        distance_km=6.4,
        duration_min=18.0,
        segments=[
            StreetSegment(
                segment_id="A1",
                street_name="Côte-des-Neiges",
                length_m=500.0,
                snow_removal_code=2
            ),
            StreetSegment(
                segment_id="A2",
                street_name="Queen Mary",
                length_m=700.0,
                snow_removal_code=1
            )
        ]
    )

    route_b = Route(
        route_id="B",
        travel_mode="driving",
        distance_km=5.9,
        duration_min=20.0,
        segments=[
            StreetSegment(
                segment_id="B1",
                street_name="Sherbrooke",
                length_m=900.0,
                snow_removal_code=0
            )
        ]
    )

    route_c = Route(
        route_id="C",
        travel_mode="driving",
        distance_km=5.6,
        duration_min=21.0,
        segments=[
            StreetSegment(
                segment_id="C1",
                street_name="Saint-Denis",
                length_m=800.0,
                snow_removal_code=1
            )
        ]
    )

    route_d = Route(
        route_id="D",
        travel_mode="driving",
        distance_km=7.2,
        duration_min=26.0,
        segments=[
            StreetSegment(
                segment_id="D1",
                street_name="Papineau",
                length_m=600.0,
                snow_removal_code=None
            )
        ]
    )

    return [route_a, route_b, route_c, route_d]
