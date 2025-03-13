"""
Flask backend for the store-counter application.
Uses PyTorch for people detection and analysis.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import os
import time
from datetime import datetime
import base64
from people_detector import PeopleDetector

app = Flask(__name__)
CORS(app)

# Initialize the PyTorch-based people detector
detector = PeopleDetector()

# Global variables to store video data
video_data = {
    'frames': [],
    'current_frame': 0,
    'counts': [],
    'demographics': [],
    'total_count': 0
}

def process_frame(frame):
    """Process a single frame with the people detector"""
    # Detect people in the frame
    results = detector.detect(frame)
    
    # Extract demographic information
    demographics = []
    for person in results['people']:
        demographics.append({
            'id': person['id'],
            'age_group': person['age_group'],
            'gender': person['gender'],
            'position': person['position']
        })
    
    # Calculate aggregate demographic statistics
    age_stats = {'0-17': 0, '18-34': 0, '35-54': 0, '55+': 0}
    gender_stats = {'Male': 0, 'Female': 0}
    
    for person in demographics:
        age_stats[person['age_group']] += 1
        gender_stats[person['gender']] += 1
    
    # Create demographic summary
    demographic_summary = {
        'age': [
            {'group': '0-17', 'count': age_stats['0-17'], 
             'percent': round(age_stats['0-17'] * 100 / max(1, len(demographics)))},
            {'group': '18-34', 'count': age_stats['18-34'], 
             'percent': round(age_stats['18-34'] * 100 / max(1, len(demographics)))},
            {'group': '35-54', 'count': age_stats['35-54'], 
             'percent': round(age_stats['35-54'] * 100 / max(1, len(demographics)))},
            {'group': '55+', 'count': age_stats['55+'], 
             'percent': round(age_stats['55+'] * 100 / max(1, len(demographics)))}
        ],
        'gender': [
            {'type': 'Male', 'count': gender_stats['Male'], 
             'percent': round(gender_stats['Male'] * 100 / max(1, len(demographics)))},
            {'type': 'Female', 'count': gender_stats['Female'], 
             'percent': round(gender_stats['Female'] * 100 / max(1, len(demographics)))}
        ]
    }
    
    return {
        'count': results['count'],
        'people': results['people'],
        'keypoints': results['keypoints'],
        'demographics': demographics,
        'demographic_summary': demographic_summary
    }

@app.route('/upload', methods=['POST'])
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
    video_data['demographic_summaries'] = []
    video_data['current_frame'] = 0
    video_data['total_count'] = 0
    
    frame_count = 0
    frame_step = 15  # Process every nth frame to improve performance
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Only process every nth frame to improve performance
        if frame_count % frame_step == 0:
            # Process the frame
            results = process_frame(frame)
            
            # Update total count
            video_data['total_count'] += results['count']
            
            # Store frame data
            video_data['frames'].append(frame_count)
            video_data['counts'].append(results['count'])
            video_data['demographics'].append(results['demographics'])
            video_data['demographic_summaries'].append(results['demographic_summary'])
        
        frame_count += 1
    
    cap.release()
    
    return jsonify({
        'success': True,
        'total_frames': frame_count,
        'processed_frames': len(video_data['frames']),
        'total_people': video_data['total_count']
    })

@app.route('/webcam', methods=['POST'])
def process_webcam_frame():
    # Receive webcam frame as image data
    img_data = request.json.get('image')
    if not img_data:
        return jsonify({'error': 'No image data provided'}), 400
    
    # Convert base64 image to OpenCV format
    img_bytes = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Process the frame
    results = process_frame(frame)
    
    # Update global data
    timestamp = datetime.now().timestamp()
    video_data['frames'].append(timestamp)
    video_data['counts'].append(results['count'])
    video_data['demographics'].append(results['demographics'])
    video_data['total_count'] += results['count']
    
    return jsonify({
        'success': True,
        'count': results['count'],
        'total_count': video_data['total_count'],
        'demographics': results['demographic_summary'],
        'keypoints': results['keypoints']
    })

@app.route('/data', methods=['GET'])
def get_data():
    # Get time position from query params
    time_pos = request.args.get('time_pos', type=int)
    if time_pos is None or time_pos >= len(video_data['frames']):
        return jsonify({'error': 'Invalid time position'}), 400
    
    # Calculate total count up to this point
    total_so_far = sum(video_data['counts'][:time_pos+1])
    
    return jsonify({
        'frame': int(video_data['frames'][time_pos]),
        'current_count': video_data['counts'][time_pos],
        'demographics': video_data['demographic_summaries'][time_pos] if 'demographic_summaries' in video_data else {},
        'timeline_data': video_data['counts'],
        'total_count': total_so_far
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)