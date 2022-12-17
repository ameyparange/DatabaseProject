CREATE TABLE `juneamenities` (
  `id` int NOT NULL,
  `Amenities` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `juneapartments` (
  `id` int NOT NULL,
  `Apt_id` int DEFAULT NULL,
  `url` varchar(300) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `Beds` decimal(10,0) DEFAULT NULL,
  `Bath` decimal(10,0) DEFAULT NULL,
  `Price` decimal(10,0) DEFAULT NULL,
  `BedArea` int DEFAULT NULL,
  `Availablefrom` date DEFAULT NULL,
  `Availabletill` date DEFAULT NULL,
  `Description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `junetransport` (
  `id` int NOT NULL,
  `Trans_id` int DEFAULT NULL,
  `stations` varchar(100) DEFAULT NULL,
  `color` varchar(100) DEFAULT NULL,
  `walktime` int DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `subleaseroommate` (
  `RoommateID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Gender` varchar(45) DEFAULT NULL,
  `PhoneNumber` varchar(10) DEFAULT NULL,
  `Email` varchar(45) DEFAULT NULL,
  `Budget` int DEFAULT NULL,
  `RoommateDietaryPref` varchar(45) DEFAULT NULL,
  `RoommateGenderPref` varchar(45) DEFAULT NULL,
  `Amenities` varchar(1000) DEFAULT NULL,
  `PrefModeofTravel` varchar(45) DEFAULT NULL,
  `TypeOfSpot` varchar(45) DEFAULT NULL,
  `PrefMoveInDate` varchar(45) DEFAULT NULL,
  `NoOfRoommates` int DEFAULT NULL,
  PRIMARY KEY (`RoommateID`),
  UNIQUE KEY `RoommateID_UNIQUE` (`RoommateID`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `subleasespot` (
  `SpotID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `PhoneNumber` varchar(10) DEFAULT NULL,
  `Email` varchar(45) DEFAULT NULL,
  `Gender` varchar(45) DEFAULT NULL,
  `Address` varchar(200) DEFAULT NULL,
  `ProxToUni` float DEFAULT NULL,
  `Brokerage` int DEFAULT NULL,
  `LeaseSpotType` varchar(100) DEFAULT NULL,
  `BedroomCount` int DEFAULT NULL,
  `BathroomCount` int DEFAULT NULL,
  `Rent` int DEFAULT NULL,
  `DietaryPref` varchar(45) DEFAULT NULL,
  `GenderPref` varchar(45) DEFAULT NULL,
  `Amenities` varchar(1000) DEFAULT NULL,
  `AvailSpot` varchar(45) DEFAULT NULL,
  `PrefMoveInDate` varchar(45) DEFAULT NULL,
  `AvailSpotNum` int DEFAULT NULL,
  PRIMARY KEY (`SpotID`),
  UNIQUE KEY `SpotID_UNIQUE` (`SpotID`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `temporaryroommate` (
  `RoommateId` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Gender` varchar(45) DEFAULT NULL,
  `PhoneNumber` varchar(10) DEFAULT NULL,
  `Email` varchar(45) DEFAULT NULL,
  `Budget` varchar(45) DEFAULT NULL,
  `DietaryPref` varchar(45) DEFAULT NULL,
  `GenderPref` varchar(45) DEFAULT NULL,
  `Amenities` varchar(100) DEFAULT NULL,
  `PrefModeofTravel` varchar(45) DEFAULT NULL,
  `TypeOfSpot` varchar(100) DEFAULT NULL,
  `PrefMoveInDate` varchar(45) DEFAULT NULL,
  `NoOfRoommates` int DEFAULT NULL,
  PRIMARY KEY (`RoommateId`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `temporaryspot` (
  `SpotID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `PhoneNumber` varchar(10) DEFAULT NULL,
  `Email` varchar(45) DEFAULT NULL,
  `Gender` varchar(45) DEFAULT NULL,
  `Address` varchar(200) DEFAULT NULL,
  `ProximityToUni` float DEFAULT NULL,
  `BedroomCount` int DEFAULT NULL,
  `BathroomCount` int DEFAULT NULL,
  `TempRent` int DEFAULT NULL,
  `DietaryPref` varchar(45) DEFAULT NULL,
  `GenderPref` varchar(45) DEFAULT NULL,
  `Amenities` varchar(1000) DEFAULT NULL,
  `AvailableSpot` varchar(45) DEFAULT NULL,
  `PrefMoveInDate` varchar(45) DEFAULT NULL,
  `PrefMoveOutDate` varchar(45) DEFAULT NULL,
  `AvailSpotNum` int DEFAULT NULL,
  PRIMARY KEY (`SpotID`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

