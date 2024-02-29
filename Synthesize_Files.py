# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 19:36:27 2024

@author: batha
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import datetime
import os
from Prepare_Data import PrepareData

class SynthesizeFiles:
    def __init__(self, root, show_menu_callback):
        self.root = root
        self.root.title("Tổng hợp dữ liệu")
        self.root.geometry("800x600")  # Đặt kích thước cửa sổ
        self.root.minsize(850,500)
        self.show_menu_callback = show_menu_callback
        
        self.employee_list_filename = 'Dataset/Employee_list.xlsx'
        self.month_folder = datetime.datetime.now().strftime('%Y-%m')
        self.date_folder = datetime.datetime.now().strftime('%Y%m%d')
        self.folder_path = os.path.join('Temp', self.month_folder, self.date_folder)
        self.checkin_filename = os.path.join(self.folder_path, f"Check-in_{self.date_folder}.csv")
        self.checkout_filename = os.path.join(self.folder_path, f"Check-out_{self.date_folder}.csv")
        
        self.button_style = ttk.Style()
        self.button_style.configure("TButton", font=("Helvetica", 12), padding=5, relief="flat", 
                                    background="#4CAF50", foreground="black")

        
        # Nút tổng hợp theo ngày
        self.day_synthesize = ttk.Button(self.root, text="Tổng hợp theo ngày", 
                                         style="TButton", command=self.day_synthesizes, width=25)
        self.day_synthesize.grid(row=0, column=0, pady=50, padx=350, sticky=tk.W) 

        # Tổng hợp theo tháng
        self.month_synthesize= ttk.Button(self.root, text="Tổng hợp theo tháng", 
                                          style="TButton", command=self.month_synthesizes, width=25)
        self.month_synthesize.grid(row=1, column=0, pady=10, padx=350, sticky=tk.W) 
        
        # Tổng hợp theo năm 
        self.year_synthesize= ttk.Button(self.root, text="Tổng hợp theo năm", 
                                         style="TButton", command=self.year_synthesizes, width=25)
        self.year_synthesize.grid(row=2, column=0, pady=10, padx=350, sticky=tk.W) 
        
        # Cập nhật dữ liệu 
        self.update_employee= ttk.Button(self.root, text="Cập nhật dữ liệu nhân viên", 
                                         style="TButton", command=lambda: PrepareData(), width=25)
        self.update_employee.grid(row=3, column=0, pady=10, padx=350, sticky=tk.W) 
        
        # Quay lại
        self.button_back= ttk.Button(self.root, text="Quay lại", 
                                         style="TButton", command=lambda: self.show_menu())
        self.button_back.grid(row=4, column=0, pady=10, padx=350, sticky=tk.W) 
        
        # Gắn sự kiện thay đổi kích thước cửa sổ
        self.root.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, event):    
        # Tính toán tọa độ cho các nút 
        self.day_synthesize.place(relx=0.5, rely=0.3, anchor="center")
        self.month_synthesize.place(relx=0.5, rely=0.4, anchor="center")
        self.year_synthesize.place(relx=0.5, rely=0.5, anchor="center")
        self.update_employee.place(relx=0.5, rely=0.6, anchor="center")
        self.button_back.place(relx=0.5, rely=0.7, anchor="center")
        
    def show_menu(self):
        self.root.destroy()  # Xóa cửa sổ chấm công
        self.show_menu_callback()  # Hiển thị lại cửa sổ menu
        
    def day_synthesizes(self):
        
        year = self.month_folder[:4]
        os.makedirs(os.path.join("Attendance_file", year), exist_ok=True)
        folder_out = os.path.join("Attendance_file", year, self.month_folder)
        os.makedirs(folder_out, exist_ok=True)
        
        if os.path.exists(self.checkin_filename) and os.path.exists(self.checkout_filename) and os.path.exists(self.employee_list_filename):
            # Đọc dữ liệu từ CHECK-IN, CHECK-OUT và Employee_list
            checkin_df = pd.read_csv(self.checkin_filename)
            checkout_df = pd.read_csv(self.checkout_filename)
            employee_list_df = pd.read_excel(self.employee_list_filename)
         
            # Gộp hai dataframe theo trường ID và date
            merged_df = pd.merge(checkin_df, checkout_df, on=['ID', 'Date'], how='inner')
         
            # Gộp dataframe đã gộp với dữ liệu từ Employee_list sử dụng gộp "outer"
            final_merged_df = pd.merge(employee_list_df, merged_df, on='ID', how='outer')
         
            # Chọn các cột quan trọng
            result_df = final_merged_df[['ID', 'Date', 'Check-in time', 'Check-out time']]
            
            # Lưu kết quả vào tệp CSV mới
            result_filename = f'{folder_out}/{self.checkin_filename[-12:]}'
            result_df.to_csv(result_filename, index=False)
            print(f"result_filename:{result_filename}")
        
        if os.path.exists(self.checkin_filename):
            print("exists(checkin_filename)")
            
        if os.path.exists(self.checkout_filename):
            print("os.path.exists(checkout_filename)")
            
        if os.path.exists(self.employee_list_filename):
            print("os.path.exists(employee_list_filename)")

    def add_additional_columns(self,df):
        # Thêm cột Month, Quarter, Year từ cột 'Date' (đảm bảo 'Date' là kiểu datetime)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='%d/%m/%Y')
        df['Month'] = df['Date'].dt.month
        df['Quarter'] = df['Date'].dt.quarter
        df['Year'] = df['Date'].dt.year
    
        # Thêm cột StatusInTime
        df['StatusInTime'] = "Absent"  # Mặc định là 0
        time_check_in = pd.to_datetime('08:30:00', format='%H:%M:%S').time()
    
        df.loc[~df['Check-in time'].isna(), 'StatusInTime'] = df.loc[~df['Check-in time'].isna(), 'Check-in time'].apply(
            lambda x: "OnTime" if pd.to_datetime(x, errors='coerce', format='%d/%m/%Y %H:%M:%S').time() >= time_check_in else (
                "Late" if pd.to_datetime(x, errors='coerce', format='%d/%m/%Y %H:%M:%S').time() < time_check_in else 0
            )
        )
    
        # Thêm cột CountDays
        df['CountDays'] = 1  # Mặc định là 1
    
        return df

    def month_synthesizes(self):
        year = self.month_folder[:4]
        folder_path = os.path.join("Attendance_file", year, self.month_folder)
        folder_out = os.path.join("Attendance_file", year)

        # Kiểm tra xem thư mục tồn tại không
        if not os.path.exists(folder_path):
            print(f"Folder '{folder_path}' does not exist.")
            return None
    
        # Lưu trữ tất cả các DataFrame từ các tệp CSV vào một danh sách
        all_dataframes = []
    
        # Lặp qua tất cả các tệp CSV trong thư mục
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                
                # Đọc từng tệp CSV và thêm vào danh sách
                df = pd.read_csv(file_path)
                df = self.add_additional_columns(df)
                all_dataframes.append(df)
    
        # Kiểm tra xem danh sách có dữ liệu hay không
        if not all_dataframes:
            print(f"No CSV files found in the folder '{folder_path}'.")
            return None
    
        # Nối tất cả các DataFrame thành một lớn
        concatenated_df = pd.concat(all_dataframes, ignore_index=True)
    
        result_filename = os.path.join(folder_out, f'Attended_{folder_path[-7:]}.csv')
        concatenated_df.to_csv(result_filename, index=False)
        
    def year_synthesizes(self):
        year = self.month_folder[:4]
        folder_path = os.path.join("Attendance_file", year)
        
        # Kiểm tra xem thư mục tồn tại không
        if not os.path.exists(folder_path):
            print(f"Folder '{folder_path}' does not exist.")
            return None
    
        # Lưu trữ tất cả các DataFrame từ các tệp CSV vào một danh sách
        all_dataframes = []
    
        # Lặp qua tất cả các tệp CSV trong thư mục
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                
                # Đọc từng tệp CSV và thêm vào danh sách
                df = pd.read_csv(file_path)
                df = self.add_additional_columns(df)
                all_dataframes.append(df)
    
        # Kiểm tra xem danh sách có dữ liệu hay không
        if not all_dataframes:
            print(f"No CSV files found in the folder '{folder_path}'.")
            return None
    
        # Nối tất cả các DataFrame thành một lớn
        concatenated_df = pd.concat(all_dataframes, ignore_index=True)
    
        result_filename = os.path.join("Attendance_file", f'Attended_{year}.csv')
        concatenated_df.to_csv(result_filename, index=False)
    
    
        
if __name__ == "__main__":
    root = tk.Tk()
    app = SynthesizeFiles(root)
    root.mainloop()
