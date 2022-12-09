DROP DATABASE ecom;
CREATE DATABASE ecom;
USE ecom;

-- CREATING TABLE
CREATE TABLE USER (
	`ID` varchar(200) NOT NULL,
    `Name` varchar(200) NOT NULL,
    `Sex` varchar(200) NOT NULL,
    `Birthdate` varchar(200) NOT NULL,
    `Phone` varchar(200) NOT NULL,
    `Email` varchar(200) NOT NULL,
    `Address` varchar(200) NOT NULL,
    PRIMARY KEY(`ID`)
);

CREATE TABLE SELLER (
	`ID` varchar(200) NOT NULL,
    `StoreName` varchar(200) NOT NULL,
    `StoreAddress` varchar(200) NOT NULL,
    `Logo` varchar(200) NOT NULL,
    `NationalID` varchar(200) NOT NULL,
    `TotalRevenue` double DEFAULT 0,
    PRIMARY KEY(`ID`),
    FOREIGN KEY (ID) REFERENCES USER(ID)
);

CREATE TABLE PERSONAL_ACCOUNT (
	`ID` varchar(200) NOT NULL,
    `PersonalTaxNum` varchar(200) NOT NULL,
    PRIMARY KEY(`ID`),
    FOREIGN KEY (ID) REFERENCES SELLER(ID)
);

CREATE TABLE BUSINESS_ACCOUNT (
	`ID` varchar(200) NOT NULL,
    `BusinessTaxNum` varchar(200) NOT NULL,
    PRIMARY KEY(`ID`),
    FOREIGN KEY (ID) REFERENCES SELLER(ID)
);

CREATE TABLE BRAND_ACCOUNT (
	`ID` varchar(200) NOT NULL,
    `BusinessTaxNum` varchar(200) NOT NULL,
    `BrandAgreement` varchar(200) NOT NULL,
    PRIMARY KEY(`ID`),
    FOREIGN KEY (ID) REFERENCES SELLER(ID)
);

CREATE TABLE BUYER (
	`ID` varchar(200) NOT NULL,
    `AccountType` varchar(200) NOT NULL,
    `TotalMoneySpent` double DEFAULT 0,
    PRIMARY KEY(`ID`),
    FOREIGN KEY (ID) REFERENCES USER(ID)
);

CREATE TABLE FAVORITE_STORE (
	`BuyerID` varchar(200) NOT NULL,
    `StoreID` varchar(200) NOT NULL,
    PRIMARY KEY(`BuyerID`, `StoreID`),
    FOREIGN KEY (BuyerID) REFERENCES BUYER(ID),
    FOREIGN KEY (StoreID) REFERENCES SELLER(ID)
);

CREATE TABLE CREDIT (
	`ID` varchar(200) NOT NULL,
    `Number` varchar(200) NOT NULL,
    `Bank` varchar(200) NOT NULL,
    `ExpDate` varchar(200) NOT NULL,
    `UserID` varchar(200) NOT NULL,
    PRIMARY KEY(`ID`),
    FOREIGN KEY (UserID) REFERENCES USER(ID)
);

CREATE TABLE PRODUCT (
	`ID` varchar(200) NOT NULL,
    `Name` varchar(200) NOT NULL,
    `Brand` varchar(200) NOT NULL,
    `Type` varchar(200) NOT NULL,
    `Price` varchar(200) NOT NULL,
    `Quantity` int NOT NULL,
    `SellerID` varchar(200) NOT NULL,
    PRIMARY KEY(`ID`),
    FOREIGN KEY (SellerID) REFERENCES SELLER(ID)
);

CREATE TABLE SHOP_ORDER (
	`ID` varchar(200) NOT NULL,
    `Date` varchar(200) NOT NULL,
    `PaymentMethod` varchar(200) NOT NULL,
    `SellerID` varchar(200) NOT NULL,
    `BuyerID` varchar(200) NOT NULL,
    `TotalCost` double DEFAULT 0,
    `TotalRange` int DEFAULT 0,
    PRIMARY KEY(`ID`),
    FOREIGN KEY (SellerID) REFERENCES SELLER(ID),
	FOREIGN KEY (BuyerID) REFERENCES BUYER(ID)
);

CREATE TABLE PRODUCT_ORDER (
	`ProductID` varchar(200) NOT NULL,
    `OrderID` varchar(200) NOT NULL,
    `Quantity` int NOT NULL,
    PRIMARY KEY(`ProductID`, `OrderID`),
    FOREIGN KEY (ProductID) REFERENCES PRODUCT(ID),
	FOREIGN KEY (OrderID) REFERENCES SHOP_ORDER(ID)
);

CREATE TABLE COUPON (
	`ID` varchar(200) NOT NULL,
    `Code` varchar(200) NOT NULL,
    `ExpDate` varchar(200) NOT NULL,
    PRIMARY KEY(`ID`)
);

CREATE TABLE BUYER_COUPON (
	`CouponID` varchar(200) NOT NULL,
    `BuyerID` varchar(200) NOT NULL,
    PRIMARY KEY(`CouponID`, `BuyerID`),
    FOREIGN KEY (CouponID) REFERENCES COUPON(ID),
	FOREIGN KEY (BuyerID) REFERENCES BUYER(ID)
);

CREATE TABLE PRODUCT_COUPON (
	`CouponID` varchar(200) NOT NULL,
    `ProductID` varchar(200) NOT NULL,
    PRIMARY KEY(`CouponID`, `ProductID`),
    FOREIGN KEY (CouponID) REFERENCES COUPON(ID),
	FOREIGN KEY (ProductID) REFERENCES PRODUCT(ID)
);

CREATE TABLE ORDER_COUPON (
	`CouponID` varchar(200) NOT NULL,
    `OrderID` varchar(200) NOT NULL,
    PRIMARY KEY(`CouponID`, `OrderID`),
    FOREIGN KEY (CouponID) REFERENCES COUPON(ID),
	FOREIGN KEY (OrderID) REFERENCES SHOP_ORDER(ID)
);

CREATE TABLE SHIPPER (
	`ID` varchar(200) NOT NULL,
    `Name` varchar(200) NOT NULL,
	`Type` varchar(200) NOT NULL,
    PRIMARY KEY(`ID`)
);

CREATE TABLE VEHICLE (
	`ID` varchar(200) NOT NULL,
	`Type` varchar(200) NOT NULL,
	 PRIMARY KEY(`ID`)
);

