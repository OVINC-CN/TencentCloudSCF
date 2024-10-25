import datetime
import time
from collections import defaultdict

from vpc_securitygroup_teo.config import Config
from vpc_securitygroup_teo.teo import TEO
from vpc_securitygroup_teo.vpc import VPC


# pylint: disable=W0613
def main(*args, **kwargs) -> None:
    """
    入口函数
    """
    # 初始化
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    teo = TEO()
    vpc = VPC()
    # 获取 EO 回源 IP
    ips = teo.get_eo_ips()
    # 获取模板列表
    old_template_ids = vpc.list_all_address_templates()
    time.sleep(1.0 / Config.vpc_api_qps)
    # 初始化新的模板列表
    new_template_map = defaultdict(list)
    new_template_ids = []
    # IP 分组
    for index, ip in enumerate(ips):
        tmpl_index = index // Config.tmpl_max_ips
        new_template_map[tmpl_index].append(ip)
    print(f"{index + 1} IPs into {len(new_template_map.keys())} groups")
    # 创建新的模板列表
    for index, ips in new_template_map.items():
        new_template_ids.append(vpc.create_address_template(date=timestamp, index=index, ips=ips))
        time.sleep(1.0 / Config.vpc_api_qps)
    # 绑定到安全组
    vpc.create_security_group_policy(new_template_ids)
    time.sleep(1.0 / Config.vpc_api_qps)
    # 删除旧模板
    for tmpl_id in old_template_ids:
        vpc.delete_address_template(tmpl_id)
        time.sleep(1.0 / Config.vpc_api_qps)
