import json
import os
from typing import Dict

from teo_refresh_cos.model import RefreshConfig


class Config:
    """
    配置
    """

    tcloud_secret_id: str = os.getenv("TCLOUD_SECRET_ID")
    tcloud_secret_key: str = os.getenv("TCLOUD_SECRET_KEY")

    refresh_config: Dict[str, RefreshConfig] = {
        bucket_name: RefreshConfig(**config)
        for bucket_name, config in json.loads(os.getenv("REFRESH_CONFIG", "{}")).items()
    }
