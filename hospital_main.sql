-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: hospital_main
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin_requests`
--

DROP TABLE IF EXISTS `admin_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_requests` (
  `requestID` varchar(10) NOT NULL,
  `requestReason` varchar(50) DEFAULT NULL,
  `signUpRequestName` varchar(30) DEFAULT NULL,
  `promotionRequestName` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`requestID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_requests`
--

LOCK TABLES `admin_requests` WRITE;
/*!40000 ALTER TABLE `admin_requests` DISABLE KEYS */;
INSERT INTO `admin_requests` VALUES ('REQ1','testing',NULL,NULL);
/*!40000 ALTER TABLE `admin_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `adminID` varchar(10) NOT NULL,
  `adminName` varchar(50) DEFAULT NULL,
  `emailID` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`adminID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES ('ADM1','Zeeman','zeeman@hotmail.com'),('ADM2','abc',NULL),('ADM3','test3','helpdesk@xyz.com'),('ADM4','astro','boo@businessmail.com'),('ADM5','xyz',NULL);
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `appointmentID` varchar(15) NOT NULL,
  `patientID` varchar(15) DEFAULT NULL,
  `doctorID` varchar(15) DEFAULT NULL,
  `appointmentDate` date DEFAULT NULL,
  `appointmentReason` varchar(150) DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  `appointmentTime` varchar(9) DEFAULT NULL,
  PRIMARY KEY (`appointmentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES ('A1','P1','D1','2024-12-12','Surgery','Scheduled','07:30'),('A4','P8','d2','2024-09-26','Surgery','Scheduled','05:30'),('A5','P5','2','2030-11-26','Surgery','Scheduled','03:58'),('A8','P1','D3','2024-09-15','Surgery','Scheduled','23:59'),('A9','P1','D5','2024-09-24','Check-up','Scheduled','18:30');
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `credentials`
--

