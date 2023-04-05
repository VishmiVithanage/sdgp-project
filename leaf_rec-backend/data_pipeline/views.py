from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import  MultiPartParser
from rest_framework.response import Response

from .serializers import ProcessImageSerializer, FileUploadSerializer
from .models import ProcessImage
from .data_processing.train_model import train_model

class ProcessImageView(ListAPIView):
    serializer_class = ProcessImageSerializer
    queryset = ProcessImage.objects.all()
    permission_classes = [AllowAny]
    
class FileUploadView(UpdateAPIView):
    parser_classes = (MultiPartParser,)
    queryset = ProcessImage.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [AllowAny]
    
    def put(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = request.FILES['file']
        prediction = train_model(file)
        ProcessImage.create_with_current_datetime(image_src=request.data['image_src'], prediction=prediction)
        return Response({"leaf_prediction": prediction})