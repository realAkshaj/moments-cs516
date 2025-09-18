from utils.azure_vision import vision_service
import os

def test_vision_api():
    # Test with a sample image - we'll create one
    print("Testing Azure Vision API...")
    
    # Check if there are any existing images in the app
    test_paths = [
        'moments/static/uploads',
        'moments/static/avatars'
    ]
    
    found_image = None
    for path in test_paths:
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    found_image = os.path.join(path, file)
                    break
        if found_image:
            break
    
    if found_image:
        print(f"Testing with: {found_image}")
        
        # Test alt text generation
        alt_text = vision_service.generate_alt_text(found_image)
        print(f"Generated alt text: {alt_text}")
        
        # Test object detection
        objects = vision_service.detect_objects(found_image)
        print(f"Detected objects/tags: {objects}")
    else:
        print("No test images found. Upload an image through the web interface first, then run this test.")
        print("Or download a test image:")
        print("wget https://via.placeholder.com/300x200.jpg -O test_image.jpg")

if __name__ == "__main__":
    test_vision_api()