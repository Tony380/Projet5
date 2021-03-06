CREATE DATABASE IF NOT EXISTS Purbeurre;

USE Purbeurre;

CREATE TABLE IF NOT EXISTS Category(
    id SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR (150) UNIQUE NOT NULL);

CREATE TABLE IF NOT EXISTS Product(
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR (150) NOT NULL,
    brand VARCHAR (150) DEFAULT NULL,
    nutriscore CHAR(1) DEFAULT NULL,
    store VARCHAR(300) DEFAULT NULL,
    cat_id SMALLINT UNSIGNED DEFAULT NULL,
    url VARCHAR (300) NOT NULL,
    CONSTRAINT fk_cat_id FOREIGN KEY (cat_id) REFERENCES Category(id) ON DELETE SET NULL);

CREATE TABLE IF NOT EXISTS Substitute(
    sub_id INT UNSIGNED NOT NULL,
    prod_id INT UNSIGNED UNIQUE NOT NULL,
    CONSTRAINT fk_sub_id FOREIGN KEY (sub_id) REFERENCES Product(id),
    CONSTRAINT fk_prod_id FOREIGN KEY (prod_id) REFERENCES Product(id));
