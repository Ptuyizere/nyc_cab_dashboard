from pydantic import BaseModel
from typing import Optional

class TripDetail(BaseModel):
    numeric_id: int
    original_id: str
    vendor_id: Optional[int]
    passenger_count: int
    pickup_datetime: str
    dropoff_datetime: str
    pickup_longitude: float
    pickup_latitude: float
    dropoff_longitude: float
    dropoff_latitude: float
    store_and_fwd_flag: str
    speed_kmph: float
    trip_distance_km: float
    trip_duration: int
    is_round_trip: bool

class StatsSummary(BaseModel):
    total_trips: int
    avg_speed_kmph: float
    avg_duration_s: float