CREATE TABLE SHIPPER_VEHICLE (
	`ShipperID` varchar(200) NOT NULL,
    `VehicleID` varchar(200) NOT NULL,
    `RangeInKM` int NOT NULL,
    `FeePerRangeUnit` int NOT NULL,
    PRIMARY KEY(`ShipperID`, `VehicleID`),
    FOREIGN KEY (ShipperID) REFERENCES SHIPPER(ID),
	FOREIGN KEY (VehicleID) REFERENCES VEHICLE(ID)
);

CREATE TABLE SHIPPER_ORDER (
	`ShipperID` varchar(200) NOT NULL,
    `OrderID` varchar(200) NOT NULL,
    `Address` varchar(200) NOT NULL,
    `StartingDate` varchar(200) NOT NULL,
    `EstimatedArrivalDate` varchar(200) NOT NULL,
    PRIMARY KEY(`ShipperID`, `OrderID`),
    FOREIGN KEY (ShipperID) REFERENCES SHIPPER(ID),
	FOREIGN KEY (OrderID) REFERENCES SHOP_ORDER(ID)
);

CREATE TABLE ROUTE (
	`ShipperID` varchar(200) NOT NULL,
    `OrderID` varchar(200) NOT NULL,
    `Route` varchar(200) NOT NULL,
    `RangeInKM` int NOT NULL,
    PRIMARY KEY(`ShipperID`, `OrderID`, `Route`),
    FOREIGN KEY (ShipperID) REFERENCES SHIPPER_ORDER(ShipperID),
	FOREIGN KEY (OrderID) REFERENCES SHIPPER_ORDER(OrderID)
);

-- INSERTING INFO
INSERT INTO `USER` (`ID`, `Name`, `Sex`, `Birthdate`, `Phone`, `Email`, `Address`) VALUES
					('000000', 'Pham Anh Quan', 'M', '1990-12-09', '0909xxxxx2', 'email0@gmail.com', '65 Ham Nghi, P.Nguyen Thai Binh, Q.1, TPHCM'),
                    ('000001', 'Nguyen Hai Dang', 'M', '2005-10-07', '0909xxxxx6', 'email1@gmail.com', '109 Tran Duy Hung, P.Trung Hoa, Q.Cau Giay, Ha Noi'),
                    ('000002', 'Nguyen Manh Dan', 'M', '1995-06-17', '0909xxxxx8', 'email2@gmail.com', '1006 3 Thang 2, P.14, Q.10, TPHCM'),
                    ('000003', 'Truong Nguyen Hung Thinh', 'M', '1998-11-29', '0903xxxxx6', 'email3@gmail.com', '84 Nui Thanh, P.Hoa Cuong Bac, Q.Hai Chau, Da Nang'),
                    ('000004', 'Dao Anh Tuan', 'M', '2001-03-23', '0903xxxxx1', 'email4@gmail.com', '241 Dao Duy Tu, P.7, Q.10, TPHCM'),
                    ('000005', 'Bui Quoc Minh Quan', 'M', '1987-01-21', '0902xxxxx7', 'email5@gmail.com', '491 Tran Nguyen Han, P.Ho Nam, Q.Le Chan, Hai Phong'),
                    ('000006', 'Nguyen Ha Trong Hieu', 'M', '1988-12-13', '0903xxxxx5', 'email6@gmail.com', '178 Le Thanh Nghi, P.Dong Tam, Q.Hai Ba Trung, Ha Noi'),
                    ('000007', 'Chu Gia Vu Khanh', 'M', '2008-05-04', '0902xxxxx4', 'email7@gmail.com', '315 Vo Van Ngan, P.Linh Chieu, Q.Thu Duc, TP.HCM');
                    
INSERT INTO `SELLER` (`ID`,`StoreName`, `StoreAddress`, `Logo`, `NationalID`) VALUES
					('000000','BigAbs Shop', '558 Tran Hung Dao, P.14, Q.5, TPHCM', 'logo0.jpg', '0972xxxxxxx2'),
                    ('000002','Dai Ca Laptop Shop', '165 3 Thang 2, P.11, Q.10, TPHCM', 'logo2.jpg', '0911xxxxxxx5'),
                    ('000003','LadyMassage Store', '428 Truong Chinh, P.Hoa An, Q.Cam Le, Da Nang', 'logo3.jpg', '0872xxxxxxx1'),
                    ('000004','Rau Xanh Groceries', '241 Dao Duy Tu, P.7, Q.10, TPHCM', 'logo4.jpg', '0199xxxxxxx8'),
                    ('000005','Chopin Musical', '182 Nguyen Binh Khiem, P.Dang Giang, Q.Ngo Quyen, Hai Phong', 'logo5.jpg', '0595xxxxxxx6'),
                    ('000007','Blackwheel Motors', '291 Pham Van Dong, P.1, Q.Go Vap, TP.HCM', 'logo7.jpg', '0447xxxxxxx3');

INSERT INTO `PERSONAL_ACCOUNT` (`ID`,`PersonalTaxNum`) VALUES
					('000000','0105xxxxx8'),
                    ('000003','0206xxxxx2'),
                    ('000004','0709xxxxx1');

INSERT INTO `BUSINESS_ACCOUNT` (`ID`, `BusinessTaxNum`) VALUES
                    ('000002','0303xxxxx9'),
                    ('000005','0702xxxxx5');
                    
INSERT INTO `BRAND_ACCOUNT` (`ID`, `BusinessTaxNum`, `BrandAgreement`) VALUES
                    ('000007','0905xxxxx5', 'agree.jpg');

INSERT INTO `BUYER` (`ID`, `AccountType`) VALUES
					('000000', 'Silver'),
                    ('000001', 'Gold'),
                    ('000002', 'Gold'),
                    ('000003', 'Diamond'),
                    ('000004', 'Bronze'),
                    ('000005', 'Silver'),
                    ('000006', 'Bronze'),
                    ('000007', 'Diamond');

INSERT INTO `FAVORITE_STORE` (`BuyerID`, `StoreID`) VALUES
					('000000', '000002'),
                    ('000001', '000002'),
                    ('000001', '000007'),
                    ('000002', '000000'),
                    ('000004', '000003'),
                    ('000005', '000007'),
                    ('000006', '000000'),
                    ('000006', '000002'),
                    ('000006', '000007'),
                    ('000007', '000000');

