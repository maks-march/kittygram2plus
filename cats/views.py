from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.throttling import AnonRateThrottle


from .throttling import WorkingHoursRateThrottle
from .models import Achievement, Cat, User
from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .pagination import CatsPagination


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    throttle_classes = (WorkingHoursRateThrottle, AnonRateThrottle,)
    pagination_class = CatsPagination
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter,)
    filter_fields = ('color', 'birth_year')
    search_fields = ('name',)
    ordering_fields = ('name', 'birth_year')
    ordering = ('birth_year',)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # def get_queryset(self):
    #     queryset = Cat.objects.all()
    #     color = self.kwargs['color']
    #     # Через ORM отфильтровать объекты модели Cat
    #     # по значению параметра color, полученного в запросе
    #     queryset = queryset.filter(color=color)
    #     return queryset


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
