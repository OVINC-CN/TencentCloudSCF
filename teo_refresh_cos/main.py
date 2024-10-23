from teo_refresh_cos.config import Config
from teo_refresh_cos.constant import RefreshType
from teo_refresh_cos.model import RefreshConfig
from teo_refresh_cos.teo import refresh_api


# pylint: disable=W0613
def refresh(config: RefreshConfig, object_key: str) -> None:
    """
    执行刷新
    """
    # 构造刷新参数
    match config.refresh_type:
        # 全站刷新
        case RefreshType.ALL:
            refresh_api(
                zone_id=config.zone_id,
                refresh_type=config.refresh_type,
                refresh_method=config.refresh_method,
                targets=[],
            )
        # Host刷新
        case RefreshType.HOST:
            refresh_api(
                zone_id=config.zone_id,
                refresh_type=config.refresh_type,
                refresh_method=config.refresh_method,
                targets=[config.domain],
            )
        # 目录刷新
        case RefreshType.PREFIX:
            refresh_api(
                zone_id=config.zone_id,
                refresh_type=config.refresh_type,
                refresh_method=config.refresh_method,
                targets=[f"/{object_key.rsplit('/', 1)[0]}/"],
            )
        # URL刷新
        case RefreshType.URL:
            # 如果是 index.html 则刷新 Host
            if object_key == "index.html" and config.index_refresh_host:
                refresh_api(
                    zone_id=config.zone_id,
                    refresh_type=RefreshType.HOST,
                    refresh_method=config.refresh_method,
                    targets=[config.domain],
                )
            # URL 刷新
            else:
                refresh_api(
                    zone_id=config.zone_id,
                    refresh_type=config.refresh_type,
                    refresh_method=config.refresh_method,
                    targets=[f"http://{config.domain}/{object_key}", f"https://{config.domain}/{object_key}"],
                )
        case _:
            print(f"Refresh Type Not Found: {config.refresh_type}")


def do(record: dict) -> None:
    """
    处理单条记录
    """
    # 获取 COS 信息
    cos = record.get("cos")
    bucket_name = cos.get("cosBucket", {}).get("name")
    if not bucket_name:
        print(f"Bucket Name Not Found: {record}")
        return
    object_key = cos.get("cosObject", {}).get("key", "").split("/", 3)[-1]
    if not object_key:
        print(f"Object Key Not Found: {record}")
        return
    # 获取刷新配置
    config = Config.refresh_config.get(bucket_name)
    if not config:
        print(f"Config Not Found For: {bucket_name}")
        return
    refresh(config=config, object_key=object_key)


# pylint: disable=W0613
def main(event: dict, context: dict) -> None:
    """
    入口函数
    传入参数：https://cloud.tencent.com/document/product/583/9707
    """
    # 获取记录
    records = event.get("Records", [])
    print(f"Event Count: {len(records)}")
    if not records:
        return
    # 逐个处理
    for record in records:
        do(record)
