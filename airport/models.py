from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class AirplaneType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=63, unique=True)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType, on_delete=models.CASCADE, related_name="airplanes"
    )

    @property
    def capacity(self) -> int:
        """PositiveInteger class isn't provide __mul__"""

        row = int(self.rows)
        seats = int(self.seats_in_row)
        return row * seats

    def __str__(self):
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        unique_together = (
            "first_name",
            "last_name",
        )

    def __str__(self):
        return self.full_name


class Airport(models.Model):
    name = models.CharField(max_length=127, unique=True)
    closest_big_city = models.CharField(max_length=127)

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="source_routes"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="destination_routes"
    )
    distance = models.PositiveIntegerField()

    class Meta:
        unique_together = (
            "source",
            "destination",
        )

    def __str__(self):
        return f"{self.source} -> {self.destination}"


class Flight(models.Model):
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="flights"
    )
    airplane = models.ForeignKey(
        Airplane, on_delete=models.CASCADE, related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="flights")

    def __str__(self):
        return f"{self.route} ({self.departure_time})"

    def clean(self):
        if self.arrival_time <= self.departure_time:
            raise ValidationError(
                f"Incorrect data(inconsistency with departure or arrival time)"
            )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at)


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        unique_together = ("row", "seat", "flight")

    def clean(self):
        if self.row > self.flight.airplane.rows:
            raise ValidationError(
                f"row must be in range (1, {self.flight.airplane.rows})"
            )
        if self.seat > self.flight.airplane.seats_in_row:
            raise ValidationError(
                f"seat must be in range (1, {self.flight.airplane.seats_in_row})"
            )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{self.flight} (row: {self.row}, seat:{self.seat})"
