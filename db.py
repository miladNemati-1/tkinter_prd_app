import mysql.connector

mydb = mysql.connector.connect(
  host="rdbms.strato.de",
  user="U4244994",
  password="PRDgroup2020"
)

print(mydb)
