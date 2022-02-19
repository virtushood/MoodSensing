from types import GeneratorType
import numpy as np
import cv2
import time
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os

camera = cv2.VideoCaputre("mood-detection.mp4")

background = None
while True:
        (grabbed, frame) = camera.read()

if not grabbed:
    #break

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

if background is None:
    background = gray 
    #continue
subtratction = cv2.absdiff (background, gray)

threshold = cv2.threshold ( subtraction, 25, 255, cv2.THRESH_BINARY)

threshold = cv2.threshold( threshold, None, iterations = 2)

countouring = threshold.copy()

im, outlines, hierarchy = cv2.findCountours (outlinesimg,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for c in outlines:
    if cv2.countourArea (c) < 500:
        continue

(x,y,w,h) = cv2.boundingRect (c)

cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow ("Camera", frame)
cv2.imshow ("Threshold", threshold)
cv2.imshow("Subtraction", subtraction)
cv2.imshow ("countour", contourimg)

key = cv2.waitKey (1) & 0xFF

time.sleep(0.015)

if key == ord("s"):
    #break
camera.release()
cv2.destroyAllWindows()


#Code for uploading to cloud storage
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os


credentials_dict = {
    'type': 'service_account',
    'client_id': os.environ['BACKUP_CLIENT_ID'],
    'client_email': os.environ['BACKUP_CLIENT_EMAIL'],
    'private_key_id': os.environ['BACKUP_PRIVATE_KEY_ID'],
    'private_key': os.environ['BACKUP_PRIVATE_KEY'],
}
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    credentials_dict
)
client = storage.Client(credentials=credentials, project='myproject')
bucket = client.get_bucket('mybucket')
blob = bucket.blob('myfile')
blob.upload_from_filename('myfile')