INSERT INTO `CREDIT` (`ID`, `Number`, `Bank`, `ExpDate`, `UserID`) VALUES
					('000000', '3968xxxxxxxxxxx5', 'ACB', '2025-12-18', '000005'),
                    ('000001', '4728xxxxxxxxxxx7', 'OCB', '2023-02-14', '000007'),
                    ('000002', '1146xxxxxxxxxxx5', 'TCB', '2023-12-23', '000000'),
                    ('000003', '2743xxxxxxxxxxx4', 'MB', '2022-05-07', '000002'),
                    ('000004', '7889xxxxxxxxxxx2', 'VCB', '2023-09-03', '000004'),
                    ('000005', '1036xxxxxxxxxxx0', 'SCB', '2024-10-07', '000003');
                    
INSERT INTO `PRODUCT` (`ID`, `Name`, `Brand`, `Type`, `Price`, `Quantity`, `SellerID`) VALUES
					('000000', 'Watermelon', 'Local', 'Fruits & Vegetables', '15000', 124, '000004'),
                    ('000001', 'Intel CPU', 'Intel', 'Electronics', '19000000', 94, '000002'),
                    ('000002', 'Car wheels', 'Michelin', 'Cars & Motorbikes', '1750000', 90, '000007'),
                    ('000003', 'Shampoo', 'Head & Shoulders', 'Beauty', '240000', 267, '000003'),
                    ('000004', 'Piano', 'Kawai', 'Music', '68000000', 93, '000005'),
                    ('000005', 'Plastic sunflower', 'Local', 'Decorations', '12000', 189, '000004'),
                    ('000006', 'Apple', 'Local', 'Fruits & Vegetables', '21000', 117, '000004'),
                    ('000007', 'ASUS Laptop', 'Local', 'Electronics', '23000000', 94, '000002'),
                    ('000008', 'Facial moisturizer', 'CeraVe', 'Beauty', '67000', 123, '000003'),
                    ('000009', 'Guitar', 'Cordoba', 'Music', '5900000', 60, '000005'),
                    ('000010', 'Helmet', 'OEM', 'Clothing', '89000', 203, '000007'),
                    ('000011', 'Protein shake', 'Fairlife', 'Foods', '133000', 52, '000000'),
                    ('000012', 'Graphics card', 'NVIDIA', 'Electronics', '27500000', 76, '000002'),
                    ('000013', 'Violin', 'Suzuki', 'Music', '10000000', 36, '000005'),
                    ('000014', 'Dumbbell - 10kg', 'OEM', 'Others', '74000', 148, '000000'),
                    ('000015', 'AMD CPU', 'AMD', 'Electronics', '16200000', 20, '000002');

INSERT INTO `SHOP_ORDER` (`ID`, `Date`, `PaymentMethod`, `SellerID`, `BuyerID`) VALUES
					('000000', '2022-01-23', 'Cash', '000002', '000001'),
                    ('000001', '2021-07-12', 'Cash', '000002', '000000'),
                    ('000002', '2020-06-07', 'Credit', '000007', '000006'),
                    ('000003', '2020-08-27', 'Cash', '000000', '000006'),
                    ('000004', '2022-10-20', 'Credit', '000007', '000005'),
                    ('000005', '2021-12-17', 'Credit', '000003', '000007'),
                    ('000006', '2021-08-08', 'Credit', '000004', '000002'),
                    ('000007', '2019-11-30', 'Cash', '000003', '000000'),
                    ('000008', '2020-04-22', 'Cash', '000005', '000001'),
                    ('000009', '2022-05-19', 'Credit', '000005', '000007'),
                    ('000010', '2021-12-28', 'Cash', '000000', '000003'),
                    ('000011', '2019-03-13', 'Credit', '000007', '000005'),
                    ('000012', '2021-09-26', 'Credit', '000005', '000004'),
                    ('000013', '2018-02-09', 'Cash', '000000', '000002'),
                    ('000014', '2020-07-29', 'Cash', '000002', '000006'),
                    ('000015', '2018-06-25', 'Credit', '000004', '000001');
                    
INSERT INTO `PRODUCT_ORDER` (`ProductID`, `OrderID`, `Quantity`) VALUES
					('000007', '000000', 4),
					('000012', '000001', 5),
                    ('000010', '000002', 9),
                    ('000014', '000003', 7),
                    ('000002', '000004', 2),
                    ('000003', '000005', 12),
                    ('000000', '000006', 21), 
                    ('000008', '000007', 3), 
                    ('000009', '000008', 4), 
                    ('000013', '000009', 8), 
                    ('000011', '000010', 1), 
                    ('000010', '000011', 11),
                    ('000013', '000012', 2),
                    ('000011', '000013', 19), 
                    ('000012', '000014', 10),
					('000005', '000015', 12),
                    ('000012', '000000', 25),
                    ('000002', '000002', 5),
                    ('000010', '000004', 9),
                    ('000005', '000006', 7),
                    ('000004', '000008', 14),
                    ('000014', '000010', 9),
                    ('000009', '000012', 5),
                    ('000001', '000014', 17),
                    ('000001', '000001', 15),
                    ('000012', '000003', 20);

INSERT INTO `COUPON` (`ID`, `Code`, `ExpDate`) VALUES
					('000000', 'AES004', '2022-12-13'),
                    ('000001', 'T4XKK9', '2022-11-09'),
                    ('000002', 'P4S11E', '2023-02-04'),
                    ('000003', 'HK141P', '2023-03-30'),
                    ('000004', 'LN5O2F', '2022-07-15'),
                    ('000005', 'R4EXE7', '2022-06-06'),
                    ('000006', '7KLF8Q', '2022-08-22'),
                    ('000007', 'M00V7D', '2022-01-15'),
                    ('000008', 'Y0PXWL', '2023-05-29'),
                    ('000009', 'GR559B', '2022-12-17'),
                    ('000010', 'Z03XJK', '2022-11-23'),
                    ('000011', 'DT8H01', '2022-08-07'),
                    ('000012', 'OPO255', '2022-05-15'),
                    ('000013', '58JN12', '2022-09-14'),
                    ('000014', 'MRNH55', '2022-12-12'),
                    ('000015', 'HLO99Y', '2023-08-24');

