from torchvision import models, transforms
import json
import torch
import torch.nn as nn
from PIL import Image
import requests
from io import BytesIO



with open('logo_classes.json', 'r') as f:
    class_to_idx = json.load(f)
    idx_to_class = {v: k for k, v in class_to_idx.items()}



def load_model():
    """ Loads model trained in google colab """
    model = models.resnet18(pretrained=False)
    num_classes = len(class_to_idx)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    # Loads the trained weights of saved model
    model.load_state_dict(torch.load('logo_model_resnet18.pth', map_location=torch.device('cpu')))
    model.eval()  
    return model

model=load_model()


from sklearn.metrics.pairwise import cosine_similarity


model = load_model()


def extract_embedding(image_path, model=None):
    """ Extracts features from image accessible through the image path"""
    if model is None:
        model = load_model()
    #transformations used in training
    transform = transforms.Compose([
    transforms.Resize((600, 600), Image.BILINEAR),
    transforms.CenterCrop((448, 448)),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.485, 0.456, 0.406),
                                 std=(0.229, 0.224, 0.225))
    ])
    if image_path.startswith(('http://', 'https://')):
        # To zaenkrat ne dela
        response = requests.get(image_path)
        image = Image.open(BytesIO(response.content)).convert('RGB')
    else:
        image = Image.open(image_path).convert('RGB')
   
    img_tensor = transform(image).unsqueeze(0)  
    
    with torch.no_grad():
        features = torch.nn.Sequential(*list(model.children())[:-1])(img_tensor)
        features = features.squeeze()
    
    return features.numpy() 


def calculate_similarity(features1, features2):
    """Calculates cosine similarity between two feature vectors"""
    return cosine_similarity([features1], [features2])[0][0]

def compare_logos(input_logo, database_logos):
    """Compares input logo features with database logos"""
    for logo in database_logos:
        
        input_features= extract_embedding(input_logo, model)
        db_features = extract_embedding(logo,  model)  
        

        similarity = calculate_similarity(input_features, db_features)
        
        # if similarity > 0.6:  # Threshold can be adjusted
        #     results.append({
        #         'logo_id': logo.id,
        #         'name': logo.name,
        #         'similarity': float(similarity),  # Convert to float for JSON serialization
        #         'image_url': logo.image_url
        #     })
    
    return similarity


import easyocr

def extract_text_dl(image_path):
    """ Extracts text from images """
    reader = easyocr.Reader(['en'])  
    results = reader.readtext(image_path)
    
    extracted_text = []
    for (bbox, text, prob) in results:
        if prob > 0.5: 
            extracted_text.append(text)
    
    return " ".join(extracted_text)