package com.example.backend_java_service.services;

import com.example.backend_java_service.models.Employee;
import com.example.backend_java_service.services.i_services.I_EmployeeService;
import org.springframework.stereotype.Service;

@Service
public class EmployeeService implements I_EmployeeService {
    @Override
    public Employee persistEmployee(Employee employee) {

        return null;
    }

    @Override
    public Employee findEmployeeByEmployeeID(Long employeeID) {
        return null;
    }

    @Override
    public Employee updateEmployee(Employee employee) {
        return null;
    }
}
