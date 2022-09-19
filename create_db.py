import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root", 
    password = "", 
)
mycursor = mydb.cursor()

#creating the database
mycursor.execute("CREATE DATABASE `game-mania`")
mycursor.execute("use `game-mania`")

#creating table
mycursor.execute("CREATE TABLE user (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(225) NOT NULL , password VARCHAR(225) NOT NULL ) ")

# adding the column of snake-score
mycursor.execute("ALTER TABLE `user` ADD `snake-score` INT NOT NULL DEFAULT '0' ")

# adding the column of pong 
mycursor.execute("ALTER TABLE `user` ADD `pong-history` VARCHAR(11) NULL DEFAULT 'none' ")

#adding the column of flappy
mycursor.execute("ALTER TABLE `user` ADD `flappy-score` INT NULL DEFAULT '0' AFTER `pong-history`")

mycursor.execute("SHOW TABLES")

for x in mycursor:
    print(x)