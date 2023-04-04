from rest_framework import serializers
from .models import ProcessImage

class ProcessImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return ProcessImage.objects.create(
            image_src=validated_data['image_src'], 
            created_at=validated_data['created_at'], 
            updated_at=validated_data['updated_at']
        )

    class Meta:
        model = ProcessImage
        fields = '__all__'