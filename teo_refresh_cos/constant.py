class RefreshType:
    """
    刷新类型
    """

    URL = "purge_url"  # URL刷新
    PREFIX = "purge_prefix"  # 目录刷新
    HOST = "purge_host"  # Hostname刷新
    ALL = "purge_all"  # 站点下全部缓存刷新


class RefreshMethod:
    """
    刷新方式
    """

    INVALIDATE = "invalidate"  # 仅刷新目录下产生了更新的资源
    DELETE = "delete"  # 无论目录下资源是否更新都刷新节点资源
