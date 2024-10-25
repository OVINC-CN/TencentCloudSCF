from typing import Generator

import httpx

from vpc_securitygroup_teo.config import Config


class TEO:
    """
    TEO Client
    """

    def get_eo_ips(self) -> Generator[str, None, None]:
        """
        获取回源IP列表
        """
        with httpx.Client(timeout=60) as client:
            try:
                response = client.get(Config.teo_ips_api)
                response.raise_for_status()
            except Exception as err:
                print("Load TEO IPs Failed: %s", err)
                raise err
        ips = (ip for ip in response.content.decode().split("\n") if ip)
        print("Load TEO IPs Success")
        return ips
