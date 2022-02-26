#ECE528 Mood Sensing Project
#Created by Garrett Parks
import cv2, time
 
# Assigning our background image to None
background_init = None

video = cv2.VideoCapture(0)
 
# While loop set to cycle every 2 seconds to avoid spam capture.
while True:

    check, frame = video.read()
 
    motion_detected = 0
 
    #gray-scale the captured image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    #grayscale image is put through GaussianBlur filter to help detection.
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
    #initialize background with first image detected
    if background_init is None:
        background_init = gray
        continue
 

    image_diff = cv2.absdiff(background_init, gray)
 
    # If change in between static background and
    # current frame is greater than 30 it will show white color(255)
    image_threshold = cv2.threshold(image_diff, 30, 255, cv2.THRESH_BINARY)[1]

    image_threshold = cv2.dilate(image_threshold, None, iterations = 2)

    cnts,_ = cv2.findContours(image_threshold.copy(),
                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        motion_detected = 1
 
        #(x, y, w, h) = cv2.boundingRect(contour)
        # making green rectangle around the moving object
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)


    if motion_detected == 1:
        cv2.imshow("Color Frame", frame)
        print("Motion Detected. Sending image to cloud.")

        # credentials_dict = {
        #     'type': 'service_account',
        #     'client_id': os.environ['BACKUP_CLIENT_ID'],
        #     'client_email': os.environ['BACKUP_CLIENT_EMAIL'],
        #     'private_key_id': os.environ['BACKUP_PRIVATE_KEY_ID'],
        #     'private_key': os.environ['BACKUP_PRIVATE_KEY'],
        # }
        # credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        #     credentials_dict
        # )
        # client = storage.Client(credentials=credentials, project='myproject')
        # bucket = client.get_bucket('mybucket')
        # blob = bucket.blob('myfile')
        # blob.upload_from_filename('myfile')


    key = cv2.waitKey(1)
    # if q entered whole process will stop
    if key == ord('q'):
        break
    time.sleep(2)
 
video.release()
cv2.destroyAllWindows()