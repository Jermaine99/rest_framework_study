from django.db import models


# Create your models here.

class UserInfo(models.Model):
    user_type_choices = (
        (1, "普通用户"),
        (2, "VIP用户"),
        (3, "SVIP用户"),

    )
    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    group = models.ForeignKey("UserGroup", on_delete=models.SET_NULL, null=True)
    roles = models.ManyToManyField("Role")


class UserGroup(models.Model):
    tittle = models.CharField(max_length=32)

    def __str__(self):
        return self.tittle


class Role(models.Model):
    role = models.CharField(max_length=32)

    def __str__(self):
        return self.role


class UserToken(models.Model):
    user = models.OneToOneField(to="UserInfo", on_delete=models.SET_NULL, null=True)
    token = models.CharField(max_length=64)
    token_time = models.IntegerField(default=0)
