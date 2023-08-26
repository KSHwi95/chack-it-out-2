# render(request, '___.html') - request요청대로, ___.html을 반환하는 패키지
from django.shortcuts import render
from user.models import User
from book.models import Book
from community.models import Community
import random
import pickle
import pandas as pd

# 추천함수
from recommend import getRecommend
import bookdata

# 추천에 사용할 매트릭스
# tfidx_matrix


def home(request):
    pickle_file_path = "data/mec_3f_007_matrix.pkl"
    with open(pickle_file_path, "rb") as file:
        tfidx_matrix = pickle.load(file)
    # "완료된" 독서모임의 책"객체"들 뽑아내기
    endcommunities = Community.objects.all().filter(is_finished=True)
    # 커뮤니티 참여 책 객체
    result = []
    isbn_list = []
    for community in endcommunities:
        result.append(community.book)
    for comubook in result:
        isbn_list.append(comubook.book_isbn)
    # 책 리스트 df로
    # DataFrame 만들기
    df = bookdata.df
    ls = getRecommend(df, tfidx_matrix, isbn_list)
    recommendbooks = Book.objects.all().filter(book_isbn__in=ls)
    # 로그인정보가 있을때
    try:
        user = User.objects.get(id=int(request.session.get("user")))
        name = user.user_name
        # 책 객체를 랜덤으로하나 보여주겠다.

    # 유저 정보가 없을때(비로그인)
    except TypeError:
        # getRecommend(df,tfidx_matrix,isbn_list)
        return render(request, "main.html", {"result": result[-1:-5:-1]})

    return render(
        request,
        "main.html",
        {
            "user": user,
            "name": name,
            "recommendbooks": recommendbooks,
            "result": result[-1:-5:-1],
        },
    )


def search(request):
    user = User.objects.get(id=int(request.session.get("user")))
    name = user.user_name
    return render(request, "search.html", {"user": user, "name": name})


def search_book(request):
    user = User.objects.get(id=int(request.session.get("user")))
    name = user.user_name
    return render(request, "search.html", {"user": user, "name": name})
