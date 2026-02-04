from rest_framework import serializers

from apps.user.models import User


class EmbeddedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'image')
