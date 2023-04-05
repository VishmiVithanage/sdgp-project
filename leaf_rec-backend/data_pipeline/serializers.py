from rest_framework import serializers
from .models import ProcessImage

class ProcessImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessImage
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
        
        
class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=False)
    
    def update(self, validated_data):
        file_obj = validated_data['file']
        print('file_obj', validated_data)
        return validated_data
    
    class Meta:
        model = ProcessImage
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'prediction']
        