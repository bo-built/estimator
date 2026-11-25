from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from rest_framework import status

from catalogue import serializers


class AuthenticatedApiView(APIView):
    def get_permissions(self):
        return [IsAuthenticated()]


class LaborItemsSerializer(AuthenticatedApiView):
    def get(self, request):
        items = request.user.labortype_set.all()
        serializer = serializers.LaborTypeSerializer(items, many=True)

        return Response(serializer.data)


class MaterialItemsSerializer(AuthenticatedApiView):
    def get(self, request):
        items = request.user.materialtype_set.all()
        serializer = serializers.MaterialTypeSerializer(items, many=True)

        return Response(serializer.data)
