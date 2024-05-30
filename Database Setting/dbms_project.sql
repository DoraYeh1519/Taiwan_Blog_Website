-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: dbms_project
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `blogpost`
--

DROP TABLE IF EXISTS `blogpost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blogpost` (
  `blogpost_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `upload_date` varchar(250) NOT NULL,
  `body` text,
  `views` int NOT NULL DEFAULT '0',
  `author_id` int NOT NULL,
  `img_url` varchar(45) DEFAULT NULL,
  `img_folder` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`blogpost_id`,`author_id`),
  KEY `author_idx` (`author_id`),
  CONSTRAINT `author_id` FOREIGN KEY (`author_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blogpost`
--

LOCK TABLES `blogpost` WRITE;
/*!40000 ALTER TABLE `blogpost` DISABLE KEYS */;
INSERT INTO `blogpost` VALUES (9,'Our First Post!','May 31, 2024','<p>To make sure the home page works well, this post is needed</p>\r\n',1,1,'',NULL);
/*!40000 ALTER TABLE `blogpost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `comment_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `post_id` int NOT NULL,
  `comment_time` varchar(250) DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`comment_id`,`user_id`,`post_id`),
  KEY `cUser_id_idx` (`user_id`),
  KEY `cBlog_id_idx` (`post_id`),
  CONSTRAINT `Cpost_id` FOREIGN KEY (`post_id`) REFERENCES `blogpost` (`blogpost_id`),
  CONSTRAINT `Cuser_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hashtag`
--

DROP TABLE IF EXISTS `hashtag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hashtag` (
  `hashtag_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `totoal_views` int NOT NULL,
  PRIMARY KEY (`hashtag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hashtag`
--

LOCK TABLES `hashtag` WRITE;
/*!40000 ALTER TABLE `hashtag` DISABLE KEYS */;
/*!40000 ALTER TABLE `hashtag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incoming_user`
--

DROP TABLE IF EXISTS `incoming_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `incoming_user` (
  `incoming_user_id` int NOT NULL,
  `origin_school` varchar(250) NOT NULL,
  `continent` varchar(250) NOT NULL,
  `country` varchar(250) NOT NULL,
  `region` varchar(250) DEFAULT NULL,
  `info` text,
  PRIMARY KEY (`incoming_user_id`),
  CONSTRAINT `incoming_user_id` FOREIGN KEY (`incoming_user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incoming_user`
--

LOCK TABLES `incoming_user` WRITE;
/*!40000 ALTER TABLE `incoming_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `incoming_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `keyword`
--

DROP TABLE IF EXISTS `keyword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `keyword` (
  `keyword_id` int NOT NULL,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`keyword_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keyword`
--

LOCK TABLES `keyword` WRITE;
/*!40000 ALTER TABLE `keyword` DISABLE KEYS */;
/*!40000 ALTER TABLE `keyword` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `outgoing_user`
--

DROP TABLE IF EXISTS `outgoing_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `outgoing_user` (
  `outgoing_user_id` int NOT NULL,
  `exchanging_school` varchar(250) NOT NULL,
  `continent` varchar(250) NOT NULL,
  `country` varchar(250) NOT NULL,
  `region` varchar(250) DEFAULT NULL,
  `info` text,
  PRIMARY KEY (`outgoing_user_id`),
  CONSTRAINT `outgoing_user_id` FOREIGN KEY (`outgoing_user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `outgoing_user`
--

LOCK TABLES `outgoing_user` WRITE;
/*!40000 ALTER TABLE `outgoing_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `outgoing_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `put`
--

DROP TABLE IF EXISTS `put`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `put` (
  `blog_id` int NOT NULL,
  `hashtag_id` int NOT NULL,
  `upload_date` datetime DEFAULT NULL,
  PRIMARY KEY (`blog_id`,`hashtag_id`),
  KEY `pHastag_id_idx` (`hashtag_id`),
  CONSTRAINT `pBlog_id` FOREIGN KEY (`blog_id`) REFERENCES `blogpost` (`blogpost_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `pHastag_id` FOREIGN KEY (`hashtag_id`) REFERENCES `hashtag` (`hashtag_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `put`
--

LOCK TABLES `put` WRITE;
/*!40000 ALTER TABLE `put` DISABLE KEYS */;
/*!40000 ALTER TABLE `put` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `react`
--

DROP TABLE IF EXISTS `react`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `react` (
  `user_id` int NOT NULL,
  `post_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`post_id`),
  KEY `rBlog_id_idx` (`post_id`),
  CONSTRAINT `Rpost_id` FOREIGN KEY (`post_id`) REFERENCES `blogpost` (`blogpost_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Ruser_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `react`
--

LOCK TABLES `react` WRITE;
/*!40000 ALTER TABLE `react` DISABLE KEYS */;
/*!40000 ALTER TABLE `react` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tagged_user`
--

DROP TABLE IF EXISTS `tagged_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tagged_user` (
  `user_id` int NOT NULL,
  `post_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`post_id`),
  KEY `Tpost_id_idx` (`post_id`),
  CONSTRAINT `Tpost_id` FOREIGN KEY (`post_id`) REFERENCES `blogpost` (`blogpost_id`),
  CONSTRAINT `Tuser_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tagged_user`
--

LOCK TABLES `tagged_user` WRITE;
/*!40000 ALTER TABLE `tagged_user` DISABLE KEYS */;
INSERT INTO `tagged_user` VALUES (1,9);
/*!40000 ALTER TABLE `tagged_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL,
  `user_name` varchar(200) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `profile_img_url` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Xchange Official','dorayeh011093@gmail.com','pbkdf2:sha256:600000$1e2Kgps2$48b1d9accb5674b9010a3549a3aeccbe58d204c59ab972616c856589b8d45b18',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-31  3:58:49
