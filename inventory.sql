PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Products(product_id integer primary key autoincrement, name text non null, quantity integer default 0, price real non null);
INSERT INTO Products VALUES(1,'Breadlovers White',-11,2.2799999999999998);
CREATE TABLE Orders (order_id integer primary key autoincrement, product_id integer, quantity integer, order_date timestamp default current_timestamp, foreign key (product_id) references Products(product_id));
INSERT INTO Orders VALUES(1,1,12,'2024-11-08 23:06:29');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('Products',1);
INSERT INTO sqlite_sequence VALUES('Orders',1);
COMMIT;