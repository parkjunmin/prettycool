CREATE DATABASE db_data;

CREATE TABLE  `db_data`.`tb_domain`(
  `domainName` VARCHAR(256) NOT NULL UNIQUE,
  `whois` JSON NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`domainName`));

CREATE TABLE `db_data`.`tb_relatedDomains`(
  `mainDomain` VARCHAR(256) NOT NULL,
  `domainName` VARCHAR(256) NOT NULL,
  `whois` JSON NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`domainName`),
  FOREIGN KEY (mainDomain) REFERENCES tb_domain(domainName) ON DELETE CASCADE
); 


CREATE TABLE `db_data`.`tb_host` (
  `ipAddress` VARCHAR(40) NOT NULL,
  `domainName` VARCHAR(256) NOT NULL,
  `hostName` Varchar(256) NOT NULL,
  `geoLocation` JSON NULL,
  `ipOwner` VARCHAR(256) NULL,
  `createdAt` DATETIME NOT NULL,
   PRIMARY KEY (`hostName`),
   FOREIGN KEY (domainName) REFERENCES tb_domain(domainName) ON DELETE CASCADE);


CREATE TABLE `db_data`.`tb_port` (
  `idPort` int(7) AUTO_INCREMENT,
  `ipAddress` varchar(40) NOT NULL,
  `port` int(11) NOT NULL,
  `protocol` varchar(256) DEFAULT NULL,
  `banner` blob DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `hostName` varchar(256) NOT NULL,
   PRIMARY KEY (`idPort`),
   FOREIGN KEY (hostName) REFERENCES tb_host(hostName) ON DELETE CASCADE);

CREATE TABLE `db_data`.`tb_application` (
  `idPort` int(6) AUTO_INCREMENT,
  `applicationName` VARCHAR(256) NULL,
  `url` VARCHAR(1024) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY(`idPort`),
  FOREIGN KEY (`idPort`) REFERENCES tb_port(idPort) ON DELETE CASCADE
);

CREATE TABLE `db_data`.`tb_applicationPathsAndFiles` (
  `idPort` int(6) AUTO_INCREMENT,
  `url` VARCHAR(1024) NOT NULL,
  `mimeType` VARCHAR(64) NOT NULL,
  `uuidFile` VARCHAR(36) NULL,
  `extension` VARCHAR(8) NULL,
  `hreflFile` VARCHAR(2048) NOT NULL,
  `isPage` TINYINT NOT NULL,
  `screenshotPath` VARCHAR(2120) NOT NULL,
  `idApplication` VARCHAR(2048) NOT NULL,
   PRIMARY KEY (idPort),
   FOREIGN KEY (idPort) REFERENCES tb_application(idPort) ON DELETE CASCADE
);

CREATE TABLE `db_data`.`tb_pastebin` (
  `uuidDump` int(6) AUTO_INCREMENT,
  `domainName` VARCHAR(256) NOT NULL,
  `url` VARCHAR(2048) NULL,
  `title` VARCHAR(2048) NOT NULL,
   `dumpDate` varchar(256) NULL, 
  `createdAt` DATETIME NOT NULL,
   PRIMARY KEY (`uuidDump`),
   FOREIGN KEY (domainName) REFERENCES tb_domain(domainName) ON DELETE CASCADE);
   
CREATE TABLE `db_data`.`tb_aws` (
  `uuidDump` int(6) AUTO_INCREMENT ,
  `domainName` VARCHAR(256) NOT NULL,
  `url` VARCHAR(2048) NULL,
   `dumpDate` varchar(12) NULL, 
  `createdAt` DATETIME NOT NULL,
   PRIMARY KEY (`uuidDump`),
   FOREIGN KEY (domainName) REFERENCES tb_domain(domainName) ON DELETE CASCADE);


CREATE TABLE IF NOT EXISTS `db_data`.`tb_victim` (
  `uuidVictim` int(6) AUTO_INCREMENT,
  `domainName` VARCHAR(256) NOT NULL,
  `email` VARCHAR(320) NULL,
  `contact` JSON NULL,
  `createdAt` DATETIME NOT NULL,
  `socialMedia` JSON NULL,
  PRIMARY KEY (`uuidVictim`),
  FOREIGN KEY (domainName) REFERENCES tb_domain(domainName) ON DELETE CASCADE);

