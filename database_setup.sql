-- Aegis Forensics Suite - Database Setup Script
-- Run this script inside phpMyAdmin to initialize your backend storage.

CREATE DATABASE IF NOT EXISTS aegis_forensics;
USE aegis_forensics;

CREATE TABLE IF NOT EXISTS activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    module VARCHAR(100) NOT NULL,
    file VARCHAR(500) NOT NULL,
    status VARCHAR(50) NOT NULL
);

-- Insert a test row to verify the connection is working
INSERT INTO activity_logs (timestamp, module, file, status) 
VALUES (NOW(), 'System Boot', 'N/A', 'Success');