INSERT INTO `BUYER_COUPON` (`CouponID`, `BuyerID`) VALUES
					('000000', '000001'),
                    ('000001', '000000'),
                    ('000002', '000006'),
                    ('000003', '000002'),
                    ('000004', '000007'),
                    ('000005', '000007'),
                    ('000006', '000003'),
                    ('000007', '000004'),
                    ('000008', '000005'),
                    ('000009', '000005'),
                    ('000010', '000001'),
                    ('000011', '000002'),
                    ('000012', '000007'),
                    ('000013', '000003'),
                    ('000014', '000005'),
                    ('000015', '000004');
                    
INSERT INTO `PRODUCT_COUPON` (`CouponID`, `ProductID`) VALUES
					('000000', '000001'),
                    ('000001', '000003'),
                    ('000015', '000009'),
                    ('000003', '000010'),
                    ('000004', '000015'),
                    ('000005', '000007'),
                    ('000006', '000003'),
                    ('000007', '000006'),
                    ('000008', '000010'),
                    ('000009', '000002'),
                    ('000011', '000011'),
                    ('000011', '000001'),
                    ('000007', '000000'),
                    ('000013', '000008'),
                    ('000014', '000006'),
                    ('000015', '000002');
                    
INSERT INTO `ORDER_COUPON` (`CouponID`, `OrderID`) VALUES
					('000000', '000001'),
                    ('000009', '000000'),
                    ('000015', '000009'),
                    ('000007', '000010'),
                    ('000011', '000015');

INSERT INTO `SHIPPER` (`ID`, `Name`, `Type`) VALUES
					('000000', 'Grab', 'Outsource'),
                    ('000001', 'Giao Hang Nhanh', 'Outsource'),
                    ('000002', 'Giao Hang Tiet Kiem', 'Outsource'),
                    ('000003', 'Tran Van B', 'Insource'),
                    ('000004', 'Nguyen Van A', 'Insource'),
                    ('000005', 'Truong Tuan C', 'Insource'),
                    ('000006', 'Ho Bao D', 'Insource'),
                    ('000007', 'Lalamove', 'Outsource');

INSERT INTO `VEHICLE` (`ID`, `Type`) VALUES
					('000000', 'Motorbike'),
                    ('000001', 'Small truck'),
                    ('000002', 'Large truck');

INSERT INTO `SHIPPER_VEHICLE` (`ShipperID`, `VehicleID`, `RangeInKM`, `FeePerRangeUnit`) VALUES
					('000000', '000000', 22, 16000),
                    ('000001', '000000', 22, 15000),
                    ('000002', '000000', 23, 15000),
                    ('000003', '000000', 18, 8000),
                    ('000004', '000000', 18, 8000),
                    ('000005', '000000', 18, 8000),
                    ('000006', '000000', 18, 8000),
                    ('000007', '000000', 24, 17000),
					('000000', '000001', 122, 14000),
                    ('000001', '000001', 122, 13000),
                    ('000002', '000001', 123, 13000),
                    ('000003', '000001', 118, 6000),
                    ('000004', '000001', 118, 6000),
                    ('000005', '000001', 118, 6000),
                    ('000006', '000001', 118, 6000),
                    ('000007', '000001', 124, 15000),
					('000000', '000002', 322, 12000),
                    ('000001', '000002', 322, 11000),
                    ('000002', '000002', 323, 11000),
                    ('000003', '000002', 318, 4000),
                    ('000004', '000002', 318, 4000),
                    ('000005', '000002', 318, 4000),
                    ('000006', '000002', 318, 4000),
                    ('000007', '000002', 324, 13000);

INSERT INTO `SHIPPER_ORDER` (`ShipperID`, `OrderID`, `Address`, `StartingDate`, `EstimatedArrivalDate`) VALUES
					('000002', '000000', '109 Tran Duy Hung, P.Trung Hoa, Q.Cau Giay, Ha Noi', '2022-01-24', '2022-01-31'),
					('000000', '000001', '65 Ham Nghi, P.Nguyen Thai Binh, Q.1, TPHCM', '2021-07-12', '2021-07-19'),
					('000007', '000002', '178 Le Thanh Nghi, P.Dong Tam, Q.Hai Ba Trung, Ha Noi', '2020-06-07', '2020-06-14'),
                    ('000006', '000003', '178 Le Thanh Nghi, P.Dong Tam, Q.Hai Ba Trung, Ha Noi', '2020-08-27', '2020-09-05'),
                    ('000005', '000004', '491 Tran Nguyen Han, P.Ho Nam, Q.Le Chan, Hai Phong', '2022-10-20', '2022-10-27'),
                    ('000002', '000005', '315 Vo Van Ngan, P.Linh Chieu, Q.Thu Duc, TP.HCM', '2022-12-17', '2022-12-24'),
                    ('000000', '000006', '1006 3 Thang 2, P.14, Q.10, TPHCM', '2021-08-08', '2021-08-15'),
                    ('000001', '000007', '65 Ham Nghi, P.Nguyen Thai Binh, Q.1, TPHCM', '2019-11-30', '2019-12-07'),
                    ('000007', '000008', '109 Tran Duy Hung, P.Trung Hoa, Q.Cau Giay, Ha Noi', '2020-04-22', '2020-04-29'),
                    ('000003', '000009', '315 Vo Van Ngan, P.Linh Chieu, Q.Thu Duc, TP.HCM', '2022-05-19', '2022-05-26'),
                    ('000003', '000010', '84 Nui Thanh, P.Hoa Cuong Bac, Q.Hai Chau, Da Nang', '2021-12-28', '2022-01-05'),
                    ('000004', '000011', '491 Tran Nguyen Han, P.Ho Nam, Q.Le Chan, Hai Phong', '2019-03-13', '2019-03-20'),
                    ('000005', '000012', '241 Dao Duy Tu, P.7, Q.10, TPHCM', '2021-09-26', '2021-10-02'),
                    ('000003', '000013', '1006 3 Thang 2, P.14, Q.10, TPHCM', '2018-02-09', '2018-02-16'),
                    ('000006', '000014', '178 Le Thanh Nghi, P.Dong Tam, Q.Hai Ba Trung, Ha Noi', '2020-07-29', '2020-08-07'),
                    ('000001', '000015', '109 Tran Duy Hung, P.Trung Hoa, Q.Cau Giay, Ha Noi', '2018-06-25', '2018-07-02');
                    
