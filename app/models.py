
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class StreetSegment:
    segment_id: str
    street_name: str | None
    length_m: float | None
    snow_removal_code: int | None = None
    snow_removal_updated_at: datetime | None = None


@dataclass
class Route:
    route_id: str
    travel_mode: str
    distance_km: float
    duration_min: float
    segments: list[StreetSegment] = field(default_factory=list)
