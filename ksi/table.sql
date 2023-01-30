-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: net
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `chat_list`
--

DROP TABLE IF EXISTS `chat_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_list` (
  `채팅방이름` varchar(45) DEFAULT NULL,
  `개설자` varchar(45) DEFAULT NULL,
  `참여인원` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_list`
--

LOCK TABLES `chat_list` WRITE;
/*!40000 ALTER TABLE `chat_list` DISABLE KEYS */;
INSERT INTO `chat_list` VALUES ('chat_room_1','dsadas','1'),('chat_room_2','dsadas','1'),('chat_room_3','dsadas','1');
/*!40000 ALTER TABLE `chat_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_room_1`
--

DROP TABLE IF EXISTS `chat_room_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_room_1` (
  `날짜` varchar(45) DEFAULT NULL,
  `시간` varchar(45) DEFAULT NULL,
  `송신자` varchar(45) DEFAULT NULL,
  `수신자` varchar(45) DEFAULT NULL,
  `내용` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_room_1`
--

LOCK TABLES `chat_room_1` WRITE;
/*!40000 ALTER TABLE `chat_room_1` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_room_1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_room_12312`
--

DROP TABLE IF EXISTS `chat_room_12312`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_room_12312` (
  `날짜` varchar(45) DEFAULT NULL,
  `시간` varchar(45) DEFAULT NULL,
  `송신자` varchar(45) DEFAULT NULL,
  `수신자` varchar(45) DEFAULT NULL,
  `내용` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_room_12312`
--

LOCK TABLES `chat_room_12312` WRITE;
/*!40000 ALTER TABLE `chat_room_12312` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_room_12312` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_room_2`
--

DROP TABLE IF EXISTS `chat_room_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_room_2` (
  `날짜` varchar(45) DEFAULT NULL,
  `시간` varchar(45) DEFAULT NULL,
  `송신자` varchar(45) DEFAULT NULL,
  `수신자` varchar(45) DEFAULT NULL,
  `내용` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_room_2`
--

LOCK TABLES `chat_room_2` WRITE;
/*!40000 ALTER TABLE `chat_room_2` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_room_2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_room_3`
--

DROP TABLE IF EXISTS `chat_room_3`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_room_3` (
  `날짜` varchar(45) DEFAULT NULL,
  `시간` varchar(45) DEFAULT NULL,
  `송신자` varchar(45) DEFAULT NULL,
  `수신자` varchar(45) DEFAULT NULL,
  `내용` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_room_3`
--

LOCK TABLES `chat_room_3` WRITE;
/*!40000 ALTER TABLE `chat_room_3` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_room_3` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_room_asddas`
--

DROP TABLE IF EXISTS `chat_room_asddas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_room_asddas` (
  `날짜` varchar(45) DEFAULT NULL,
  `시간` varchar(45) DEFAULT NULL,
  `송신자` varchar(45) DEFAULT NULL,
  `수신자` varchar(45) DEFAULT NULL,
  `내용` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_room_asddas`
--

LOCK TABLES `chat_room_asddas` WRITE;
/*!40000 ALTER TABLE `chat_room_asddas` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_room_asddas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_room_dsadsaads`
--

DROP TABLE IF EXISTS `chat_room_dsadsaads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_room_dsadsaads` (
  `날짜` varchar(45) DEFAULT NULL,
  `시간` varchar(45) DEFAULT NULL,
  `송신자` varchar(45) DEFAULT NULL,
  `수신자` varchar(45) DEFAULT NULL,
  `내용` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_room_dsadsaads`
--

LOCK TABLES `chat_room_dsadsaads` WRITE;
/*!40000 ALTER TABLE `chat_room_dsadsaads` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_room_dsadsaads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `net_chat`
--

DROP TABLE IF EXISTS `net_chat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `net_chat` (
  `날짜` varchar(45) DEFAULT NULL,
  `시간` varchar(45) DEFAULT NULL,
  `송신자` varchar(45) DEFAULT NULL,
  `수신자` varchar(100) DEFAULT NULL,
  `내용` varchar(100) DEFAULT NULL,
  `채팅방` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `net_chat`
--

LOCK TABLES `net_chat` WRITE;
/*!40000 ALTER TABLE `net_chat` DISABLE KEYS */;
/*!40000 ALTER TABLE `net_chat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `online_user`
--

DROP TABLE IF EXISTS `online_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `online_user` (
  `이름` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `online_user`
--

LOCK TABLES `online_user` WRITE;
/*!40000 ALTER TABLE `online_user` DISABLE KEYS */;
INSERT INTO `online_user` VALUES ('asdsaddsa');
/*!40000 ALTER TABLE `online_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-30 21:09:01
