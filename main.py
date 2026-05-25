############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2, os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
from collections import Counter

############################################# FUNCTIONS ################################################

def get_attendance_status():
    """
    For 10:00 AM class
    """
    current_time = datetime.datetime.now().time()

    # 10:00 AM class timings
    morning_start = datetime.time(10, 0, 0)     # 10:00 AM
    morning_end = datetime.time(10, 15, 0)      # 10:15 AM (15 min grace)
    late_threshold = datetime.time(10, 30, 0)   # 10:30 AM (30 min late)

    print(f"\n[ATTENDANCE] Time: {current_time}")
    
    if current_time < morning_start:
        return "Early"
    elif morning_start <= current_time <= morning_end:
        return "On Time"
    elif morning_end < current_time <= late_threshold:
        return "Late"
    else:
        return "Very Late"

##################################################################################

def tick():
    ts = time.time()
    now = datetime.datetime.fromtimestamp(ts)
    day_name = now.strftime("%A")
    date_display = now.strftime(f"%d %B %Y  ({day_name})")
    time_display = time.strftime('%H:%M:%S')
    date_label.config(text=f"{date_display}   {time_display}")
    window.after(1000, tick)

###################################################################################

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'Tam.hussain2003@gmail.com' ")

###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            if os.path.isfile(cascade_path):
                return cascade_path
            else:
                mess._show(title='Some file missing', message='Please install opencv-contrib-python')
                window.destroy()
        except:
            mess._show(title='Some file missing', message='Please contact us for help')
            window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        tf = open("TrainingImageLabel/psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel/psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel/psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=('comic', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('comic', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('comic', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('comic', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('comic', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('comic', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('comic', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#00fcca", height = 1,width=25, activebackground="white", font=('comic', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#####################################################################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        tf = open("TrainingImageLabel/psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel/psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################################

def TrainImages():
    assure_path_exists("TrainingImageLabel/")
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    if not os.path.isfile(harcascadePath):
        harcascadePath = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    
    detector = cv2.CascadeClassifier(harcascadePath)
    
    faces = []
    ids = []
    
    imagePaths = [os.path.join("TrainingImage", f) for f in os.listdir("TrainingImage")]
    
    if len(imagePaths) == 0:
        mess._show(title='No Images', message='Please take images first!')
        return
    
    print("=== TRAINING DEBUG ===")
    print(f"Total images found: {len(imagePaths)}")
    
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')  # grayscale
        img_numpy = np.array(PIL_img, 'uint8')

        # ✅ ENHANCEMENT 4: Histogram Equalization during training
        img_numpy = cv2.equalizeHist(img_numpy)
        
        filename = os.path.basename(imagePath)
        print(f"Processing: {filename}")
        
        try:
            # Format: Name.Serial.ID.ImageNumber_Angle.jpg
            parts = filename.split(".")
            if len(parts) >= 3:
                name = parts[0]
                serial_num = parts[1]
                id_str = parts[2]
                
                print(f"  Name: {name}, Serial: {serial_num}, ID: {id_str}")
                
                id_num = int(id_str)
                faces.append(img_numpy)
                ids.append(id_num)
                print(f"  Added - ID: {id_num}")
            else:
                print(f"  ERROR: Filename format incorrect")
        except Exception as e:
            print(f"  ERROR processing {filename}: {e}")
            continue
    
    if len(faces) == 0:
        mess._show(title='Error', message='No valid faces found for training!')
        return
    
    ids = np.array(ids)
    
    print(f"\nTraining with {len(faces)} images...")
    print(f"Unique IDs in training: {set(ids)}")
    
    recognizer.train(faces, ids)
    
    assure_path_exists("TrainingImageLabel/")
    recognizer.save("TrainingImageLabel/Trainner.yml")
    
    res = f"Images Trained: {len(faces)}\nModel saved to Trainner.yml"
    message1.configure(text=res)
    mess._show(title='Training Complete', message=f'Successfully trained {len(faces)} images!')

#######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

#######################################################################################

def load_student_data():
    """Load student data from CSV with correct column mapping"""
    student_data = {}
    
    try:
        with open("StudentDetails/StudentDetails.csv", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            if not lines:
                return student_data
            
            first_line = lines[0].strip().split(',')
            print(f"\n=== CSV DEBUG ===")
            print(f"CSV Header: {first_line}")
            print(f"Number of columns: {len(first_line)}")
            
            for line_num, line in enumerate(lines[1:], start=2):
                line = line.strip()
                if not line:
                    continue
                    
                parts = line.split(',')
                parts = [p.strip() for p in parts if p.strip()]
                
                if len(parts) >= 3:
                    serial_no = parts[0]
                    student_id = parts[1]
                    name = parts[2]
                    
                    student_data[student_id] = {
                        'serial': serial_no,
                        'name': name
                    }
                    
                    print(f"Line {line_num}: ID={student_id}, Name={name}, Serial={serial_no}")
                else:
                    print(f"Warning: Line {line_num} has insufficient data: {parts}")
            
            print(f"Total students loaded: {len(student_data)}\n")
    
    except Exception as e:
        print(f"Error loading student data: {e}")
    
    return student_data

#######################################################################################

def TakeImages():
    check_haarcascadefile()
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    
    if os.path.exists("StudentDetails/StudentDetails.csv"):
        with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
            reader = csv.reader(csvFile1)
            rows = list(reader)
            serial = len(rows) - 1
        csvFile1.close()
    
    Id = (txt.get().strip())
    name = (txt2.get().strip())
    
    print(f"DEBUG: ID='{Id}', Name='{name}'")
    
    if Id == "" or name == "":
        mess._show(title='Empty Fields', message='Please enter both ID and Name!')
        return
        
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        cam = cv2.VideoCapture(1)
        if not cam.isOpened():
            mess._show(title='Camera Error', message='Camera access nahi ho raha!')
            return
            
        harcascadePath = "haarcascade_frontalface_default.xml"
        if not os.path.isfile(harcascadePath):
            harcascadePath = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            
        detector = cv2.CascadeClassifier(harcascadePath)
        if detector.empty():
            mess._show(title='Error', message='Face detector load nahi ho raha!')
            cam.release()
            return
        
        # ✅ ENHANCEMENT 2: More samples per angle for better training
        angles = [
            {"name": "STRAIGHT", "samples": 10, "instruction": "Look STRAIGHT at camera"},
            {"name": "RIGHT",    "samples": 5,  "instruction": "Slowly turn head to RIGHT"},
            {"name": "LEFT",     "samples": 5,  "instruction": "Slowly turn head to LEFT"},
            {"name": "UP",       "samples": 3,  "instruction": "Slowly look UP"},
            {"name": "DOWN",     "samples": 3,  "instruction": "Slowly look DOWN"}
        ]
        
        sampleNum = 0
        current_angle_index = 0
        angle_sample_count = 0
        total_samples = sum(angle["samples"] for angle in angles)
        
        print(f"Starting face capture for {total_samples} samples across different angles...")
        
        instruction_start_time = time.time()
        current_instruction = angles[0]["instruction"]
        capture_delay = 1.5
        last_capture_time = 0
        
        while True:
            ret, img = cam.read()
            if not ret:
                print("Frame read error!")
                mess._show(title='Camera Error', message='Frame read nahi ho raha!')
                break
            
            current_angle = angles[current_angle_index]
            angle_name = current_angle["name"]
            angle_max_samples = current_angle["samples"]
            current_instruction = current_angle["instruction"]
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # ✅ ENHANCEMENT 4: Histogram equalization during capture
            gray = cv2.equalizeHist(gray)

            # ✅ ENHANCEMENT 5: Better detectMultiScale parameters
            faces = detector.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=6,
                minSize=(60, 60),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            cv2.putText(img, f"INSTRUCTION: {current_instruction}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(img, f"Angle: {angle_name} ({angle_sample_count}/{angle_max_samples})", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(img, f"Total Progress: {sampleNum}/{total_samples}", (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(img, f"Press 'Q' to quit", (10, img.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            current_time = time.time()
            time_since_last_capture = current_time - last_capture_time
            
            if len(faces) > 0 and time_since_last_capture >= capture_delay:
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    
                    sampleNum += 1
                    angle_sample_count += 1
                    last_capture_time = current_time
                    
                    # Save equalized grayscale face region
                    filename = f"TrainingImage/{name}.{serial}.{Id}.{sampleNum}_{angle_name}.jpg"
                    success = cv2.imwrite(filename, gray[y:y + h, x:x + w])
                    
                    if success:
                        print(f"Image {sampleNum} saved: {filename}")
                        cv2.putText(img, "CAPTURED!", (x, y-10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    else:
                        print(f"Failed to save: {filename}")
                    
                    if angle_sample_count >= angle_max_samples:
                        angle_sample_count = 0
                        current_angle_index += 1
                        
                        if current_angle_index >= len(angles):
                            mess._show(title='Success', 
                                     message=f'All {total_samples} images captured successfully!\nNow click Save Profile.')
                            break
                        else:
                            next_angle = angles[current_angle_index]
                            current_instruction = f"READY: {next_angle['instruction']}"
                            last_capture_time = current_time + 1.0
                    
                    break
            
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(img, "Face Detected", (x, y-30), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            if len(faces) > 0:
                countdown = max(0, capture_delay - time_since_last_capture)
                cv2.putText(img, f"Next capture in: {countdown:.1f}s", 
                          (img.shape[1] - 250, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            else:
                cv2.putText(img, "No face detected! Adjust position", 
                          (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            cv2.imshow('Taking Images - Follow Instructions - Press Q to quit', img)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            if current_angle_index >= len(angles):
                break
                
        cam.release()
        cv2.destroyAllWindows()
        
        print(f"Total images taken: {sampleNum}")
        
        if sampleNum > 0:
            res = f"{sampleNum} Images Taken for ID : {Id} | Now Save Profile"
            
            header = ['Serial No', 'ID', 'NAME']
            row = [serial, Id, name]
            
            if not os.path.exists("StudentDetails/StudentDetails.csv"):
                with open('StudentDetails/StudentDetails.csv', 'w', newline='') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(header)
                    writer.writerow(row)
            else:
                with open('StudentDetails/StudentDetails.csv', 'a', newline='') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
            
            message1.configure(text=res)
            message.configure(text=f'Total Registrations till now: {serial+1}')
        else:
            mess._show(title='No Images', message='Koi image capture nahi hui! Camera ya face detection check karein.')
    else:
        mess._show(title='Invalid Name', message='Please enter alphabetic name only!')

########################################################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

#########################################################################################

# ✅ ENHANCEMENT 3: Multi-Frame Voting Function
def get_majority_prediction(predictions, threshold=35):
    """
    predictions = list of (id, confidence) tuples from last N frames
    Returns most common ID only if majority of frames agree with confidence < threshold
    Lower confidence = better match in LBPH
    """
    # Filter only confident predictions
    valid = [(pid, c) for pid, c in predictions if c < threshold]

    if len(valid) < 3:  # Need at least 3 confident reads
        return None, 999

    ids = [pid for pid, c in valid]
    most_common_id, count = Counter(ids).most_common(1)[0]

    # 60% of valid frames must agree on same person
    if count >= len(valid) * 0.6:
        avg_conf = sum(c for pid, c in valid if pid == most_common_id) / count
        return most_common_id, avg_conf

    return None, 999  # No consensus

#########################################################################################

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    
    for k in tv.get_children():
        tv.delete(k)
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel/Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel/Trainner.yml")
        print("Model loaded successfully")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to train data first!!')
        return
        
    harcascadePath = "haarcascade_frontalface_default.xml"
    if not os.path.isfile(harcascadePath):
        harcascadePath = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        mess._show(title='Camera Error', message='Camera access nahi ho raha!')
        return

    font = cv2.FONT_HERSHEY_SIMPLEX
    
    student_data = load_student_data()
    
    if not student_data:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        return

    attendance_recorded = False
    last_attendance_time = 0
    face_detection_start_time = 0
    current_face_id = None
    attendance_marked_ids = set()

    # ✅ ENHANCEMENT 3: Frame buffer for multi-frame voting
    frame_buffer = []
    BUFFER_SIZE = 5
    
    print("=== STARTING ATTENDANCE (Enhanced) ===")
    
    while True:
        ret, im = cam.read()
        if not ret:
            print("Frame read error in attendance!")
            break
            
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        # ✅ ENHANCEMENT 4: Histogram equalization for better recognition in any lighting
        gray = cv2.equalizeHist(gray)

        # ✅ ENHANCEMENT 5: Better face detection parameters
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=6,
            minSize=(60, 60),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        current_time = time.time()
        
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            
            predicted_id = str(serial)
            print(f"DEBUG: Recognized ID: {predicted_id}, Confidence: {conf:.1f}")

            # ✅ ENHANCEMENT 3: Add to frame buffer for voting
            frame_buffer.append((predicted_id, conf))
            if len(frame_buffer) > BUFFER_SIZE:
                frame_buffer.pop(0)

            # ✅ ENHANCEMENT 1: Tighter confidence threshold (35 not 50)
            # ✅ ENHANCEMENT 3: Use majority vote instead of single frame
            voted_id, voted_conf = get_majority_prediction(frame_buffer, threshold=35)

            # Determine display name from voted result
            if voted_id is not None and voted_id in student_data:
                display_name = student_data[voted_id]['name']
                actual_id = voted_id
                print(f"  Vote Matched: ID={actual_id}, Name={display_name}, Avg Conf={voted_conf:.1f}")
            elif voted_id is not None:
                # Try serial fallback
                display_name = 'Unknown'
                actual_id = 'Unknown'
                for sid, info in student_data.items():
                    if info['serial'] == voted_id:
                        display_name = info['name']
                        actual_id = sid
                        print(f"  Vote Matched by serial: ID={actual_id}, Name={display_name}")
                        break
            else:
                display_name = 'Unknown'
                actual_id = 'Unknown'

            # Show voting status on screen
            votes_collected = len([p for p in frame_buffer if p[1] < 35])
            cv2.putText(im, f"Votes: {votes_collected}/{BUFFER_SIZE}", (x, y + h + 70),
                       font, 0.6, (200, 200, 0), 1)

            if voted_id is not None and display_name != 'Unknown':
                # ✅ ENHANCEMENT 6: 2.5s stable time instead of 1s
                if current_face_id != voted_id:
                    current_face_id = voted_id
                    face_detection_start_time = current_time
                    print(f"New face voted: {display_name} (ID: {voted_id})")
                
                detection_duration = current_time - face_detection_start_time
                
                if detection_duration < 2.5:
                    countdown = 2.5 - detection_duration
                    cv2.putText(im, f"Recognized: {display_name}", (x, y-50), font, 0.7, (0, 255, 0), 2)
                    cv2.putText(im, f"Confirming: {countdown:.1f}s", (x, y-20), font, 0.6, (0, 255, 255), 2)
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                else:
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.putText(im, f"Attendance: {display_name}", (x, y-30), font, 0.8, (0, 255, 0), 2)
                    
                    if (current_face_id not in attendance_marked_ids and 
                        display_name != 'Unknown' and
                        (current_time - last_attendance_time) > 2):
                        
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        status = get_attendance_status()
                        
                        try:
                            attendance = [str(actual_id), '', display_name, '', str(date), '', str(timeStamp), '', status]
                            
                            exists = os.path.isfile("Attendance/Attendance_" + date + ".csv")
                            if exists:
                                with open("Attendance/Attendance_" + date + ".csv", 'a+', newline='') as csvFile1:
                                    writer = csv.writer(csvFile1)
                                    writer.writerow(attendance)
                            else:
                                with open("Attendance/Attendance_" + date + ".csv", 'a+', newline='') as csvFile1:
                                    writer = csv.writer(csvFile1)
                                    writer.writerow(['Id', '', 'Name', '', 'Date', '', 'Time', '', 'Status'])
                                    writer.writerow(attendance)
                            
                            save_attendance_csv(actual_id, display_name, date, timeStamp, status)
                            
                            attendance_marked_ids.add(current_face_id)
                            last_attendance_time = current_time
                            attendance_recorded = True
                            
                            iidd = str(actual_id) + '   '
                            tv.insert('', 0, text=iidd, values=(str(display_name), str(date), str(timeStamp), str(status)))
                            
                            print(f"✓ Attendance marked: {display_name} at {timeStamp} - {status}")
                            
                        except Exception as e:
                            print(f"✗ Error in attendance: {e}")
            else:
                # Unknown or low confidence
                print(f"  No consensus yet or unknown face. Conf: {conf:.1f}")
                if display_name == 'Unknown':
                    current_face_id = None
                    face_detection_start_time = 0
                    cv2.putText(im, "Unknown - Move closer", (x, y-20), font, 0.6, (0, 0, 255), 2)
            
            cv2.putText(im, str(display_name), (x, y + h + 25), font, 0.8, (255, 255, 255), 2)
            cv2.putText(im, f"Conf: {conf:.1f}", (x, y + h + 50), font, 0.6, (255, 255, 255), 1)
            
        if len(faces) == 0:
            current_face_id = None
            face_detection_start_time = 0
            frame_buffer.clear()  # Reset buffer when no face visible
            
        cv2.imshow('Taking Attendance - Press Q to quit', im)
        if (cv2.waitKey(1) == ord('q')):
            break

    cam.release()
    cv2.destroyAllWindows()
    
    print("=== ATTENDANCE COMPLETE ===")

#################################################################################################

def save_attendance_csv(student_id, name, date, timeStamp, status):
    """
    Save attendance record to the fixed CSV file with PROPER FORMATTING
    """
    filename = "attendance.csv"
    
    print(f"\n{'='*60}")
    print("SAVING ATTENDANCE TO CSV:")
    print(f"File: {filename}")
    print(f"ID: {student_id}")
    print(f"Name: {name}")
    print(f"Date: {date}")
    print(f"Time: {timeStamp}")
    print(f"Status: {status}")
    print('='*60)

    try:
        file_exists = os.path.isfile(filename)
        
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            if not file_exists or os.path.getsize(filename) == 0:
                writer.writerow(['ID', 'Name', 'Date', 'Time', 'Status'])
                print("✓ Header written")
            
            writer.writerow([student_id, name, date, timeStamp, status])
            print("✓ Data saved successfully!")
            
    except PermissionError:
        print("✗ Permission denied! File might be open in Excel.")
        alt_filename = "attendance_backup.csv"
        with open(alt_filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not os.path.isfile(alt_filename):
                writer.writerow(['ID', 'Name', 'Date', 'Time', 'Status'])
            writer.writerow([student_id, name, date, timeStamp, status])
        print(f"✓ Saved to backup: {alt_filename}")
        
    except Exception as e:
        print(f"✗ Error saving attendance: {e}")
        with open("attendance_log.txt", 'a', encoding='utf-8') as f:
            f.write(f"{student_id},{name},{date},{timeStamp},{status}\n")
        print("✓ Saved to text file: attendance_log.txt")
            
######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry("1286x768")
window.resizable(False, False)
window.title("Face Recognition Attendance System")
window.configure(background="#FBE6C0")

header = tk.Label(window, text="Face Recognition Based Attendance Monitoring System",
                  fg="black", bg="#EB7227", width=58, height=1, font=('comic sans ms', 28, 'bold'))
header.place(relx=0.00, rely=0.01)

date_label = tk.Label(window, fg="black", bg="#FBBE3C",
                      font=('comic sans ms', 20, 'bold'), relief="ridge", bd=4)
date_label.place(relx=0.25, rely=0.12, relwidth=0.5, relheight=0.07)
tick()

# LEFT FRAME
frame1 = tk.Frame(window, bg="#EB7227", bd=5, relief="ridge")
frame1.place(relx=0.08, rely=0.23, relwidth=0.40, relheight=0.70)

head1 = tk.Label(frame1, text="For Already Registered",
                 fg="black", bg="#FBBE3C", font=('comic sans ms', 17, 'bold'))
head1.pack(pady=10)

trackBtn = tk.Button(frame1, text="Take Attendance",
                     fg="black", bg="#FBBE3C", activebackground="#EB7227",
                     font=('comic sans ms', 14, 'bold'), width=20, height=1,
                     command=TrackImages)
trackBtn.pack(pady=10)

lbl3 = tk.Label(frame1, text="Attendance", fg="white",
                bg="#D80000", font=('comic sans ms', 16, 'bold'))
lbl3.pack(pady=5)

tv = ttk.Treeview(frame1, height=10, columns=('name', 'date', 'time', 'status'))
tv.column('#0', width=80)
tv.column('name', width=120)
tv.column('date', width=100)
tv.column('time', width=100)
tv.column('status', width=100)
tv.heading('#0', text='ID')
tv.heading('name', text='NAME')
tv.heading('date', text='DATE')
tv.heading('time', text='TIME')
tv.heading('status', text='STATUS')
tv.pack(padx=10, pady=10, fill='x')

scroll = ttk.Scrollbar(frame1, orient='vertical', command=tv.yview)
tv.configure(yscrollcommand=scroll.set)
scroll.pack(side='right', fill='y')

quitButton = tk.Button(frame1, text="Quit", fg="black", bg="#FBBE3C",
                       activebackground="#EB7227", font=('comic sans ms', 14, 'bold'), width=20,
                       command=window.destroy)
quitButton.pack(pady=15)

# RIGHT FRAME
frame2 = tk.Frame(window, bg="#EB7227", bd=5, relief="ridge")
frame2.place(relx=0.52, rely=0.23, relwidth=0.40, relheight=0.70)

head2 = tk.Label(frame2, text="For New Registrations",
                 fg="black", bg="#FBBE3C", font=('comic sans ms', 17, 'bold'))
head2.pack(pady=10)

lbl = tk.Label(frame2, text="Enter ID", fg="white", bg="#D80000",
               font=('comic sans ms', 14, 'bold'))
lbl.pack(pady=5)
txt = tk.Entry(frame2, width=25, fg="black", font=('comic sans ms', 14))
txt.pack()

clear1 = tk.Button(frame2, text="Clear", fg="black", bg="#FBBE3C",
                   activebackground="#EB7227", font=('comic sans ms', 12, 'bold'),
                   command=clear)
clear1.pack(pady=5)

lbl2 = tk.Label(frame2, text="Enter Name", fg="white", bg="#D80000",
                font=('comic sans ms', 14, 'bold'))
lbl2.pack(pady=5)
txt2 = tk.Entry(frame2, width=25, fg="black", font=('comic sans ms', 14))
txt2.pack()

clear2 = tk.Button(frame2, text="Clear", fg="black", bg="#FBBE3C",
                   activebackground="#EB7227", font=('comic sans ms', 12, 'bold'),
                   command=clear2)
clear2.pack(pady=5)

message1 = tk.Label(frame2, text="1) Take Images  >>>  2) Save Profile",
                    bg="#FBBE3C", fg="black", font=('comic sans ms', 13, 'bold'))
message1.pack(pady=10)

takeImg = tk.Button(frame2, text="Take Images", fg="black", bg="#FBBE3C",
                    activebackground="#EB7227", font=('comic sans ms', 14, 'bold'), width=20,
                    command=TakeImages)
takeImg.pack(pady=10)

trainImg = tk.Button(frame2, text="Save Profile", fg="black", bg="#FBBE3C",
                     activebackground="#EB7227", font=('comic sans ms', 14, 'bold'), width=20,
                     command=psw)
trainImg.pack(pady=10)

message = tk.Label(frame2, text="Total Registrations till now: 0",
                   bg="#D80000", fg="white", font=('comic sans ms', 14, 'bold'))
message.pack(pady=20)

# MENU BAR
menubar = tk.Menu(window, relief='ridge')
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Change Password', command=change_pass)
filemenu.add_command(label='Contact Us', command=contact)
filemenu.add_command(label='Exit', command=window.destroy)
menubar.add_cascade(label='Help', font=('comic sans ms', 14, 'bold'), menu=filemenu)
window.configure(menu=menubar)

window.mainloop()
