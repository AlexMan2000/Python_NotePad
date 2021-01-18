from flask import Flask,render_template,request,redirect

app = Flask(__name__)
app.config.from_pyfile("settings.py")

USERS = {
    1:{'name':'Arthur','age':99,'gender':'男'},
    2:{'name':'Arthur2','age':991,'gender':'男'},
    3:{'name':'Arthur3','age':992,'gender':'女'},
    4:{'name':'Arthur4','age':993,'gender':'男'}
}


#endpoint就是url的别名
@app.route('/index/',methods = ['GET',],endpoint = 'n1')
def index():
    return render_template('index.html',user_dict = USERS)



@app.route('/login/',methods = ['GET','POST'])
def login():
    if request.method == "GET":

        return render_template('login.html')
    else:
        headers = request.query_string  #url中的数据
        user = request.form.get('user')  #form表单的提交数据
        pwd = request.form.get('pwd')
        if user == "root" and pwd =="123123":
            return redirect('/index/')
        else:
            return render_template('login.html',error = '用户名或密码错误')



if __name__ =='__main__':

    app.run()