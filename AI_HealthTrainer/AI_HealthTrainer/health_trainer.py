from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse

import time, json, cv2, threading, io, numpy as np, mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from asgiref.sync import async_to_sync

mp_drawing = mp.solutions.drawing_utils # pose를 시각화해줌 (drawing utilities를 제공)
mp_pose = mp.solutions.pose # mediapipe에서 여러가지 모델들 중 pose model을 가져옴

lock = threading.Lock()

global feedback_text, reps_counter

reps_counter = 0
feedback_text = ""

def rest():
    global sets_counter, reps_counter, stage, is_rest, feedback_text
    time.sleep(rest_time)
    
    lock.acquire()
    reps_counter = 0
    sets_counter += 1
    stage = None
    is_rest = False
    feedback_text = "Rest time is over, Let's workout"
    lock.release()


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


def send_feedback():
    global feedback_text    
    return feedback_text


def pluscounter():
    global reps_counter
    
    lock.acquire()
    reps_counter += 1
    lock.release()     


def generate_frames():
    
    # set, reps, rest variable
    global exerciseType, sets, sets_counter, reps, reps_counter, rest_time, is_rest, stage, feedback_text, min_arm_angle
    
    exerciseType = 'dumbbellcurl'
    # exerciseType = 'jumpingjack'
    # exerciseType = 'lunge'
    
    sets = 3
    sets_counter = 1
    reps = 5
    rest_time = 5
    is_rest = False    
    stage = None
    min_arm_angle = 180
    bend = False

    # Video Feed
    cap = cv2.VideoCapture(0) # setup video capture camera


    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose: # 값을 높일수록 더 자세히 탐지하지만 너무 정확하게 해서 아예 탐지 안될수도(trade off)
        while cap.isOpened():
            
            ret, frame = cap.read() #frame: webcam의 image가 담김
            arm_status = None
            
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
                
                # Get coordinates
                # dumbbell curl
                rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                rightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                rightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                
                # lunge
                rightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                rightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                rightHeel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
    
                leftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                leftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                leftHeel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
                
                # jumpingjack                
                leftShoulder  = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                leftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                
                # counter
                if reps_counter < reps:
                    if exerciseType == 'dumbbellcurl':
                        right_arm_angle = calculate_angle(rightShoulder, rightElbow, rightWrist)
                        
                        cv2.putText(image, str(right_arm_angle), 
                                    tuple(np.multiply(rightElbow, [640, 480]).astype(int)), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                            )
                        
                        min_arm_angle = min(right_arm_angle, min_arm_angle)
                        
                        if right_arm_angle > 90 and bend: # feedback이나 개수를 올려줘야 함
                            if right_arm_angle > 150:
                                bend = False
                                if stage == "down":
                                    feedback_text = "bend your arms more"
                                    
                                elif stage == "up":
                                    stage = "down"
                                    pluscounter()
                                                
                                    feedback_text = str(reps_counter)
                                    min_arm_angle = 180
                                    
                        if min_arm_angle < 90:
                            bend = True
                            if min_arm_angle < 40:
                                stage = "up"
                        
                            
                    elif exerciseType == 'jumpingjack':
                        #jumpingjack
                        right_hip_angle = calculate_angle(leftHeel, rightHip, rightHeel)
                        left_hip_angle = calculate_angle(rightHeel, leftHip, leftHeel)
                        right_shoulder_angle = calculate_angle(rightHip, rightShoulder, rightWrist)
                        left_shoulder_angle = calculate_angle(leftHip, leftShoulder, leftWrist)
                        
                        cv2.putText(image, str(right_hip_angle), 
                                    tuple(np.multiply(rightHip, [640, 480]).astype(int)), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                            )               
                        cv2.putText(image, str(left_hip_angle), 
                                    tuple(np.multiply(leftHip, [640, 480]).astype(int)), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                            )  
                        cv2.putText(image, str(right_shoulder_angle), 
                                    tuple(np.multiply(rightShoulder, [640, 480]).astype(int)), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                            )               
                        cv2.putText(image, str(left_shoulder_angle), 
                                    tuple(np.multiply(leftShoulder, [640, 480]).astype(int)), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                            )
                        
                        if right_hip_angle > 30 and left_hip_angle > 30 and right_shoulder_angle > 130 and left_shoulder_angle > 130:
                            stage = 'down'
                        if right_hip_angle < 8 and left_hip_angle < 8 and right_shoulder_angle < 15 and left_shoulder_angle < 15 and stage == 'down':
                            stage = 'up'
                            pluscounter()
                            
                        
                        
                        
                    
                    elif exerciseType == 'lunge':
                        right_leg_angle = calculate_angle(rightHip, rightKnee, rightHeel)
                        left_leg_angle = calculate_angle(leftHip, leftKnee, leftHeel)
                        
                        cv2.putText(image, str(right_leg_angle), 
                                    tuple(np.multiply(rightKnee, [640, 480]).astype(int)), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                            )               
                        cv2.putText(image, str(left_leg_angle), 
                                    tuple(np.multiply(leftKnee, [640, 480]).astype(int)), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                            )      
                            
                        if left_leg_angle < 100 and right_leg_angle < 100:
                            stage = 'down'
                        if left_leg_angle > 160 and right_leg_angle > 160 and stage == 'down':
                            stage = 'up'
                            pluscounter()
                            
                    else:
                        print('exercise type error')
                        
                    cv2.putText(image, 'REPS', (15, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(image, str(reps_counter),
                                (30, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2, cv2.LINE_AA)        
                
                # start timer
                if reps_counter == reps and not is_rest and sets_counter < sets:
                    is_rest = True                    
                    thread = threading.Thread(target=rest)
                    thread.start()
                
                # rest time
                if reps_counter == reps and is_rest and sets_counter < sets:
                    cv2.putText(image, 'REST!', (15, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2, cv2.LINE_AA)
                    feedback_text = "Rest"
                
                # work out done
                if sets_counter == sets and reps_counter == reps:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                    )
            
                    ret, buffer = cv2.imencode('.jpg', image)
                    render_image = buffer.tobytes()
                    feedback_text = "All sets is done, congratulation!"
                    
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + render_image+ b'\r\n')
                    break     

            except:
                pass
            
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                    )
            
            ret, buffer = cv2.imencode('.jpg', image)
            render_image = buffer.tobytes()
            
            
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + render_image+ b'\r\n')
    