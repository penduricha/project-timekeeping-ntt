package com.example.backend_java_service.models;

import jakarta.persistence.*;
import lombok.*;

import java.io.Serializable;
import java.time.LocalDateTime;

@Getter
@Entity
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "attendance_counts")
public class AttendanceCount implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(nullable = false, name = "attendance_count_id")
    private Long attendanceCountID;

    @Column(nullable = false, columnDefinition = "datetime", name = "time_clock")
    private LocalDateTime timeClock;

    @Column(nullable = false, columnDefinition = "longblob", name = "image_employee")
    private byte[] imageEmployee;

    //map AttendanceCount n -1 Employee

}
