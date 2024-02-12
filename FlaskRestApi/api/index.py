from flask_restful import Resource
from flask import make_response
import json


#자원(Resource)을 HTTP method에 맞게 처리하는 api(메소드)를 정의한 클래스
#1.Resource상속
class Index(Resource):

    def get(self):
        # flask_restful은 디폴트 응답헤더 Content-Type: application/json
        # flask는 디폴트 응답헤더 Content-Type: text/html
        # 1.직접 문자열 반환: Content-Type: application/json라 "<h2>Hello World</h2>"그대로 브라우저에 출력됨
        #return "<h2>HELLO WORLD</h2>"
        # 2.Response객체 반환:make_response("문자열")
        # ※make_response("문자열")로 반환시 응답헤더 Content-Type이 자동으로 text/html로 변경된다
        #return make_response("<h2>HELLO WORLD</h2>")
        # 3.딕셔너리객체 반환:Content-Type: application/json
        #return json.dumps({'server':'오픈 RESTFul API'},ensure_ascii=False)#자스의 JSON객체가 아닌 문자열로 처리된다
        #return {'server': '오픈 RESTFul API'} #JSON객체이다.한글 URL인코딩 처리
        #return make_response({'server': '오픈 RESTFul API'})#JSON객체이다.한글 URL인코딩 처리
        #return make_response(json.dumps({'server':'오픈 RESTFul API'},ensure_ascii=False))#JSON객체.한글 URL인코딩이 일어나지 않음
        '''
        RESTFul api는 주로 JSON형태로 데이타를 서비스 한다
        1. import json
        2. make_response(json.dumps(딕셔너리객체,ensure_ascii=False))호출해서 Response객체 반환
        '''
        return make_response(json.dumps([{'NAME': '가길동','AGE':20},{'NAME': '가길동','AGE':30},{'NAME': '다길동','AGE':25}], ensure_ascii=False))
