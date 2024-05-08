CREATE DATABASE IF NOT EXISTS zchat;
USE zchat;

DELIMITER //

CREATE FUNCTION IF NOT EXISTS datadec(input_encrypted VARBINARY(255)) RETURNS varchar(255) CHARSET latin1
READS SQL DATA
BEGIN
    DECLARE aespass VARCHAR(255);
    DECLARE aesdec VARCHAR(255);

    SET aespass = 'alpha@zchat';
    SET aesdec = AES_DECRYPT(input_encrypted, aespass);

    RETURN aesdec;
END//

DELIMITER ;

DELIMITER //

CREATE FUNCTION IF NOT EXISTS dataenc(i TEXT CHARSET latin1) RETURNS text CHARSET latin1
DETERMINISTIC
BEGIN
    DECLARE aespass VARCHAR(255);
    DECLARE aesenc VARBINARY(255);

    SET aespass = 'alpha@zchat';
    SET aesenc = AES_ENCRYPT(i, aespass);

    RETURN aesenc;
END//

DELIMITER ;


CREATE TABLE IF NOT EXISTS message_history (
    timestamp varchar(50) DEFAULT NULL,
    mobile_number varchar(1000) DEFAULT NULL,
    message varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS users (
    id int(11) NOT NULL AUTO_INCREMENT,
    mobile_number varchar(255) DEFAULT NULL,
    username varchar(255) DEFAULT NULL,
    active_ip varchar(255) DEFAULT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS userview (
    datadec_mobile_number VARCHAR(255) NULL,
    username VARCHAR(255) NULL,
    datadec_active_ip VARCHAR(255) NULL
) ENGINE=MyISAM;

DELIMITER //
CREATE TRIGGER IF NOT EXISTS user_insert_trigger
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    SET NEW.mobile_number = dataenc(NEW.mobile_number);
    SET NEW.active_ip = dataenc(NEW.active_ip);
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER IF NOT EXISTS user_update_trigger
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF dataenc(NEW.mobile_number) = dataenc(OLD.mobile_number) THEN
        SET NEW.mobile_number = OLD.mobile_number;
    ELSE
        SET NEW.mobile_number = dataenc(NEW.mobile_number);
    END IF;

    IF dataenc(NEW.active_ip) = dataenc(OLD.active_ip) THEN
        SET NEW.active_ip = OLD.active_ip;
    ELSE
        SET NEW.active_ip = dataenc(NEW.active_ip);
    END IF;
END//
DELIMITER ;

DROP TABLE IF EXISTS userview;

CREATE VIEW userview AS
SELECT datadec(mobile_number) AS datadec_mobile_number, username, datadec(active_ip) AS datadec_active_ip
FROM users;
