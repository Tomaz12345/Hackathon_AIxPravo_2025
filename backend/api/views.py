import os
import logging
import requests
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BrandCheck
from .serializers import BrandCheckSerializer
from rest_framework.generics import get_object_or_404
import json
#import tensorflow as tf
from sentence_transformers import SentenceTransformer
from .utils.prompting import get_prompt_main, get_prompt_evaluation
from .utils.data import get_specific_data
from .utils.deepseek_interface import get_deepseek_response
from .utils.other import get_message_status

# Set up logging
logger = logging.getLogger(__name__)

class BrandCheckViewSet(viewsets.ModelViewSet):
    queryset = BrandCheck.objects.all()
    serializer_class = BrandCheckSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            # Perform the brand check and update the instance
            self.perform_brand_check(instance)
        
            return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_brand_check(self, instance):
        """Performs the actual brand check against databases and using AI"""
        # Here we would normally do real API calls to trademark databases
        # For demonstration, we'll simulate the checks
        
        # Simulated database checks
        euipo_result = self.check_euipo_database(instance.brandName, instance.goodsServices)
        wipo_result = self.check_wipo_database(instance.brandName, instance.goodsServices)
        sipo_result = self.check_sipo_database(instance.brandName, instance.goodsServices)
        
        # Image similarity check would be done here
        # For this demo, we'll simulate it
        image_check_result = "Logo analysis shows no significant similarity with registered trademarks."
        
        # Use LLM to analyze results
        ai_feedback = self.get_ai_feedback(
            instance.brandName,
            instance.goodsServices,
            euipo_result,
            wipo_result,
            sipo_result,
            image_check_result
        )
        
        # Determine overall status based on AI feedback
        status = self.determine_status(ai_feedback)
        
        # Update the instance with results
        instance.euipoResults = euipo_result
        instance.wipoResults = wipo_result
        instance.sipoResults = sipo_result
        instance.feedback = ai_feedback
        instance.status = status
        instance.save()
    
    def check_euipo_database(self, brand_name, goods_services):
        euipo_data = get_specific_data("euipo", brand_name, goods_services)
        return euipo_data
    
    def check_wipo_database(self, brand_name, goods_services):
        wipo_data = get_specific_data("wipo", brand_name, goods_services)
        return wipo_data

    def check_sipo_database(self, brand_name, goods_services):
        sipo_data = get_specific_data("sipo", brand_name, goods_services)
        return sipo_data

    def get_ai_feedback(self, brand_name, goods_services, euipo_result, wipo_result, sipo_result, image_result):
        # In a real app, you would call an AI service like OpenAI's API
        # For demonstration purposes, let's simulate an OpenAI call
        
        try:
            # Prepare the prompt
            message = get_prompt_main(brand_name, goods_services)

            # Call the Deepseek API
            response = get_deepseek_response(message)
            print(f"full get ai feedback response: {response}")

            return response["choices"][0]["message"]["content"][:]
            
        except Exception as e:
            # Fallback response in case of API errors
            print(f"Error calling Deepseek: {e}")
            return f"Based on preliminary analysis, the brand '{brand_name}' appears to have moderate potential for registration, but further legal consultation is recommended due to some potential similarities found in the EUIPO database."
    
    
    def determine_status(self, feedback):
        # Analyze feedback to determine status
        try:
            # Prepare the prompt
            message = get_prompt_evaluation(feedback)

            # Call the Deepseek API
            response = get_deepseek_response(message)
            resp_message = response["choices"][0]["message"]["content"][:]
            print(f"full determine status message: {resp_message}")

            return get_message_status(resp_message)
        except Exception as e:
            print(f"Error calling Deepseek: {e}")
            return "caution"


    
    def retrieve(self, request, pk=None):
        brand_check = get_object_or_404(BrandCheck, pk=pk)
        serializer = self.get_serializer(brand_check)
        return Response(serializer.data)