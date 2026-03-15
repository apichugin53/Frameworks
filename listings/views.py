from rest_framework import viewsets, permissions
from .models import Listing
from .serializers import ListingSerializer
from core.permissions import IsOwnerOrAdmin


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
def increment_view_count(listing_id, user):
    if user.is_authenticated:
        if not ListingView.objects.filter(listing_id=listing_id, user=user).exists():
            ListingView.objects.create(listing_id=listing_id, user=user)
            Listing.objects.filter(id=listing_id).update(views_count=models.F('views_count') + 1)
    else:
        ListingView.objects.create(listing_id=listing_id)
        Listing.objects.filter(id=listing_id).update(views_count=models.F('views_count') + 1
