from pydantic import BaseModel


class DashboardSummary(BaseModel):
    active_alerts: int
    critical_alerts: int
    total_sensors: int
    active_sensors: int
    zones_count: int
    last_hour_readings: int
