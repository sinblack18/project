from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.template import loader
from django.core.paginator import Paginator
from django.core import serializers
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, DetailView

from json import loads

from .models import Board, Reply


# Create your views here.
# views.py의 함수에 들어있는 request 파라미터 : 요청객체


# 게시판 목록보기
def index(request):
    print('index() 실행')

    result = None

    context = {}

    # request.GET : GET 방식으로 보낸 데이터들을 딕셔너리 타입으로 저장
    # print(request.GET)

    # 검색 조건과 검색 키워드가 있어야 필터링 실행
    if 'searchType' in request.GET and 'searchWord' in request.GET:
        search_type = request.GET['searchType']  # GET 안의 문자열은
        search_word = request.GET['searchWord']  # HTML의 name 속성

        print("search_type : {}, search_word : {}".format(
            search_type, search_word))

        # match : Java의 switch랑 비슷함
        match search_type:
            case 'title':  # 검색 기준이 제목일 때
                result = Board.objects.filter(title1__contains=search_word)
            case 'writer':  # 검색 기준이 글쓴이일 때
                result = Board.objects.filter(writer__contains=search_word)
            case 'content':  # 검색 기준이 내용일 때
                result = Board.objects.filter(content__contains=search_word)

        # 검색을 했을때만 검색 기준과 키워드를 context에 넣는다
        context['searchType'] = search_type
        context['searchWord'] = search_word

    else:  # QueryDict에 검색 조건에 키워드가 없을 때
        result = Board.objects.all()

    # 검색 결과 또는 전체 목록을 id의 내림차순 정렬
    result = result.order_by('-id')

    # 페이징 넣기
    # Paginator(목록, 목록에 보여줄 개수)
    paginator = Paginator(result, 10)

    # Paginator 클래스를 이용해서 자른 목록의 단위에서
    # 몇번째 단위를 보여줄 것인지 정한다
    page_obj = paginator.get_page(request.GET.get('page'))

    # context['board_list'] = result
    # 페이징한 일부 목록 반환
    context['page_obj'] = page_obj

    return render(request, 'board/index.html', context)


def read(request, id):

    print(id)

    board = Board.objects.get(id=id)

    # 고전적인 방법으로 가져오기
    reply_list = Reply.objects.filter(board_obj=id).order_by('-id')

    # 조회수 올리기
    board.view_count += 1
    board.save()

    context = {
        'board': board,
        # 'replyList': reply_list
    }

    return render(request, 'board/read.html', context)


def home(request):

    return HttpResponseRedirect('/board/')


# 내가 따로 만든 로그인 url이 있다면 login_url 키워드 변수를
# 지정해야한다.
@login_required(login_url='common:login')
def write(request):

    if request.method == 'GET':  # 요청방식이 GET이면 화면 표시
        return render(request, 'board/board_form.html')

    else:  # 요청방식이 POST일 때 할 일

        print(request.POST)
        # print(request.FILES)
        # 폼의 데이터를 DB에 저장
        title1 = request.POST['title1']
        content = request.POST['content']
        author = request.user  # 요청에 들어있는 User 객체

        # 현재 세션정보의 writer라는 키를 가진 데이터 취득
        # session_writer = request.session.get('writer')
        # if not session_writer:  # 세션에 정보가 없는 경우
        #     # 폼에서 가져온 writer 값 세션에 저장
        #     request.session['writer'] = request.POST['writer']

        # print(session_writer)

        # 객체.save()

        board = Board(
            title1=title1,
            author=author,
            content=content
        )

        # get 메서드 사용하는 이유
        # 딕셔너리에서 존재하지 않는 키를 딕셔너리[키] -> KeyError
        # 딕셔너리.get("키") -> None
        if request.FILES.get("uploadFile"):
            upload_file = request.FILES["uploadFile"]
            # 요청에 들어있던 처부파일을 모델에 설정
            board.attached_file = upload_file
            board.original_file_name = upload_file.name

        board.save()  # db에 insert

        # 모델.objects.create(값)
        # Board.objects.create(
        #     title1=title1,
        #     author=author,  # user 객체 저장
        #     content=content
        # )

        return HttpResponseRedirect('/board/')


