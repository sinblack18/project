from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import models
from django.db.models import Count

from .models import Movie, Review

# Create your views here.


def index(request):

    if 'search_genre' in request.GET:

        search_genre = request.GET['search_genre']

        movie = Movie.objects.filter(
            genre__contains=search_genre).order_by('-id')

    else:

        movie = Movie.objects.all().order_by('-id')

    context = {'movie': movie}

    return render(request, 'exam/index.html', context)


def orderby_review(request):

    if 'search_genre' in request.GET:

        search_genre = request.GET['search_genre']

        movie = Movie.objects.annotate(
            review_count=models.Count('review')).filter(
            genre__contains=search_genre).order_by('-review_count')

    else:

        movie = Movie.objects.annotate(
            review_count=models.Count('review')).order_by('-review_count')

        # Count import하고 임시 필드생성
        # 예시 w3
        # from django.db.models import Count
        # pubs = Publisher.objects.annotate(num_books=Count('book'))
        # 이렇게하면 쿼리셋으로 나온다

    context = {'movie': movie}

    return render(request, 'exam/index.html', context)


def movieadd(request):

    if request.method == 'GET':

        return render(request, 'exam/movieadd.html')

    else:

        print(request.POST)

        genre = request.POST['genre']

        movie_name = request.POST['movie_name']

        summary = request.POST['summary']

        print(genre, movie_name, summary)

        Movie.objects.create(
            genre=genre,
            movie_name=movie_name,
            movie_summary=summary
        )

        return HttpResponseRedirect('/')


def movieinfo(request, id):

    print(id)

    movie = Movie.objects.get(id=id)

    review = Review.objects.all()

    # review2 = review.get(movie_id=id)
    # print(review2)

    review3 = Review.objects.filter(movie_id=id).order_by('id')

    print(review3)

    context = {
        'movie': movie,
        'review': review3
    }

    return render(request, 'exam/movieinfo.html', context)


def load_review(request, id):

    review_list = Review.objects.filter(movie_id=id).order_by('-id')

    review_dict_list = []

    for review in review_list:
        review_dict = {
            'id': review.id,
            'reviewer_name': review.reviewer_name,
            'review_text': review.review_text,
            'score': review.score,
            'reg_date': review.reg_date
        }

        review_dict_list.append(review_dict)

    context = {'reviewList': review_dict_list}

    return JsonResponse(context)


def movieupdate(request, id):

    movie = Movie.objects.get(id=id)

    if request.method == 'GET':

        context = {'movie': movie}

        return render(request, 'exam/movieupdate.html', context)

    else:

        movie.genre = request.POST['genre']

        movie.movie_name = request.POST['movie_name']

        movie.movie_summary = request.POST['summary']

        movie.save()

        redirect_url = '/movieinfo/'+str(id) + '/'

        return HttpResponseRedirect(redirect_url)


def moviedelete(request, id):

    Movie.objects.get(id=id).delete()

    return HttpResponseRedirect('/')


def reviewadd(request, id):

    movie = Movie.objects.get(id=id)

    # reviewer_name = request.POST['reviewer_name']

    if request.POST['reviewer_name'] == '':
        reviewer_name = '익명의 관객'
    else:
        reviewer_name = request.POST['reviewer_name']

    review_text = request.POST['review_text']

    score = request.POST['score']

    Review.objects.create(
        reviewer_name=reviewer_name,
        movie=movie,
        review_text=review_text,
        score=score
    )

    redirect_url = '/movieinfo/'+str(id) + '/'

    return HttpResponseRedirect(redirect_url)
