from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
# views.py의 함수에 들어있는 request 파라미터 : 요청객체
def index(request):
    template = loader.get_template('app/index.html')

    # dictionary 타입의 변수 context
    context = {}

    # 응답객체안에 템플릿과 표시할 값(context), 요청(request)
    return HttpResponse(template.render(context, request))

def call1(request):
    template = loader.get_template('app/template.html')
    
    context = {}

    print(request)
    
    return HttpResponse(template.render(context, request))

# RESTful 방식으로 호출된 주소에 대한 함수
# 요청 객체 뒤의 파라미터에 해당하는 변수명 써줘야
def call2(request, number):
    template = loader.get_template('app/template.html')
    print("number :",number)
    context = {}

    return HttpResponse(template.render(context, request))

def call3(request):
    #request 객체에서 가져오는 모든 데이터는 str 타입이다.
    age = request.GET['age']
    name = request.GET['name']
    print("name :", name)
    print("age : ",age)
    return HttpResponse('호출됨')

def call4(request):
    template = loader.get_template("app/template.html")
    name = request.GET['name']
    context = {
        # 텍스트 보내기
        'item' :'This text is sent from server.',
        'name' : name,
        'board_list' :[
        {'title':'1등', 'writer':'홍길동'},
        {'title':'2등', 'writer':'이길동'},
        {'title':'3등', 'writer':'삼길동'},
        ],
        # 딕셔너리 보내기
        'mydata':{
            'name':name,
            'age':30,
            'address':'광주'
        }
    }
    return HttpResponse(template.render(context,request))

def call5(request):
    template = loader.get_template('app/tag.html')
    str_list = ['사과','딸기','바나나']

    context={
        'list' : str_list,
        'number':3,
             }


    return HttpResponse(template.render(context))

def call6(request):
    template = loader.get_template('app/form.html')
    context ={}
    return HttpResponse(template.render(context,request))

def call_submit(request):
    # template = loader.get_template('app/form.html')
    name = request.POST['name']
    age= request.POST['age']
    print('name :',name)
    print('age : ',age)
    return HttpResponse("submit OK")