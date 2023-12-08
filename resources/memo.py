import datetime
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error


class MemoReigsterResource(Resource):

    @jwt_required()
    def post(self):

        data =request.get_json()

        user_id=get_jwt_identity()
        # date=datetime.datetime.strptime(data['date'],'%Y-%m-%d %H:%M:%S')
        try:
            connection = get_connection()
            query ='''insert into Memo
                        (userId,title,content,date)
                        values
                        (%s,%s,%s,%s);'''
            record = (user_id,data['title'],data['content'],data['date'])

            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()
            
            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)},500
        return{'result':'success'},200
    
    @jwt_required()
    def get(self):
        user_id=get_jwt_identity()
        try :
            connection = get_connection()
            query = '''select*
                        from Memo
                        where userId=%s;'''
            record =(user_id,)

            cursor = connection.cursor(dictionary= True)
            cursor.execute(query,record)

            result_list = cursor.fetchall()
            print(result_list)

            i =0
            for row in result_list:
                result_list[i]['date']=row['date'].isoformat()
                result_list[i]['createdAt']=row['createdAt'].isoformat()
                result_list[i]['updateAt']=row['updateAt'].isoformat()
                i = i + 1
            
            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)},500
        return{'result':'success',
               'items':result_list,
               'count':len(result_list)},200

    
class MemoResource(Resource):

    @jwt_required()
    def put(self,Memo_id):

        data = request.get_json()
        user_id=get_jwt_identity()

        try:
            connection = get_connection()
            query = '''update Memo
                        set title=%s,
                            content = %s
                        where id=%s and userId=%s;'''
            record =(data['title'],data['content'],Memo_id,user_id)

            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()

            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)},500
        return{'result':'success'},200
    
    @jwt_required()
    def delete(self,Memo_id):
        
        user_id=get_jwt_identity()
        try:
            connection = get_connection()
            query = '''delete from Memo
                        where id = %s and userId = %s;'''
            record = (Memo_id,user_id)

            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()

            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {'error':str(e)},500
        
        return {'result':'success'},200