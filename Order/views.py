from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from Order.models import Order
from Order.serializers import OrderSerializer


class OrderThrottle(UserRateThrottle):
    rate = '5/min'

class OrderViewSet(ModelViewSet):
    throttle_classes = [OrderThrottle]
    permission_classes = [IsAuthenticated]

    http_method_names = ['get', 'post']
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)