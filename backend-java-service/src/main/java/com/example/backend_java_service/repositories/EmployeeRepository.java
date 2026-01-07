package com.example.backend_java_service.repositories;

import com.example.backend_java_service.models.Employee;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.*;

public interface EmployeeRepository extends JpaRepository<Employee,Long> {
    Employee findEmployeeByEmployeeID(Long employeeID);


}
