from rest_framework.pagination import LimitOffsetPagination


class DigLimitOffsetPagination(LimitOffsetPagination):
    """
    @limit_query_param: assign query parameter, otherwise, the query maybe invalidated;
    @offset_query_param:
    """
    default_limit = 10
    max_limit = 50
    limit_query_param = "limit"
    offset_query_param = "offset"


class RecommendPagination(DigLimitOffsetPagination):
    default_limit = 25
    max_limit = 100
    limit_query_param = "limit"
    offset_query_param = "offset"
