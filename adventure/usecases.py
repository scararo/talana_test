from __future__ import annotations

from .notifiers import Notifier
from .repositories import JourneyRepository


class StartJourney:
    def __init__(self, repository: JourneyRepository, notifier: Notifier):
        self.repository = repository
        self.notifier = notifier

    def set_params(self, data: dict) -> StartJourney:
        self.data = data
        return self

    def execute(self) -> None:
        car = self.repository.get_or_create_car()
        vehicle = self.repository.get_vehicle(
                            self.data["number_plate"],
                    )

        if not vehicle:
            vehicle = self.repository.create_vehicle(vehicle_type=car, **self.data)

        vehicle = self.repository.add_passengers(vehicle, self.data["passengers"])

        if not vehicle.can_start():
           raise StartJourney.CantStart("vehicle can't start")

        journey = self.repository.create_journey(vehicle)
        self.notifier.send_notifications(journey)
        return journey

    class CantStart(Exception):
        pass


class StopJourney:
    def __init__(self, repository: JourneyRepository, notifier: Notifier):
        self.repository = repository
        self.notifier = notifier

    def set_params(self, data: dict) -> StartJourney:
        self.data = data
        return self

    def execute(self) -> None:
        journey = self.repository.stop_journey(self.data["id"])

        if not journey:
           raise StopJourney.CantStop("can't stop journey")

        self.notifier.send_notifications_stop_journey(journey)

    class CantStop(Exception):
        pass