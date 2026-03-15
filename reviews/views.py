from rest_framework import viewsets
from .models import Review
from .serializers import ReviewSerializer
from core.permissions import IsReviewAuthorOrAdmin

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrAdmin]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        serializer.save(author=self.request.user)