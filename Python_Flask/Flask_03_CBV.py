from flask import Flask,render_template,request,redirect,views

app = Flask(__name__)
app.config.from_pyfile("settings.py")

USERS = {
    1:{'name':'Arthur','age':99,'gender':'男'},
    2:{'name':'Arthur2','age':991,'gender':'男'},
    3:{'name':'Arthur3','age':992,'gender':'女'},
    4:{'name':'Arthur4','age':993,'gender':'男'}
}

def auth(func):
    def inner(*args,**kwargs):
        result = func(*args,**kwargs)
        return result
    return inner

#CBV写法
class IndexView(views.MethodView):
    method = ['GET',]
    decorators = [auth,]


    def get(self):
        return 'Index.GET'

    def post(self):
        return 'Index.POST'

app.add_url_rule('/index/',view_func = IndexView.as_view(name = 'index'))  #name = endpoint







if __name__ =='__main__':

    app.run()