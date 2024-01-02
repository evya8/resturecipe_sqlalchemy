import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234"
)
mycursor = mydb.cursor()
def create_table():
    sql = """CREATE TABLE `garage`.`cars` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `model` INT NULL,
    `brand` VARCHAR(25) NULL,
    `color` VARCHAR(10) NULL,
    PRIMARY KEY (`id`));
    """
    mycursor.execute(sql)

# create_table()
def add_row():
    sql = """INSERT INTO `garage`.`cars` (`model`, `brand`,`color`)  VALUES  (-1,"kia","red");"""
    mycursor.execute(sql)
    mydb.commit()

add_row()
add_row()
add_row()

def get_data():
    sql= """SELECT `cars`.`id`,
        `cars`.`model`,
        `cars`.`brand`,
        `cars`.`color`
    FROM `garage`.`cars`
    where color ='red';"""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)
get_data()
print(mydb)