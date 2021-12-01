CREATE DATABASE IF NOT EXISTS lab5ece140a;

USE lab5ece140a;

CREATE TABLE IF NOT EXISTS Commands (
  id         int AUTO_INCREMENT PRIMARY KEY,
  message    VARCHAR(32) NOT NULL,
  completed  boolean DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS Telemetry;

-- CREATE TABLE Telemetry to store Telemetry data here
-- Call it "Telemetry"!!!
CREATE TABLE Telemetry (
  id         int AUTO_INCREMENT PRIMARY KEY,
  pitch      int DEFAULT NULL,
  roll       int DEFAULT NULL,
  yaw        int DEFAULT NULL,
  vgx        int DEFAULT NULL,
  vgy        int DEFAULT NULL,
  vgz        int DEFAULT NULL,
  templ      int DEFAULT NULL,
  temph      int DEFAULT NULL,
  tof        int DEFAULT NULL,
  h          int DEFAULT NULL,
  bat        int DEFAULT NULL,
  baro       DOUBLE DEFAULT NULL,
  time       int DEFAULT NULL,
  agx        DOUBLE DEFAULT NULL,
  agy        DOUBLE DEFAULT NULL,
  agz        DOUBLE DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);