from flask import Blueprint, request, jsonify
import cv2
import numpy as np
import os
import time
from datetime import datetime

# Create a Blueprint with a name that matches how it's used
backend_app = Blueprint('backend', __name__)  # Changed from 'app' to 'backend_app'

# Global variables to store video data
video_data = {
    'frames': [],
    'current_frame': 0,
    'counts': [],
    'demographics': []
}

def detect_people(frame):
    """
    Simple placeholder for people detection algorithm.
    In a real implementation, this would use a trained model like YOLO.
    """
    # Convert frame to grayscale for processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Use a simple blob detector as a placeholder
    # In a real implementation, this would be replaced with a more sophisticated model
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 1000
    detector = cv2.SimpleBlobDetector_create(params)
    
    # Detect blobs (potential people)
    keypoints = detector.detect(gray)
    
    # For demo purposes, generate some random demographic data
    # In a real implementation, this would come from a trained model
    demographics = []
    for i in range(len(keypoints)):
        demographics.append({
            'id': i,
            'age_group': np.random.choice(['0-17', '18-34', '35-54', '55+']),
            'gender': np.random.choice(['Male', 'Female']),
            'position': (int(keypoints[i].pt[0]), int(keypoints[i].pt[1]))
        })
    
    return {
        'count': len(keypoints),
        'demographics': demographics,
        'keypoints': [(int(kp.pt[0]), int(kp.pt[1])) for kp in keypoints]
    }

@backend_app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    video_file = request.files['video']
    video_path = os.path.join('uploads', video_file.filename)
    
    # Ensure uploads directory exists
    os.makedirs('uploads', exist_ok=True)
    
    # Save the uploaded video
    video_file.save(video_path)
    
    # Process the video
    cap = cv2.VideoCapture(video_path)
    
    # Reset global data
    video_data['frames'] = []
    video_data['counts'] = []
    video_data['demographics'] = []
    video_data['current_frame'] = 0
    
    frame_count = 0
    total_people = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Only process every 10th frame to speed things up
        if frame_count % 10 == 0:
            results = detect_people(frame)
            total_people += results['count']
            
            # Store results
            video_data['frames'].append(frame_count)
            video_data['counts'].append(results['count'])
            video_data['demographics'].append(results['demographics'])
        
        frame_count += 1
    
    cap.release()
    
    return jsonify({
        'success': True,
        'total_frames': frame_count,
        'processed_frames': len(video_data['frames']),
        'total_people': total_people
    })

@backend_app.route('/webcam', methods=['POST'])
def process_webcam_frame():
    # Receive webcam frame as image data
    img_data = request.json.get('image')
    if not img_data:
        return jsonify({'error': 'No image data provided'}), 400
    
    # Convert base64 image to OpenCV format
    import base64
    img_bytes = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Process the frame
    results = detect_people(frame)
    
    # Update global data
    video_data['frames'].append(datetime.now().timestamp())
    video_data['counts'].append(results['count'])
    video_data['demographics'].append(results['demographics'])
    
    return jsonify({
        'success': True,
        'count': results['count'],
        'demographics': results['demographics'],
        'keypoints': results['keypoints']
    })

@backend_app.route('/data', methods=['GET'])
def get_data():
    # Get time position from query params
    time_pos = request.args.get('time_pos', type=int)
    if time_pos is None or time_pos >= len(video_data['frames']):
        return jsonify({'error': 'Invalid time position'}), 400
    
    return jsonify({
        'frame': int(video_data['frames'][time_pos]),
        'current_count': video_data['counts'][time_pos],
        'demographics': video_data['demographics'][time_pos],
        'timeline_data': video_data['counts'],
        'total_count': sum(video_data['counts'][:time_pos+1])
    })