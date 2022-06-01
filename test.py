import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root", 
    password = "", 
    database = "game-mania"
)
mycursor = mydb.cursor()

mycursor.execute("ALTER TABLE `user` ADD `pong-history` INT NOT NULL DEFAULT '0' AFTER `snake-score`")