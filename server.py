from flask import Flask
from flask import render_template 
from flask import request, redirect, make_response
from aws import detect_labels_local_file as label
from werkzeug.utils import secure_filename
from aws import compare_faces as cf
# from flask import Flask, render_template 로 써도된다.
# html문서를 load한다!
# 단, template폴더에 있는 html만 바라볼 수 있다
# 터미널에서 mkdir templates 하고
#  cp .\html\exam03.html .\templates\exam03.html로 복사한다!
app = Flask(__name__)

# 서버 주소 /로 들어오면
# return html문서
@app.route("/")
def index():
    return render_template("home.html")


@app.route("/compare", methods=["POST"])
def compare():
    try:
        if request.method == "POST":
            f1 = request.files["file1"]
            f2 = request.files["file2"]

            f1_filename = secure_filename(f1.filename)
            f2_filename = secure_filename(f2.filename)
            f1.save("static/" + f1_filename)
            f2.save("static/" + f2_filename)

            r1 = cf("static/" + f1_filename, "static/" + f2_filename)
            return r1
    except:
        return "비교 실패"
    

@app.route("/detect", methods=["POST"])
def detect():
    try:
        if request.method =="POST":
            # 서버에 클라이언트가 보낸 이미지를 저장하고,
            # 그 저장 경로를 라벨로 던지자!
            f = request.files["file"]
            
            filename = secure_filename(f.filename)
            # 외부에서 온 이미지, 파일 등을
            # 마음대로 지정할 수 없음
            # static 폴더에 저장하자! (터미널에서 mkdir static하고나서)
            f.save("static/" + filename)
            r = label("static/" + filename)
            return r
    except:
        return "감지 실패"


@app.route("/mbti", methods=["POST"])
def mbti():
    try:
        if request.method == "POST":
            mbti = request.form["mbti"]

            return f"당신의 MBTI는 {mbti}입니다"
    except:
        return "데이터 수신 실패"


@app.route("/login", methods=["GET"])
def login():
    try:
        if request.method == "GET":
            # login_id, login_pw
            # get -> request.args로 받을 수 있다.
            # login?어쩌고~ 형식이면 get방식! ?key=value
            # /login으로 끝나면 get방식 아님!
            login_id = request.args["login_id"]
            login_pw = request.args["login_pw"]

            if (login_id == "seoyoung") and (login_pw == "1234"):
            # 로그인 성공 -> 로그인 성공 페이지로 이동
            # seoyoung님 환영합니다

                response = make_response(redirect("/login/success"))
                response.set_cookie("user", login_id)

                return response
            else:
                # 로그인 실패 -> /경로로 다시 이동
                return redirect("/")
    except:
        return "로그인 실패"
    
    
@app.route("/login/success")
def login_success():
    
    login_id = request.cookies.get("user")
    return f"{login_id}님 환영합니다."


# 실행하면 exam03이 나오는 데
# 링크뒤에 /exam04 치면 exam04가 뜬다!
# @app.route("/exam04")
# def exam04():
#     return render_template("exam04.html")


if __name__ == "__main__":
    # 1. host
    # 2. port
    app.run(host="0.0.0.0")

# 컨트럴 + L : 터미널 클리어
# 컨트럴 + C : 서버 내림