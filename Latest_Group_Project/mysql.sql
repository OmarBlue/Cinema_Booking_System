-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: localhost    Database: DESD
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Booking_System_account`
--

DROP TABLE IF EXISTS `Booking_System_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_account` (
  `account_number` char(32) NOT NULL,
  `account_title` varchar(100) NOT NULL,
  `credit_left` decimal(5,2) NOT NULL,
  `discount_rate` decimal(5,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `account_holder_name` varchar(100) DEFAULT NULL,
  `club_rep_id` bigint DEFAULT NULL,
  `student_id` int DEFAULT NULL,
  PRIMARY KEY (`account_number`),
  KEY `Booking_System_accou_club_rep_id_1020b9f9_fk_Booking_S` (`club_rep_id`),
  KEY `Booking_System_accou_student_id_9e49c51b_fk_Booking_S` (`student_id`),
  CONSTRAINT `Booking_System_accou_club_rep_id_1020b9f9_fk_Booking_S` FOREIGN KEY (`club_rep_id`) REFERENCES `Booking_System_clubrep` (`id`),
  CONSTRAINT `Booking_System_accou_student_id_9e49c51b_fk_Booking_S` FOREIGN KEY (`student_id`) REFERENCES `Booking_System_student` (`Student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_account`
--

LOCK TABLES `Booking_System_account` WRITE;
/*!40000 ALTER TABLE `Booking_System_account` DISABLE KEYS */;
INSERT INTO `Booking_System_account` VALUES ('530074322b6d4793b249cecd78052a3d','Club1 Rep1 Account',0.00,10.00,'2023-05-01 21:13:26.507784','681e1a1d05',1,NULL),('f72f7a547c8e41d88e7138785deae77d','Club2 Rep2 Account',0.00,10.00,'2023-05-01 21:22:42.846531','50a7e6f69d',2,NULL);
/*!40000 ALTER TABLE `Booking_System_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_accountstatement`
--

DROP TABLE IF EXISTS `Booking_System_accountstatement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_accountstatement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `statement_date` date NOT NULL,
  `film_name` varchar(255) NOT NULL,
  `ticket_quantity` int NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `credit_balance` decimal(10,2) NOT NULL,
  `transaction_type` varchar(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Booking_System_accou_user_id_b5da4be2_fk_Booking_S` (`user_id`),
  CONSTRAINT `Booking_System_accou_user_id_b5da4be2_fk_Booking_S` FOREIGN KEY (`user_id`) REFERENCES `Booking_System_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_accountstatement`
--

LOCK TABLES `Booking_System_accountstatement` WRITE;
/*!40000 ALTER TABLE `Booking_System_accountstatement` DISABLE KEYS */;
/*!40000 ALTER TABLE `Booking_System_accountstatement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_address`
--

DROP TABLE IF EXISTS `Booking_System_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_address` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `street_number` varchar(50) NOT NULL,
  `street` varchar(200) NOT NULL,
  `city` varchar(200) NOT NULL,
  `post_code` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_address`
--

LOCK TABLES `Booking_System_address` WRITE;
/*!40000 ALTER TABLE `Booking_System_address` DISABLE KEYS */;
INSERT INTO `Booking_System_address` VALUES (1,'45','West','London','LG1 3EU'),(2,'51','North','London','WR1 5WE');
/*!40000 ALTER TABLE `Booking_System_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_booking`
--

DROP TABLE IF EXISTS `Booking_System_booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_booking` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_booked` datetime(6) NOT NULL,
  `booking_number` varchar(36) NOT NULL,
  `student_tickets` smallint unsigned NOT NULL,
  `adult_tickets` smallint unsigned NOT NULL,
  `senior_tickets` smallint unsigned NOT NULL,
  `amount` decimal(5,2) NOT NULL,
  `film_id` int NOT NULL,
  `screen_id` bigint NOT NULL,
  `showtime_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Booking_System_booki_film_id_494fa356_fk_Booking_S` (`film_id`),
  KEY `Booking_System_booki_screen_id_2169d24a_fk_Booking_S` (`screen_id`),
  KEY `Booking_System_booki_showtime_id_c55af5ad_fk_Booking_S` (`showtime_id`),
  KEY `Booking_System_booki_user_id_c17c548f_fk_Booking_S` (`user_id`),
  CONSTRAINT `Booking_System_booki_film_id_494fa356_fk_Booking_S` FOREIGN KEY (`film_id`) REFERENCES `Booking_System_film` (`film_id`),
  CONSTRAINT `Booking_System_booki_screen_id_2169d24a_fk_Booking_S` FOREIGN KEY (`screen_id`) REFERENCES `Booking_System_screen` (`id`),
  CONSTRAINT `Booking_System_booki_showtime_id_c55af5ad_fk_Booking_S` FOREIGN KEY (`showtime_id`) REFERENCES `Booking_System_showtime` (`id`),
  CONSTRAINT `Booking_System_booki_user_id_c17c548f_fk_Booking_S` FOREIGN KEY (`user_id`) REFERENCES `Booking_System_customuser` (`id`),
  CONSTRAINT `Booking_System_booking_chk_1` CHECK ((`student_tickets` >= 0)),
  CONSTRAINT `Booking_System_booking_chk_2` CHECK ((`adult_tickets` >= 0)),
  CONSTRAINT `Booking_System_booking_chk_3` CHECK ((`senior_tickets` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_booking`
--

LOCK TABLES `Booking_System_booking` WRITE;
/*!40000 ALTER TABLE `Booking_System_booking` DISABLE KEYS */;
/*!40000 ALTER TABLE `Booking_System_booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_cast`
--

DROP TABLE IF EXISTS `Booking_System_cast`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_cast` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_cast`
--

LOCK TABLES `Booking_System_cast` WRITE;
/*!40000 ALTER TABLE `Booking_System_cast` DISABLE KEYS */;
INSERT INTO `Booking_System_cast` VALUES (1,'Robert Downey Jr'),(2,'Chris Evans'),(3,'Chris Hemsworth'),(4,'Sam Worthington'),(5,'Zoe Salda├▒a'),(6,'Sigourney Weaver'),(7,'Stephen Lang'),(8,'Kate Winslet'),(9,'Michael B. Jordan'),(10,'Tessa Thompson'),(11,'Jonathan Majors'),(12,'Phylicia Rash─üd'),(13,'Mila Davis-Kent'),(14,'Chris Pratt'),(15,'Charlie Day'),(16,'Anya Taylor-Joy'),(17,'Jack Black'),(18,'Keegan-Michael Key'),(19,'Keanu Reeves'),(20,'Donnie Yen'),(21,'Bill Skarsg├Ñrd'),(22,'Ian McShane'),(23,'Laurence Fishburne'),(24,'Dave Bautista'),(25,'Karen Gillan'),(26,'Pom Klementieff');
/*!40000 ALTER TABLE `Booking_System_cast` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_club`
--

DROP TABLE IF EXISTS `Booking_System_club`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_club` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `account_id` char(32) DEFAULT NULL,
  `address_id` bigint NOT NULL,
  `contact_id` bigint NOT NULL,
  `representative_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Booking_System_club_contact_id_082efe5d_fk_Booking_S` (`contact_id`),
  KEY `Booking_System_club_representative_id_b9fe810f_fk_Booking_S` (`representative_id`),
  KEY `Booking_System_club_account_id_8d3071c1_fk_Booking_S` (`account_id`),
  KEY `Booking_System_club_address_id_911e58be_fk_Booking_S` (`address_id`),
  CONSTRAINT `Booking_System_club_account_id_8d3071c1_fk_Booking_S` FOREIGN KEY (`account_id`) REFERENCES `Booking_System_account` (`account_number`),
  CONSTRAINT `Booking_System_club_address_id_911e58be_fk_Booking_S` FOREIGN KEY (`address_id`) REFERENCES `Booking_System_address` (`id`),
  CONSTRAINT `Booking_System_club_contact_id_082efe5d_fk_Booking_S` FOREIGN KEY (`contact_id`) REFERENCES `Booking_System_contact` (`id`),
  CONSTRAINT `Booking_System_club_representative_id_b9fe810f_fk_Booking_S` FOREIGN KEY (`representative_id`) REFERENCES `Booking_System_representative` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_club`
--

LOCK TABLES `Booking_System_club` WRITE;
/*!40000 ALTER TABLE `Booking_System_club` DISABLE KEYS */;
INSERT INTO `Booking_System_club` VALUES (1,'Club1',NULL,1,1,1),(2,'Club2',NULL,2,2,2);
/*!40000 ALTER TABLE `Booking_System_club` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_clubrep`
--

DROP TABLE IF EXISTS `Booking_System_clubrep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_clubrep` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `approved` tinyint(1) NOT NULL,
  `club_id` bigint NOT NULL,
  `representative_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `representative_id` (`representative_id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `Booking_System_clubr_club_id_1f48c68c_fk_Booking_S` (`club_id`),
  CONSTRAINT `Booking_System_clubr_club_id_1f48c68c_fk_Booking_S` FOREIGN KEY (`club_id`) REFERENCES `Booking_System_club` (`id`),
  CONSTRAINT `Booking_System_clubr_representative_id_6159c6a1_fk_Booking_S` FOREIGN KEY (`representative_id`) REFERENCES `Booking_System_representative` (`id`),
  CONSTRAINT `Booking_System_clubr_user_id_98d33acb_fk_Booking_S` FOREIGN KEY (`user_id`) REFERENCES `Booking_System_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_clubrep`
--

LOCK TABLES `Booking_System_clubrep` WRITE;
/*!40000 ALTER TABLE `Booking_System_clubrep` DISABLE KEYS */;
INSERT INTO `Booking_System_clubrep` VALUES (1,1,1,1,5),(2,1,2,2,6);
/*!40000 ALTER TABLE `Booking_System_clubrep` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_contact`
--

DROP TABLE IF EXISTS `Booking_System_contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_contact` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `landline` varchar(20) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_contact`
--

LOCK TABLES `Booking_System_contact` WRITE;
/*!40000 ALTER TABLE `Booking_System_contact` DISABLE KEYS */;
INSERT INTO `Booking_System_contact` VALUES (1,'07123456789','07123456789','club1@gmail.com'),(2,'07123465489','07123465489','club2@gmail.com');
/*!40000 ALTER TABLE `Booking_System_contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_customuser`
--

DROP TABLE IF EXISTS `Booking_System_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `user_type` smallint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  CONSTRAINT `Booking_System_customuser_chk_1` CHECK ((`user_type` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_customuser`
--

LOCK TABLES `Booking_System_customuser` WRITE;
/*!40000 ALTER TABLE `Booking_System_customuser` DISABLE KEYS */;
INSERT INTO `Booking_System_customuser` VALUES (1,'pbkdf2_sha256$390000$lymS8u23UqYO9cip8V9ACd$Xv893qrv5IXwwgN79y6eyh5MtEZTfrOypRMmEEAbMko=','2023-05-01 21:22:10.467495',0,'User_CM','','','cinema_manager@gmail.com',0,1,'2023-05-01 20:42:29.133767',1),(2,'pbkdf2_sha256$390000$RR5ATo4UF9MvuBMxzepmYB$2Not+syc3Ashfl+6hDTUxaXOSaGCr0zC64qB+nfwPRA=','2023-05-01 21:24:09.922632',0,'User_AM','','','account_manager@gmail.com',0,1,'2023-05-01 20:42:29.247553',2),(3,'pbkdf2_sha256$390000$qBhKvPX9bCVUBXKbTkiSYA$hJYuT0iDoebiSdzIw25pEc18ZpfEyCtCBQ3XEbVElks=',NULL,1,'superuser','','','superuser@gmail.com',1,1,'2023-05-01 20:42:43.799557',0),(4,'pbkdf2_sha256$390000$EoxK1C2rpAxN3PFsKBLn7p$JsMo+pin400/3h/nvUGmPRooEExzuRlxo98gNZWkSfA=','2023-05-01 21:10:40.961078',0,'student1','student1','student1','student1@gmail.com',0,1,'2023-05-01 20:57:47.650533',3),(5,'pbkdf2_sha256$390000$zsCjJbqJHkhNsJ8zfd5vDF$2N0u0QikHttH1s4zyR0F2yzc4lZ7/hguP5aQ6C+Wq1E=','2023-05-01 21:19:09.964510',0,'681e1a1d05','Club1','Rep1','club1@gmail.com',0,1,'2023-05-01 20:58:25.180200',4),(6,'pbkdf2_sha256$390000$3lFlmuew092F9zi6iG2QR3$DRPyPxjT1GrHRGKSf5LZaa/mnF8tU5mMauEa2V10JTc=','2023-05-01 21:22:42.813315',0,'50a7e6f69d','Club2','Rep2','club2@gmail.com',0,1,'2023-05-01 21:21:44.521384',4);
/*!40000 ALTER TABLE `Booking_System_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_customuser_groups`
--

DROP TABLE IF EXISTS `Booking_System_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Booking_System_customuse_customuser_id_group_id_01160e6b_uniq` (`customuser_id`,`group_id`),
  KEY `Booking_System_custo_group_id_565e93b2_fk_auth_grou` (`group_id`),
  CONSTRAINT `Booking_System_custo_customuser_id_7d32faf1_fk_Booking_S` FOREIGN KEY (`customuser_id`) REFERENCES `Booking_System_customuser` (`id`),
  CONSTRAINT `Booking_System_custo_group_id_565e93b2_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_customuser_groups`
--

LOCK TABLES `Booking_System_customuser_groups` WRITE;
/*!40000 ALTER TABLE `Booking_System_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `Booking_System_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_customuser_user_permissions`
--

DROP TABLE IF EXISTS `Booking_System_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Booking_System_customuse_customuser_id_permission_184db5cb_uniq` (`customuser_id`,`permission_id`),
  KEY `Booking_System_custo_permission_id_57ecf97b_fk_auth_perm` (`permission_id`),
  CONSTRAINT `Booking_System_custo_customuser_id_1904e2a1_fk_Booking_S` FOREIGN KEY (`customuser_id`) REFERENCES `Booking_System_customuser` (`id`),
  CONSTRAINT `Booking_System_custo_permission_id_57ecf97b_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_customuser_user_permissions`
--

LOCK TABLES `Booking_System_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `Booking_System_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `Booking_System_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_director`
--

DROP TABLE IF EXISTS `Booking_System_director`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_director` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_director`
--

LOCK TABLES `Booking_System_director` WRITE;
/*!40000 ALTER TABLE `Booking_System_director` DISABLE KEYS */;
INSERT INTO `Booking_System_director` VALUES (1,'Anthony Russo'),(2,'Joe Russo'),(3,'Stephen E. Rivkin'),(4,'Peter Boyle'),(5,'Chris Meledandri'),(6,'Manfred Banach'),(7,'John Murphy');
/*!40000 ALTER TABLE `Booking_System_director` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_film`
--

DROP TABLE IF EXISTS `Booking_System_film`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_film` (
  `film_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `release_date` date NOT NULL,
  `description` longtext NOT NULL,
  `age_rating` varchar(5) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `now_showing` tinyint(1) NOT NULL,
  PRIMARY KEY (`film_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_film`
--

LOCK TABLES `Booking_System_film` WRITE;
/*!40000 ALTER TABLE `Booking_System_film` DISABLE KEYS */;
INSERT INTO `Booking_System_film` VALUES (1,'Avengers: Endgame','2019-04-25','Adrift in space with no food or water, Tony Stark sends a message to Pepper Potts as his oxygen supply starts to dwindle. Meanwhile, the remaining Avengers -- Thor, Black Widow, Captain America and Bruce Banner -- must figure out a way to bring back their vanquished allies for an epic showdown with Thanos -- the evil demigod who decimated the planet and the universe.','PG-13','film_images/avengers_end_game.jpg',1),(2,'Avatar: The Way of Water','2022-12-14','Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.','PG-13','film_images/Avatar_The_Way_of_Water.jpg',1),(3,'Creed III','2023-03-01','After dominating the boxing world, Adonis Creed has been thriving in both his career and family life. When a childhood friend and former boxing prodigy, Damian Anderson, resurfaces after serving a long sentence in prison, he is eager to prove that he deserves his shot in the ring. The face-off between former friends is more than just a fight. To settle the score, Adonis must put his future on the line to battle Damian ΓÇö a fighter who has nothing to lose.','PG-13','film_images/Creed_III.jpg',1),(4,'The Super Mario Bros. Movie','2023-04-05','While working underground to fix a water main, Brooklyn plumbersΓÇöand brothersΓÇöMario and Luigi are transported down a mysterious pipe and wander into a magical new world. But when the brothers are separated, Mario embarks on an epic quest to find Luigi.','PG','film_images/The_Super_Mario_Bros._Movie.jpg',1),(5,'John Wick: Chapter 4','2023-03-22','With the price on his head ever increasing, John Wick uncovers a path to defeating The High Table. But before he can earn his freedom, Wick must face off against a new enemy with powerful alliances across the globe and forces that turn old friends into foes.','','film_images/John_Wick_Chapter_4.jpg',1),(6,'Guardians of the Galaxy Volume 3','2023-05-03','Peter Quill, still reeling from the loss of Gamora, must rally his team around him to defend the universe along with protecting one of their own. A mission that, if not completed successfully, could quite possibly lead to the end of the Guardians as we know them.','PG-13','film_images/Guardians_of_the_Galaxy_Volume_3.jpg',1);
/*!40000 ALTER TABLE `Booking_System_film` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_film_cast`
--

DROP TABLE IF EXISTS `Booking_System_film_cast`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_film_cast` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `film_id` int NOT NULL,
  `cast_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Booking_System_film_cast_film_id_cast_id_67e47e12_uniq` (`film_id`,`cast_id`),
  KEY `Booking_System_film__cast_id_cdc4901a_fk_Booking_S` (`cast_id`),
  CONSTRAINT `Booking_System_film__cast_id_cdc4901a_fk_Booking_S` FOREIGN KEY (`cast_id`) REFERENCES `Booking_System_cast` (`id`),
  CONSTRAINT `Booking_System_film__film_id_cae7b23e_fk_Booking_S` FOREIGN KEY (`film_id`) REFERENCES `Booking_System_film` (`film_id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_film_cast`
--

LOCK TABLES `Booking_System_film_cast` WRITE;
/*!40000 ALTER TABLE `Booking_System_film_cast` DISABLE KEYS */;
INSERT INTO `Booking_System_film_cast` VALUES (1,1,1),(2,1,2),(3,1,3),(4,2,4),(5,2,5),(6,2,6),(7,2,7),(8,2,8),(9,3,9),(10,3,10),(11,3,11),(12,3,12),(13,3,13),(14,4,14),(15,4,15),(16,4,16),(17,4,17),(18,4,18),(19,5,19),(20,5,20),(21,5,21),(22,5,22),(23,5,23),(24,6,5),(25,6,14),(26,6,24),(27,6,25),(28,6,26);
/*!40000 ALTER TABLE `Booking_System_film_cast` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_film_directors`
--

DROP TABLE IF EXISTS `Booking_System_film_directors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_film_directors` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `film_id` int NOT NULL,
  `director_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Booking_System_film_directors_film_id_director_id_4f23776b_uniq` (`film_id`,`director_id`),
  KEY `Booking_System_film__director_id_fbf752fe_fk_Booking_S` (`director_id`),
  CONSTRAINT `Booking_System_film__director_id_fbf752fe_fk_Booking_S` FOREIGN KEY (`director_id`) REFERENCES `Booking_System_director` (`id`),
  CONSTRAINT `Booking_System_film__film_id_3ca02bdb_fk_Booking_S` FOREIGN KEY (`film_id`) REFERENCES `Booking_System_film` (`film_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_film_directors`
--

LOCK TABLES `Booking_System_film_directors` WRITE;
/*!40000 ALTER TABLE `Booking_System_film_directors` DISABLE KEYS */;
INSERT INTO `Booking_System_film_directors` VALUES (1,1,1),(2,1,2),(3,2,3),(4,3,4),(5,4,5),(6,5,6),(7,6,7);
/*!40000 ALTER TABLE `Booking_System_film_directors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_paymentdetail`
--

DROP TABLE IF EXISTS `Booking_System_paymentdetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_paymentdetail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cardholder_name` varchar(100) NOT NULL,
  `card_number` varchar(16) NOT NULL,
  `expiration_month` varchar(2) NOT NULL,
  `expiration_year` varchar(4) NOT NULL,
  `cvv` varchar(3) NOT NULL,
  `account_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Booking_System_payme_account_id_f7719541_fk_Booking_S` (`account_id`),
  CONSTRAINT `Booking_System_payme_account_id_f7719541_fk_Booking_S` FOREIGN KEY (`account_id`) REFERENCES `Booking_System_account` (`account_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_paymentdetail`
--

LOCK TABLES `Booking_System_paymentdetail` WRITE;
/*!40000 ALTER TABLE `Booking_System_paymentdetail` DISABLE KEYS */;
/*!40000 ALTER TABLE `Booking_System_paymentdetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_representative`
--

DROP TABLE IF EXISTS `Booking_System_representative`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_representative` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  `rep_number` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rep_number` (`rep_number`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_representative`
--

LOCK TABLES `Booking_System_representative` WRITE;
/*!40000 ALTER TABLE `Booking_System_representative` DISABLE KEYS */;
INSERT INTO `Booking_System_representative` VALUES (1,'Club1','Rep1','1997-09-16','681e1a1d05'),(2,'Club2','Rep2','1996-05-09','50a7e6f69d');
/*!40000 ALTER TABLE `Booking_System_representative` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_screen`
--

DROP TABLE IF EXISTS `Booking_System_screen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_screen` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `screen_number` int unsigned NOT NULL,
  `seats` int unsigned NOT NULL,
  `social_distancing` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `screen_number` (`screen_number`),
  CONSTRAINT `Booking_System_screen_chk_1` CHECK ((`screen_number` >= 0)),
  CONSTRAINT `Booking_System_screen_chk_2` CHECK ((`seats` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_screen`
--

LOCK TABLES `Booking_System_screen` WRITE;
/*!40000 ALTER TABLE `Booking_System_screen` DISABLE KEYS */;
INSERT INTO `Booking_System_screen` VALUES (1,1,100,0),(2,2,100,0),(3,3,100,0),(4,4,100,0),(5,5,100,0),(6,6,100,0),(7,7,100,0),(8,8,100,0),(9,9,100,0),(10,10,100,0);
/*!40000 ALTER TABLE `Booking_System_screen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_seat`
--

DROP TABLE IF EXISTS `Booking_System_seat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_seat` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `seat_number` varchar(3) NOT NULL,
  `is_available` tinyint(1) NOT NULL,
  `film_id` int NOT NULL,
  `screen_id` bigint NOT NULL,
  `show_time_id` bigint NOT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Booking_System_seat_screen_id_seat_number_sh_1ceec459_uniq` (`screen_id`,`seat_number`,`show_time_id`),
  KEY `Booking_System_seat_show_time_id_3b220d12_fk_Booking_S` (`show_time_id`),
  KEY `Booking_System_seat_user_id_14e136ff_fk_Booking_S` (`user_id`),
  KEY `Booking_System_seat_film_id_27e748af_fk_Booking_S` (`film_id`),
  CONSTRAINT `Booking_System_seat_film_id_27e748af_fk_Booking_S` FOREIGN KEY (`film_id`) REFERENCES `Booking_System_film` (`film_id`),
  CONSTRAINT `Booking_System_seat_screen_id_808ffc09_fk_Booking_S` FOREIGN KEY (`screen_id`) REFERENCES `Booking_System_screen` (`id`),
  CONSTRAINT `Booking_System_seat_show_time_id_3b220d12_fk_Booking_S` FOREIGN KEY (`show_time_id`) REFERENCES `Booking_System_showtime` (`id`),
  CONSTRAINT `Booking_System_seat_user_id_14e136ff_fk_Booking_S` FOREIGN KEY (`user_id`) REFERENCES `Booking_System_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_seat`
--

LOCK TABLES `Booking_System_seat` WRITE;
/*!40000 ALTER TABLE `Booking_System_seat` DISABLE KEYS */;
/*!40000 ALTER TABLE `Booking_System_seat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_seatselection`
--

DROP TABLE IF EXISTS `Booking_System_seatselection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_seatselection` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `booking_id` bigint NOT NULL,
  `seat_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Booking_System_seats_booking_id_0b6ca62b_fk_Booking_S` (`booking_id`),
  KEY `Booking_System_seats_seat_id_49cfe982_fk_Booking_S` (`seat_id`),
  CONSTRAINT `Booking_System_seats_booking_id_0b6ca62b_fk_Booking_S` FOREIGN KEY (`booking_id`) REFERENCES `Booking_System_booking` (`id`),
  CONSTRAINT `Booking_System_seats_seat_id_49cfe982_fk_Booking_S` FOREIGN KEY (`seat_id`) REFERENCES `Booking_System_seat` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_seatselection`
--

LOCK TABLES `Booking_System_seatselection` WRITE;
/*!40000 ALTER TABLE `Booking_System_seatselection` DISABLE KEYS */;
/*!40000 ALTER TABLE `Booking_System_seatselection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_showtime`
--

DROP TABLE IF EXISTS `Booking_System_showtime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_showtime` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `film_id` int NOT NULL,
  `screen_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Booking_System_showt_film_id_caa974f7_fk_Booking_S` (`film_id`),
  KEY `Booking_System_showt_screen_id_e0feac75_fk_Booking_S` (`screen_id`),
  CONSTRAINT `Booking_System_showt_film_id_caa974f7_fk_Booking_S` FOREIGN KEY (`film_id`) REFERENCES `Booking_System_film` (`film_id`),
  CONSTRAINT `Booking_System_showt_screen_id_e0feac75_fk_Booking_S` FOREIGN KEY (`screen_id`) REFERENCES `Booking_System_screen` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_showtime`
--

LOCK TABLES `Booking_System_showtime` WRITE;
/*!40000 ALTER TABLE `Booking_System_showtime` DISABLE KEYS */;
INSERT INTO `Booking_System_showtime` VALUES (1,'2023-05-08 08:00:00.000000','2023-05-08 12:46:00.000000',1,1),(2,'2023-05-09 07:48:00.000000','2023-05-09 10:48:00.000000',2,2),(3,'2023-05-09 09:49:00.000000','2023-05-09 12:49:00.000000',3,3),(4,'2023-05-09 07:50:00.000000','2023-05-09 11:50:00.000000',1,1),(5,'2023-05-09 10:52:00.000000','2023-05-09 12:52:00.000000',4,4),(6,'2023-05-09 08:52:00.000000','2023-05-09 12:52:00.000000',5,5),(7,'2023-05-08 05:46:00.000000','2023-05-08 10:53:00.000000',5,5),(8,'2023-05-09 15:53:00.000000','2023-05-09 18:53:00.000000',1,1),(9,'2023-05-08 08:53:00.000000','2023-05-08 12:53:00.000000',2,2),(10,'2023-05-08 08:54:00.000000','2023-05-08 11:54:00.000000',3,3),(11,'2023-05-09 06:55:00.000000','2023-05-09 09:55:00.000000',6,6),(12,'2023-05-08 06:55:00.000000','2023-05-08 21:55:00.000000',6,6),(13,'2023-05-08 07:56:00.000000','2023-05-08 12:56:00.000000',4,4);
/*!40000 ALTER TABLE `Booking_System_showtime` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_statementaccountrequest`
--

DROP TABLE IF EXISTS `Booking_System_statementaccountrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_statementaccountrequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cardholder_name` varchar(100) NOT NULL,
  `card_number` varchar(16) NOT NULL,
  `expiration_month` varchar(2) NOT NULL,
  `expiration_year` varchar(4) NOT NULL,
  `cvv` varchar(3) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Booking_System_state_user_id_1ace0d88_fk_Booking_S` (`user_id`),
  CONSTRAINT `Booking_System_state_user_id_1ace0d88_fk_Booking_S` FOREIGN KEY (`user_id`) REFERENCES `Booking_System_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_statementaccountrequest`
--

LOCK TABLES `Booking_System_statementaccountrequest` WRITE;
/*!40000 ALTER TABLE `Booking_System_statementaccountrequest` DISABLE KEYS */;
/*!40000 ALTER TABLE `Booking_System_statementaccountrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Booking_System_student`
--

DROP TABLE IF EXISTS `Booking_System_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking_System_student` (
  `Student_id` int NOT NULL AUTO_INCREMENT,
  `has_discount` tinyint(1) NOT NULL,
  `approved` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`Student_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `Booking_System_stude_user_id_57d69966_fk_Booking_S` FOREIGN KEY (`user_id`) REFERENCES `Booking_System_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking_System_student`
--

LOCK TABLES `Booking_System_student` WRITE;
/*!40000 ALTER TABLE `Booking_System_student` DISABLE KEYS */;
INSERT INTO `Booking_System_student` VALUES (1,0,1,4);
/*!40000 ALTER TABLE `Booking_System_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add account',6,'add_account'),(22,'Can change account',6,'change_account'),(23,'Can delete account',6,'delete_account'),(24,'Can view account',6,'view_account'),(25,'Can add address',7,'add_address'),(26,'Can change address',7,'change_address'),(27,'Can delete address',7,'delete_address'),(28,'Can view address',7,'view_address'),(29,'Can add booking',8,'add_booking'),(30,'Can change booking',8,'change_booking'),(31,'Can delete booking',8,'delete_booking'),(32,'Can view booking',8,'view_booking'),(33,'Can add cast',9,'add_cast'),(34,'Can change cast',9,'change_cast'),(35,'Can delete cast',9,'delete_cast'),(36,'Can view cast',9,'view_cast'),(37,'Can add club',10,'add_club'),(38,'Can change club',10,'change_club'),(39,'Can delete club',10,'delete_club'),(40,'Can view club',10,'view_club'),(41,'Can add contact',11,'add_contact'),(42,'Can change contact',11,'change_contact'),(43,'Can delete contact',11,'delete_contact'),(44,'Can view contact',11,'view_contact'),(45,'Can add director',12,'add_director'),(46,'Can change director',12,'change_director'),(47,'Can delete director',12,'delete_director'),(48,'Can view director',12,'view_director'),(49,'Can add film',13,'add_film'),(50,'Can change film',13,'change_film'),(51,'Can delete film',13,'delete_film'),(52,'Can view film',13,'view_film'),(53,'Can add representative',14,'add_representative'),(54,'Can change representative',14,'change_representative'),(55,'Can delete representative',14,'delete_representative'),(56,'Can view representative',14,'view_representative'),(57,'Can add screen',15,'add_screen'),(58,'Can change screen',15,'change_screen'),(59,'Can delete screen',15,'delete_screen'),(60,'Can view screen',15,'view_screen'),(61,'Can add seat',16,'add_seat'),(62,'Can change seat',16,'change_seat'),(63,'Can delete seat',16,'delete_seat'),(64,'Can view seat',16,'view_seat'),(65,'Can add user',17,'add_customuser'),(66,'Can change user',17,'change_customuser'),(67,'Can delete user',17,'delete_customuser'),(68,'Can view user',17,'view_customuser'),(69,'Can add student',18,'add_student'),(70,'Can change student',18,'change_student'),(71,'Can delete student',18,'delete_student'),(72,'Can view student',18,'view_student'),(73,'Can add statement account request',19,'add_statementaccountrequest'),(74,'Can change statement account request',19,'change_statementaccountrequest'),(75,'Can delete statement account request',19,'delete_statementaccountrequest'),(76,'Can view statement account request',19,'view_statementaccountrequest'),(77,'Can add show time',20,'add_showtime'),(78,'Can change show time',20,'change_showtime'),(79,'Can delete show time',20,'delete_showtime'),(80,'Can view show time',20,'view_showtime'),(81,'Can add seat selection',21,'add_seatselection'),(82,'Can change seat selection',21,'change_seatselection'),(83,'Can delete seat selection',21,'delete_seatselection'),(84,'Can view seat selection',21,'view_seatselection'),(85,'Can add payment detail',22,'add_paymentdetail'),(86,'Can change payment detail',22,'change_paymentdetail'),(87,'Can delete payment detail',22,'delete_paymentdetail'),(88,'Can view payment detail',22,'view_paymentdetail'),(89,'Can add club rep',23,'add_clubrep'),(90,'Can change club rep',23,'change_clubrep'),(91,'Can delete club rep',23,'delete_clubrep'),(92,'Can view club rep',23,'view_clubrep'),(93,'Can add account statement',24,'add_accountstatement'),(94,'Can change account statement',24,'change_accountstatement'),(95,'Can delete account statement',24,'delete_accountstatement'),(96,'Can view account statement',24,'view_accountstatement');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_Booking_S` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_Booking_S` FOREIGN KEY (`user_id`) REFERENCES `Booking_System_customuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(6,'Booking_System','account'),(24,'Booking_System','accountstatement'),(7,'Booking_System','address'),(8,'Booking_System','booking'),(9,'Booking_System','cast'),(10,'Booking_System','club'),(23,'Booking_System','clubrep'),(11,'Booking_System','contact'),(17,'Booking_System','customuser'),(12,'Booking_System','director'),(13,'Booking_System','film'),(22,'Booking_System','paymentdetail'),(14,'Booking_System','representative'),(15,'Booking_System','screen'),(16,'Booking_System','seat'),(21,'Booking_System','seatselection'),(20,'Booking_System','showtime'),(19,'Booking_System','statementaccountrequest'),(18,'Booking_System','student'),(4,'contenttypes','contenttype'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-05-01 20:42:26.295588'),(2,'contenttypes','0002_remove_content_type_name','2023-05-01 20:42:26.358041'),(3,'auth','0001_initial','2023-05-01 20:42:26.570939'),(4,'auth','0002_alter_permission_name_max_length','2023-05-01 20:42:26.618551'),(5,'auth','0003_alter_user_email_max_length','2023-05-01 20:42:26.626305'),(6,'auth','0004_alter_user_username_opts','2023-05-01 20:42:26.634856'),(7,'auth','0005_alter_user_last_login_null','2023-05-01 20:42:26.642267'),(8,'auth','0006_require_contenttypes_0002','2023-05-01 20:42:26.647785'),(9,'auth','0007_alter_validators_add_error_messages','2023-05-01 20:42:26.654784'),(10,'auth','0008_alter_user_username_max_length','2023-05-01 20:42:26.662460'),(11,'auth','0009_alter_user_last_name_max_length','2023-05-01 20:42:26.670472'),(12,'auth','0010_alter_group_name_max_length','2023-05-01 20:42:26.696530'),(13,'auth','0011_update_proxy_permissions','2023-05-01 20:42:26.717082'),(14,'auth','0012_alter_user_first_name_max_length','2023-05-01 20:42:26.727081'),(15,'Booking_System','0001_initial','2023-05-01 20:42:28.864964'),(16,'admin','0001_initial','2023-05-01 20:42:29.017505'),(17,'admin','0002_logentry_remove_auto_add','2023-05-01 20:42:29.031747'),(18,'admin','0003_logentry_add_action_flag_choices','2023-05-01 20:42:29.046224'),(19,'sessions','0001_initial','2023-05-01 20:42:29.085197');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('l8dsu6f82e2sq8z5qoukompu8fzlh3sf','.eJxVjs1OxDAMhF8F5QqJHMf563HvPEOVxAktrFppm0VCiHcnlfYAR898M55vMad7X-b7UW_zymISKF7-ajmVj7qdBr-n7W1XZd_6bc3qRNTDPdTrzvV6ebD_CpZ0LCNtarM11sYU0RNYTYVc0FFTK75xaM7Ukk0OFdn73DxFJnBcHaZUOYzSazr6nEpfP9f-dS4FNBKsBP2EekKaIKqIFiI8A0wAI9L3MWigJZJjzVoy-yDHe5TBeSvZEIyDikcQP79xAVC9:1ptb4L:1-cL40cRHcjUloflfI1ko1XR07blC4VC1cjdnUkRylU','2023-05-02 17:28:25.082240');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-01 21:36:43
