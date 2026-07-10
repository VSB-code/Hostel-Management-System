-- ============================================================
-- NIT Durgapur Hostel Management System - Database Schema
-- ============================================================

-- Drop tables in correct order (avoid foreign key conflicts)
DROP TABLE IF EXISTS Allocations;
DROP TABLE IF EXISTS Rooms;
DROP TABLE IF EXISTS Hostels;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Admins;
DROP TABLE IF EXISTS Users;

-- ============================================================
-- 1. Hostels Table
-- ============================================================
CREATE TABLE Hostels (
    hostel_id INT AUTO_INCREMENT PRIMARY KEY,
    hostel_name VARCHAR(50) NOT NULL UNIQUE,
    total_rooms INT NOT NULL DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 2. Rooms Table
-- ============================================================
CREATE TABLE Rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    hostel_id INT NOT NULL,
    room_number INT NOT NULL,
    floor_number INT,
    capacity INT DEFAULT 2,
    occupied_count INT DEFAULT 0,
    status ENUM('AVAILABLE', 'FULL', 'MAINTENANCE') DEFAULT 'AVAILABLE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_room_per_hostel (hostel_id, room_number),
    FOREIGN KEY (hostel_id) REFERENCES Hostels(hostel_id) ON DELETE CASCADE
);

-- ============================================================
-- 3. Users Table (UNIFIED AUTHENTICATION)
-- ============================================================
CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'student') NOT NULL DEFAULT 'student',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_role (role)
);

-- ============================================================
-- 4. Students Profile (Extended info for students)
--    student_id = Users.id (foreign key)
-- ============================================================
CREATE TABLE Students (
    student_id INT PRIMARY KEY,  -- References Users.id
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),  -- can be synced with Users.email or separate
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES Users(id) ON DELETE CASCADE
);

-- ============================================================
-- 5. Admins Profile (Extended info for admins)
--    admin_id = Users.id (foreign key)
-- ============================================================
CREATE TABLE Admins (
    admin_id INT PRIMARY KEY,  -- References Users.id
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (admin_id) REFERENCES Users(id) ON DELETE CASCADE
);

-- ============================================================
-- 6. Allocations Table (History + Active)
-- ============================================================
CREATE TABLE Allocations (
    allocation_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,  -- References Users.id (where role = 'student')
    room_id INT NOT NULL,
    allocated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    vacated_at TIMESTAMP NULL,
    status ENUM('ACTIVE', 'VACATED') DEFAULT 'ACTIVE',
    
    FOREIGN KEY (student_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id) ON DELETE CASCADE,
    
    INDEX idx_student_status (student_id, status),
    INDEX idx_room_status (room_id, status)
);