from django.db import models

from user.models import User


class AirplaneType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name


# TODO: calculate seats_number
class Airplane(models.Model):
    name = models.CharField(max_length=63, unique=True)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplanes"
    )

    @property
    def capacity(self) -> int:
        """PositiveInteger class isn't provide __mul__"""

        row = int(self.rows)
        seats = int(self.seats_in_row)
        return row * seats

    def __str__(self):
        return self.name


# TODO: unique together
class Crew(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    class Meta:
        unique_together = ("first_name", "last_name",)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Airport(models.Model):
    name = models.CharField(max_length=127, unique=True)
    closest_big_city = models.CharField(max_length=127)

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="source_routes"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="destination_routes"
        )
    distance = models.PositiveIntegerField()

    class Meta:
        unique_together = ("source", "destination",)

    def __str__(self):
        return f"{self.source} -> {self.destination}"


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.route} ({self.departure_time})"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    def __str__(self):
        return str(self.created_at)


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    class Meta:
        unique_together = ("row", "seat", "flight")

    def __str__(self):
        return f"{self.flight} (row: {self.row}, seat:{self.seat})"
