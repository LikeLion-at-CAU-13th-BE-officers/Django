from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils.timezone import now
import datetime

class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user

class BlockDuringMaintenanceHours(BasePermission):
    message = "현재는 API 사용이 제한된 시간입니다."

    def has_permission(self, request, view):
        current_time = now().time()
        print(current_time)

        start = datetime.time(22, 0, 0)
        end = datetime.time(7, 0, 0)

        if datetime.time(0, 0, 0) <= current_time <= start and datetime.time(0, 0, 0) <= current_time <= end:
            return False

        return True
