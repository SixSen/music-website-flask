CREATE DATABASE  IF NOT EXISTS `musicdb` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `musicdb`;
-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: musicdb
-- ------------------------------------------------------
-- Server version	5.7.17-log

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

--
-- Table structure for table `music`
--

DROP TABLE IF EXISTS `music`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `music` (
  `music_id` int(11) NOT NULL AUTO_INCREMENT,
  `music_name` varchar(100) NOT NULL,
  `author` varchar(100) DEFAULT NULL,
  `download` int(11) NOT NULL,
  `listen` int(11) NOT NULL,
  `style` varchar(50) DEFAULT NULL,
  `free` int(11) NOT NULL,
  `address` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`music_id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `music`
--

LOCK TABLES `music` WRITE;
/*!40000 ALTER TABLE `music` DISABLE KEYS */;
INSERT INTO `music` VALUES (2,'小城谣','胡碧桥',132,4327,'Folk',0,'533204535'),(3,'小城谣（cover胡碧桥）','泥鳅Niko',25,994,'Folk',1,'533204535'),(4,'小城谣（cover胡碧桥）','洛少爷',12,535,'Folk',1,'533204535'),(5,'起风了','吴青峰',123,2319,'Pop',0,'1335868818'),(6,'校园寓言故事','AR',123,2330,'Jazz',0,'1335868818'),(7,'一个酒馆老板的独白','留声玩具',118,2159,'R&B',0,'1335868818'),(8,'有梦可待','陈立农',101,1924,'classical',1,'1338519683'),(10,'生僻字','陈珂宇',245,421,'Pop',0,'1335868818'),(11,'一曲相思','半阳',188,352,'Jazz',1,'1335868818'),(12,'沙漠骆驼','展展与罗罗',146,337,'classical',1,'1319073956'),(13,'知否知否','胡夏',188,456,'Pop',0,'466128196'),(14,'夜之光','花姐',54,89,'Jazz',1,'1333257461'),(15,'光年之外','邓紫棋',876,9339,'Pop',0,'516847399'),(16,'38度6','黑龙',245,54,'classical',0,'1314197765'),(17,'可不可以','张紫豪',48,145,'Pop',1,'1314197765'),(18,'往后余生','马良',845,2482,'Pop',0,'1314197765'),(19,'Without Me','Halsey',189,1555,'Jazz',1,'25683968'),(20,'Thank U Next','Halsey',579,2456,'Folk',1,'36150266'),(21,'Sunflower','Post',264,359,'classical',0,'36150266'),(22,'Hign Hopes','Panic',64,215,'Folk',1,'36150266'),(23,'Drip Too Hard','Lil',84,348,'Jazz',1,'36150266'),(24,'Better Now','Post Malone',19,220,'Pop',0,'36150266'),(25,'Shallow','Lady',25,161,'Pop',1,'36150266'),(26,'Natural','Imagine',187,1552,'Jazz',1,'36150266'),(27,'SICKO','Travis',136,249,'classical',0,'36150266'),(28,'Yousay','Lauren',289,2424,'Folk',1,'36150266'),(29,'沐春风','谢安琪',289,1899,'calssical',1,'573577094'),(30,'废青','谭咏麟',389,2498,'classical',0,'573577094'),(31,'倒数','邓紫棋',268,1597,'Pop',0,'573577094'),(32,'喜欢你','邓紫棋',355,3555,'Pop',1,'427015262'),(33,'盗将行','司南',888,2477,'Pop',0,'1310542851'),(34,'98K','WayneWaste',123,1369,'R&B',1,'521704784');
/*!40000 ALTER TABLE `music` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-13  9:38:46
