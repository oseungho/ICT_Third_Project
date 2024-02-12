#https://flask.palletsprojects.com/en/3.0.x/deploying/asgi/
#pip install hypercorn #파이썬 기반 ASGI서버
#pip install asgiref #플라스크 앱을 Wsgi로 변환용
#pip install uvicorn #파이썬 기반 ASGI서버
'''
아래는 둘다 파이썬 웹 어플리케이션(Flask App)과 웹 서버 간의 공통적인 인터페이스를 정의한 프로토콜이다
CGI(Common Geteway Interface)방식은 요청 수만큼 서버에 프로세스가 실행되지만
아래 두 프로토콜은 하나만 실행된다.
WSGI(Web Server Gateway Interface): 동기 요청 처리 방식
ASGI(Asynchronus Server Gateway Interface): 비동기 요청 처리 방식
여러 요청시에는 ASGI가 성능이 우수하다.
'''
from app2 import app #플라스크 어플리케이션
from asgiref.wsgi import WsgiToAsgi
import uvicorn
import hypercorn

asgi_app = WsgiToAsgi(app) #플라스크 앱을 ASGI와 호환되는 WSGI 앱으로 변환

if __name__ == '__main__':
    uvicorn.run(asgi_app,host='0.0.0.0',port=8989)

#명령어로 실행시
#
#hypercorn main:asgi_app