def download(request, id):
    print(id)

    board = Board.objects.get(id=id)
    attached_file = board.attached_file
    original_file_name = board.original_file_name

    # 글 번호에 달려있던 첨부파일로 파일형식 응답 객체 생성
    response = FileResponse(attached_file)
    response['Content-Disposition'] = 'attachment; filename=%s' % original_file_name  # 포맷

    return response


@login_required(login_url='common:login')
def update(request, id):

    print(id)

    board = Board.objects.get(id=id)

    if board.author.username != request.user.username:
        return HttpResponseRedirect('/board/'+str(id) + '/')

    if request.method == "GET":

        context = {'board': board}

        return render(request, 'board/board_update.html', context)

    else:
        board.title1 = request.POST['title1']
        board.content = request.POST['content']

        # 첨부파일이 있다면
        if request.FILES.get("uploadFile"):
            upload_file = request.FILES["uploadFile"]
            # 요청에 들어있던 처부파일을 모델에 설정
            board.attached_file = upload_file
            board.original_file_name = upload_file.name
        else:  # 첨부파일이 없다면
            board.attached_file = None
            board.original_file_name = None

        board.save()

        redirect_url = '/board/'+str(id) + '/'

        return HttpResponseRedirect(redirect_url)


@login_required(login_url='common:login')
def delete(request, id):

    print(id)
    # 해당 객체를 가져와서(get 가져올꺼니깐)
    board = Board.objects.get(id=id)

    # 글 작성자의 id와 접속한 사람의 id가 같을때
    if board.author.username == request.user.username:
        board.delete()
    # 다를때
    return HttpResponseRedirect('/board/')


def write_reply(request, id):
    print(request.POST)

    user = request.user
    # reply_text = request.POST['replyText']
    reply = loads(request.body)  # 요청의 body를 해석

    print(reply)

    reply_text = reply['replyText']

    board = Board.objects.get(id=id)
    board.reply_set.create(
        user=user,
        reply_content=reply_text
    )
    # Reply.objects.create(
    #     user=user,
    #     reply_content=reply_text,
    #     board_obj=Board.objects.get(id=id)
    # )

    # queryset을 이용해 봅시다

    # return HttpResponseRedirect('/board/'+str(id))

    return JsonResponse({'result': 'success'})


def delete_reply(request, id):

    request_body = loads(request.body)

    rid = request_body['rid']

    print(f'id: {id}, rid: {rid}')

    Board.objects.get(id=id).reply_set.get(id=rid).delete()

    # Reply.objects.get(id=rid).delete() # 위랑 같음

    return JsonResponse({'result': 'success'})


def update_reply(request, id):

    if request.method == 'GET':

        rid = request.GET.get('rid')

        print(id)

        print(rid)

        # board = Board.objects.get(id=id)
        # reply = Reply.objects.get(id=rid)
        reply = Board.objects.get(id=id).reply_set.get(id=rid)

        context = {
            # rid에 해당하는 Reply객체의 id하고 replyText
            'id': reply.id,
            'replyText': reply.reply_content
        }

        # return render(request, 'board/read.html', context)
        return JsonResponse(context)

    else:
        request_body = loads(request.body)  # 요청에 들어있는 body를 해석한다

        rid = request_body['rid']
        reply_text = request_body['replyText']

        reply = Board.objects.get(id=id).reply_set.get(id=rid)

        # 폼에 들어 있던 새로운 댓글 텍스트로 갱신
        reply.reply_content = reply_text
        reply.save()  # 그 이외의 정보가 바뀌는게 없으므로 저장하면 됨

        return JsonResponse({'result': 'success'})


def call_ajax(request):
    print("views. 성공한거 같아요")
    print(request.POST)
    # JSON.stringify 하면 아래 표현은 사용할 수 없음
    # print(request.POST['txt'])

    data = loads(request.body)
    print('템플릿에서 보낸 데이터', data)
    print(data['txt'])
    print(type(data))

    return JsonResponse({'result': 'ㅊㅋㅊㅋ'})


