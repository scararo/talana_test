from django.core.checks.messages import Error
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from adventure import models, notifiers, repositories, serializers, usecases


class CreateVehicleAPIView(APIView):
    def post(self, request: Request) -> Response:
        payload = request.data
        vehicle_type = models.VehicleType.objects.get(name=payload["vehicle_type"])
        vehicle = models.Vehicle.objects.create(
            name=payload["name"],
            passengers=payload["passengers"],
            vehicle_type=vehicle_type,
        )
        return Response(
            {
                "id": vehicle.id,
                "name": vehicle.name,
                "passengers": vehicle.passengers,
                "vehicle_type": vehicle.vehicle_type.name,
            },
            status=201,
        )

class BaseJourneyAPIView(generics.CreateAPIView):
    notifier = notifiers.Notifier()
    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()


class StartJourneyAPIView(BaseJourneyAPIView):
    serializer_class = serializers.JourneySerializer

    def perform_create(self, serializer) -> None:
        repo = self.get_repository()
        usecase = usecases.StartJourney(repo, self.notifier).set_params(
            serializer.validated_data
        )
        try:
            usecase.execute()
        except usecases.StartJourney.CantStart as e:
            raise ValidationError({"detail": str(e)})
        except Exception as e:
            raise ValidationError({"detail": str(e)}) 

class StopJourneyAPIView(BaseJourneyAPIView):
    serializer_class = serializers.StopJourneySerializer
    
    def perform_create(self, serializer) -> None:

        repo = self.get_repository()
        usecase = usecases.StopJourney(repo, self.notifier).set_params(
            serializer.validated_data
        )

        try:
            usecase.execute()
        except usecases.StopJourney.CantStop as e:
            raise ValidationError({"detail": str(e)})