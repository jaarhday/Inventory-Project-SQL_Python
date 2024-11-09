PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Products(product_id integer primary key autoincrement, name text non null, quantity integer default 0, price real non null);
INSERT INTO Products VALUES(4,'Chocolate Chip Cookie',-76,2.41999999999999992);
INSERT INTO Products VALUES(5,'Peanut Butter Cookie',1,2.41999999999999992);
INSERT INTO Products VALUES(6,'Apple Cookie',1,2.41999999999999992);
INSERT INTO Products VALUES(7,'Raspberry Oatmeal Cookie',1,2.41999999999999992);
INSERT INTO Products VALUES(8,'Sugar Cookie',-9,2.41999999999999992);
INSERT INTO Products VALUES(9,'Snicker Doodle Cookie',1,2.41999999999999992);
INSERT INTO Products VALUES(10,'Texas Toast',-19,1.96999999999999997);
INSERT INTO Products VALUES(11,'Homestyle White',1,1.8700000000000001);
INSERT INTO Products VALUES(12,'Homestyle Wheat',1,1.8700000000000001);
INSERT INTO Products VALUES(13,'Mckenzie Farm Buttermilk',1,2.68000000000000016);
INSERT INTO Products VALUES(14,'San Juan',1,2.68000000000000016);
INSERT INTO Products VALUES(15,'Raspberry Donuts',-4,2.18999999999999994);
INSERT INTO Products VALUES(16,'Old Fashion Donuts',2,2.18999999999999994);
INSERT INTO Products VALUES(17,'Chocolate Donuts',1,2.18999999999999994);
INSERT INTO Products VALUES(18,'Blueberry Donuts',1,2.18999999999999994);
INSERT INTO Products VALUES(19,'Lemon Donuts',-11,2.18999999999999994);
INSERT INTO Products VALUES(20,'Apple Donuts',1,2.18999999999999994);
INSERT INTO Products VALUES(21,'Seasonal Donuts',1,2.18999999999999994);
INSERT INTO Products VALUES(22,'Svenhards Cinnamon',1,4.09999999999999964);
INSERT INTO Products VALUES(23,'Svenhards Breakfast Claw',1,4.09999999999999964);
INSERT INTO Products VALUES(24,'Svenhards Mixed Berry',1,4.09999999999999964);
INSERT INTO Products VALUES(25,'Svenhards 12 Pack',1,7.99000000000000021);
INSERT INTO Products VALUES(26,'Breadlovers Stoneground',-21,1.70999999999999996);
INSERT INTO Products VALUES(27,'Breadlovers Buttermilk',1,1.70999999999999996);
INSERT INTO Products VALUES(28,'Breadlovers Wheat',1,1.70999999999999996);
INSERT INTO Products VALUES(29,'Breadlovers White',-195,1.70999999999999996);
INSERT INTO Products VALUES(30,'Hamburger 12 Pack',1,2.5);
INSERT INTO Products VALUES(31,'Hotdog 12 Pack',1,2.5);
INSERT INTO Products VALUES(32,'Hotdog 8 Packs',1,2.2799999999999998);
INSERT INTO Products VALUES(33,'Hamburger 12 Pack',1,2.2799999999999998);
CREATE TABLE Orders (order_id integer primary key autoincrement, product_id integer, quantity integer, order_date timestamp default current_timestamp, foreign key (product_id) references Products(product_id));
INSERT INTO Orders VALUES(2,4,12,'2024-11-08 23:34:56');
INSERT INTO Orders VALUES(3,19,12,'2024-11-08 23:35:03');
INSERT INTO Orders VALUES(4,4,55,'2024-11-08 23:55:19');
INSERT INTO Orders VALUES(5,26,12,'2024-11-08 23:55:27');
INSERT INTO Orders VALUES(6,26,10,'2024-11-09 00:01:58');
INSERT INTO Orders VALUES(7,15,5,'2024-11-09 00:02:08');
INSERT INTO Orders VALUES(8,10,20,'2024-11-09 00:02:15');
INSERT INTO Orders VALUES(9,4,10,'2024-11-09 00:07:15');
INSERT INTO Orders VALUES(10,8,10,'2024-11-09 00:07:23');
INSERT INTO Orders VALUES(11,29,200,'2024-11-09 00:07:29');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('Products',33);
INSERT INTO sqlite_sequence VALUES('Orders',11);
COMMIT;
