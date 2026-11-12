
from app.models import Route, StreetSegment


def test_create_street_segment():
    segment = StreetSegment(
        segment_id="S001",
        street_name="Côte-des-Neiges",
        length_m=500.0,
        snow_removal_code=2
    )

    assert segment.segment_id == "S001"
    assert segment.length_m == 500.0
    assert segment.snow_removal_code == 2


def test_create_route():
    route = Route(
        route_id="A",
        travel_mode="driving",
        distance_km=6.4,
        duration_min=18.0
    )

    assert route.route_id == "A"
    assert route.travel_mode == "driving"
    assert route.distance_km == 6.4
    assert route.segments == []


def test_route_contains_segment():
    segment = StreetSegment(
        segment_id="S002",
        street_name="Sherbrooke",
        length_m=300.0
    )

    route = Route(
        route_id="B",
        travel_mode="driving",
        distance_km=4.5,
        duration_min=15.0,
        segments=[segment]
    )

    assert len(route.segments) == 1
    assert route.segments[0].street_name == "Sherbrooke"
