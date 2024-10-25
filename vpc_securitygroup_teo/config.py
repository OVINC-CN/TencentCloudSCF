import os


class Config:
    """
    配置
    """

    security_group_region = os.getenv("APP_SG_REGION")  # 安全组所在地域，如 ap-beijing
    security_group_id = os.getenv("APP_SG_ID")  # 安全组ID
    tmpl_max_ips = int(
        os.getenv("APP_TMPL_MAX_IPS", "20")
    )  # 单个 IP 模板中的 IP 数量，建议提前申请配额到 100，减少需要管理的模板数量
    tmpl_name_prefix = os.getenv("APP_TMPL_PREFIX", "TEO IP Tmpl")
    tmpl_name_format = "{prefix} {date} {index}"

    secret_id = os.getenv("APP_TENCENTCLOUD_SECRETID", "")  # AKID
    secret_key = os.getenv("APP_TENCENTCLOUD_SECRETKEY", "")  # AKSK

    vpc_api_qps = int(os.getenv("APP_VPC_API_QPS", "20"))  # 腾讯云 API QPS 限制

    teo_ips_api = os.getenv(
        "APP_TEO_IPS_API", "https://api.edgeone.ai/ips"
    )  # https://cloud.tencent.com/document/product/1552/100181
