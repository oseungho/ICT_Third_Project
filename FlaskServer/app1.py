from flask import Flask #Flask 앱 생성용
from flask import request #url에 따른 요청 객체

#하나의 웹 어플리케이션 생성
app = Flask(__name__)#app는 WSGI어플리케이션(WSGI(Web Server Gateway Interface)를 따르는 웹 어플리케이션)
#@app.route('/로 시작하는 url') 데코레이터로 url요청과 요청을 처리할 함수 매핑 : 라우팅한다
#라우팅 함수(view function)는 반드시 리턴해야 한다 즉 응답을 해야한다
#TypeError: The view function for '함수명' did not return a valid response

#1.GET방식(디폴트)요청
@app.route('/')
def hello_world():
    print('HELLO WORLD')
    # 브라우저로 전송되는 문자열(응답바디에 쓰이는 문자열)
    # 문자열 전송시 응답헤더 Content-Type 디폴트는 text/html; charset=utf-8
    return '<h2>Hello World!!!</h2>'

#2. 데이타 받기:GET - URL
@app.route('/query',methods=['GET'])#반드시 [] 리스트로 설정
def query():
    # 쿼리 스트링 받기(GET요청:KEY=VALUE):request.args.get('파라미터명')
    print('request.args:',request.args)
    print('list(request.args):', list(request.args))
    name = request.args.get('name')
    username = request.args.get('username')
    password = request.args.get('password')

    return f'''
        <ul>
            <li>이름 : {name}</li>
            <li>아이디 : {username}</li>
            <li>비밀번호 : {password}</li>
        </ul>
    '''
#3. 데이타 받기:POST - 요청바디
@app.route('/post',methods=['POST'])
def post():
    #요청바디 받기(POST요청:KEY=VALUE):request.form['파라미터명']
    print('request.form:', request.form)
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']

    return f'''
            <ul>
                <li>이름 : {name}</li>
                <li>아이디 : {username}</li>
                <li>비밀번호 : {password}</li>
            </ul>
        '''
#4.GET방식 및 POST요청 모두 받기(파라미터 포함)
@app.route('/both',methods=['POST','GET'])
def both():
    print('요청방식:',request.method)
    print('request.values:',request.values)
    # request.values.get('파라미터명')
    name = request.values.get('name')
    username = request.values.get('username')
    password = request.values.get('password')
    method=None
    if request.method =='GET':
        method='<h1>GET방식 요청입니다</h1>'
    else:
        method = '<h1>POST방식 요청입니다</h1>'
    return f'''
                {method}
                <ul>
                    <li>이름 : {name}</li>
                    <li>아이디 : {username}</li>
                    <li>비밀번호 : {password}</li>
                </ul>
            '''
#5.데이타 받기 - URL 파라미터(혹은 패스 파라미터)
@app.route('/path/<name>')
def path(name):
    return f'<h2>URL 파라미터 : {name}</h2>'

if __name__ == '__main__':
    #app.run()#Debug mode: off
    '''
    디폴트 포트 5000
    debug=False이 디폴트 .debug=True 서버는 코드 변경을 감지하고 자동으로 리로드
    #host='0.0.0.0' 원격의 모든 호스트에서 접속 가능하도록 설정시
    (디폴트는 127.0.0.1으로  로컬에서만 접속 가능한 테스트서버가 된다). 
    '''
    # Flask의 테스트 서버(프레임워크에 내장된)에서 실행(배포용은 비권장)
    app.run(debug=True,host='0.0.0.0',port=8282)#Debug mode: on