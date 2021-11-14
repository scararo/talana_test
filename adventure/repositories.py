from django.core.exceptions import ValidationError
from django.utils import timezone

from adventure import models, validate_number_plate


class JourneyRepository:
    def get_or_create_car(self) -> models.VehicleType:
        car, _ = models.VehicleType.objects.get_or_create(name="car", max_capacity=5)
        return car

    def create_vehicle(
        self, name: str, passengers: int, 
        vehicle_type: models.VehicleType,
        number_plate: str,
    ) -> models.Vehicle:

        if validate_number_plate(number_plate):
            return models.Vehicle.objects.create(
                name=name, passengers=passengers, vehicle_type=vehicle_type,
                number_plate=number_plate,
            )
        else:
             raise ValidationError("invalid number plate")


    def create_journey(self, vehicle: models.Vehicle) -> models.Journey:
        return models.Journey.objects.create(
            vehicle=vehicle, start=timezone.now().date()
        )

    def get_vehicle(self, number_plate: str):

        query  =  models.Vehicle.objects.filter(
                            number_plate=number_plate
        )
        if query:
            return query.first()
        else:
            return False

    def add_passengers(self, 
                    vehicle: models.Vehicle, 
                    passengers: int
    ) -> models.Vehicle:

        vehicle.passengers = passengers
        vehicle.save()
        return vehicle


    def stop_journey(self, id: int) -> bool:

        journey = models.Journey.objects.filter(id=id)

        if journey:
            journey = journey.first()
            journey.end = timezone.now().date()
            journey.save()
            return True
        else:
            return False