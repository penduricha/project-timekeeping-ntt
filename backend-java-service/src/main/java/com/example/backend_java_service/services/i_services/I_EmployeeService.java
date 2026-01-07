package com.example.backend_java_service.services.i_services;

import com.example.backend_java_service.models.*;

public interface I_EmployeeService {
    public Employee persistEmployee(Employee employee);

    public Employee findEmployeeByEmployeeID(Long employeeID);

    public Employee updateEmployee(Employee employee);
}
