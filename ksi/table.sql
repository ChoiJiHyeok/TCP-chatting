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
  `연번` int NOT NULL AUTO_INCREMENT,
  `채팅방이름` varchar(45) DEFAULT NULL,
  `개설자` varchar(45) DEFAULT NULL,
  `참여인원` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`연번`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_list`
--

LOCK TABLES `chat_list` WRITE;
/*!40000 ALTER TABLE `chat_list` DISABLE KEYS */;
INSERT INTO `chat_list` VALUES (1,'chat_room_1','dsadas','8'),(2,'chat_room_2','dsadas','3'),(3,'chat_room_3','dsadas','0'),(4,'chat_room_asdasd','asdasd','0'),(5,'chat_room_asdasdasd','asdsad','0');
/*!40000 ALTER TABLE `chat_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_room_asdasd`
--

DROP TABLE IF EXISTS `chat_room_asdasd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_room_asdasd` (
  `날짜` varchar(45) DEFAULT NULL,
  `시간` varchar(45) DEFAULT NULL,
  `송신자` varchar(45) DEFAULT NULL,
  `수신자` varchar(45) DEFAULT NULL,
  `내용` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_room_asdasd`
--

LOCK TABLES `chat_room_asdasd` WRITE;
/*!40000 ALTER TABLE `chat_room_asdasd` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_room_asdasd` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_room_asdasdasd`
--

DROP TABLE IF EXISTS `chat_room_asdasdasd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_room_asdasdasd` (
  `날짜` varchar(45) DEFAULT NULL,
  `시간` varchar(45) DEFAULT NULL,
  `송신자` varchar(45) DEFAULT NULL,
  `수신자` varchar(45) DEFAULT NULL,
  `내용` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_room_asdasdasd`
--

LOCK TABLES `chat_room_asdasdasd` WRITE;
/*!40000 ALTER TABLE `chat_room_asdasdasd` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_room_asdasdasd` ENABLE KEYS */;
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
  `내용` varchar(100) DEFAULT NULL,
  `채팅방` varchar(45) DEFAULT NULL,
  `채팅방연번` int DEFAULT NULL,
  `알림` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `net_chat`
--

LOCK TABLES `net_chat` WRITE;
/*!40000 ALTER TABLE `net_chat` DISABLE KEYS */;
INSERT INTO `net_chat` VALUES ('23-01-31','17:03','dasdsa','123213','2',2,NULL),('23-01-31','17:03','123123.','123213','2',2,NULL),('23-01-31','17:03','dasdsa','님이 채팅방을 나가셨습니다.','2',2,'퇴장'),('23-01-31','17:03','123123.','님이 채팅방을 나가셨습니다.','2',2,'퇴장');
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
INSERT INTO `online_user` VALUES ('sadasd');
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

-- Dump completed on 2023-01-31 19:29:59
