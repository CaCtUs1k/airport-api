from django.db.models import F, Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from airport.models import (
    AirplaneType,
    Airplane,
    Crew,
    Airport,
    Route,
    Flight,
    Order,
)
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.serializers import (
    AirplaneTypeSerializer,
    AirplaneSerializer,
    CrewSerializer,
    AirportSerializer,
    RouteSerializer,
    FlightSerializer,
    OrderSerializer,
    AirplaneListSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    RouteListSerializer,
)


class AirplaneTypeViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        return self.serializer_class


class CrewViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        queryset = self.queryset

        if first_name:
            queryset = queryset.filter(first_name=first_name)

        if last_name:
            queryset = queryset.filter(last_name=last_name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "first_name",
                type=OpenApiTypes.ANY,
                description="Filter by crew's first name (ex. ?first_name=John)",
            ),
            OpenApiParameter(
                "last_name",
                type=OpenApiTypes.ANY,
                description=(
                    "Filter by crew's last_name " "(ex. ?last_name=Doe)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AirportViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        name = self.request.query_params.get("name")
        closest_big_city = self.request.query_params.get("city")
        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)
        if closest_big_city:
            queryset = queryset.filter(
                closest_big_city__icontains=closest_big_city
            )
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=OpenApiTypes.ANY,
                description="Filter by name (ex. ?name=San Rafael Airport)",
            ),
            OpenApiParameter(
                "city",
                type=OpenApiTypes.ANY,
                description=(
                    "Filter by closest_big_city " "(ex. ?city=San Rafael)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RouteViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        return self.serializer_class

    def get_queryset(self):
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("city")
        queryset = self.queryset

        if source:
            queryset = queryset.filter(source__icontains=source)
        if destination:
            queryset = queryset.filter(destination__icontains=destination)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "first_name",
                type=OpenApiTypes.ANY,
                description="Filter by crew's first name (ex. ?first_name=John)",
            ),
            OpenApiParameter(
                "last_name",
                type=OpenApiTypes.ANY,
                description=(
                    "Filter by crew's last_name " "(ex. ?last_name=Doe)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related(
        "route__source", "route__destination", "airplane"
    ).annotate(
        tickets_available=(
            F("airplane__rows") * F("airplane__seats_in_row")
            - Count("tickets")
        )
    )
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return self.serializer_class

    def get_queryset(self):
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        queryset = self.queryset

        if source:
            queryset = queryset.filter(source__icontains=source)
        if destination:
            queryset = queryset.filter(destination__icontains=destination)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "source",
                type=OpenApiTypes.ANY,
                description="Filter by source (ex. ?source=San Rafael Airport)",
            ),
            OpenApiParameter(
                "destination",
                type=OpenApiTypes.ANY,
                description=(
                    "Filter by destination "
                    "(ex. ?destination=San Rafael Airport)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
