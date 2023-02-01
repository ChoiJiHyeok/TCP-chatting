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
  `참여인원` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_list`
--

LOCK TABLES `chat_list` WRITE;
/*!40000 ALTER TABLE `chat_list` DISABLE KEYS */;
INSERT INTO `chat_list` VALUES ('chat_room_asdasd','adsdsa',0),('chat_room_123','asdasd',0),('chat_room_345','dasdsadsa',0),('chat_room_칼바람나락','김기태',0);
/*!40000 ALTER TABLE `chat_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_room_123`
--

DROP TABLE IF EXISTS `chat_room_123`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_room_123` (
  `날짜` varchar(45) DEFAULT NULL,
  `시간` varchar(45) DEFAULT NULL,
  `송신자` varchar(45) DEFAULT NULL,
  `내용` varchar(100) DEFAULT NULL,
  `채팅방` varchar(45) DEFAULT NULL,
  `알림` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_room_123`
--

LOCK TABLES `chat_room_123` WRITE;
/*!40000 ALTER TABLE `chat_room_123` DISABLE KEYS */;
INSERT INTO `chat_room_123` VALUES ('23-02-01','15:21','asdasd','님이 입장하셨습니다.','123','입장'),('23-02-01','15:21','asdasd','sadda','123',NULL),('23-02-01','15:21','asdasd','님이 채팅방을 나가셨습니다.','123','퇴장'),('23-02-01','15:31','asddas','님이 입장하셨습니다.','123','입장'),('23-02-01','15:31','asddas','님이 채팅방을 나가셨습니다.','123','퇴장'),('23-02-01','15:32','asdasd','님이 입장하셨습니다.','123','입장'),('23-02-01','15:32','asdasd','님이 채팅방을 나가셨습니다.','123','퇴장'),('23-02-01','15:34','asdasddas','님이 입장하셨습니다.','123','입장'),('23-02-01','15:34','asdasddas','님이 채팅방을 나가셨습니다.','123','퇴장'),('23-02-01','15:36','asdasdads','님이 입장하셨습니다.','123','입장'),('23-02-01','15:36','asdasdads','님이 채팅방을 나가셨습니다.','123','퇴장'),('23-02-01','15:36','asdasdads','님이 입장하셨습니다.','123','입장'),('23-02-01','15:36','asdasdads','asdasdasd','123',NULL),('23-02-01','15:36','asdasdads','님이 채팅방을 나가셨습니다.','123','퇴장'),('23-02-01','15:41','123213','님이 입장하셨습니다.','123','입장'),('23-02-01','15:41','123213','님이 채팅방을 나가셨습니다.','123','퇴장'),('23-02-01','15:42','123213','님이 입장하셨습니다.','123','입장'),('23-02-01','15:42','123213','님이 채팅방을 나가셨습니다.','123','퇴장'),('23-02-01','15:44','asdasd','님이 입장하셨습니다.','123','입장'),('23-02-01','15:44','asdasd','님이 채팅방을 나가셨습니다.','123','퇴장'),('23-02-01','15:44','asdasd','님이 입장하셨습니다.','123','입장'),('23-02-01','15:44','asdasdasd','님이 입장하셨습니다.','123','입장'),('23-02-01','15:44','asdasdasd','님이 채팅방을 나가셨습니다.','123','퇴장'),('23-02-01','16:01','123','님이 입장하셨습니다.','123','입장'),('23-02-01','16:01','123','님이 채팅방을 나가셨습니다.','123','퇴장');
/*!40000 ALTER TABLE `chat_room_123` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_room_345`
--

DROP TABLE IF EXISTS `chat_room_345`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_room_345` (
  `날짜` varchar(45) DEFAULT NULL,
  `시간` varchar(45) DEFAULT NULL,
  `송신자` varchar(45) DEFAULT NULL,
  `내용` varchar(100) DEFAULT NULL,
  `채팅방` varchar(45) DEFAULT NULL,
  `알림` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_room_345`
--

LOCK TABLES `chat_room_345` WRITE;
/*!40000 ALTER TABLE `chat_room_345` DISABLE KEYS */;
INSERT INTO `chat_room_345` VALUES ('23-02-01','15:44','asdasdasd','님이 입장하셨습니다.','345','입장'),('23-02-01','15:44','asdasdasd','님이 채팅방을 나가셨습니다.','345','퇴장');
/*!40000 ALTER TABLE `chat_room_345` ENABLE KEYS */;
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
  `내용` varchar(100) DEFAULT NULL,
  `채팅방` varchar(45) DEFAULT NULL,
  `알림` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_room_asdasd`
--

LOCK TABLES `chat_room_asdasd` WRITE;
/*!40000 ALTER TABLE `chat_room_asdasd` DISABLE KEYS */;
INSERT INTO `chat_room_asdasd` VALUES ('23-02-01','15:47','asdasd','님이 입장하셨습니다.','asdasd','입장'),('23-02-01','15:47','asdasd','님이 채팅방을 나가셨습니다.','asdasd','퇴장'),('23-02-01','15:47','123213','님이 입장하셨습니다.','asdasd','입장'),('23-02-01','15:47','123213','님이 채팅방을 나가셨습니다.','asdasd','퇴장'),('23-02-01','15:48','asdasd','님이 입장하셨습니다.','asdasd','입장'),('23-02-01','15:48','asdasd','님이 채팅방을 나가셨습니다.','asdasd','퇴장'),('23-02-01','17:16','asdasd','님이 입장하셨습니다.','asdasd','입장'),('23-02-01','17:16','asdasd','님이 채팅방을 나가셨습니다.','asdasd','퇴장'),('23-02-01','17:18','김기태','님이 입장하셨습니다.','asdasd','입장'),('23-02-01','17:18','김기태','님이 채팅방을 나가셨습니다.','asdasd','퇴장'),('23-02-01','17:19','김기태','님이 입장하셨습니다.','asdasd','입장'),('23-02-01','17:19','김기태','님이 채팅방을 나가셨습니다.','asdasd','퇴장'),('23-02-01','17:21','김기태','님이 입장하셨습니다.','asdasd','입장'),('23-02-01','17:21','123123','님이 입장하셨습니다.','asdasd','입장'),('23-02-01','17:23','김기태','님이 채팅방을 나가셨습니다.','asdasd','퇴장'),('23-02-01','17:23','123123','님이 채팅방을 나가셨습니다.','asdasd','퇴장');
/*!40000 ALTER TABLE `chat_room_asdasd` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_room_칼바람나락`
--

DROP TABLE IF EXISTS `chat_room_칼바람나락`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_room_칼바람나락` (
  `날짜` varchar(45) DEFAULT NULL,
  `시간` varchar(45) DEFAULT NULL,
  `송신자` varchar(45) DEFAULT NULL,
  `내용` varchar(100) DEFAULT NULL,
  `채팅방` varchar(45) DEFAULT NULL,
  `알림` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_room_칼바람나락`
--

LOCK TABLES `chat_room_칼바람나락` WRITE;
/*!40000 ALTER TABLE `chat_room_칼바람나락` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_room_칼바람나락` ENABLE KEYS */;
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

-- Dump completed on 2023-02-01 20:12:23
