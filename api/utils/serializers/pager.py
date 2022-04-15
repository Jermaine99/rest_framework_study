from rest_framework import serializers
from api import models


class PageSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = '__all__'
        depth = 1
