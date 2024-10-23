from dataclasses import dataclass

from teo_refresh_cos.constant import RefreshMethod, RefreshType


@dataclass
class RefreshConfig:
    zone_id: str
    domain: str
    refresh_type: str = RefreshType.URL
    refresh_method: str = RefreshMethod.INVALIDATE
    index_refresh_host: bool = False
