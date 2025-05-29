DROP DATABASE IF EXISTS RealStateDB;
CREATE DATABASE RealStateDB;
USE RealStateDB;

CREATE TABLE houses (
    id VARCHAR(10) PRIMARY KEY,
    address1 VARCHAR(100),
    address2 VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50),
    photo VARCHAR(255),
    size FLOAT,
    register_date DATE
);

-- H001 is the example insertion
INSERT INTO houses (
    id, address1, address2, city, state, postal_code, country, photo, size, register_date
) VALUES (
    'H001', '567 calle Quito', 'suite 439', 'San Juan', 'PR', '00921', 'Puerto Rico', 'myhome.jpg', 100, '2000-10-31'
);
-- Verify if it inserted well
SELECT * FROM houses;