from rest_framework.filters import BaseFilterBackend


class SelfFilterBackend(BaseFilterBackend):
    """
    func: Filter data of database which belongs to current logged-in user.
    """
    def filter_queryset(self, request, queryset, view):
        if request.user.id:
            return queryset.filter(user=request.user)
        else:
            return