INSERT INTO `ROUTE` (`ShipperID`, `OrderID`, `Route`, `RangeInKM`) VALUES
					('000002', '000000', 'TPHCM -> Ha Noi', 1641),
					('000000', '000001', 'TPHCM', 13),
					('000007', '000002', 'TPHCM -> Ha Noi', 1641),
                    ('000006', '000003', 'TPHCM -> Ha Noi', 1641),
                    ('000005', '000004', 'TPHCM -> Hai Phong', 1780),
                    ('000002', '000005', 'Da Nang -> TPHCM', 958),
                    ('000000', '000006', 'TPHCM', 5),
                    ('000001', '000007', 'Da Nang -> TPHCM', 958),
                    ('000007', '000008', 'Hai Phong -> Ha Noi', 139),
                    ('000003', '000009', 'Hai Phong -> TPHCM', 1780),
                    ('000003', '000010', 'TPHCM -> Da Nang', 958),
                    ('000004', '000011', 'TPHCM -> Hai Phong', 1780),
                    ('000005', '000012', 'Hai Phong -> TPHCM', 1780),
                    ('000003', '000013', 'TPHCM', 9),
                    ('000006', '000014', 'TPHCM -> Ha Noi', 1641),
                    ('000001', '000015', 'TPHCM', 12);
                    
-- CALCULATE TOTAL COST OF EACH ORDER
CREATE TABLE TOTALCOST
	AS SELECT OrderID, USER.Name, sum(PRODUCT_ORDER.Quantity * Price) as TotalCost
		FROM PRODUCT_ORDER
			INNER JOIN PRODUCT ON ProductID = PRODUCT.ID
			INNER JOIN SHOP_ORDER ON OrderID = SHOP_ORDER.ID
			INNER JOIN USER ON BuyerID = USER.ID
				GROUP BY OrderID
					ORDER BY OrderID ASC;
ALTER TABLE TOTALCOST
	ADD PRIMARY KEY (OrderID);
UPDATE SHOP_ORDER 
	INNER JOIN TOTALCOST
		ON SHOP_ORDER.ID = TOTALCOST.OrderID
			SET SHOP_ORDER.TotalCost = TOTALCOST.TotalCost;
            
-- CALCULATE TOTAL MONEY SPENT BY EACH BUYER
CREATE TABLE TOTALMONEYSPENT
	AS SELECT USER.ID, USER.Name, sum(PRODUCT_ORDER.Quantity * Price) as TotalMoneySpent
		FROM PRODUCT_ORDER
			INNER JOIN PRODUCT ON ProductID = PRODUCT.ID
			INNER JOIN SHOP_ORDER ON OrderID = SHOP_ORDER.ID
			INNER JOIN USER ON BuyerID = USER.ID
				GROUP BY USER.Name
					ORDER BY USER.ID ASC;
ALTER TABLE TOTALMONEYSPENT
	ADD PRIMARY KEY (ID);
UPDATE BUYER 
	INNER JOIN TOTALMONEYSPENT
		ON BUYER.ID = TOTALMONEYSPENT.ID
			SET BUYER.TotalMoneySpent = TOTALMONEYSPENT.TotalMoneySpent;
            
-- CALCULATE TOTAL REVENUE EARNED BY EACH SELLER
CREATE TABLE TOTALREVENUE
	AS SELECT USER.ID, USER.Name, sum(PRODUCT_ORDER.Quantity * Price) as TotalRevenue
		FROM PRODUCT_ORDER
			INNER JOIN PRODUCT ON ProductID = PRODUCT.ID
			INNER JOIN SHOP_ORDER ON OrderID = SHOP_ORDER.ID
			INNER JOIN USER ON SHOP_ORDER.SellerID = USER.ID
				GROUP BY USER.Name
					ORDER BY USER.ID ASC;
ALTER TABLE TOTALREVENUE
	ADD PRIMARY KEY (ID);
UPDATE SELLER 
	INNER JOIN TOTALREVENUE
		ON SELLER.ID = TOTALREVENUE.ID
			SET SELLER.TotalRevenue = TOTALREVENUE.TotalRevenue;

-- CALCULATE TOTAL DISTANCE TRAVELED BY ORDER
CREATE TABLE TOTALDISTANCE
	AS SELECT OrderID, ROUTE.RangeInKM
		FROM SHOP_ORDER
			INNER JOIN ROUTE ON SHOP_ORDER.ID = OrderID
					ORDER BY SHOP_ORDER.ID ASC;
ALTER TABLE TOTALDISTANCE
	ADD PRIMARY KEY (OrderID);
UPDATE SHOP_ORDER 
	INNER JOIN TOTALDISTANCE
		ON SHOP_ORDER.ID = TOTALDISTANCE.OrderID
			SET SHOP_ORDER.TotalRange = TOTALDISTANCE.RangeInKM;

DELIMITER $	
CREATE PROCEDURE READTABLE(
	IN tablename varchar(200)
)
BEGIN
	IF tablename = 'USER' THEN SELECT * FROM USER;
    ELSEIF tablename = 'SELLER' THEN SELECT * FROM SELLER;
    ELSEIF tablename = 'PERSONAL_ACCOUNT' THEN SELECT * FROM PERSONAL_ACCOUNT;
    ELSEIF tablename = 'BUSINESS_ACCOUNT' THEN SELECT * FROM BUSINESS_ACCOUNT;
    ELSEIF tablename = 'BRAND_ACCOUNT' THEN SELECT * FROM BRAND_ACCOUNT;
    ELSEIF tablename = 'BUYER' THEN SELECT * FROM BUYER;
    ELSEIF tablename = 'FAVORITE_STORE' THEN SELECT * FROM FAVORITE_STORE;
    ELSEIF tablename = 'CREDIT' THEN SELECT * FROM CREDIT;
    ELSEIF tablename = 'PRODUCT' THEN SELECT * FROM PRODUCT;
    ELSEIF tablename = 'SHOP_ORDER' THEN SELECT * FROM SHOP_ORDER;
    ELSEIF tablename = 'PRODUCT_ORDER' THEN SELECT * FROM PRODUCT_ORDER;
    ELSEIF tablename = 'COUPON' THEN SELECT * FROM COUPON;
    ELSEIF tablename = 'BUYER_COUPON' THEN SELECT * FROM BUYER_COUPON;
    ELSEIF tablename = 'PRODUCT_COUPON' THEN SELECT * FROM PRODUCT_COUPON;
    ELSEIF tablename = 'ORDER_COUPON' THEN SELECT * FROM ORDER_COUPON;
    ELSEIF tablename = 'SHIPPER' THEN SELECT * FROM SHIPPER;
    ELSEIF tablename = 'VEHICLE' THEN SELECT * FROM VEHICLE;
    ELSEIF tablename = 'SHIPPER_VEHICLE' THEN SELECT * FROM SHIPPER_VEHICLE;
    ELSEIF tablename = 'SHIPPER_ORDER' THEN SELECT * FROM SHIPPER_ORDER;
    ELSEIF tablename = 'ROUTE' THEN SELECT * FROM ROUTE;
    END IF;
