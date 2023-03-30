from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.core.paginator import Paginator
from django.core import serializers
from django.contrib.auth.decorators import login_required

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

        # board = Board(
        #     title1=title1,
        #     writer=writer,
        #     content=content
        # )

        # board.save()  # db에 insert

        # 모델.objects.create(값)

        Board.objects.create(
            title1=title1,
            author=author,  # user 객체 저장
            content=content
        )

        return HttpResponseRedirect('/board/')


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
    reply_text = request.POST['replyText']

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

    return HttpResponseRedirect('/board/'+str(id))


def delete_reply(request, id, rid):

    print(f'id: {id}, rid: {rid}')

    Board.objects.get(id=id).reply_set.get(id=rid).delete()

    # Reply.objects.get(id=rid).delete() # 위랑 같음

    return HttpResponseRedirect('/board/'+str(id))


def update_reply(request, id):

    if request.method == 'GET':

        rid = request.GET['rid']

        board = Board.objects.get(id=id)
        # reply = Reply.objects.get(id=rid)

        context = {
            'update': 'update',
            'board': board,  # id에 해당하는 Board 객체
            'reply': board.reply_set.get(id=rid)  # rid에 해당하는 Reply 객체
        }

        return render(request, 'board/read.html', context)

    else:
        rid = request.POST['rid']

        reply = Board.objects.get(id=id).reply_set.get(id=rid)

        # 폼에 들어 있던 새로운 댓글 텍스트로 갱신
        reply.reply_content = request.POST['replyText']

        reply.save()

        return HttpResponseRedirect('/board/'+str(id))


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


def load_reply(request):
    id = request.POST['id']
    print(id)

    # 해당하는 board id에 달려있는 모든 Reply 가져오기
    # 1번 방법
    # Reply.objects.filter(board=id)
    # 2번 방법
    reply_list = Board.objects.get(id=id).reply_set.all()

    # QuerySet 그 자체는 JS에서는 알 수 없는 타입
    # 그래서 JSON타입으로 형변환
    serialized_list = serializers.serialize("json", reply_list)

    response = {'response': serialized_list}
    return JsonResponse(response)


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


def write_reply(request, id):

    print(request.POST)

    user = request.user
    reply_text = request.POST['replyText']

    board = Board.objects.get(id=id)
    board.reply_set.create(
        user=user,
        reply_content=reply_text
    )

    response = {'response': '글쓰기'}
    return JsonResponse(response)


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
