AWS_RDS_DB_USERNAME = admin
AWS_RDS_DB_PW = fEFd8dnv62fPUWB
AWS_RDS_DB_PORT = 3306
AWS_RDS_DB_ENDPOINT = us-mines-map-user-database.cks4a7kjmicd.us-west-1.rds.amazonaws.com

To connect from mysql terminal, type:

mysql -h us-mines-map-user-database.cks4a7kjmicd.us-west-1.rds.amazonaws.com -P 3306 -u admin -p

(Then type in the password when prompted)
The user has admin status so you can do whatever in there (create, insert, update, delete, etc.)
