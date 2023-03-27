from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from supabase import create_client, Client
import environ  

env = environ.Env()
environ.Env.read_env()

url: str = env("SUPABASE_URL")
key: str = env("SUPABASE_KEY")
supabase_client: Client = create_client(url, key)

# Create your views here.
class DataIngressView(GenericAPIView):
    
    def get(): 
        return Response(200)
