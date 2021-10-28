BEGIN TRANSACTION;
CREATE TABLE client (person_id INTEGER PRIMARY KEY AUTOINCREMENT, fullname CHAR, address TEXT, zipcode TEXT, city TEXT, email TEXT, phone_number TEXT);
INSERT INTO "client" VALUES(1,'Lili Anderson','','','','habar@hotmail.com','');
INSERT INTO "client" VALUES(2,'Anne Banwarth','4444KJ','3111KA','Schiedam','no@ho.com','0677283982');
INSERT INTO "client" VALUES(5,'Osman','jagoed1','9878UY','Den haag','osman@gmail.com','+31-6-22222333');
INSERT INTO "client" VALUES(7,'Mark Suikerberg','hallo 13','3111OP','Amsterdam','sdfsd@mgasdgfsd.nl','+31-6-44444444');
INSERT INTO "client" VALUES(8,'Hannie amar','straaat 33','8888BD','Nijmegen','jan@hotmail.nl','+31-6-34444444');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('client',8);
CREATE TABLE users (username TEXT, password TEXT, firstname TEXT, lastname TEXT, admin INT, system_admin INT, advisor INT, joinDate TIMESTAMP);
INSERT INTO "users" VALUES('superadmin','Admin!23','admin','',1,0,0,'2021-10-25 18:09:12.091144');
INSERT INTO "users" VALUES('Appelstroop','P@ssw0rd100','appeltest','oog',1,0,0,'2021-10-26 13:15:15.925577');
INSERT INTO "users" VALUES('admin','P@ssw0rd100','ik ben admin','admin',1,0,0,'2021-10-26 15:00:30.561814');
INSERT INTO "users" VALUES('Advisor','Welkom@01','advisor','',1,0,0,'2021-10-26 15:12:18.406554');
INSERT INTO "users" VALUES('newadvisor','P@ssw0rd100','advisor','advisor',1,0,0,'2021-10-27 20:38:23.914642');
INSERT INTO "users" VALUES('Advisor','Welkom@01','','',1,0,0,'2021-10-27 20:46:05.508503');
INSERT INTO "users" VALUES('jezus','Welkom@01','hoi','isawesome',0,0,1,'2021-10-27 21:27:07.550793');
INSERT INTO "users" VALUES('waarom','Welkom@01','dddd','dddd',0,1,0,'2021-10-27 21:30:29.175600');
COMMIT;