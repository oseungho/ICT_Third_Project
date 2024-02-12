from flask import make_response,request
from flask_restful import Resource,reqparse
from api.items import TODOS,abort_if_todo_dosent_exist
import json

'''
    클래스의 각 HTTP 메소드(get/post/put/delete등)에서 파라미터를 받는 방법
    방법1]
    1. __init__()에서
      RequestParser객체 생성
      RequestParser객체.add_argument('파라미터명1')
      RequestParser객체.add_argument('파라미터명2')
      ..
      로 모든 파라미터 추가
    2.파라미터를 받는 HTTP 메소드인 get/post/delete/put()에서는
      RequestParser객체.parse_args() 호출하여  등록된 모든 파라미터를 받는다

    방법2]
     1. __init__()에서
      RequestParser객체 생성
      공통으로 받은 파라미터만 추가
      RequestParser객체.add_argument('공통파라미터명1')
      RequestParser객체.add_argument('공통파라미터명2')
      ..

    2.파라미터를 받는 get/post/delete/put()메소드에서는
      해당 메소드별로 추가적으로 필요한 파라미터 추가
      RequestParser객체.add_argument('파라미터명3')

      RequestParser객체.parse_args() 호출하여 받는다
    방법3]
      파라미터를 받는 get/post/delete/put()메소드에서
      RequestParser객체 생성
      RequestParser객체.add_argument('파라미터명1')
      RequestParser객체.add_argument('파라미터명2')
      RequestParser객체.parse_args() 호출하여 받는다
'''
#자원을 HTTP method에 맞게 처리하는 api(메소드)를 정의한 클래스
#[1.Resource상속]
class Todos(Resource):
    # 파라미터 받는 방법1일때 혹은 2일때
    def __init__(self):
        # 생성자에서 파라미터 받기위한 파라미터 등록(입력시나 수정시)
        # STEP1. RequestParser객체 생성
        self.parser= reqparse.RequestParser()
        # STEP2. RequestParser객체에 add_argument('파라미터명')로 모든 파라미터 혹은 공통 파라미터 추가
        #self.parser.add_argument('task')#요청시 파라미터로 전달되는 파라미터명을 인자로 추가
    # [2.HTTP 메소드(post,get,put,delete)별로 오버라이딩]
    # 1.키값(todo_id)에 따른 데이타 조회용 api
    # get(self,키)의 키(todo_id)와 app.py의 add_resource(클래스명,'/todos/<변수명>')의 <변수명>이 일치해야 한다
    def get(self,todo_id):
        # 없는 키(todo_id)로 조회시 KeyError: 'todo4'
        #return make_response(json.dumps(TODOS[todo_id],ensure_ascii=False))
        abort_if_todo_dosent_exist(todo_id)
        return make_response(json.dumps(TODOS[todo_id], ensure_ascii=False))
    # 2. 키값(todo_id)에 따른 데이타 삭제 api
    # PUT이나 DELETE로 요청시 클라이언트에서 포스트맨으로 파라미터 전달시에는
    # 요청의 Body탭 -> raw - > JSON 선택후 {"파라미터명1":"값1","파라미터명2","값2",.....}
    # https://flask-restful.readthedocs.io/en/latest/reqparse.html?highlight=add_argument#argument-locations
    # RequestParser는 기본적으로 JSON값을 분석한다 이를 변경하려면 location키워드를 사용한다
    def delete(self,todo_id):
        abort_if_todo_dosent_exist(todo_id)
        deleted_obj = TODOS.get(todo_id)
        del TODOS[todo_id]
        #삭제된 데이타 반환
        return make_response(json.dumps(deleted_obj, ensure_ascii=False))
        #삭제후 전체 데이타
        #return make_response(json.dumps(TODOS, ensure_ascii=False))
    # 3. 키값(todo_id)에 따른 데이타 수정 api-'task'라는 파라미터명으로 할 일 내용 받는다
    def put(self,todo_id):
        abort_if_todo_dosent_exist(todo_id)
        '''
        # [데이타를 JSON으로 받을때(RequestParser는 기본적으로 JSON값을 분석)]
        # 추가로 when키 받기
        self.parser.add_argument('when')
        args= self.parser.parse_args()#args는 딕셔너리 형태 {'task':'할일','when':'언제'}
        print(f'수정 데이타 args:{args}')
        # 받은 데이타로 수정        
        TODOS[todo_id]=args
        return make_response(json.dumps(TODOS,ensure_ascii=False))
        '''
        # [데이타를 key=value으로 받을때(RequestParser는 기본적으로 JSON값을 분석)]
        # 생성자의 self.parser.add_argument('task') 반드시 주석처리(미 주석시 415에러)
        self.parser.add_argument('task',location='form')
        self.parser.add_argument('when', location='form')
        args = self.parser.parse_args()
        # 받은 데이타로 수정
        TODOS[todo_id] = args
        return make_response(json.dumps(TODOS, ensure_ascii=False))