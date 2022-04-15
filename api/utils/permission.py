from rest_framework.permissions import BasePermission


class SVPPermission(BasePermission):
    message = '用户必须是SVIP才能访问'       # 当不允许访问时返回的数据

    def has_permission(self, request, view):
        # 加入自己的条件判断
        if request.user.user_type != 3:
            return False    # False 禁止放行
        return True

    def has_object_permission(self, request, view, obj):
        # """ 控制对obj 对象的访问权限，此案例解决所有对对象的访问"""
        # if obj.id > 6:  # 不能访问id 大于6的对象的信息
        #     return False
        return True