END $
DELIMITER ;

DELIMITER $	
CREATE PROCEDURE ADDVALUE (
	IN tablename varchar(200),
    IN att1 varchar(200),
    IN att2 varchar(200),
    IN att3 varchar(200),
    IN att4 varchar(200),
    IN att5 varchar(200),
    IN att6 varchar(200),
    IN att7 varchar(200)
)
BEGIN
	IF tablename = 'USER' THEN 
	INSERT INTO USER VALUES (att1, att2, att3, str_to_date(att4, '%Y-%m-%d'), att5, att6, att7);
    ELSEIF tablename = 'SELLER' THEN INSERT INTO SELLER VALUES (att1, att2, att3, att4, att5, att6);
    ELSEIF tablename = 'PERSONAL_ACCOUNT' THEN INSERT INTO PERSONAL_ACCOUNT VALUES (att1, att2);
    ELSEIF tablename = 'BUSINESS_ACCOUNT' THEN INSERT INTO BUSINESS_ACCOUNT VALUES (att1, att2);
    ELSEIF tablename = 'BRAND_ACCOUNT' THEN INSERT INTO BRAND_ACCOUNT VALUES (att1, att2, att3);
    ELSEIF tablename = 'BUYER' THEN INSERT INTO BUYER VALUES (att1, att2, att3);
    ELSEIF tablename = 'FAVORITE_STORE' THEN INSERT INTO FAVORITE_STORE VALUES (att1, att2);
    ELSEIF tablename = 'CREDIT' THEN INSERT INTO CREDIT VALUES (att1, att2, att3, att4, att5);
    ELSEIF tablename = 'PRODUCT' THEN INSERT INTO PRODUCT VALUES (att1, att2, att3, att4, att5, att6, att7);
    ELSEIF tablename = 'SHOP_ORDER' THEN INSERT INTO SHOP_ORDER VALUES (att1, att2, att3, att4, att5, att6, att7);
    ELSEIF tablename = 'PRODUCT_ORDER' THEN INSERT INTO PRODUCT_ORDER VALUES (att1, att2, att3);
    ELSEIF tablename = 'COUPON' THEN INSERT INTO COUPON VALUES (att1, att2, att3);
    ELSEIF tablename = 'BUYER_COUPON' THEN INSERT INTO BUYER_COUPON VALUES (att1, att2);
    ELSEIF tablename = 'PRODUCT_COUPON' THEN INSERT INTO PRODUCT_COUPON VALUES (att1, att2);
    ELSEIF tablename = 'ORDER_COUPON' THEN INSERT INTO ORDER_COUPON VALUES (att1, att2);
    ELSEIF tablename = 'SHIPPER' THEN INSERT INTO SHIPPER VALUES (att1, att2, att3);
    ELSEIF tablename = 'VEHICLE' THEN INSERT INTO VEHICLE VALUES (att1, att2);
    ELSEIF tablename = 'SHIPPER_VEHICLE' THEN INSERT INTO SHIPPER_VEHICLE VALUES (att1, att2, att3, att4);
    ELSEIF tablename = 'SHIPPER_ORDER' THEN INSERT INTO SHIPPER_ORDER VALUES (att1, att2, att3, att4, att5);
    ELSEIF tablename = 'ROUTE' THEN INSERT INTO ROUTE VALUES (att1, att2, att3, att4);
    END IF;
END $
DELIMITER ;

DELIMITER $	
CREATE PROCEDURE DELETEVALUE(
	IN tablename varchar(200),
    IN att1 varchar(200),
    IN att2 varchar(200),
    IN att3 varchar(200)
)
BEGIN
	IF tablename = 'USER' THEN DELETE FROM USER WHERE att1 = USER.ID;
    ELSEIF tablename = 'SELLER' THEN DELETE FROM SELLER WHERE att1 = SELLER.ID;
    ELSEIF tablename = 'PERSONAL_ACCOUNT' THEN DELETE FROM PERSONAL_ACCOUNT WHERE att1 = PERSONAL_ACCOUNT.ID;
    ELSEIF tablename = 'BUSINESS_ACCOUNT' THEN DELETE FROM BUSINESS_ACCOUNT WHERE att1 = BUSINESS_ACCOUNT.ID;
    ELSEIF tablename = 'BRAND_ACCOUNT' THEN DELETE FROM BRAND_ACCOUNT WHERE att1 = BRAND_ACCOUNT.ID;
    ELSEIF tablename = 'BUYER' THEN DELETE FROM BUYER WHERE att1 = BUYER.ID;
    ELSEIF tablename = 'FAVORITE_STORE' THEN DELETE FROM FAVORITE_STORE WHERE att1 = FAVORITE_STORE.BuyerID AND att2 = FAVORITE_STORE.StoreID;
    ELSEIF tablename = 'CREDIT' THEN DELETE FROM CREDIT WHERE att1 = CREDIT.ID;
    ELSEIF tablename = 'PRODUCT' THEN DELETE FROM PRODUCT WHERE att1 = PRODUCT.ID;
    ELSEIF tablename = 'SHOP_ORDER' THEN DELETE FROM SHOP_ORDER WHERE att1 = SHOP_ORDER.ID;
    ELSEIF tablename = 'PRODUCT_ORDER' THEN DELETE FROM PRODUCT_ORDER WHERE att1 = PRODUCT_ORDER.ProductID AND att2 = PRODUCT_ORDER.OrderID;
    ELSEIF tablename = 'COUPON' THEN DELETE FROM COUPON WHERE att1 = COUPON.ID;
    ELSEIF tablename = 'BUYER_COUPON' THEN DELETE FROM BUYER_COUPON WHERE att1 = BUYER_COUPON.CouponID AND att2 = BUYER_COUPON.BuyerID;
    ELSEIF tablename = 'PRODUCT_COUPON' THEN DELETE FROM PRODUCT_COUPON WHERE att1 = PRODUCT_COUPON.CouponID AND att2 = PRODUCT_COUPON.ProductID;
    ELSEIF tablename = 'ORDER_COUPON' THEN DELETE FROM ORDER_COUPON WHERE att1 = ORDER_COUPON.CouponID AND att2 = ORDER_COUPON.OrderID;
    ELSEIF tablename = 'SHIPPER' THEN DELETE FROM SHIPPER WHERE att1 = SHIPPER.ID;
    ELSEIF tablename = 'VEHICLE' THEN DELETE FROM VEHICLE WHERE att1 = VEHICLE.ID;
    ELSEIF tablename = 'SHIPPER_VEHICLE' THEN DELETE FROM SHIPPER_VEHICLE WHERE att1 = SHIPPER_VEHICLE.ShipperID AND att2 = SHIPPER_VEHICLE.VehicleID;
    ELSEIF tablename = 'SHIPPER_ORDER' THEN DELETE FROM SHIPPER_ORDER WHERE att1 = SHIPPER_ORDER.ShipperID AND att2 = SHIPPER_ORDER.OrderID;
    ELSEIF tablename = 'ROUTE' THEN DELETE FROM ROUTE WHERE att1 = ROUTE.ShipperID AND att2 = ROUTE.OrderID AND att3 = ROUTE.Route;
    END IF;
