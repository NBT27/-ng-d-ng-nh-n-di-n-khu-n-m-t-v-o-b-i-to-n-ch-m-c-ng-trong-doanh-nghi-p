# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 13:00:28 2024

@author: batha
"""

import tkinter as tk
from tkinter import Canvas
from tkinter import ttk, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw
import pandas as pd
import face_recognition
from keras_facenet import FaceNet
import os
from Employees import Employee, EmployeesList


class AddEmployeeWindow:
    process_current_frame = True
   
    def __init__(self, root, show_menu_callback,embedding_data_FaceNet, embedding_data_cv2, employees_list, update_callback):
        
        self.employees_list = employees_list
        self.embedding_data_FaceNet = embedding_data_FaceNet
        self.embedding_data_cv2 = embedding_data_cv2
        self.show_menu_callback = show_menu_callback
        
        self.update_callback = update_callback  # Callback để cập nhật các biến trong MainWindow
        
        self.root = root
        self.root.title("Thêm nhân viên")
        self.root.geometry("400x300")  # Đặt kích thước cửa sổ

        self.EmpList = EmployeesList()
        
        self.MyFaceNet = FaceNet()
        
        self.setup_ui()
        
    def setup_ui(self):
        
        # Thiết lập cấu hình cột để căn giữa các thành phần
        self.root.columnconfigure(0, weight=1)  # Cột giữa
        self.root.columnconfigure(1, weight=1)  # Cột giữa
    
        # Tạo combo box chọn phòng ban
        department_label = ttk.Label(self.root, text="Phòng:")
        department_label.grid(row=0, column=0, pady=10, sticky="e")  # Căn phải
    
        department_options = ["Công nghệ thông tin", "Hậu cần và quản lý chuỗi cung ứng", 
                              "Kế toán", "Kinh doanh", "Nghiên cứu và phát triển", 
                              "Nhân sự", "Pháp luật", "Quan hệ cộng đồng",
                              "Quản lý dự án", "Quản trị chiến lược"]
        self.department_combo_box = ttk.Combobox(self.root, values=department_options, 
                                                 width=27)
        self.department_combo_box.grid(row=0, column=1, pady=10, sticky="w")  # Căn trái
        self.department_combo_box.set("Lựa chọn phòng ban")  # Thiết lập giá trị mặc định
        # self.department_combo_box.set("Công nghệ thông tin") 

        # Liên kết hàm với sự kiện chọn Combobox
        self.department_combo_box.bind("<<ComboboxSelected>>", self.handle_department_change)

        # Tạo entry nhập thông tin
        self.id_entry = ttk.Entry(self.root, textvariable=tk.StringVar(), width=30)
        id_entry_label = ttk.Label(self.root, text="Mã nhân viên:")
        id_entry_label.grid(row=1, column=0, pady=10, sticky="e")  # Căn phải
        self.id_entry.grid(row=1, column=1, pady=10, sticky="w")  # Căn trái
        
        #self.id_entry.insert(tk.END, "IT0145")        
        
        self.name_entry = ttk.Entry(self.root, textvariable=tk.StringVar(), width=30)
        name_entry_label = ttk.Label(self.root, text="Tên:")
        name_entry_label.grid(row=3, column=0, pady=10, sticky="e")  # Căn phải
        self.name_entry.grid(row=3, column=1, pady=10, sticky="w")  # Căn trái
        
        #self.name_entry.insert(tk.END, "Nguyen Thanh")

    
        # Tạo button
        confirm_button = ttk.Button(self.root, text="Tiếp theo", command=self.confirm_add_employee)
        confirm_button.grid(row=4, column=0, columnspan=2, pady=20)
    
        show_back_button = ttk.Button(self.root, text="Quay lại", 
                                      command=lambda: self.show_menu(self.root))
        show_back_button.grid(row=5, column=0, columnspan=2, pady=10)
        

    def handle_department_change(self, event):
        selected_department = self.department_combo_box.get()

        # Update id_entry based on the selected department
        if selected_department == "Công nghệ thông tin":
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, "IT")
        elif selected_department == "Hậu cần và quản lý chuỗi cung ứng":
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, "LS")
        elif selected_department == "Kế toán":
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, "AF")
        elif selected_department == "Kinh doanh":
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, "BD")
        elif selected_department == "Nghiên cứu và phát triển":
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, "RD")
        elif selected_department == "Nhân sự":
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, "HR")
        elif selected_department == "Pháp luật":
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, "CL")
        elif selected_department == "Quan hệ cộng đồng":
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, "PR")
        elif selected_department == "Quan hệ cộng đồng":
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, "PM")
        elif selected_department == "Quản trị chiến lược":
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, "SM")
        
            
    def show_menu(self, root):
        root.destroy()  # Xóa cửa sổ hiện tại
        self.show_menu_callback()  # Hiển thị lại cửa sổ menu
        
        
    def check_exist_by_id(self, employee_id):
        for student in self.employees_list:
            if student == employee_id:
                return student
     
        return None
    
    def confirm_add_employee(self):
        name = self.name_entry.get()
        employee_id = self.id_entry.get()
        department = self.department_combo_box.get()
        
        # Check if any field is empty
        if not name or not employee_id or not department or department == "Lựa chọn phòng ban":
            messagebox.showerror("Lỗi", "Vui lòng nhập đủ thông tin.")
            return

        existing_employee = self.check_exist_by_id(employee_id)
        if existing_employee:
            messagebox.showerror("Lỗi", "Nhân viên đã tồn tại với mã này.")
            return

        new_employee = Employee(employee_id, name, department)
   
        self.root.destroy()
        
        # Open camera window
        self.open_camera_window(new_employee)
        
    def open_camera_window(self, new_employee):
        self.camera_window = tk.Toplevel()
        self.camera_window.title("Camera")
        
        # Tạo và cấu hình video feed
        self.cap = cv2.VideoCapture(0)
        self.video_frame = tk.Label(self.camera_window)
        self.video_frame.grid(row=0, column=0, padx=10, pady=10)
        
       
        # Tạo frame cho thông tin điểm danh
        self.info_frame = ttk.Frame(self.camera_window)
        self.info_frame.grid(row=0, column=1, padx=10, pady=10)
    
        # Hiển thị thông tin điểm danh
        pad_x = 110
        self.name_label = ttk.Label(self.info_frame, text=f"Tên: {new_employee.name}")
        # self.name_label.grid(row=0, column=0, pady=10)
        self.name_label.grid(row=0, column=0, pady=10, padx=pad_x, sticky=tk.W)  
        self.studentID_label = ttk.Label(self.info_frame, text=f"Mã nhân viên: {new_employee.employeeID}")
        self.studentID_label.grid(row=1, column=0, pady=10, padx=pad_x, sticky=tk.W)
        self.major_label = ttk.Label(self.info_frame, text=f"Phòng: {new_employee.department}")
        self.major_label.grid(row=2, column=0, pady=10, padx=pad_x, sticky=tk.W)
    
        # Tạo khung canvas để hiển thị ảnh đã chụp
        self.captured_image_canvas = Canvas(self.info_frame, width=320, height=240)
        self.captured_image_canvas.grid(row=3, column=0, pady=10, padx=10, sticky=tk.W)
    
        self.capture_button = ttk.Button(self.info_frame, text="Chụp ảnh", command=lambda: self.capture_image(new_employee))
        self.capture_button.grid(row=4, column=0, pady=10, padx=pad_x,  sticky=tk.W)
    
        self.show_menu_button = ttk.Button(self.info_frame, text="Quay lại", command=lambda: self.show_menu(self.camera_window))
        self.show_menu_button.grid(row=5, column=0, pady=10, padx=pad_x,  sticky=tk.W)
    
         
        self.captured_face_filename = ""
        
        # Thêm dòng sau để tạo thư mục 'cropped_faces' trước khi chạy ứng dụng
        if not os.path.exists('cropped_faces'):
            os.makedirs('cropped_faces')
                
        while True:
            ret, frame = self.cap.read()
            
            if self.process_current_frame:
                small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
               
                largest_face_index = self.find_largest_face()
                
                    
            self.process_current_frame = not self.process_current_frame
            
            # Hiển thị nhãn khuôn mặt
            for (top, right, bottom, left) in self.face_locations:
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame, (left, bottom), (right, bottom), (0, 255, 0))

            # Chuyển đổi hình ảnh để hiển thị trên widget Tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)
            self.video_frame.configure(image=frame)
            self.video_frame.image = frame
            
            self.root.update()
                 
        self.cap.release()
        cv2.destroyAllWindows()
                
    def capture_image(self, new_employee):
        # Chụp frame hiện tại từ camera
        ret, frame = self.cap.read()

        # Thay đổi kích thước và chuyển đổi frame
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Lấy vị trí khuôn mặt
        largest_face_index = self.find_largest_face()
        if largest_face_index is not None:
            new_face = self.face_locations[largest_face_index]

            # Lưu khuôn mặt đã nhận diện thành tập tin JPG
            self.captured_face_filename = f'Temp/{new_employee.employeeID}.jpg'

            cv2.imwrite(self.captured_face_filename, frame)                    

            # Vẽ hộp khuôn mặt trên ảnh đã chụp
            self.draw_face_box(frame, new_face)

            # Hiển thị ảnh đã chụp trên canvas
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            image = image.resize((320, 240), Image.LANCZOS)     # Thay đổi kích thước ảnh thành 300x300
            photo = ImageTk.PhotoImage(image)   # Tạo đối tượng PhotoImage từ ảnh đã thay đổi kích thước
        
            # Hiển thị ảnh đã chụp trên canvas
            self.captured_image_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.captured_image_canvas.image = photo
            
            # Tạo button Lưu 
            self.save_button = ttk.Button(self.info_frame, text="Lưu", command=lambda: self.save_cropped_face(new_face, new_employee))
            self.save_button.grid(row=7, column=0, pady=10, padx=110, sticky=tk.W)  
            
        else:
            messagebox.showwarning("Cảnh báo", "Không tìm thấy khuôn mặt để chụp ảnh.")

    def draw_face_box(self, frame, face_location):
        top, right, bottom, left = face_location
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    def save_cropped_face(self, new_face, new_employee):
        if self.captured_face_filename:
            # Mở ảnh đã chụp
            image = Image.open(self.captured_face_filename)

            # Cắt khuôn mặt từ ảnh
            # face_location = self.face_locations[self.find_largest_face()]
            face_location = new_face
            top, right, bottom, left = face_location
            face_image = image.crop((left * 4, top * 4, right * 4, bottom * 4))
            face_image = face_image.resize((160, 160), Image.LANCZOS)
            
            # Lưu khuôn mặt đã cắt
            cropped_folder = os.path.join("Employees", f"{new_employee.employeeID}")
            if not os.path.exists(cropped_folder):
                os.mkdir(cropped_folder)
            cropped_filename = f'{cropped_folder}/{new_employee.name}.jpg'
            face_image.save(cropped_filename)
            os.remove(self.captured_face_filename)
            
            # Embedding và lưu vào dataset
            face_array = np.array(face_image)
            embedding_cv2 = face_recognition.face_encodings(face_array)
            new_employee_embedding_cv2 = np.array(embedding_cv2)
            face_array = np.expand_dims(face_array, axis=0)
            new_employee_embedding_FaceNet = self.MyFaceNet.embeddings(face_array)

            # Thêm embedding data của nhân viên mới
            self.embedding_data_cv2 = np.vstack([self.embedding_data_cv2, new_employee_embedding_cv2])
            self.embedding_data_FaceNet = np.concatenate([self.embedding_data_FaceNet, new_employee_embedding_FaceNet.reshape(1, 1, 512)])
            self.employees_list = np.append(self.employees_list, new_employee.employeeID)
          
            # Lưu thông tin nhân viên mới            
            np.save('Dataset/Employee_data_embedding_FaceNet', self.embedding_data_FaceNet)
            np.save('Dataset/Employee_data_embedding_cv2', self.embedding_data_cv2)
            np.save('Dataset/Employee_data_label', self.employees_list)
            
            self.update_callback(self.embedding_data_FaceNet, self.embedding_data_cv2, self.employees_list)

            # Lưu thông tin vào file excel
            self.save_new_student(new_employee)
            
            messagebox.showinfo("Thông báo", "Khuôn mặt đã được cắt và lưu thành công.")
            
            self.show_menu(self.camera_window)

        else:
            messagebox.showwarning("Cảnh báo", "Chưa có ảnh nào được chụp để lưu.")

    def find_largest_face(self):
        if not self.face_locations:
            return None

        largest_face_index = np.argmax([(bottom - top) * (right - left) for (top, right, bottom, left) in self.face_locations])
        return largest_face_index
        
    def save_new_student(self, new_employee):
        # self.EmpList.write_to_csv(new_employee, 'Dataset/Employee_list.csv')
        self.EmpList.write_to_csv(new_employee, 'Dataset/Employee_list.xlsx')

    
        
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = AddStudentWindow(root)
#     root.mainloop()
                