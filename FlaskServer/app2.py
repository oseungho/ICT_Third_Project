from flask import Flask #Flask 앱 생성용
from flask import request #url에 따른 요청 객체(Request)
from flask import render_template##템플릿 파일(.html) 서비스용
from flask import make_response#응답 객체(Response) 생성용
from flask import jsonify#JSON형태의 문자열로 응답시
from flask import flash,redirect,url_for#응답메시지 및 리다이렉트용
#https://flask-cors.readthedocs.io/en/latest/
#https://flask-cors.readthedocs.io/en/latest/index.html?highlight=CORS#resource-specific-cors
#pip install flask-cors
from flask_cors import CORS#CORS에러 해결
import os

#app=Flask(__name__,template_folder='webapp')#템플릿 파일의  기본 폴더 위치명 변경시
app=Flask(__name__)
CORS(app)
'''
아래는 위와 같다(모든 자원에 대해서 모든 사용자(도메인)한테 허용)
CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})
특정 URL패턴의 자원에 대해서만 모든 사용자에게 허용시는
CORS(app, resource={
    r"/api/*":{
        "origins":"*"
    }
})

모든 패턴의 자원에 대해서 특정 사용자(도메인)에게 허용시는
CORS(app, resource={
    r"/*":{
        "origins":[“http://localhost:9090”, “https://example.com”]
    }
})

'''
#플라스크 웹 어플리케이션 설정
#1)JSON응답시 한글이 깨지는 경우(디폴트가 ascii 인코딩)
app.config['JSON_AS_ASCII']=False
#2)업로드 파일 용량 설정
app.config['MAX_CONTENT_LENGTH']=1 * 1024 * 1024 #1MB
#메시지 Flash를 사용하기 위해서는 반드시 아래 secret_key설정
app.secret_key='$%&^*@##$'
'''
[템플릿 파일 사용하기]
Flask 템플릿 파일은 .html을 사용하고 템플릿 엔진은 jinja2
.html파일을 기본적으로 app.py가 실행되는 같은 위치에 templates폴더에서 찾는다
단,app = Flask(__name__,template_folder='임의의 폴더명')코드로 templates 폴더명 변경 가능
템플릿 파일인 .html파일을 templates 폴더에 저장
'''

#HTML FORM요소로 요청 보내고 받기

#[1.str타입 즉 문자열로 응답하기]
@app.route("/")# 시작페이지으로 이동
def index():
    # 렌더링된 HTML소소 문자열 반환(문자열로 응답)
    # 디폴트로 index.html파일을 templates폴더에서 찾는다
    return render_template('index.html',title='메인 화면')
@app.route("/form")# 로그인 폼으로 이동
def form():
    title=request.args.get('title')
    return render_template('views/form.html',title=title)

@app.route("/formul",methods=['POST'])# 로그인처리
def form_ul():
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
@app.route("/formtemplate",methods=['POST'])# 로그인처리
def form_template():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']

    return render_template('views/form.html',**{'name':name,'username':username,'password':password,'title':'로그인'})

#[2.Response객체로 응답하기]
@app.route('/response')
def response():
    # 브라우저로 응답하는 방법
    # 방법1. 문자열로 응답 - 응답헤더 설정 불가(Content-Type은 디폴트 text/html;charset=UTF-8)
    # render_template('html파일명')함수(즉 렌더링된 HTML소스 문자열 반환) 혹은 직접 문자열 반환
    # 방법2. Response객체로 응답
    # 응답헤더 설정 가능 즉 응답헤더를 설정해야할때 사용(JSON으로 응답시(내부적으로 utf8을 사용))
    response = make_response(render_template('index.html'))
    print(f'response:{response}\ndir(response):{dir(response)}')
    print('응답헤더 설정 전:',response.content_type)#'text/html; charset=utf-8'
    # 응답헤더 설정
    # response.headers['헤더명'] = '헤더값'
    # response.헤더명='헤더값'
    #response.content_type='text/plain; charset=utf-8'
    response.headers['content-type']='text/html; charset=utf-8'#디폴트 값
    return response

#[3.정적 자원(이미지,.css,.js등) 사용하기]
@app.route('/static')
def static_resource():
    title = request.args.get('title')
    return render_template('views/static.html',**{'title':title})

@app.route('/ajax')
def ajax_form():#ajax요청 폼으로 이동
    title = request.args.get('title')
    return render_template('views/ajax.html', **{'title': title})

@app.route('/ajax',methods=['POST'])
def ajax():
    '''
    JSON형태의 데이타를 받을때: request.get_json()는 JSON형태의 문자열을 파이썬 객체(딕셔너리)로 변환
    JSON형태의 문자열로 응답시: flask모듈의 jsonify(딕션너리 객체)해서 Response객체로 반환
    request.is_json : JSON형태의 문자열인지 판단
    request.content_type : 컨텐츠의 타입
    '''
    print('JSON형태의 문자열인지 판단:',request.is_json)
    print('요청 컨텐츠 타입:',request.content_type)
    json_data=None
    if request.is_json:#JSON형식인 경우
        json_data = request.get_json()
        print('사용자로부터 받은 데이타:',json_data)
        print('사용자로부터 받은 데이타 타입:', type(json_data))
    if json_data:
        json_data['loc']='서초동'
        #return jsonify(json_data)#JSON형식으로 반환
        return json_data

    else:#JSON형식의 문자열을 만들어서 반환
        return jsonify({'institute':'한국ICT 인재 개발원','loc':'강남'})