END $
DELIMITER ;

DELIMITER $	
CREATE PROCEDURE SEARCHVALUE(
	IN tablename varchar(200),
    IN att1 varchar(200),
    IN att2 varchar(200),
    IN att3 varchar(200)
)
BEGIN
	IF tablename = 'USER' THEN SELECT * FROM USER WHERE att1 = USER.ID;
    ELSEIF tablename = 'SELLER' THEN SELECT * FROM SELLER  WHERE att1 = SELLER.ID;
    ELSEIF tablename = 'PERSONAL_ACCOUNT' THEN SELECT * FROM PERSONAL_ACCOUNT WHERE att1 = PERSONAL_ACCOUNT.ID;
    ELSEIF tablename = 'BUSINESS_ACCOUNT' THEN SELECT * FROM BUSINESS_ACCOUNT  WHERE att1 = BUSINESS_ACCOUNT.ID;
    ELSEIF tablename = 'BRAND_ACCOUNT' THEN SELECT * FROM BRAND_ACCOUNT WHERE att1 = BRAND_ACCOUNT.ID;
    ELSEIF tablename = 'BUYER' THEN SELECT * FROM BUYER WHERE att1 = BUYER.ID;
    ELSEIF tablename = 'FAVORITE_STORE' THEN SELECT * FROM FAVORITE_STORE WHERE att1 = FAVORITE_STORE.BuyerID AND att2 = FAVORITE_STORE.StoreID;
    ELSEIF tablename = 'CREDIT' THEN SELECT * FROM CREDIT WHERE att1 = CREDIT.ID;
    ELSEIF tablename = 'PRODUCT' THEN SELECT * FROM PRODUCT WHERE att1 = PRODUCT.ID;
    ELSEIF tablename = 'SHOP_ORDER' THEN SELECT * FROM SHOP_ORDER  WHERE att1 = SHOP_ORDER.ID;
    ELSEIF tablename = 'PRODUCT_ORDER' THEN SELECT * FROM PRODUCT_ORDER WHERE att1 = PRODUCT_ORDER.ProductID AND att2 = PRODUCT_ORDER.OrderID;
    ELSEIF tablename = 'COUPON' THEN SELECT * FROM COUPON  WHERE att1 = COUPON.ID;
    ELSEIF tablename = 'BUYER_COUPON' THEN SELECT * FROM BUYER_COUPON WHERE att1 = BUYER_COUPON.CouponID AND att2 = BUYER_COUPON.BuyerID;
    ELSEIF tablename = 'PRODUCT_COUPON' THEN SELECT * FROM PRODUCT_COUPON WHERE att1 = PRODUCT_COUPON.CouponID AND att2 = PRODUCT_COUPON.ProductID;
    ELSEIF tablename = 'ORDER_COUPON' THEN SELECT * FROM ORDER_COUPON WHERE att1 = ORDER_COUPON.CouponID AND att2 = ORDER_COUPON.OrderID;
    ELSEIF tablename = 'SHIPPER' THEN SELECT * FROM SHIPPER WHERE att1 = SHIPPER.ID;
    ELSEIF tablename = 'VEHICLE' THEN SELECT * FROM VEHICLE WHERE att1 = VEHICLE.ID;
    ELSEIF tablename = 'SHIPPER_VEHICLE' THEN SELECT * FROM SHIPPER_VEHICLE WHERE att1 = SHIPPER_VEHICLE.ShipperID AND att2 = SHIPPER_VEHICLE.VehicleID;
    ELSEIF tablename = 'SHIPPER_ORDER' THEN SELECT * FROM SHIPPER_ORDER WHERE att1 = SHIPPER_ORDER.ShipperID AND att2 = SHIPPER_ORDER.OrderID;
    ELSEIF tablename = 'ROUTE' THEN SELECT * FROM ROUTE WHERE att1 = ROUTE.ShipperID AND att2 = ROUTE.OrderID AND att3 = ROUTE.Route;
    END IF;
END $
DELIMITER ;