DROP TABLE IF EXISTS `credentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `credentials` (
  `userid` varchar(30) NOT NULL,
  `password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credentials`
--

LOCK TABLES `credentials` WRITE;
/*!40000 ALTER TABLE `credentials` DISABLE KEYS */;
INSERT INTO `credentials` VALUES ('ADM1','adminboi'),('ADM2','omghiii'),('ADM3','fpfvebutbetter'),('ADM4','fein'),('ADM5',NULL),('D1','hxbzj'),('D2','fpfve'),('D3','zman'),('D4','noice'),('D5','[ebzv]'),('D6','welp'),('P1','adgro'),('P10','zman'),('P11','noice'),('P12','password'),('P13','sdsdgdgdgdgdgdgdgdgdgdgdgdgggdgddggdgg'),('P2','tsuyq'),('P3','gpfin'),('P4','iwhkr'),('P5','brwrb'),('P6','hocls'),('P7','pmjnc'),('P8','xiybu'),('P9','xkyag');
/*!40000 ALTER TABLE `credentials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `DoctorID` varchar(10) NOT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `Specialization` varchar(30) DEFAULT NULL,
  `Phone` int DEFAULT NULL,
  `ConsultationFee` int DEFAULT NULL,
  PRIMARY KEY (`DoctorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES ('D1','doc1',NULL,NULL,NULL),('D2','ebzv',NULL,NULL,NULL),('D3','doczeeman',NULL,NULL,NULL),('D4','doczeeman2',NULL,NULL,NULL),('D5','ebzv','Cardiologist',1143,8500),('D6','Samrit','ENT',954,NULL);
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicalhistory`
--

DROP TABLE IF EXISTS `medicalhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicalhistory` (
  `recordID` varchar(30) NOT NULL,
  `patientID` varchar(30) DEFAULT NULL,
  `doctorID` varchar(30) DEFAULT NULL,
  `visitDate` date DEFAULT NULL,
  `diagnosis` varchar(300) DEFAULT NULL,
  `prescriptionID` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `time` varchar(9) DEFAULT NULL,
  PRIMARY KEY (`recordID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicalhistory`
--

LOCK TABLES `medicalhistory` WRITE;
/*!40000 ALTER TABLE `medicalhistory` DISABLE KEYS */;
INSERT INTO `medicalhistory` VALUES ('R1','P1','D1','2024-08-10','Acute tonsillitis','PRC1','Completed',NULL),('R10','P5','D5','2024-07-30','Gastric ulcer','PRC10','Completed',NULL),('R11','P1','D3','2024-09-09','NULL','NULL','Cancelled','08:00'),('R12','P5','D3','2024-09-09','type 1 diabetes','PRC4','Completed','07:17'),('R13','P2','D1','2024-09-09','coronary heart disease','prc5','Completed',NULL),('R14','P2','D1','2024-09-09','tonsillitis','prc1','Completed',NULL),('R15','P8','D1','2024-09-09','NULL','NULL','Cancelled','17:28'),('R16','P1','D2','2024-09-10','NULL','NULL','Cancelled','05:30'),('R17','P1','D2','2024-09-09','common cold','prc1','Completed','22:00'),('R18','P1','D2','2024-09-10','same thing','prc2','Completed','17:00'),('R19','P1','D2','2024-09-09','haha nothing','prc1','Completed','20:10'),('R2','P2','D2','2024-07-15','Mild fever and headache','PRC2','Completed',NULL),('R20','P1','D2','2024-09-09','NULL','NULL','Cancelled','21:30'),('R21','P7','D4','2024-09-09','rhinitis ig','prc2','Completed','17:45'),('R22','P1','D3','2024-09-10','NULL','NULL','Cancelled','18:30'),('R23','P9','D3','2024-09-11','NULL','NULL','Cancelled','05:30'),('R24','P9','D3','2024-09-09','NULL','NULL','Cancelled','07:45'),('R25','P7','D1','2024-09-09','NULL','NULL','Cancelled','17:43'),('R26','P4','D1','2024-09-12','ADHD','prc2','Completed','18:32'),('R27','P1','D5','2024-09-12','smth i didnt really hear','prc2','Completed','21:30'),('R28','P1','D5','2024-09-16','','','Completed','18:30'),('R29','P1','D5','2024-09-17','','','Completed','09:00'),('R3','P3','D1','2024-08-19','Acute bronchitis','PRC3','Completed',NULL),('R4','P3','D3','2024-09-01','Type 2 diabetes','PRC4','Completed',NULL),('R5','P4','D4','2024-06-21','Hypertension','PRC5','Completed',NULL),('R6','P5','D5','2024-08-03','Hyperlipidemia','PRC6','Completed',NULL),('R7','P1','D2','2024-09-05','Urinary tract infection','PRC7','Completed',NULL),('R8','P2','D3','2024-07-28','Community-acquired pneumonia','PRC8','Completed',NULL),('R9','P4','D4','2024-09-04','Allergic rhinitis','PRC9','Completed',NULL);
/*!40000 ALTER TABLE `medicalhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `PatientID` varchar(10) NOT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `Gender` char(1) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `Phone` int DEFAULT NULL,
  PRIMARY KEY (`PatientID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES ('P1','andrew','B','2007-05-28',143),('P10','zeeman4','M','2009-10-16',1112),('P11','zeeman5',NULL,NULL,NULL),('P12','XYZ','F','1995-09-28',985),('P13','poli',NULL,NULL,NULL),('P2','def',NULL,NULL,NULL),('P3','ran1',NULL,NULL,NULL),('P4','ABC',NULL,NULL,NULL),('P5','ran2',NULL,NULL,NULL),('P6','zeba',NULL,NULL,NULL),('P7','zeeeeman',NULL,NULL,NULL),('P8','zeeman2',NULL,NULL,NULL),('P9','zeeman3',NULL,NULL,NULL);
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prescriptions`
--

DROP TABLE IF EXISTS `prescriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prescriptions` (
  `prescriptionID` varchar(20) NOT NULL,
  `medication_name` varchar(30) DEFAULT NULL,
  `dosage` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`prescriptionID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescriptions`
--

LOCK TABLES `prescriptions` WRITE;
/*!40000 ALTER TABLE `prescriptions` DISABLE KEYS */;
INSERT INTO `prescriptions` VALUES ('PRC1','Amoxicillin','500 mg every 8 hours for 7 days'),('PRC10','Omeprazole','20 mg once daily before breakfast'),('PRC2','Ibuprofen','200 mg every 4-6 hours as needed'),('PRC3','Paracetamol','500 mg every 4-6 hours as needed'),('PRC4','Metformin','500 mg twice daily with meals'),('PRC5','Lisinopril','10 mg once daily'),('PRC6','Atorvastatin','20 mg once daily at bedtime'),('PRC7','Ciprofloxacin','500 mg twice daily for 10 days'),('PRC8','Azithromycin','500 mg once daily for 3 days'),('PRC9','Prednisone','10 mg once daily for 5 days');
/*!40000 ALTER TABLE `prescriptions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-21  7:26:08
