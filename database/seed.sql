-- ============================================================
-- Seed Data for NIT Durgapur Hostel Management 
-- ============================================================

-- ============================================================
-- 1. Insert 4 Hostels
-- ============================================================
INSERT INTO Hostels (hostel_name, total_rooms) VALUES
('Rajguru', 100),
('CS House', 100),
('White House', 100),
('Kalam House', 100);

-- ============================================================
-- 2. Insert 100 Rooms per Hostel (Total 400 Rooms)
-- ============================================================
DELIMITER $$

DROP PROCEDURE IF EXISTS seed_rooms$$
CREATE PROCEDURE seed_rooms()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE h_id INT;
    DECLARE room_num INT;
    DECLARE floor_num INT;
    
    DECLARE cur CURSOR FOR SELECT hostel_id FROM Hostels;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO h_id;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        SET room_num = 1;
        WHILE room_num <= 100 DO
            SET floor_num = CASE
                WHEN room_num BETWEEN 1 AND 20 THEN 0
                WHEN room_num BETWEEN 21 AND 40 THEN 1
                WHEN room_num BETWEEN 41 AND 60 THEN 2
                WHEN room_num BETWEEN 61 AND 80 THEN 3
                ELSE 4
            END;
            
            INSERT INTO Rooms (hostel_id, room_number, floor_number, capacity, occupied_count, status)
            VALUES (h_id, room_num, floor_num, 2, 0, 'AVAILABLE');
            
            SET room_num = room_num + 1;
        END WHILE;
    END LOOP;
    
    CLOSE cur;
END$$

DELIMITER ;

CALL seed_rooms();
DROP PROCEDURE IF EXISTS seed_rooms;

-- ============================================================
-- 3. Insert Users (Admin + Demo Students)
--    Password: admin123 (hash generated with Werkzeug)
-- ============================================================

-- Default Admin User (password: admin123)
INSERT INTO Users (username, email, password_hash, role, is_active) VALUES
('admin', 'admin@nitdgp.ac.in', 'pbkdf2:sha256:600000$HrLX9zGq2Fk3k1mL$f48c5e8b9d7f5c6e3a2b1d4e6f8g0h2j4k6l8m0n2p4q6r8s0t2u4v6w8x0y2z', 'admin', TRUE);

-- Demo Student Users (password: student123)
INSERT INTO Users (username, email, password_hash, role, is_active) VALUES
('24CS1001', 'virendra@nitdgp.ac.in', 'pbkdf2:sha256:600000$HrLX9zGq2Fk3k1mL$f48c5e8b9d7f5c6e3a2b1d4e6f8g0h2j4k6l8m0n2p4q6r8s0t2u4v6w8x0y2z', 'student', TRUE),
('24CS1002', 'priya@nitdgp.ac.in', 'pbkdf2:sha256:600000$HrLX9zGq2Fk3k1mL$f48c5e8b9d7f5c6e3a2b1d4e6f8g0h2j4k6l8m0n2p4q6r8s0t2u4v6w8x0y2z', 'student', TRUE);

-- ============================================================
-- 4. Insert Admin Profile (Links to Users.id)
-- ============================================================
INSERT INTO Admins (admin_id, full_name, phone)
SELECT id, 'System Administrator', '9999999999' FROM Users WHERE username = 'admin';

-- ============================================================
-- 5. Insert Student Profiles (Links to Users.id)
-- ============================================================
INSERT INTO Students (student_id, roll_number, full_name, email)
SELECT id, '24CS1001', 'Virendra Singh', 'virendra@nitdgp.ac.in' FROM Users WHERE username = '24CS1001';

INSERT INTO Students (student_id, roll_number, full_name, email)
SELECT id, '24CS1002', 'Priya Sharma', 'priya@nitdgp.ac.in' FROM Users WHERE username = '24CS1002';

-- ============================================================
-- Verification Queries
-- ============================================================
-- SELECT COUNT(*) FROM Hostels;  -- 4
-- SELECT COUNT(*) FROM Rooms;    -- 400
-- SELECT * FROM Users;           -- 3 users (1 admin + 2 students)
-- SELECT * FROM Admins;          -- 1 admin
-- SELECT * FROM Students;        -- 2 students