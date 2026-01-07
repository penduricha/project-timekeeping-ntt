package com.example.backend_java_service.models;

import jakarta.persistence.*;
import lombok.*;

import java.io.Serializable;

@Getter
@Entity
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "employees")
public class Employee implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(nullable = false, name = "employee_id")
    private Long employeeID;

    @Column(nullable = false, name = "employee_name", columnDefinition = "nvarchar(50)")
    private String employeeName;

    @Column(nullable = false, name = "gender")
    private boolean gender;

    @Column(nullable = false, name = "position", columnDefinition = "nvarchar(20)")
    private String position;

    @Column(nullable = false, columnDefinition = "longblob", name = "image_face")
    private byte[] imageFace;

    @Column(nullable = false, columnDefinition = "longblob", name = "image_for_timekeeping")
    private byte[] imageForTimeKeeping;
}
