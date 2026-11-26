from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

from catalogue.models import WorkType, MaterialType
from catalogue import serializers


class AuthenticatedApiView(APIView):
    def get_permissions(self):
        return [IsAuthenticated()]


class CatalogueItemApi(AuthenticatedApiView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.serializer_class = None
        self.model = None
        self.queryset = None

    def get(self, request):
        items = self.queryset.all()
        serializer = self.serializer_class(items, many=True)

        return Response(serializer.data)

    def patch(self, request, item_pk):
        item = get_object_or_404(
            request.user.materialtype_set,
            pk=item_pk
        )
        try:
            serializer = serializers.MaterialTypeSerializer(
                item,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'status': 'ok',
                        'message': 'Item updated',
                        'data': serializer.data,
                    }
                )
            else:
                return Response(
                    {
                        'status': 'error',
                        'message': 'Data error',
                        'errors': serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:  # noqa TO DO
            return Response(
                {
                    'status': 'error',
                    'message': 'Data error',
                    'errors': 'Unknown Error',
                },
                status=status.HTTP_418_IM_A_TEAPOT
            )

    def post(self, request):
        try:
            new_item = self.model(user=request.user)
            serializer = self.serializer_class(
                new_item,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'status': 'ok',
                        'message': 'Item created',
                        'machine': serializer.data,
                    },
                )
            else:
                return Response(
                    {
                        'status': 'error',
                        'message': 'Error saving',
                        'errors': serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:  # noqa TO DO
            return Response(
                {
                    'status': 'error',
                    'message': 'POST error',
                },
                status=status.HTTP_418_IM_A_TEAPOT
            )


class WorkItemsApi(CatalogueItemApi):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.serializer_class = serializers.WorkTypeSerializer
        self.queryset = request.user.worktype_set
        self.model = WorkType


class MaterialItemsApi(CatalogueItemApi):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.serializer_class = serializers.MaterialTypeSerializer
        self.queryset = request.user.materialtype_set
        self.model = MaterialType
