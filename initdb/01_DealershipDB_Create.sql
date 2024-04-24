-- MySQL Script generated by MySQL Workbench
-- Tue Mar  5 21:15:43 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema DealershipDB
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `DealershipDB` ;

-- -----------------------------------------------------
-- Schema DealershipDB
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `DealershipDB` DEFAULT CHARACTER SET utf8 ;
USE `DealershipDB` ;

-- -----------------------------------------------------
-- Table `DealershipDB`.`customer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`customer` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`customer` (
  `customer_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(32) NOT NULL,
  `last_name` VARCHAR(32) NULL,
  `email` VARCHAR(254) NULL,
  `password` VARCHAR(256) NOT NULL,
  `ssn` VARCHAR(11) NULL,
  `birth_date` DATE NULL,
  `drivers_license` VARCHAR(16) NULL,
  `address_id` INT NULL,
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `status` INT NOT NULL DEFAULT 1,
  PRIMARY KEY (`customer_id`),
  UNIQUE INDEX `customer_id_UNIQUE` (`customer_id` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `DealershipDB`.`credit_report`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`credit_report` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`credit_report` (
  `credit_report_id` INT UNSIGNED NOT NULL,
  `customer_id` INT UNSIGNED NOT NULL,
  `score` INT NOT NULL,
  PRIMARY KEY (`credit_report_id`),
  INDEX `fk_customer_idx` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_credit_report_customer`
    FOREIGN KEY (`customer_id`)
    REFERENCES `DealershipDB`.`customer` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `DealershipDB`.`customer_vehicle`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`customer_vehicle` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`customer_vehicle` (
  `customer_vehicle_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `vin` VARCHAR(45) NOT NULL UNIQUE,
  `year` VARCHAR(4) NULL,
  `make` VARCHAR(254) NULL,
  `model` VARCHAR(254) NULL,
  `customer_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`customer_vehicle_id`),
  UNIQUE INDEX `customer_vehicle_id_UNIQUE` (`customer_vehicle_id` ASC) VISIBLE,
  INDEX `fk_customer_idx` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_customer_vehicle_customer`
    FOREIGN KEY (`customer_id`)
    REFERENCES `DealershipDB`.`customer` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `DealershipDB`.`vehicle`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`vehicle` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`vehicle` (
  `vehicle_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `vin` VARCHAR(17) NOT NULL,
  `price` INT NULL,
  `year` VARCHAR(4) NULL,
  `make` VARCHAR(45) NULL,
  `model` VARCHAR(45) NULL,
  `miles` INT NULL,
  `mpg` INT NULL,
  `color` VARCHAR(45) NULL,
  `fuel_type` VARCHAR(45) NULL,
  `transmission` VARCHAR(45) NULL,
  `image` VARCHAR(254) NULL,
  `vehicle_status` INT NULL,
  PRIMARY KEY (`vehicle_id`),
  UNIQUE INDEX `vehicle_id_UNIQUE` (`vehicle_id` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `DealershipDB`.`negotiation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`negotiation` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`negotiation` (
  `negotiation_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `vehicle_id` INT UNSIGNED NOT NULL,
  `customer_id` INT UNSIGNED NOT NULL,
  `negotiation_status` INT NOT NULL DEFAULT 1,
  `start_date` DATETIME NULL DEFAULT NOW(),
  `end_date` DATETIME NULL,
  PRIMARY KEY (`negotiation_id`),
  UNIQUE INDEX `negotiation_id_UNIQUE` (`negotiation_id` ASC) VISIBLE,
  INDEX `fk_customer_idx` (`customer_id` ASC) VISIBLE,
  INDEX `fk_vehicle_idx` (`vehicle_id` ASC) VISIBLE,
  CONSTRAINT `fk_negotiation_customer`
    FOREIGN KEY (`customer_id`)
    REFERENCES `DealershipDB`.`customer` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_negotiation_vehicle`
    FOREIGN KEY (`vehicle_id`)
    REFERENCES `DealershipDB`.`vehicle` (`vehicle_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `DealershipDB`.`offer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`offer` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`offer` (
  `offer_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `negotiation_id` INT UNSIGNED NOT NULL,
  `offer_type` INT NOT NULL,
  `offer_price` INT NOT NULL,
  `offer_date` DATETIME NULL DEFAULT NOW(),
  `offer_status` INT NOT NULL DEFAULT 1,
  `message` VARCHAR(512) NULL,
  PRIMARY KEY (`offer_id`),
  UNIQUE INDEX `offer_counter_id_UNIQUE` (`offer_id` ASC) VISIBLE,
  INDEX `fk_negotiation_idx` (`negotiation_id` ASC) VISIBLE,
  CONSTRAINT `fk_offer_negotiation`
    FOREIGN KEY (`negotiation_id`)
    REFERENCES `DealershipDB`.`negotiation` (`negotiation_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `DealershipDB`.`role`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`role` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`role` (
  `role_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `role` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE INDEX `role_id_UNIQUE` (`role_id` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `DealershipDB`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`user` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`user` (
  `user_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `role_id` INT UNSIGNED NOT NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(72) NOT NULL,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE,
  INDEX `fk_user_role_idx` (`role_id` ASC) VISIBLE,
  CONSTRAINT `fk_user_role`
    FOREIGN KEY (`role_id`)
    REFERENCES `DealershipDB`.`role` (`role_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- -----------------------------------------------------
-- Table `DealershipDB`.`time_slot`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`time_slot` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`time_slot` (
  `time_slot_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `start_time` DATETIME NULL,
  `end_time` DATETIME NULL,
  `time_slot_type` INT NOT NULL,
  `is_available` INT NOT NULL,
  PRIMARY KEY (`time_slot_id`),
  UNIQUE INDEX `time_slot_id_UNIQUE` (`time_slot_id` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `DealershipDB`.`appointment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`appointment` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`appointment` (
  `appointment_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `time_slot_id` INT UNSIGNED NOT NULL,
  `customer_id` INT UNSIGNED NOT NULL,
  `appointment_type` INT NOT NULL,
  `status` INT NOT NULL,
  PRIMARY KEY (`appointment_id`),
  UNIQUE INDEX `appointment_id_UNIQUE` (`appointment_id` ASC) VISIBLE,
  INDEX `fk_customer_appointment_idx` (`customer_id` ASC) VISIBLE,
  INDEX `fk_time_slot_idx` (`time_slot_id` ASC) VISIBLE,
  CONSTRAINT `fk_appointment_customer`
    FOREIGN KEY (`customer_id`)
    REFERENCES `DealershipDB`.`customer` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_appointment_time_slot`
    FOREIGN KEY (`time_slot_id`)
    REFERENCES `DealershipDB`.`time_slot` (`time_slot_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `DealershipDB`.`service_ticket`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`service_ticket` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`service_ticket` (
  `service_ticket_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `customer_id` INT UNSIGNED NOT NULL,
  `user_id` INT UNSIGNED NOT NULL,
  `customer_vehicle_id` INT UNSIGNED NOT NULL,
  `time_slot_id` INT UNSIGNED NOT NULL,
  `customer_note` VARCHAR(512) NULL,
  `technician_note` VARCHAR(512) NULL,
  `status` INT NOT NULL,
  PRIMARY KEY (`service_ticket_id`),
  UNIQUE INDEX `service_ticket_id_UNIQUE` (`service_ticket_id` ASC) VISIBLE,
  INDEX `fk_customer_service_ticket_idx` (`customer_id` ASC) VISIBLE,
  INDEX `fk_customer_vehicle_service_ticket_idx` (`customer_vehicle_id` ASC) VISIBLE,
  INDEX `fk_time_slot_service_ticket_idx` (`time_slot_id` ASC) VISIBLE,
  INDEX `fk_user_service_ticket_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_service_ticket_customer`
    FOREIGN KEY (`customer_id`)
    REFERENCES `DealershipDB`.`customer` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_service_ticket_customer_vehicle`
    FOREIGN KEY (`customer_vehicle_id`)
    REFERENCES `DealershipDB`.`customer_vehicle` (`customer_vehicle_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_service_ticket_time_slot`
    FOREIGN KEY (`time_slot_id`)
    REFERENCES `DealershipDB`.`time_slot` (`time_slot_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_service_ticket_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `DealershipDB`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- -----------------------------------------------------
-- Table `DealershipDB`.`service_ticket_service`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`service_ticket_service` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`service_ticket_service` (
  `service_ticket_id` INT UNSIGNED NOT NULL,
  `service_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`service_ticket_id`, `service_id`),
  INDEX `fk_service_ticket_service_idx` (`service_id` ASC) VISIBLE,
  CONSTRAINT `fk_service_ticket_service_service_ticket`
    FOREIGN KEY (`service_ticket_id`)
    REFERENCES `DealershipDB`.`service_ticket` (`service_ticket_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_service_ticket_service_service`
    FOREIGN KEY (`service_id`)
    REFERENCES `DealershipDB`.`service` (`service_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `DealershipDB`.`service'
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`service` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`service` (
  `service_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `service_type` VARCHAR(45) NULL,
  `price` INT NULL,
  `description` VARCHAR(254) NULL,
  `status` INT NULL DEFAULT 1,
  PRIMARY KEY (`service_id`),
  UNIQUE INDEX `service_id_UNIQUE` (`service_id` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `DealershipDB`.`purchase`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`purchase` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`purchase` (
  `purchase_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `customer_id` INT UNSIGNED NOT NULL,
  `open_date` DATETIME NULL DEFAULT NOW(),
  `close_date` DATETIME NULL,
  `purchase_type` INT NULL,
  `purchase_status` INT NULL,
  `tax` FLOAT NULL,
  PRIMARY KEY (`purchase_id`),
  UNIQUE INDEX `purchase_id_UNIQUE` (`purchase_id` ASC) VISIBLE,
  INDEX `fk_customer_purchase_idx` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_purchase_customer`
    FOREIGN KEY (`customer_id`)
    REFERENCES `DealershipDB`.`customer` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- -----------------------------------------------------
-- Table `DealershipDB`.`finance`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`finance` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`finance` (
  `finance_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `purchase_id` INT UNSIGNED NOT NULL,
  `start_date` DATETIME NULL DEFAULT NOW(),
  `end_date` DATETIME NULL,
  `down_payment` INT NULL,
  `loan_amount` INT NULL,
  `apy` FLOAT NULL,
  `term` INT NULL,
  `paid` INT NULL,
  `finance_status` INT NULL,
  PRIMARY KEY (`finance_id`),
  UNIQUE INDEX `finance_id_UNIQUE` (`finance_id` ASC) VISIBLE,
  UNIQUE INDEX `financecol_UNIQUE` (`purchase_id` ASC) VISIBLE,
  CONSTRAINT `fk_finance_purchase`
    FOREIGN KEY (`purchase_id`)
    REFERENCES `DealershipDB`.`purchase` (`purchase_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `DealershipDB`.`payment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`payment` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`payment` (
  `payment_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `purchase_id` INT UNSIGNED NOT NULL,
  `finance_id` INT UNSIGNED NULL,
  `routing_number` VARCHAR(45) NULL,
  `account_number` VARCHAR(45) NULL,
  `payment_amount` INT NULL,
  PRIMARY KEY (`payment_id`),
  UNIQUE INDEX `payment_id_UNIQUE` (`payment_id` ASC) VISIBLE,
  INDEX `fk_purchase_idx` (`purchase_id` ASC) VISIBLE,
  CONSTRAINT `fk_payment_purchase`
    FOREIGN KEY (`purchase_id`)
    REFERENCES `DealershipDB`.`purchase` (`purchase_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- -----------------------------------------------------
-- Table `DealershipDB`.`purchase_addon`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `DealershipDB`.`purchase_addon` (
  `purchase_addon_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `purchase_id` INT UNSIGNED NOT NULL,
  `addon_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`purchase_addon_id`),
  UNIQUE INDEX `purchase_addon_id_UNIQUE` (`purchase_addon_id` ASC) VISIBLE,
  INDEX `fk_purchase_addon_purchase_idx` (`purchase_id` ASC) VISIBLE,
  INDEX `fk_purchase_addon_addon_idx` (`addon_id` ASC) VISIBLE,
  CONSTRAINT `fk_purchase_addon_purchase`
    FOREIGN KEY (`purchase_id`)
    REFERENCES `DealershipDB`.`purchase` (`purchase_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_purchase_addon_addon`
    FOREIGN KEY (`addon_id`)
    REFERENCES `DealershipDB`.`addon` (`addon_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- -----------------------------------------------------
-- Table `DealershipDB`.`purchase_vehicle`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`purchase_vehicle` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`purchase_vehicle` (
  `purchase_vehicle_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `purchase_id` INT UNSIGNED NOT NULL,
  `vehicle_id` INT UNSIGNED NOT NULL,
  `offer_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`purchase_vehicle_id`),
  UNIQUE INDEX `purchase_vehicle_id_UNIQUE` (`purchase_vehicle_id` ASC) VISIBLE,
  INDEX `fk_purchase_vehicle_purchase_idx` (`purchase_id` ASC) VISIBLE,
  INDEX `fk_purchase_vehicle_vehicle_idx` (`vehicle_id` ASC) VISIBLE,
  CONSTRAINT `fk_purchase_vehicle_purchase`
    FOREIGN KEY (`purchase_id`)
    REFERENCES `DealershipDB`.`purchase` (`purchase_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_purchase_vehicle_vehicle`
    FOREIGN KEY (`vehicle_id`)
    REFERENCES `DealershipDB`.`vehicle` (`vehicle_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_purchase_vehicle_offer`
    FOREIGN KEY (`offer_id`)
    REFERENCES `DealershipDB`.`offer` (`offer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
  
-- -----------------------------------------------------
-- Table `DealershipDB`.`addon`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`addon` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`addon` (
  `addon_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `addon_name` VARCHAR(45) NULL,
  `price` INT NULL,
  `description` VARCHAR(254) NULL,
  `status` INT NULL DEFAULT 1,
  PRIMARY KEY (`addon_id`),
  UNIQUE INDEX `addon_id_UNIQUE` (`addon_id` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `DealershipDB`.`contract`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`contract` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`contract` (
  `contract_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `purchase_id` INT UNSIGNED NOT NULL,
  `contract_type` INT NULL,
  `contract_status` INT NULL,
  `signer_full_name` VARCHAR(45) NULL,
  `customer_signature` VARCHAR(254) NULL,
  `dealer_signature` VARCHAR(254) NULL,
  `vehicle_year` VARCHAR(4) NULL,
  `vehicle_make` VARCHAR(45) NULL,
  `vehicle_model` VARCHAR(45) NULL,
  `vehicle_vin` VARCHAR(17) NULL,
  `contract_date` DATETIME NULL DEFAULT NOW(),
  `contract_path` VARCHAR(254) NULL,
  PRIMARY KEY (`contract_id`),
  UNIQUE INDEX `contract_id_UNIQUE` (`contract_id` ASC) VISIBLE,
  INDEX `fk_purchase_contract_idx` (`purchase_id` ASC) VISIBLE,
  UNIQUE INDEX `ux_purchase_id_contract_type` (`purchase_id` ASC, `contract_type` ASC) VISIBLE,
  CONSTRAINT `fk_contract_purchase`
    FOREIGN KEY (`purchase_id`)
    REFERENCES `DealershipDB`.`purchase` (`purchase_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);



-- -----------------------------------------------------
-- Table `DealershipDB`.`Log`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DealershipDB`.`Log` ;

CREATE TABLE IF NOT EXISTS `DealershipDB`.`Log` (
  `log_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NULL,
  `message` VARCHAR(512) NULL,
  `date` DATETIME NULL DEFAULT NOW(),
  `customer_id` INT UNSIGNED NULL,
  `user_id` INT UNSIGNED NULL,
  PRIMARY KEY (`log_id`),
  UNIQUE INDEX `retail_item_id_UNIQUE` (`log_id` ASC) VISIBLE,
  INDEX `fk_user_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_customer_idx` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_log_customer`
    FOREIGN KEY (`customer_id`)
    REFERENCES `DealershipDB`.`customer` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_log_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `DealershipDB`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
