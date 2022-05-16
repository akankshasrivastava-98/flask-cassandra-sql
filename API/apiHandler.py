from flask_restplus import Namespace, Resource
from flask_restplus.marshalling import request

from dbhelper.SQLManager import MySQLManager
from dbhelper.CassHandler import CassandraManager

api = Namespace('demo1', description='Cassandra SQL demo')


@api.route('/GetDetatils')
class Getdata(Resource):
    def get(self):
        try:
            info_list = request.get_json(force=True)
            sqlmang = MySQLManager()
            data1 = sqlmang.get_from_sqlDB()  
            cassdata = CassandraManager()
            data2 = cassdata.get_user_details()
            data = {'data1' : data1,
                    'data2' : data2[0][0]
            }
            return data
        except Exception as e:
            return str(e), 500


