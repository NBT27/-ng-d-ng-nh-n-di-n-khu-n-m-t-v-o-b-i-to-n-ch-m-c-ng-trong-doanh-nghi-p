# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 20:30:30 2024

@author: batha
"""

import os
import numpy as np
from keras_facenet import FaceNet
from tensorflow.keras.preprocessing import image

class PrepareData:
    
    def __init__(self):
        self.data_prepare()
    
    def data_prepare(self):
        # Đường dẫn đến thư mục Human_data_cropped
        data_folder = "Employees"
        
        # Import Keras FaceNet 
        facenet_model = FaceNet()  
        embedding_data_FaceNet = []
        embedding_data_cv2s = []
        label = []
        
        def load_and_preprocess_image(image_path):
            img = image.load_img(image_path, target_size=(160, 160))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            # img_array = preprocess_input(img_array)
            return img_array
        
        face_location = (0, 160, 160, 0)
        
        # Duyệt qua tất cả các thư mục con trong Human_data_cropped
        for folder_name in os.listdir(data_folder):
            folder_path = os.path.join(data_folder, folder_name)
            
            # Kiểm tra xem đối tượng trong folder_path có phải là thư mục không
            if os.path.isdir(folder_path):
                # Lấy danh sách các file ảnh trong thư mục con
                image_files = [file for file in os.listdir(folder_path) if file.endswith(".jpg") or file.endswith(".png")]
                
                # Kiểm tra xem có ít nhất 1 file ảnh trong thư mục con hay không
                if len(image_files) > 0:
                    # Lấy đường dẫn của ảnh đầu tiên trong danh sách
                    img_path = os.path.join(folder_path, image_files[0])
                    print(img_path)
        
                     # Load và xử lý ảnh
                    img_array = load_and_preprocess_image(img_path)
            
                    # Sử dụng FaceNet để nhúng ảnh
                    embedding_FaceNet = facenet_model.embeddings(img_array)
                    
                    embedding_data_FaceNet.append(embedding_FaceNet)
                    label.append(folder_name)
        
        np.save('Employee_data_embedding_FaceNet', embedding_data_FaceNet)
        np.save('Employee_data_label', label)