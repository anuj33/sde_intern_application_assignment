
import pymysql.cursors
import pymysql

class Dao:
    def __init__(self, config):
        self.db_handle = pymysql.connect(host=config.db_cred.get("host"), user=config.db_cred.get("username"), passwd=config.db_cred.get("password"), db=config.db_cred.get("db_name"),
                             cursorclass=pymysql.cursors.DictCursor)


    def persist_medical_metadata(self, medical_condition, metadata):
        try:
            with self.db_handle.cursor() as cursor:
                sql = "INSERT INTO `medical_data` (`medical_condition`, `metadata`) VALUES ('{}', '{}')".format(medical_condition, metadata)
                cursor.execute(sql)
            self.db_handle.commit()
        finally:
            pass


    def fetch_metadata_by_medical_condition(self, medical_condition):
        try:
            with self.db_handle.cursor() as cursor:
                sql_query = "select metadata from `medical_data` where medical_condition = '{}'".format(medical_condition)
                cursor.execute(sql_query)
                return cursor.fetchone()
        finally:
            pass




