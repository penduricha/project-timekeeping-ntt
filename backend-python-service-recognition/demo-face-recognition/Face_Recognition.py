# Cài đặt thư viện
# !pip install -q insightface onnxruntime opencv-python-headless matplotlib pillow

# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# import base64
# from io import BytesIO
# from PIL import Image
# from google.colab import files
# from insightface.app import FaceAnalysis
# from insightface.utils import face_align
# import pandas as pd

# app = FaceAnalysis(allowed_modules=['detection', 'recognition'])
# app.prepare(ctx_id=0, det_size=(640, 640))

# def upload_and_get_base64():
#     print("Please upload ảnh...")
#     uploaded = files.upload()
#     for filename in uploaded.keys():
#         bytes_data = uploaded[filename]
#         b64 = base64.b64encode(bytes_data).decode('utf-8')
#         print(f"Upload thành công: {filename}")
#         return b64

# def base64_to_image(b64_string):
#     if ',' in b64_string:
#         b64_string = b64_string.split(',')[1]
#     if b64_string.startswith("data:image/png;base64,"):
#        b64_string = b64_string.replace("data:image/png;base64,", "")
#     img_data = base64.b64decode(b64_string)
#     nparr = np.frombuffer(img_data, np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     if img is None:
#         raise ValueError("Base64 không phải ảnh hợp lệ!")
#     return img

# def get_face_info(b64_string):
#     embedding = None
#     bbox = None
#     aligned = None
#     img = base64_to_image(b64_string)
#     faces = app.get(img)
#     if len(faces) == 0:
#         # raise ValueError("No face detected.")
#         embedding = None
#         bbox = None
#         aligned = None
#     else:
#       face = max(faces, key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
#       aligned = face_align.norm_crop(img, face.kps, image_size=112)
#       embedding = face.normed_embedding
#       bbox = face.bbox.astype(int)
#     return img, aligned, embedding, bbox

# def compare_faces_and_recognize(b64_1, b64_2):
#   orig1, aligned1, emb1, bbox1 = get_face_info(b64_1)
#   orig2, aligned2, emb2, bbox2 = get_face = get_face_info(b64_2)
#   b64_return = None
#
#   cosine = 0
#   distance = 0
#   percent = 0
#   # result = -1: Ko tìm thấy,
#   # result = -2: Khuôn mặt chưa được tạo trong hệ thống.
#   # result = 0: Ko phải nhân viên.
#   # result = 1: Là nhân viên
#
#   if emb1 is None:
#     cosine = 0
#     distance = 0
#     percent = 0
#     result = -1
#   elif emb2 is None:
#     cosine = 0
#     distance = 0
#     percent = 0
#     result = -2
#   else:
#     emb1 = emb1 / np.linalg.norm(emb1)
#     emb2 = emb2 / np.linalg.norm(emb2)
#
#     cosine = np.dot(emb1, emb2)
#     distance = 1 - cosine
#     percent = cosine * 100
#
#     if distance < 0.30:
#         result = 1
#         color = "green"
#         b64_return = b64_2
#     elif distance < 0.45:
#         result = 1
#         color = "limegreen"
#         b64_return = b64_2
#     elif distance < 0.60:
#         result = 0
#         color = "orange"
#     else:
#         result = 0
#         color = "red"
#   return cosine, distance, percent, result, b64_return

# def compare_faces(b64_1, b64_2):
#     orig1, aligned1, emb1, bbox1 = get_face_info(b64_1)
#     orig2, aligned2, emb2, bbox2 = get_face = get_face_info(b64_2)
#
#     if emb1 is None or emb2 is None:
#       print("Ko có khuôn mặt")
#       return
#     cosine = np.dot(emb1, emb2)
#     distance = 1 - cosine
#     percent = cosine * 100
#
#     if distance < 0.30:
#         result = "Hoàn toàn cùng 1 người"
#         color = "green"
#     elif distance < 0.45:
#         result = "Tương đối cùng 1 người"
#         color = "limegreen"
#     elif distance < 0.60:
#         result = "Hơi khác người"
#         color = "orange"
#     else:
#         result = "Hoàn toàn khác người"
#         color = "red"
#
#     print(f"Cosine similarity: {cosine}")
#     print(f"Khoảng cách: {distance}")
#     print(f"Độ giống: {percent}%")
#     print(f"Kết quả: {result}")
#
#     # Plot ảnh kết quả đẹp
#     orig1_rgb = cv2.cvtColor(orig1, cv2.COLOR_BGR2RGB)
#     orig2_rgb = cv2.cvtColor(orig2, cv2.COLOR_BGR2RGB)
#
#     cv2.rectangle(orig1_rgb, (bbox1[0], bbox1[1]), (bbox1[2], bbox1[3]), (0,255,0), 4)
#     cv2.rectangle(orig2, (bbox2[0], bbox2[1]), (bbox2[2], bbox2[3]), (0,255,0), 4)
#
#     plt.figure(figsize=(16,10))
#
#     plt.subplot(2,3,1); plt.imshow(orig1_rgb); plt.title("Ảnh 1"); plt.axis('off')
#     plt.subplot(2,3,2); plt.imshow(aligned1); plt.title("Cắt chuẩn 112x112"); plt.axis('off')
#     plt.subplot(2,3,3); plt.imshow(orig2_rgb); plt.title("Ảnh 2"); plt.axis('off')
#     plt.subplot(2,3,5); plt.imshow(aligned2); plt.title(f"{result}\n{percent:.1f}%", color=color, fontsize=16, fontweight='bold'); plt.axis('off')
#
#     plt.subplot(2,3,4)
#     plt.barh(["Similarity"], [cosine], color='skyblue')
#     plt.xlim(0,1)
#     plt.title(f"Cosine = {cosine:.4f}")
#
#     plt.subplot(2,3,6)
#     plt.text(0.5, 0.6, "INSIGHTFACE ArcFace\n2025 Accuracy", ha='center', va='center', fontsize=14, transform=plt.gca().transAxes)
#     plt.text(0.5, 0.3, f"Distance = {distance:.4f}\nThreshold < 0.30", ha='center', va='center', fontsize=12, color='red', transform=plt.gca().transAxes)
#     plt.axis('off')
#
#     plt.suptitle("SO SÁNH KHUÔN MẶT CHUẨN XÁC NHẤT 2025", fontsize=20, fontweight='bold')
#     plt.tight_layout()
#     plt.show()

# b64_1 = upload_and_get_base64()
# b64_2 = upload_and_get_base64()
# dfEmployees = pd.DataFrame({
#     'employee_id' : [2119],
#     'employee_name' : ['Từ Quang Nhật'],
#     'gender' : [True],
#     'employee_image_b64' : [b64_2]
# })

# run
# compare_faces(b64_1, b64_2)
# try:
#   cosine, distance, percent, result, b64_return = compare_faces_and_recognize(b64_1, b64_2)
#   print(f"Cosine similarity: {cosine}")
#   print(f"Khoảng cách: {distance}")
#   print(f"Độ giống: {percent}%")
#   print(f"Kết quả: {result}")
# except ValueError as e:
#   print('Hệ thống không nhận diện được:', e)

# employee_id = None
# employee_name = None
# gender = None
# for index, row in dfEmployees.iterrows():
#     cosine, distance, percent, result, b64_return = compare_faces_and_recognize(b64_1, row['employee_image_b64'])
#     if(result == 1):
#         employee_id = row['employee_id']
#         employee_name = row['employee_name']
#         gender = row['gender']
#         break
# employee_id, employee_name, gender