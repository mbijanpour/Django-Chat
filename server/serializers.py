from rest_framework import serializers

from .models import Category, Server, Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'


class ServerSerializer(serializers.ModelSerializer):
    num_members = serializers.SerializerMethodField()
    Channel_server = ChannelSerializer(many=True)

    class Meta:
        model = Server
        exclude = ("member",)

    def get_num_members(self, obj):
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")
        if not num_members:
            data.pop("num_members", None)
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        Model = Category
        fields = '__all__'
