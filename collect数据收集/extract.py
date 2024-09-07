import cv2
import os
import matplotlib as plt

# save_step=50
# num=0
# data_dir='D:\\datasets\\origin_video+images_20240716\\'
# for filename in os.listdir(data_dir): 
#         # print('ok1')
#         if filename.lower().endswith('.mp4'): 
#             # print(filename)
#             video_dir=data_dir+filename
#             print(video_dir)
#             video=cv2.VideoCapture(video_dir)
#             while True:
#                 # print('ok3')
#                 ret, frame = video.read()
#                 if not ret:
#                     break
#                 num+=1
#                 # print('do')
#                 if num%save_step==0:
#                     # print('ok')
#                     cv2.imwrite("D:\\datasets\\temp\\"+str(num+280900)+".jpg",frame)



save_step=1
num=000000

video=cv2.VideoCapture('C:\\Users\\li\\Desktop\\repo\\SiamTrackers-master\\NanoTrack\\data\\got_tank\\originvideo\\35.mp4')
while True:
    # print('ok3')
    ret, frame = video.read()
    if not ret:
        break
    num+=1
    # print('do')
    if num%save_step==0:
        # print('ok')
        image_path="C:\\Users\\li\\Desktop\\repo\\SiamTrackers-master\\NanoTrack\\data\\got_tank\\train\\000002\\"
        new_filename = f"{num:08d}.jpg"  
        new_file_path = os.path.join(image_path, new_filename)  
        cv2.imwrite(new_file_path,frame)

                