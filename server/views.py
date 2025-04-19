from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count

from .models import Category, Server, Channel
from .serializers import ServerSerializer
from accounts.models import Accounts


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get("category")
        by_user = request.query_params.get("by_user") == "true"
        with_num_members = request.query_params.get(
            "with_num_members") == "true"
        qty = request.query_params.get("qty")
        by_serverId = request.query_params.get("by_serverId")

        if by_user and not request.user.is_authenticated:
            raise AuthenticationFailed(f"You must login first!")

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if qty:
            self.queryset = self.queryset[: int(qty)]

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if by_user:
            user = request.user.id
            self.queryset = self.queryset.filter(member=user)

        if by_serverId:
            try:
                self.queryset = self.queryset.filter(pk=by_serverId)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with {by_serverId} does not exist!")
            except ValueError:
                raise ValidationError(
                    detail=f"Your server Id is not a valid value")

        serializer = ServerSerializer(self.queryset, many=True, context={
                                      "num_member": with_num_members})
        return Response(serializer.data)

    def listMembers(self, request):
        user = request.post
