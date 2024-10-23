import json
from typing import List

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)
from tencentcloud.teo.v20220901 import models, teo_client

from teo_refresh_cos.config import Config


def refresh_api(
    zone_id: str,
    refresh_type: str,
    refresh_method: str,
    targets: List[str] = None,
):
    """
    清除缓存 https://cloud.tencent.com/document/api/1552/80703
    """
    print(f"Refresh Task: {zone_id} {refresh_type} {refresh_method} {targets}")
    try:
        client = teo_client.TeoClient(
            credential=credential.Credential(Config.tcloud_secret_id, Config.tcloud_secret_key),
            region="",
        )
        request = models.CreatePurgeTaskRequest()
        params = {
            "ZoneId": zone_id,
            "Type": refresh_type,
            "Method": refresh_method,
            "Targets": targets,
        }
        request.from_json_string(json.dumps(params))
        response = client.CreatePurgeTask(request)
        print(f"Refresh Result {response.to_json_string()}")
    except TencentCloudSDKException as err:
        print(f"Refresh Failed: {err}")
