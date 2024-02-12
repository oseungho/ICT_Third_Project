from flask import make_response,request
from flask_restful import Resource,reqparse
#더미 데이타(TODOS)및 공통으로 사용할 함수(abort_if_todo_dosent_exist)가 있는 items모듈 import
from api.items import TODOS
import json

class Todo(Resource):
    # 1.모든 todo조회
    def get(self):
        return make_response(json.dumps(TODOS,ensure_ascii=False))
    # 2.입력
    def post(self):

        # STEP1. RequestParser객체 생성
        parser = reqparse.RequestParser()
        # STEP2. RequestParser객체에 add_argument('파라미터명')로 모든 파라미터명 추가
        # https://flask-restful.readthedocs.io/en/latest/reqparse.html?highlight=add_argument#argument-locations
        # RequestParser는 기본적으로 JSON값을 분석한다 이를 변경하려면 location키워드를 사용한다
        if request.is_json:#데이타를 클라이언트가 json으로 보낼때
            parser.add_argument('task')
            parser.add_argument('when')
        else:#데이타가 key=value형식일때 예를들면 form태그로 데이타 전송시
            parser.add_argument('task',location='form')
            parser.add_argument('when', location='form')
        # STEP3 모든 파라미터 받기:parse_args()호출
        args = parser.parse_args()
        print(f'args:{args},type;{type(args)}')#args:{'task': '놀이공원 가기', 'when': '내일'},type;<class 'flask_restful.reqparse.Namespace'>
        next_max_id = 'todo'+str(max(map(int,map(lambda s:s[4:],TODOS.keys())))+1)
        print(f'next_max_id:{next_max_id},type:{type(next_max_id)}')
        TODOS[next_max_id]=args
        return make_response(json.dumps(TODOS,ensure_ascii=False))