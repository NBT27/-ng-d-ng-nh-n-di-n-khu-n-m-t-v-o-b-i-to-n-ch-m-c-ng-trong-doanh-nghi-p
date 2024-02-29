# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 22:25:05 2024

@author: batha
"""
import pandas as pd
import os
import datetime

class Employee:
    def __init__(self, employeeID, name, department):
        self.name = name
        self.employeeID = employeeID
        self.department = department

    def display_employee(self):
        print(f"Tên: {self.name}, ID: {self.employeeID}, Phòng: {self.department}")

class EmployeesList:
    current_employee = Employee("", "", "",)
    current_employee_id = ""
    
    def __init__(self):
        self.employee = []
         
    def add_employee(self, employee):
        self.employee.append(employee)
    
    def load_employees_from_csv(self, file_path):
        try:
            df = pd.read_csv(file_path)
            employee_list = []
            for index, row in df.iterrows():
                employee = Employee(row['ID'], row['Name'], row['Department'])
                employee_list.append(employee)
            print("loaded employee from CSV")
            return employee_list
        except Exception as e:
            print(f"Error loading employee from CSV: {e}")
            return []

    def display_employees(self):
        for employee in self.employee:
            employee.display_employee()

    def get_employee_by_index(self, index):
        if 0 <= index < len(self.employee):
            return self.employee[index]
        else:
            return None

    def get_employee_by_id(self, employee_id):
        for employee in self.employee:
            if employee.employeeID == employee_id:
                return employee
        return None
    
    def write_to_csv(self,current_employee,csv_file_path):
        # # Kiểm tra xem có thông tin sinh viên hiện tại không
        # if current_employee is not None:
        #     employee_id = current_employee.employeeID
        #     employee_name = current_employee.name
        #     employee_department = current_employee.department
    
        #     # Lấy thời gian điểm danh
        #     timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
        #     df = pd.DataFrame()
        #     if os.path.exists(csv_file_path):
        #         df = pd.read_csv(csv_file_path, encoding='utf-8')
    
        #         new_row = pd.DataFrame({
        #             'ID': [employee_id],
        #             'Name': [employee_name],
        #             'Department': [employee_department],
        #             'Add Time': [timestamp]
        #         })
        #         df = pd.concat([df, new_row], ignore_index=True)
        #         df.to_csv(csv_file_path, index=False, encoding='utf-8')
        
        # Kiểm tra xem có thông tin nhân viên hiện tại không
        if current_employee is not None:
            employee_id = current_employee.employeeID
            employee_name = current_employee.name
            employee_department = current_employee.department

            # Lấy thời gian điểm danh
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Tạo hoặc mở tệp Excel
            if os.path.exists(csv_file_path):
                df = pd.read_excel(csv_file_path, engine='openpyxl')
            else:
                df = pd.DataFrame(columns=['ID', 'Name', 'Department', 'Add Time'])

            # Thêm dữ liệu mới
            new_row = pd.DataFrame({
                'ID': [employee_id],
                'Name': [employee_name],
                'Department': [employee_department],
                'Add Time': [timestamp]
            })
            df = pd.concat([df, new_row], ignore_index=True)

            # Ghi dữ liệu vào tệp Excel
            df.to_excel(csv_file_path, index=False, engine='openpyxl')
               
