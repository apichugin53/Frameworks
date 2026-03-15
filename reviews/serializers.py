class ReviewSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['author']