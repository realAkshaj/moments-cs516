from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import os
from config.api_keys import AZURE_VISION_KEY, AZURE_VISION_ENDPOINT

class AzureVisionService:
    def __init__(self):
        self.client = ComputerVisionClient(
            AZURE_VISION_ENDPOINT, 
            CognitiveServicesCredentials(AZURE_VISION_KEY)
        )
    
    def generate_alt_text(self, image_path):
        """Generate alternative text for an image"""
        try:
            with open(image_path, "rb") as image_stream:
                # Analyze image for description
                analysis = self.client.describe_image_in_stream(
                    image_stream, 
                    max_candidates=1,
                    language='en'
                )
                
                if analysis.captions:
                    return analysis.captions[0].text
                else:
                    return "Image content could not be described"
                    
        except Exception as e:
            print(f"Error generating alt text: {e}")
            return "Image description unavailable"
    
    def detect_objects(self, image_path):
        """Detect objects in image for search functionality"""
        try:
            with open(image_path, "rb") as image_stream:
                # Analyze image for objects and tags
                analysis = self.client.analyze_image_in_stream(
                    image_stream,
                    visual_features=[
                        VisualFeatureTypes.objects,
                        VisualFeatureTypes.tags,
                        VisualFeatureTypes.categories
                    ]
                )
                
                # Combine objects, tags, and categories
                detected_items = []
                
                # Add object names
                if analysis.objects:
                    detected_items.extend([obj.object_property for obj in analysis.objects])
                
                # Add high-confidence tags
                if analysis.tags:
                    detected_items.extend([
                        tag.name for tag in analysis.tags 
                        if tag.confidence > 0.7
                    ])
                
                # Add categories
                if analysis.categories:
                    detected_items.extend([
                        cat.name.split('_')[-1] for cat in analysis.categories 
                        if cat.score > 0.5
                    ])
                
                return list(set(detected_items))  # Remove duplicates
                
        except Exception as e:
            print(f"Error detecting objects: {e}")
            return []

# Create global instance
vision_service = AzureVisionService()