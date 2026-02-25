import aiohttp
from datetime import datetime

class AxleApi:
    """
    Production API client for Axle Energy VPP events.
    
    Fetches real event data from Axle and formats it for the coordinator/sensors.
    """

    BASE_URL = "https://api.axle.energy/vpp/home-assistant/event"

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }

    async def async_get_event(self) -> dict | None:
        """
        Fetch the latest VPP event from Axle.

        Returns:
            dict with keys: start_time, end_time, import_export, updated_at
            or None if no event is active.
        Raises:
            Exception on network or API errors.
        """
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(self.BASE_URL) as resp:
                    if resp.status != 200:
                        raise Exception(f"Axle API returned status {resp.status}")
                    data = await resp.json()
        except Exception as err:
            raise Exception(f"Error fetching Axle API: {err}") from err

        # If API returns nothing or missing start_time, treat as no event
        if not data or "start_time" not in data:
            return None

        # Map API response to coordinator format
        event = {
            "start_time": data.get("start_time"),               # ISO 8601 string
            "end_time": data.get("end_time"),                   # ISO 8601 string
            "import_export": data.get("import_export", 0),      # Default to 0
            "updated_at": data.get("updated_at", datetime.utcnow().isoformat() + "Z"),
        }

        return event
