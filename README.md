# Effective-Accident-Detection-and-Prevention-System
Effective Accident Detection and Prevention System. Project developed and presented at WCE_HACKATHON 2019.

Steps to run the various modules of our system:

1) Web Server (Django-Python): python manage.py runserver <ip_addr>:<port>

2) Accident Alert system (Raspberry Pi + ADXL335 Accelerometer + GPS Module): 
	a) Interface the ADXL335 sensors and the GPS Module with the Raspberry Pi 
	b) Run the python scripts acclocation.py and Adxl.py

3) CCTV Accident Detection (Python + YOLO Object Detector with OpenCV):
	a) Enter the directory of YOLO-object-detection (To be downloaded from github)
	b) Copy yolo_video.py to the directory and enter in terminal: 
	python yolo_video.py --input <input path to video> --yolo yolo-coco 

4) Blackspot Detection (googlemaps api + Clustering Algorithm): This Module runs automatically on the webserver from inputs obtained from Modules (2) and (3)

5) Drowsiness Detection (Python + OpenCV + dlib): Standalone application
	a) Run in terminal: python detect_drowsiness.py --shape-predictor shape_predictor_68_face_landmarks.dat --alarm alarm.wav
