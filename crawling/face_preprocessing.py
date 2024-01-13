from deepface import DeepFace
from deepface.commons import functions
from deepface.detectors import FaceDetector
import cv2

backend = 'mtcnn' #face detection에 사용할 pre-trained 모델
save_nums = 1 #저장할 이미지 숫자
image_nums = 1 #원본 이미지 숫자
total_image_nums = 1255 - image_nums +1 #가져올 전체 원본 이미지 개수

for i in range(total_image_nums):
    #img_path = 'images_google/image_{}.jpg'.format(image_nums+i) #원본 이미지 저장 경로(구글)
    img_path = 'images_pinterest/image_{}.jpg'.format(image_nums+i) #원본 이미지 저장 경로(핀터레스트)
    
    #얼굴 크롭 and 얼굴 정렬 (traget은 1024, 1024)
    detected_and_aligned_faces = DeepFace.extract_faces(img_path, target_size=(1024, 1024), detector_backend = backend, align=True, enforce_detection=False)
    #얼굴 검출 안되면 오류나고 멈춤. (save_nums, image_nums 조절해서 다시 실행)
        
    for detected_and_aligned_face in detected_and_aligned_faces:
        detected_and_aligned_face = detected_and_aligned_face['face']
        save_path = 'images_crop_1024/image_{}.jpg'.format(save_nums) #전처리 이미지 저장 경로
        
        # #이미지 보기(선택)
        # detected_and_aligned_face_rgb = cv2.cvtColor(detected_and_aligned_face[0], cv2.COLOR_BGR2RGB)#BGR to RGB 변환
        # print(detected_and_aligned_face_rgb)
        # cv2.imshow('Image view', detected_and_aligned_face_rgb)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        #이미지 저장
        print('--원본 이미지 번호{}--'.format(i+image_nums))
        detected_face = detected_and_aligned_face * 255
        cv2.imwrite(save_path, detected_face[:, :, ::-1])
        print('--{}번째 이미지 저장 완료--'.format(save_nums))
        save_nums += 1
    