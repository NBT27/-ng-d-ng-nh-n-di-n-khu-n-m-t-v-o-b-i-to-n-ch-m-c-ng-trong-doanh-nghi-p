# -*- coding: utf-8 -*-

import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter

from Employees import Employee, EmployeesList
from Attendance_Window import AttendanceWindow
from Add_Employee_Window import AddEmployeeWindow
from Synthesize_Files import SynthesizeFiles

class MainWindow:        
    def __init__(self, root):
        icon_folder = "Picture"
        
        # Đọc danh sách nhân viên
        self.EmployeesList = EmployeesList()
        self.embedding_data_FaceNet, self.embedding_data_cv2, self.employees_list = self.load_embedding_data()
        
        self.root = root
        self.root.title('Hệ thống chấm công')
        self.root.geometry("800x600")  # Đặt kích thước cửa sổ
        self.root.minsize(850,500)

        # Load ảnh nền và icon ---------------------------------------------------------------------------------
        # Thêm hình nền
        self.background_image = Image.open(f"{icon_folder}/download.jpg")
        self.background_label = tk.Label(root)
        self.background_label.place(relwidth=1, relheight=1)

        # Load ảnh cho nút Check in
        check_in_image = Image.open(f"{icon_folder}/check-in.png")
        check_in_image = check_in_image.resize((50, 50), Image.LANCZOS)
        self.check_in_photo = ImageTk.PhotoImage(check_in_image)

        # Load ảnh cho nút Check out
        check_out_image = Image.open(f"{icon_folder}/check-out.png")
        check_out_image = check_out_image.resize((50, 50), Image.LANCZOS)
        self.check_out_photo = ImageTk.PhotoImage(check_out_image)

        # Load ảnh cho nút Thêm nhân viên
        add_employee_image = Image.open(f"{icon_folder}/add-person.png")
        add_employee_image = add_employee_image.resize((50, 50), Image.LANCZOS)
        self.add_employee_photo = ImageTk.PhotoImage(add_employee_image)

        # Load ảnh cho nút Thêm nhân viên
        synthesize_file_image = Image.open(f"{icon_folder}/shared-folder.png")
        synthesize_file_image = synthesize_file_image.resize((50, 50), Image.LANCZOS)
        self.synthesize_file_photo = ImageTk.PhotoImage(synthesize_file_image)

        # Tạo kiểu cho button (style)
        self.button_style = ttk.Style()
        self.button_style.configure("TButton", font=("Helvetica", 12), padding=5, relief="flat",
                                    background="#4CAF50", foreground="black")

        # Nút Check in với ảnh
        self.check_in_button = ttk.Button(root, text="Check-in", image=self.check_in_photo,
                                           compound="left", style="TButton", command=self.check_in)

        # Nút Check out với ảnh
        self.check_out_button = ttk.Button(root, text="Check-out", image=self.check_out_photo,
                                            compound="left", style="TButton", command=self.check_out)

        # Nút Thêm Sinh viên với ảnh
        self.add_employee_button = ttk.Button(root, text="Thêm nhân viên",
                                              image=self.add_employee_photo, compound="left",
                                              style="TButton", command=self.add_employee)

        # Nút Thêm Tổng hợp file với ảnh
        self.synthesize_file_button = ttk.Button(root, text="Tổng hợp file",
                                                 image=self.synthesize_file_photo, compound="left",
                                                 style="TButton", command=self.synthesize_file)

        # Gắn sự kiện thay đổi kích thước cửa sổ
        self.root.bind("<Configure>", self.on_window_resize)

        # Tắt tự động điều chỉnh kích thước của widget
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

    def on_window_resize(self, event):
        # Khi kích thước cửa sổ thay đổi, cập nhật kích thước và phủ mờ lại background
        width = self.root.winfo_width()
        height = self.root.winfo_height()
    
        # Thay đổi kích thước hình nền
        resized_image = self.background_image.resize((width, height), Image.LANCZOS)
        blurred_background_image = resized_image.filter(ImageFilter.BLUR)
        blurred_background_photo = ImageTk.PhotoImage(blurred_background_image)
    
        # Cập nhật background phủ mờ
        self.background_label.config(image=blurred_background_photo)
        self.background_label.image = blurred_background_photo
    
        # Căn giữa theo chiều dọc
        vertical_padding = (height - 4 * self.check_out_button.winfo_reqheight()) // 5
    
        # Tính toán tọa độ cho nút Check-in
        self.check_in_button.place(relx=0.35, rely=0.4, anchor="center")
    
        # Tính toán tọa độ cho nút Check-out
        self.check_out_button.place(relx=0.65, rely=0.4, anchor="center")
    
        # Tính toán tọa độ cho nút Thêm nhân viên
        self.add_employee_button.place(relx=0.35, rely=0.6, anchor="center")
    
        # Tính toán tọa độ cho nút Tổng hợp file
        self.synthesize_file_button.place(relx=0.65, rely=0.6, anchor="center")
    
    
    def check_in(self):
        self.root.withdraw()
        check_in_window = tk.Toplevel(self.root)
        title = 'Check-in'
        AttendanceWindow(check_in_window, self.show_menu, self.embedding_data_FaceNet, 
                         self.embedding_data_cv2, self.employees_list, title)
        
    def check_out(self):
        self.root.withdraw()
        check_out_window = tk.Toplevel(self.root)
        title = 'Check-out'
        AttendanceWindow(check_out_window, self.show_menu, self.embedding_data_FaceNet, 
                         self.embedding_data_cv2, self.employees_list, title)

    def add_employee(self):
        self.root.withdraw()
        add_employee_window = tk.Toplevel(self.root)
        AddEmployeeWindow(add_employee_window, self.show_menu, self.embedding_data_FaceNet, 
                         self.embedding_data_cv2, self.employees_list, self.update_embeddings_and_list)
        
    def synthesize_file(self):
        self.root.withdraw()
        synthesize_file_window = tk.Toplevel(self.root)
        SynthesizeFiles(synthesize_file_window, self.show_menu)
    
    def show_menu(self):
        self.root.deiconify()  # Hiển thị lại cửa sổ menu
        
    def load_embedding_data(self):
        dataset_folder = "Dataset"
        embedding_data_FaceNet = np.load(f"{dataset_folder}/Employee_data_embedding_FaceNet.npy")
        embedding_data_cv2 = np.load(f"{dataset_folder}/Employee_data_embedding_cv2.npy")
        students = np.load(f"{dataset_folder}/Employee_data_label.npy")
        print('Loaded embedding')
        
        return embedding_data_FaceNet, embedding_data_cv2, students
    
    def update_embeddings_and_list(self, embedding_data_FaceNet, embedding_data_cv2, employees_list):
        self.embedding_data_FaceNet = embedding_data_FaceNet
        self.embedding_data_cv2 = embedding_data_cv2
        self.employees_list = employees_list
        # self.root.deiconify()  # Show the main window again

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()