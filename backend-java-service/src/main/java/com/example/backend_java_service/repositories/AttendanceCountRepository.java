package com.example.backend_java_service.repositories;

import com.example.backend_java_service.models.*;
import org.springframework.data.jpa.repository.JpaRepository;


public interface AttendanceCountRepository extends JpaRepository<AttendanceCount,Long> {
}
