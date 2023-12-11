from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error

class FollowerResource(Resource):
  
    @jwt_required()
    def post(self,frind_id):
        user_id=get_jwt_identity()
        try :
            connection = get_connection()
            
            query ='''insert into frind
                        (followerId,followeeId)
                        values
                        (%s,%s);'''
            record = (user_id,frind_id)

            if user_id == frind_id:
                return{'error':'본인을 친구추가할수 없습니다'}
            
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {'error': str(e)},500
        
        return {'result':'success'} ,200
    
    @jwt_required()
    def delete(self,frind_id):
        user_id=get_jwt_identity()
        try :
            connection = get_connection()
            

            query ='''delete from frind
                        where followerId = %s and followeeId = %s;'''
            record = (user_id,frind_id)
            
            
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {'error': str(e)},500
    
        return {'result':'success'} ,200
    

class FollowerMemoResource(Resource):

    @jwt_required()
    def get(self):
        offset = request.args.get('offset')
        limit = request.args.get('limit')
        user_id=get_jwt_identity()

        try:
            connection = get_connection()
            query = '''select M.id as meomId, M.userId, M.title, M.date,
                        M.content, M.createdAt,M.updateAt, u.nickname
                        from Memo M
                        join frind f
                        on f.followeeId=M.userId
                        join user u
                        on u.id = M.userId
                        where f.followerId = %s and M.date > now()
                        order by M.date desc
                        limit '''+offset+''','''+limit+''';'''
            record = (user_id,)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            
            result_list = cursor.fetchall()
            print(result_list)

            i = 0
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
            return {'error': str(e)},500
         
        return{'result':'success',
                'items': result_list,
                'count':len(result_list)}