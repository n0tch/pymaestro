-- MySQL dump 10.10
--
-- Host: localhost    Database: Maestro
-- ------------------------------------------------------
-- Server version	5.0.24a-Debian_9ubuntu2.1-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Creating database maestro

CREATE database maestro;
USE maestro;
--
-- Table structure for table `agenda`
--

DROP TABLE IF EXISTS `agenda`;
CREATE TABLE `agenda` (
  `data` varchar(10) NOT NULL,
  `horario` varchar(6) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `obs` varchar(100) default NULL,
  `valor` float default NULL,
  `pago` float default NULL,
  PRIMARY KEY  (`data`,`horario`,`nome`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
CREATE TABLE `clientes` (
  `clienteID` int(11) NOT NULL auto_increment,
  `nome` varchar(100) NOT NULL,
  `endereco` varchar(200) default NULL,
  `telefone` varchar(20) NOT NULL,
  `rg` varchar(20) default NULL,
  `cpf` varchar(20) default NULL,
  `celular` varchar(20) default NULL,
  `nascimento` varchar(12) default NULL,
  `sexo` varchar(10) default NULL,
  `observacao` text,
  PRIMARY KEY  (`clienteID`),
  UNIQUE KEY `clienteID` (`clienteID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `clientes`
--


/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