def load_reply(request, id):

    reply_list = Board.objects.get(id=id).reply_set.all()

    reply_dict_list = []

    # reply_list의 정보를 가지고 dictionary 만들기
    for reply in reply_list:
        reply_dict = {
            'id': reply.id,
            'username': reply.user.username,
            'replyText': reply.reply_content,
            'inputDate': reply.input_date
        }

        reply_dict_list.append(reply_dict)

    context = {'replyList': reply_dict_list}

    return JsonResponse(context)


def load_reply_delete(request, id, rid):
    data = request.POST
    print(data)
    print(f'id: {id}, rid: {rid}')

    Board.objects.get(id=id).reply_set.get(id=rid).delete()

    # Reply.objects.get(id=rid).delete() # 위랑 같음

    response = {'response': '삭제'}
    return JsonResponse(response)


def load_update_reply(request, id, rid):

    print(id)
    print(request.method)
    print(rid)

    if request.method == 'GET':

        board = Board.objects.get(id=id)
        # reply = Reply.objects.get(id=rid)

        context = {
            'update': 'update',
            'board': board,  # id에 해당하는 Board 객체
            'reply': board.reply_set.get(id=rid)  # rid에 해당하는 Reply 객체
        }

        print(context)

        print(context['reply'])

        # response = context['reply']

        return render(request, 'board/read.html', context)

    else:

        data = request.POST

        print(data)

        print(request.POST['replyText'])

        reply = Board.objects.get(id=id).reply_set.get(id=rid)

        # 폼에 들어 있던 새로운 댓글 텍스트로 갱신
        reply.reply_content = request.POST['replyText']

        reply.save()

        response = {'response': '수정'}

        return JsonResponse(response)


# def write_reply(request, id):

#     print(request.POST)

#     user = request.user
#     reply_text = request.POST['replyText']

#     board = Board.objects.get(id=id)
#     board.reply_set.create(
#         user=user,
#         reply_content=reply_text
#     )

#     response = {'response': '글쓰기'}
#     return JsonResponse(response)


# def load_reply_update(request, id, rid):

#     if request.method == 'GET':

#         board = Board.objects.get(id=id)
#         # reply = Reply.objects.get(id=rid)

#         context = {
#             'update': 'update',
#             'board': board,  # id에 해당하는 Board 객체
#             'reply': board.reply_set.get(id=rid)  # rid에 해당하는 Reply 객체
#         }

#         return render(request, 'board/read.html', context)

    # else:

    #     reply = Board.objects.get(id=id).reply_set.get(id=rid)

    #     # 폼에 들어 있던 새로운 댓글 텍스트로 갱신
    #     reply.reply_content = request.POST['replyText']

    #     reply.save()

    #     response = {'response': '수정'}
    #     return JsonResponse(response)


# def search_board(request):

#     title1 = request.POST['search']

#     bList = Board.objects.filter(title1__contains=title1)

#     context = {
#         'board_list': bList
#     }

#     return render(request, 'board/index.html', context)


### Class Based View ###
class BoardList(ListView):
    # ListView : 목록을 보여주는 기능(장고 기본 기능 import)
    # model = 이 페이지에서 표시할 객체 타입
    model = Board

    # ordering 속성에는 문자열로 내가 정렬하고 싶은 열 이름을 쓴다
    # 열 이름 앞에 -가 붙어 있으면 내림차순 정렬
    ordering = '-id'

    # 클래스 기반 뷰에서 사용하는 템플릿은
    # 일반적으로 이름이 객체이름_list.html


class BoardDetail(DetailView):
    model = Board

    # template_name 속성 : 내가 별도로 이용하고 싶은 템플릿 파일이 있을 때
    # 해당 파일 이름 지정
    # template_name 을 사용하지 않으면 model이름_detail.html을 찾아간다
    template_name = 'board/read.html'

    # def get_object(self):
    #     object = get(Board, id=self.kwargs['id'])
    #     return object