DELIMITER $	
CREATE PROCEDURE UPDATEVALUE(
	IN tablename varchar(200),
    IN att1 varchar(200),
    IN att2 varchar(200),
    IN att3 varchar(200),
    IN att4 varchar(200),
    IN att5 varchar(200),
    IN att6 varchar(200),
    IN att7 varchar(200)
)
BEGIN
	IF tablename = 'USER' THEN UPDATE USER SET 
		USER.ID = att1, 
        USER.Name = att2, 
        USER.Sex = att3, 
        USER.Birthdate = att4, 
        USER.Phone = att5, 
        USER.Email = att6, 
        USER.Address = att7
			WHERE att1 = USER.ID;
    ELSEIF tablename = 'SELLER' THEN UPDATE SELLER SET
		SELLER.ID = att1, 
        SELLER.StoreName = att2, 
        SELLER.StoreAddress = att3, 
        SELLER.Logo = att4, 
        SELLER.NationalID = att5, 
        SELLER.TotalRevenue = att6
			 WHERE att1 = SELLER.ID;
    ELSEIF tablename = 'PERSONAL_ACCOUNT' THEN UPDATE PERSONAL_ACCOUNT SET
		PERSONAL_ACCOUNT.ID = att1, 
        PERSONAL_ACCOUNT.PersonalTaxNum = att2
			WHERE att1 = PERSONAL_ACCOUNT.ID;
    ELSEIF tablename = 'BUSINESS_ACCOUNT' THEN UPDATE BUSINESS_ACCOUNT SET
		BUSINESS_ACCOUNT.ID = att1, 
        BUSINESS_ACCOUNT.BusinessTaxNum = att2
			WHERE att1 = BUSINESS_ACCOUNT.ID;
    ELSEIF tablename = 'BRAND_ACCOUNT' THEN UPDATE BRAND_ACCOUNT SET
		BRAND_ACCOUNT.ID = att1, 
        BRAND_ACCOUNT.BusinessTaxNum = att2,
        BRAND_ACCOUNT.BrandAgreement = att3
			WHERE att1 = BRAND_ACCOUNT.ID;
    ELSEIF tablename = 'BUYER' THEN UPDATE BUYER SET
		BUYER.ID = att1, 
        BUYER.AccountType = att2,
        BUYER.TotalMoneySpent = att3
			WHERE att1 = BUYER.ID;
    ELSEIF tablename = 'FAVORITE_STORE' THEN UPDATE FAVORITE_STORE SET
		FAVORITE_STORE.BuyerID = att1, 
        FAVORITE_STORE.StoreID = att2
			 WHERE att1 = FAVORITE_STORE.BuyerID AND att2 = FAVORITE_STORE.StoreID;
    ELSEIF tablename = 'CREDIT' THEN UPDATE CREDIT SET
		CREDIT.ID = att1, 
        CREDIT.Number = att2, 
        CREDIT.Bank = att3, 
        CREDIT.ExpDate = att4, 
        CREDIT.UserID = att5
			WHERE att1 = CREDIT.ID;
    ELSEIF tablename = 'PRODUCT' THEN UPDATE PRODUCT SET
		PRODUCT.ID = att1, 
        PRODUCT.Name = att2, 
        PRODUCT.Brand = att3, 
        PRODUCT.Type = att4, 
        PRODUCT.Price = att5, 
        PRODUCT.Quantity = att6, 
        PRODUCT.SellerID = att7
			WHERE att1 = PRODUCT.ID;
    ELSEIF tablename = 'SHOP_ORDER' THEN UPDATE SHOP_ORDER SET
		SHOP_ORDER.ID = att1, 
        SHOP_ORDER.Date = str_to_date(att2, '%Y-%m-%d'), 
        SHOP_ORDER.PaymentMethod = att3, 
        SHOP_ORDER.SellerID = att4, 
        SHOP_ORDER.BuyerID = att5, 
        SHOP_ORDER.TotalCost = att6, 
        SHOP_ORDER.TotalRange = att7
			WHERE att1 = SHOP_ORDER.ID;
    ELSEIF tablename = 'PRODUCT_ORDER' THEN UPDATE PRODUCT_ORDER SET
		PRODUCT_ORDER.ProductID = att1, 
        PRODUCT_ORDER.OrderID = att2,
        PRODUCT_ORDER.Quantity = att3
			WHERE att1 = PRODUCT_ORDER.ProductID AND att2 = PRODUCT_ORDER.OrderID;
    ELSEIF tablename = 'COUPON' THEN UPDATE COUPON SET
		COUPON.ID = att1, 
        COUPON.Code = att2,
        COUPON.ExpDate = att3
			WHERE att1 = COUPON.ID;
    ELSEIF tablename = 'BUYER_COUPON' THEN UPDATE BUYER_COUPON SET
		BUYER_COUPON.CouponID = att1,
        BUYER_COUPON.BuyerID = att2
			WHERE att1 = BUYER_COUPON.CouponID AND att2 = BUYER_COUPON.BuyerID;
    ELSEIF tablename = 'PRODUCT_COUPON' THEN UPDATE PRODUCT_COUPON SET
		PRODUCT_COUPON.CouponID = att1,
        PRODUCT_COUPON.ProductID = att2
			 WHERE att1 = PRODUCT_COUPON.CouponID AND att2 = PRODUCT_COUPON.ProductID;
    ELSEIF tablename = 'ORDER_COUPON' THEN UPDATE ORDER_COUPON SET
		ORDER_COUPON.CouponID = att1,
        ORDER_COUPON.OrderID = att2
			WHERE att1 = ORDER_COUPON.CouponID AND att2 = ORDER_COUPON.OrderID;
    ELSEIF tablename = 'SHIPPER' THEN UPDATE SHIPPER SET
		SHIPPER.ID = att1,
        SHIPPER.Name = att2,
        SHIPPER.Type = att3
			WHERE att1 = SHIPPER.ID;
    ELSEIF tablename = 'VEHICLE' THEN UPDATE VEHICLE SET
		VEHICLE.ID = att1,
        VEHICLE.Type = att2
			WHERE att1 = VEHICLE.ID;
    ELSEIF tablename = 'SHIPPER_VEHICLE' THEN UPDATE SHIPPER_VEHICLE SET
		SHIPPER_VEHICLE.ShipperID = att1,
        SHIPPER_VEHICLE.VehicleID = att2,
		SHIPPER_VEHICLE.RangeInKM = att3,
        SHIPPER_VEHICLE.FeePerRangeUnit = att4
			 WHERE att1 = SHIPPER_VEHICLE.ShipperID AND att2 = SHIPPER_VEHICLE.VehicleID;
    ELSEIF tablename = 'SHIPPER_ORDER' THEN UPDATE SHIPPER_ORDER SET
		SHIPPER_ORDER.ShipperID = att1,
        SHIPPER_ORDER.OrderID = att2,
		SHIPPER_ORDER.Address = att3,
        SHIPPER_ORDER.StartingDate = att4,
        SHIPPER_ORDER.EstimatedArrivalDate = att5
			WHERE att1 = SHIPPER_ORDER.ShipperID AND att2 = SHIPPER_ORDER.OrderID;
    ELSEIF tablename = 'ROUTE' THEN UPDATE ROUTE SET
		ROUTE.ShipperID = att1,
        ROUTE.OrderID = att2,
		ROUTE.Route = att3,
        ROUTE.RangeInKM = att4
			WHERE att1 = ROUTE.ShipperID AND att2 = ROUTE.OrderID AND att3 = ROUTE.Route;
    END IF;
END $
DELIMITER ;