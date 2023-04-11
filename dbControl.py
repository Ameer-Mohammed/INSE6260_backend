import csv
import pymysql

# Connect to the database
db = pymysql.connect(host='localhost', user='root', password='asdfgh', db='userdb')

# Open the CSV file
with open('ratings.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    unique_userIDs = set()
    for row in reader:
        # Extract the value from the 'userID' column and add it to the set of unique userIDs
        unique_userIDs.add(int(row['userID']))

    # Insert the unique userIDs into the MySQL database
    cursor = db.cursor()
    for userID in unique_userIDs:
        query = f"INSERT IGNORE INTO user (username, password) VALUES ('{userID}','{userID}')"
        cursor.execute(query)
    db.commit()

# Close the database connection
db.close()