#[4. jinja2 템플릿엔진 사용하기]
#https://jinja.palletsprojects.com/en/3.0.x/templates/
'''
템플릿 파일인 .html에서 파이썬 코드 사용하기
{{변수 혹은 함수(단,반환값이 있는 함수)}} 는 출력문(EL)과 같다 즉 ${JSTL변수} 혹은 <%= %>) 
{% 파이썬 코드 %} (스크립팅요소인 <% 자바코드 %>와 같다)
{#   주석   #}  (<%-- --%>와 같다)
for문이나 if문은 반드시 블락을 닫아야 한다
{% for i in range(10) %}

{% endfor %}
{% if True %}

{% endif %} 식으로
'''
@app.route('/jinja2')
def jinja2():
    title=request.args.get('title')
    year = request.args.get('year')
    #render_template('템플릿파일명',키워드인수=값,....) 즉 키워드 인수를 html페이지에서 변수로 사용
    return render_template('views/jinja2.html',title=title,year=year)

#[5. 파일 업로드]
#https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
@app.route('/uploadform')#업로드 폼으로 이동
def uploadform():
    title = request.args.get('title')
    return render_template('views/upload.html',title=title)

#업로드 파일 경로 설정
UPLOAD_FOLDER = os.path.join(os.getcwd(),'upload')
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
#업로드할 파일의 허용가능한 확장자
ALLOWED_EXTENSIONS =set(['txt','png','jpg','gif','bmp'])
def allowed_file(filename):#업로드가 가능한 파일인지 체크하는 함수
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/fileupload',methods=['POST'])#업로드 처리
def upload_ok():

    try:
        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        """
        # 파일하나 업로드: request.files['파라미터명'] 으로 파일을 받는다
        file = request.files['upload']#<input type="file" name="upload"/>
        title = request.form['title']
        print('Upload file:',file)#FileStorage타입
        print('FileStorage타입의 filename속성:', file.filename)
        print('이름공간:',dir(file))
        if len(file.filename)==0:#파일을 업로드 안한 경우
            '''
            메시지 플래싱은 사용자에게 한 번만 보여줄 메시지를 저장하고 다음 요청에서 표시하는 기능
            주로 사용자에게 알림, 성공 또는 오류 메시지를 표시할 때 유용
            리다이렉트 되는 혹은 렌더링 되는 템플릿 파일에서는 get_flashed_messages() 함수를 사용하여 플래싱된 메시지를 가져와 뿌려준다 
            이 함수는 플래싱된 메시지를 리스트로 반환하며 플래싱된 메시지가 없을 경우 빈 리스트를 반환
            단,플라스크 앱의 secret_key를 반드시 설정해야 한다
            '''
            flash('파일을 업로드 하세요')
            #return redirect(request.url)
            return render_template('views/upload.html',title='파일 업로드')
        if allowed_file(file.filename):#파일을 업로드 한 경우
            print(f'values:{file},type:{type(file)},conten-type:{file.content_type},업로드한 파일명:{file.filename}')
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return jsonify({'success':filename,'title':title})
        else:#허용된 파일이 아닌 경우
            flash('허용된 파일의 타입이 아닙니다')
            return redirect(request.url)
        """
        # 파일 여러개 업로드: request.files.getlist('파라미터명') 으로 파일을 받는다
        filenames = []
        files = request.files.getlist('upload')#[FileStorage,FileStorage,....]
        title = request.form['title']
        #파일 미첨부시 :value:[<FileStorage: '' ('application/octet-stream')>],type:<class 'list'>
        #파일 여러개 첨부시:value:[<FileStorage: 'mask1.jpg' ('image/jpeg')>, <FileStorage: 'mask2.jpg' ('image/jpeg')>],type:<class 'list'>
        print(f'value:{files},type:{type(files)}')
        if len(files[0].filename)==0:#파일을 업로드 안한 경우
            flash('파일을 업로드 하세요')
            return redirect(request.url)
        #허용된 파일만 업로드
        for file_storage in files:

            if allowed_file(file_storage.filename):
                filenames.append(file_storage.filename)
                file_storage.save(os.path.join(app.config['UPLOAD_FOLDER'],file_storage.filename))
            else:
                flash(f'허용된 파일의 타입이 아닙니다:{file_storage.filename}')

        return render_template('views/upload.html',title='파일 업로드')
    except Exception as e:
        print('업로드 오류:',e)
        flash('최대 업로드 용량을 초과 했어요')
        #url_for()함수 사용시 endpoint명은 함수명이어야 한다
        return redirect(url_for('uploadform',**{'title':'파일 업로드'}))

@app.route('/project')
def project():
    return render_template('frontend.html')
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8282)