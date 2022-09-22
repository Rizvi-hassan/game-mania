import sqlite3
import datetime

con = sqlite3.connect("game-mania.db")

cursor = con.cursor()

# data = [
#  (0, 'admin@cooldude', 'very_important', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 31, 52), datetime.datetime(2022, 9, 19, 22, 31, 52)),
#  (1, 'Rizvi', '7860', 0, 31, 17, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 20, 18, 28, 11)),
#  (2, 'A', '1', 0, 7, 5, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 27, 2)),
#  (3, 'Raunak', '1234', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)),
#  (4, 'hero', 'iamgreat', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)),
#  (5, 'Aryan Raj', '12345', 0, 48, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)),
#  (6, 'Abhinav', 'heroalom', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)), 
# (7, 'Shark', 'Tank', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)), 
# (8, 'Faltu', 'gamer', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)), 
# (9, 'Fukra Insan', '121@gmail.com', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)), 
# (10, 'Faarukh', 'Sheikh', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)), 
# (11, 'Alian', 'ufo', 0, 31, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)), 
# (12, 'coding_Ninja', 'ninjablade', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57))
# ]

# data = [
#  ( 'admin@cooldude', 'very_important', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 31, 52), datetime.datetime(2022, 9, 19, 22, 31, 52)),
#  ( 'Rizvi', '7860', 0, 31, 17, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 20, 18, 28, 11)),
#  ( 'A', '1', 0, 7, 5, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 27, 2)),
#  ( 'Raunak', '1234', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)),
#  ( 'hero', 'iamgreat', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)),
#  ( 'Aryan Raj', '12345', 0, 48, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)),
#  ( 'Abhinav', 'heroalom', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)), 
# ( 'Shark', 'Tank', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)), 
# ( 'Faltu', 'gamer', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)), 
# ( 'Fukra Insan', '121@gmail.com', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)), 
# ( 'Faarukh', 'Sheikh', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)), 
# ( 'Alian', 'ufo', 0, 31, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57)), 
# ( 'coding_Ninja', 'ninjablade', 0, 0, 0, datetime.datetime(2022, 9, 19, 22, 9, 7), datetime.datetime(2022, 9, 19, 22, 21, 57))
# ]

# cursor.executemany("INSERT INTO user(`username`, `password`, `snake-score`, `flappy-score`, `pong-history`, `doj`, `last_seen`) VALUES(?, ?, ?, ?, ?, ?, ?)", data)
# con.commit()
cursor.execute("update user set username = 'admin@121', password = 'secret_pass' where username = 'admin@cooldude'")
con.commit()

cursor.execute("select * from user")
res = cursor.fetchall()
for i in res:
    for j in i:
        print(j, end = "\t\t")
    print()

