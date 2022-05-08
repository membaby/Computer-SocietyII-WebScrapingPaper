import mysql.connector as msql
from mysql.connector import Error
import json
import os
from scrapy.utils.project import get_project_settings

###############################################################
# Example of CONNECTION variable to be created in settings.py #
###############################################################
# CONNECTION = {                                              #
#     'host': 'localhost',                                    #
#     'user': 'root',                                         #
#     'password': 'password',                                 #
#     'database': 'databaseName',                             #
#     'port': '3306'                                          #
# }                                                           #
###############################################################

class MySQLpipeline:
    def __init__(self):
        settings = get_project_settings()
        self.CONNECTION = settings.get('CONNECTION') # Read connection variable from settings.py file

        self.create_connection()
        self.create_table()

    def create_connection(self):
        try:
            self.conn = msql.connect(host=self.CONNECTION['host'], user=self.CONNECTION['user'], password=self.CONNECTION['password'])
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.CONNECTION['database']}")
                self.cursor.execute(f"USE {self.CONNECTION['database']}")
        except Error as e:
            print("Error while connecting to MySQL", e)

    def create_table(self):
        self.conn = msql.connect(host=self.CONNECTION['host'], user=self.CONNECTION['user'], password=self.CONNECTION['password'],database=self.CONNECTION['database'])
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `projects`
            (
                project_id INT PRIMARY KEY,
                project_url TEXT,
                name TEXT,
                year INT,
                short_description TEXT,
                minplayers INT,
            );
        ''')

    def store_db(self, item):
        try:
            elif item['DATA'] == 'project':
                self.cursor.execute(f"""INSERT IGNORE INTO `projects` VALUES (
                    {item['project_id']},
                    '{item['project_url']}',
                    '{item['name']}',
                    {item['year']},
                    '{item['short_description']}',
                    {item['minplayers']}
                    )
                """)        
        except Exception as err:
            print(err)
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item