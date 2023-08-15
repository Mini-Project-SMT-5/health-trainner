from django.shortcuts import render
from django.http import StreamingHttpResponse

import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


mp_drawing = mp.solutions.drawing_utils # pose를 시각화해줌 (drawing utilities를 제공)
mp_pose = mp.solutions.pose # mediapipe에서 여러가지 모델들 중 pose model을 가져옴

# angle calculate function
def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def generate_frames():
    # Video Feed
    cap = cv2.VideoCapture(0) # setup video capture camera

    # Curl counter variable
    curl_counter = 0
    stage = None


    ## Setup mediapipe instance
    # min_detection_confidence: 성공적인 것으로 간주되는 포즈 감지에 대한 최소 신뢰도 점수
    # min_tracking_confidence: 성공적인 것으로 간주되는 포즈 추적에 대한 최소 신뢰도 점수
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose: # 값을 높일수록 더 자세히 탐지하지만 너무 정확하게 해서 아예 탐지 안될수도(trade off)
        while cap.isOpened():
            
            ret, frame = cap.read() #frame: webcam의 image가 담김
            
            # Recolor image to RGB (opencv는 BGR을 mediapipe는 RGB를 사용해서 BGR을 RGB로 바꿔준다)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # make detection
            results = pose.process(image)
            
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract Landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # print(landmarks)
                # print(len(landmarks))
                
                # for lndmrk in mp_pose.PoseLandmark:
                #     print(lndmrk)
                
                # Get coordinates
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                # Calculate angle
                angle = calculate_angle(shoulder, elbow, wrist)
                
                # Visualize angle
                cv2.putText(image, str(angle), 
                            tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )                  
            
                # calulate counter
                if angle > 160:
                    stage = "down"
                if angle < 60 and stage == "down":
                    stage="up"
                    curl_counter += 1  
        
            except:
                pass
            
            # Render detection and curl counter
            # setup status box (startpoint, endpoint, color, )
            
            # Rep data
            cv2.putText(image, 'REPS', (15, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(curl_counter),
                        (30, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2, cv2.LINE_AA)
            
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                    )
            
            ret, buffer = cv2.imencode('.jpg', image)
            render_image = buffer.tobytes()
            
            
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + render_image+ b'\r\n')
            

def webcam(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def index(request):
    
    return render(request, 'index.html')