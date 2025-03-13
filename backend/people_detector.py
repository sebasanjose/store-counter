"""
PyTorch-based people detector for the store-counter application.
Uses a pre-trained model to detect people in images and videos.
"""
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.transforms import functional as F
import numpy as np
import cv2
from PIL import Image
import random

class PeopleDetector:
    def __init__(self):
        # Load pre-trained model
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        # Load a pre-trained Faster R-CNN model
        self.weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
        self.model = fasterrcnn_resnet50_fpn_v2(weights=self.weights)
        self.model.to(self.device)
        self.model.eval()
        
        # Get class names from weights metadata
        self.classes = self.weights.meta["categories"]
        self.person_class_id = self.classes.index('person')
        
        # Random color for each detected person (for tracking visualization)
        self.colors = {}

    def preprocess_image(self, image):
        """Convert OpenCV image to PyTorch tensor"""
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Convert to PIL Image
        image_pil = Image.fromarray(image_rgb)
        # Apply transformations
        image_tensor = F.to_tensor(image_pil)
        return image_tensor
    
    def detect(self, image, confidence_threshold=0.7):
        """
        Detect people in the image
        
        Args:
            image: OpenCV image (BGR format)
            confidence_threshold: Detection confidence threshold
            
        Returns:
            Dictionary with detection results
        """
        # Preprocess the image
        image_tensor = self.preprocess_image(image)
        
        # Perform inference
        with torch.no_grad():
            predictions = self.model([image_tensor.to(self.device)])
        
        # Extract results for person class
        boxes = predictions[0]['boxes'].cpu().numpy()
        scores = predictions[0]['scores'].cpu().numpy()
        labels = predictions[0]['labels'].cpu().numpy()
        
        # Filter detections for people with confidence above threshold
        person_indices = np.where((labels == self.person_class_id) & (scores > confidence_threshold))[0]
        
        detected_people = []
        keypoints = []
        
        # For each detected person
        for i, idx in enumerate(person_indices):
            box = boxes[idx].astype(int)
            score = scores[idx]
            
            # Calculate positions
            x1, y1, x2, y2 = box
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            
            # Track ID based on position (simple implementation)
            # In a real app, use a proper tracking algorithm like DeepSORT
            position_id = f"{center_x//50}_{center_y//50}"
            if position_id not in self.colors:
                self.colors[position_id] = [random.randint(0, 255) for _ in range(3)]
            
            # Generate simple demographic data
            # In a real app, use a dedicated model for demographic analysis
            age_group = random.choice(['0-17', '18-34', '35-54', '55+'])
            gender = random.choice(['Male', 'Female'])
            
            detected_people.append({
                'id': position_id,
                'box': box.tolist(),
                'confidence': float(score),
                'age_group': age_group,
                'gender': gender,
                'position': (center_x, center_y)
            })
            
            keypoints.append((center_x, center_y))
        
        return {
            'count': len(detected_people),
            'people': detected_people,
            'keypoints': keypoints
        }
    
    def annotate_image(self, image, detections):
        """
        Draw detection results on the image
        
        Args:
            image: Original OpenCV image
            detections: Detection results from detect()
            
        Returns:
            Annotated image
        """
        result_img = image.copy()
        
        # Draw each person detection
        for person in detections['people']:
            x1, y1, x2, y2 = person['box']
            position_id = person['id']
            color = self.colors.get(position_id, [0, 255, 0])
            
            # Draw bounding box
            cv2.rectangle(result_img, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f"Person {person['confidence']:.2f}"
            cv2.putText(result_img, label, (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Draw total count
        count_text = f"People count: {detections['count']}"
        cv2.putText(result_img, count_text, (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return result_img

# For testing
if __name__ == "__main__":
    detector = PeopleDetector()
    
    # Test with a sample image if available
    test_image = cv2.imread("test.jpg")
    if test_image is not None:
        results = detector.detect(test_image)
        annotated_img = detector.annotate_image(test_image, results)
        cv2.imwrite("output.jpg", annotated_img)
        print(f"Detected {results['count']} people")
    else:
        print("No test image found")