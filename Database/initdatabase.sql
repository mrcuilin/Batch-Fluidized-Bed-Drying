CREATE DATABASE `dataCapture` /*!40100 DEFAULT CHARACTER SET utf8 */;

use dataCapture;

CREATE TABLE `dataSession` (
  `sampleTime` varchar(45) NOT NULL,
  `sessionId` varchar(45) NOT NULL,
  PRIMARY KEY (`sampleTime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Sensordata` (
  `sessionId` varchar(45) NOT NULL,
  `sensor1` varchar(100) DEFAULT NULL,
  `sensor2` varchar(100) DEFAULT NULL,
  `sensor3` varchar(100) DEFAULT NULL,
  `sensor4` varchar(100) DEFAULT NULL,
  `sensor5` varchar(100) DEFAULT NULL,
  `sensor6` varchar(100) DEFAULT NULL,
  `sensor7` varchar(100) DEFAULT NULL,
  `sensor8` varchar(100) DEFAULT NULL,
  `sensor9` varchar(100) DEFAULT NULL,
  `sensor10` varchar(100) DEFAULT NULL,
  `sampleTimeStamp` int(11) NOT NULL,
  PRIMARY KEY (`sessionId`,`sampleTimeStamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `statusTB` (
  `Keyword` varchar(40) NOT NULL,
  `Status` varchar(45) NOT NULL,
  PRIMARY KEY (`Keyword`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

//当前状态
INSERT INTO `dataCapture`.`statusTB`
(`Keyword`,`Status`) VALUES ('RUNNING','NO'),('ENABLED','NO');

//至少一个点的数据，共2条
INSERT INTO `dataCapture`.`dataSession`
(`sampleTime`,`sessionId`) VALUES ('20160504080918', '2016-05-04');
INSERT INTO `dataCapture`.`Sensordata`
VALUES ('20160504080918', '24.320000', '27.365085', '24.390000', '27.336455', '24.420000', '27.338752', '7', '8', '9', '10', '986'
);
