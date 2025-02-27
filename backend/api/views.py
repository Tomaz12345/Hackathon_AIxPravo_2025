import os
import requests
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BrandCheck
from .serializers import BrandCheckSerializer

# AI utilities
#import tensorflow as tf
from sentence_transformers import SentenceTransformer
import openai

# Set the OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

class BrandCheckViewSet(viewsets.ModelViewSet):
    queryset = BrandCheck.objects.all()
    serializer_class = BrandCheckSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the basic data first
            instance = serializer.save()
            
            # Now perform the checks and update the instance
            self.perform_brand_check(instance)
            
            # Return the updated instance
            return Response(
                self.get_serializer(instance).data,
                status=status.HTTP_201_CREATED
            )
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
            instance.territories,
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
        # Simulated EUIPO database check
        # In a real app, you would use their API or web scraping
        return f"Found 2 potentially similar marks to '{brand_name}' in different classes. Further analysis recommended."
    
    def check_wipo_database(self, brand_name, goods_services):
        # Simulated WIPO database check
        return f"No direct conflicts found for '{brand_name}' in the Madrid System database for the specified goods and services."
    
    def check_sipo_database(self, brand_name, goods_services):
        # Simulated SIPO database check
        return f"No existing registrations for '{brand_name}' found in the Slovenian Intellectual Property Office database."
    
    def get_ai_feedback(self, brand_name, territories, goods_services, euipo_result, wipo_result, sipo_result, image_result):
        # In a real app, you would call an AI service like OpenAI's API
        # For demonstration purposes, let's simulate an OpenAI call
        
        try:
            # Prepare the prompt
            prompt = f"""
            Analyze the following trademark registration check results:
            
            Brand Name: {brand_name}
            Territories: {territories}
            Goods and Services: {goods_services}
            
            EUIPO Results: {euipo_result}
            WIPO Results: {wipo_result}
            SIPO Results: {sipo_result}
            Logo Analysis: {image_result}
            
            Based on these results, provide a detailed analysis of whether this brand can likely be registered. 
            Include specific recommendations and highlight any potential issues.
            """
            
            # Call the OpenAI API
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a trademark registration expert providing detailed analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            # Extract and return the AI feedback
            return response.choices[0].message.content
            
        except Exception as e:
            # Fallback response in case of API errors
            print(f"Error calling OpenAI API: {e}")
            return f"Based on preliminary analysis, the brand '{brand_name}' appears to have moderate potential for registration, but further legal consultation is recommended due to some potential similarities found in the EUIPO database."
    
    
    def determine_status(self, feedback):
        # Analyze feedback to determine status
        feedback_lower = feedback.lower()
        
        if "cannot be registered" in feedback_lower or "high risk" in feedback_lower or "direct conflict" in feedback_lower:
            return "rejected"
        elif "caution" in feedback_lower or "potential issues" in feedback_lower or "further analysis" in feedback_lower:
            return "caution"
        elif "eligible" in feedback_lower or "likely to be approved" in feedback_lower or "good candidate" in feedback_lower:
            return "approved"
        else:
            return "caution"  # Default to caution if unclear