# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 23:01:16 2024

@author: batha
"""

import os
import cv2
import datetime
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Employees import Employee, EmployeesList

from keras_facenet import FaceNet
import face_recognition
import time


class AttendanceWindow:
    process_current_frame = True
    face_names = ""
    face_locations = []
    
    def __init__(self, root, show_menu_callback,embedding_data_FaceNet, embedding_data_cv2, employees_list, title):
        
        self.EmpList = EmployeesList
        self.show_menu_callback = show_menu_callback
        self.embedding_data_FaceNet = embedding_data_FaceNet
        self.embedding_data_cv2 = embedding_data_cv2
        self.employees_list = employees_list
        self.title = title
        
        # Cửa sổ giao diện:
        self.root = root
        self.root.title(title)
        self.root.minsize(800,550)
        
        # Tạo và cấu hình video feed
        self.cap = cv2.VideoCapture(0)
        self.video_frame = tk.Label(root)
        self.video_frame.grid(row=0, column=0, padx=10, pady=10)

        # Tạo frame cho thông tin 
        self.info_frame = ttk.Frame(root)
        self.info_frame.grid(row=0, column=1, padx=10, pady=10)
        
        # # Hiển thị thông tin 
        self.employeeID_label = ttk.Label(self.info_frame, text="Mã nhân viên:")
        self.employeeID_label.grid(row=1, column=0, pady=10)
        self.status_label = ttk.Label(self.info_frame, text = "Trạng thái: ")
        self.status_label.grid(row=3, column=0,pady=10)
        
        self.back_button = ttk.Button(self.info_frame, text="Quay lại", command=self.show_menu)
        self.back_button.grid(row=4, column=0, pady=10)
        
        self.run_recognition()
        
    def show_menu(self):
        self.root.destroy()  # Xóa cửa sổ chấm công
        self.show_menu_callback()  # Hiển thị lại cửa sổ menu
        
    def create_csv_file(self, title):
        header = ['ID']

        # Tạo thư mục với định dạng Year/month_Year 
        month_folder  = datetime.datetime.now().strftime("%Y-%m")
        date_folder  = datetime.datetime.now().strftime("%Y%m%d")
        month_folder_path= os.path.join("Temp", month_folder)
        
        folder_name = os.path.join("Temp", month_folder,date_folder)
        
        # Kiểm tra xem thư mục đã tồn tại chưa
        if not os.path.exists(month_folder_path):
            os.mkdir(month_folder_path)

        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
            
        file_name = datetime.datetime.now().strftime(f"{title}_%Y%m%d.csv")
        file_path = os.path.join(folder_name, file_name)
        
        # Kiểm tra xem file đã tồn tại chưa
        if not os.path.isfile(file_path):
            # Tạo DataFrame với header
            df = pd.DataFrame(columns=header)

            # Ghi DataFrame vào file CSV
            df.to_csv(file_path, index=False, encoding='utf-8')

        return file_path
    
    def find_largest_face(self):
        if not self.face_locations:
            return None

        largest_face_index = np.argmax([(bottom - top) * (right - left) for (top, right, bottom, left) in self.face_locations])
        return largest_face_index
    
    def euclidean_distance(self, embedding1, embedding2):
        return np.linalg.norm(embedding1 - embedding2)
    
    def write_to_csv(self,current_employee_id,csv_file_path, title):
        # Kiểm tra xem có thông tin sinh viên hiện tại không
        if current_employee_id is not None:
            employee_id = current_employee_id
            
            # Lấy thời gian điểm danh
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Đọc dữ liệu từ file CSV vào DataFrame (nếu file tồn tại)
            df = pd.DataFrame()
            if os.path.exists(csv_file_path):
                df = pd.read_csv(csv_file_path, encoding='utf-8')

            # Kiểm tra xem ID đã tồn tại trong DataFrame không
            id_exists = self.check_id_exists_in_dataframe(df, employee_id)

            # Nếu ID không tồn tại, thêm dòng mới vào DataFrame và ghi vào file
            if not id_exists:
                new_row = pd.DataFrame({
                    'ID': [employee_id],
                    'Date': [date],
                    f'{title} time': [time]
                })
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(csv_file_path, index=False, encoding='utf-8')

    def check_id_exists_in_dataframe(self, df, employee_id):
        # Kiểm tra xem ID đã tồn tại trong DataFrame không
        return not df.empty and employee_id in df['ID'].values
    
    def run_recognition(self):
        MyFaceNet = FaceNet()
        
        attended_file_name = self.create_csv_file(self.title)

        
        while True:
            face_distances_FaceNet = []
            ret, frame = self.cap.read()
            
            #----------------------------------------------
            start_time = time.time()

            if self.process_current_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]

                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                face_names = ""
                largest_face_index = self.find_largest_face()

                if largest_face_index is not None:
                
                    name = 'Unknown'
                 
                    (top, right, bottom, left) = self.face_locations[largest_face_index]
                    face = rgb_small_frame[top:bottom, left:right]
                    face = Image.fromarray(face)
                    face = face.resize((160, 160))
                    face = np.asarray(face)
                    face = np.expand_dims(face, axis=0)
                
                    # Dự đoán chữ ký của khuôn mặt sử dụng mô hình FaceNet
                    signature = MyFaceNet.embeddings(face)
              
                    for i in range(len(self.employees_list)):
                        dist_FaceNet = self.euclidean_distance(self.embedding_data_FaceNet[i], signature)
                        face_distances_FaceNet.append(dist_FaceNet)
               
                
                    # Tìm nhân viên có khoảng cách nhỏ nhất
                    best_match_index = np.argmin(face_distances_FaceNet)
                    if face_distances_FaceNet[best_match_index] < 0.85:
                        name = self.employees_list[best_match_index]
                        self.current_employee = (name)
                    else:
                        name = "Unknown"

                    self.face_names = [f'{name}']
                
            self.process_current_frame = not self.process_current_frame
            
            
            # Hiển thị nhãn khuôn mặt
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
       
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), -1)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 1)
                
            # Chuyển đổi hình ảnh để hiển thị trên widget Tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)
            self.video_frame.configure(image=frame)
            self.video_frame.image = frame
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("Time elapsed: {:.5f} seconds".format(elapsed_time))
            print("---------------------------------------------------------")
                
            self.root.update()
            
            # Lưu và hiển thị thông tin điểm danh
            # Xóa thông tin sinh viên nếu không nhận diện được khuôn mặt
            if not self.face_names or 'Unknown' in self.face_names or largest_face_index is None:
                self.current_employee = None
                self.employeeID_label['text'] = "Mã nhân viên: "
                self.status_label['text'] = "Trạng thái: "
            else:
                self.write_to_csv(self.current_employee, attended_file_name, self.title)
                self.employeeID_label['text'] = f"Mã nhân viên: {self.current_employee}"
                self.status_label['text'] = f"Trạng thái: Đã {self.title}"
            
            
            if cv2.waitKey(1) == ord('q'):
                break
            
        self.cap.release()
        cv2.destroyAllWindows()
        
    # def run_attendance(self):
    #     if self.title == 'check out':