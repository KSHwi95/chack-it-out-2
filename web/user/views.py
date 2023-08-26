from django.shortcuts import render, redirect

# POST로 받을 DB 모델

# 회원가입오류
# 1. 아이디 또는 비밀번호 오류
from django.db import IntegrityError

from book.models import Book
from .models import User, Favorite, Reading, Wish
from book.models import Category
from community.models import Community, Member
from django.db.models import Q
import random
import pickle
import bookdata
import recommend4book
from recommend4book import getRecommend

# 로그인폼
from .forms import LoginForm

# Create your views here.


# request to VIEW if "GET"(/link/), return templates to user
def register(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "register.html", {"categories": categories})
    # 사용자의 요청이 POST인 경우
    elif request.method == "POST":
        # 각 input tag에서 name 속성값을 이용해 사용자가 보낸 값을 꺼내옵니다.
        try:
            user_id = request.POST["user_id"]
            user_name = request.POST["user_name"]
            password = request.POST["password"]
            # User모델 객체에 담는는다..
            user = User(user_id=user_id, user_name=user_name, password=password)
            user.save()
            categories = Category.objects.all()
            # 선택된 것들을 리스트로 담음
            selected = request.POST.getlist("selected")
            for choice in selected:
                favorite = Favorite(
                    user=User.objects.latest("id"),
                    category=Category.objects.get(id=choice),
                )
                favorite.save()

        except IntegrityError:
            error = "이미 존재하는 아이디이거나 아이디가 공백입니다."
            return render(request, "register.html", {"error": error})

        # 가입 완료시 메인으로 이동
        return render(request, "main.html")


# 로그인 기능
def login(request):
    if request.method == "POST":
        # POST로 들어오는경우, loginForm에 받아준다.
        form = LoginForm(request.POST)
        # is_valid - post로 들어온 form을 둘다 적었다.
        if form.is_valid():
            # 유저 pk를 세션에 저장
            request.session["user"] = form.user_id
            return redirect("/")
    # POST방식이 아닌 경우
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout(request):
    # 현재 로그인한 사용자의 정보가 세션에 존재하면
    if request.session.get("user"):
        del request.session["user"]  # user 정보 삭제

    # 로그아웃 수행 후 홈 페이지로 이동
    return redirect("/")


def userpage(request, pk):
    user = User.objects.get(id=pk)
    loginuser = User.objects.get(id=int(request.session.get("user")))
    name = user.user_name
    # user_id가 pk와 일치하는 카테고리 객체집합
    favorites = Favorite.objects.all().filter(user_id=pk)
    cate_ls = []
    cate_name = []
    for favorite in favorites:
        # category - fk의 값 category_id - fk
        # list에 담아줌
        cate_name.append(favorite.category)
        cate_ls.append(favorite.category_id)
    # 필터링된 책들
    selectedbooks = Book.objects.all().filter(category_id__in=cate_ls)
    # 랜덤으로 4개 추출
    randomresult = []
    for i in range(4):
        randomresult.append(random.choice(selectedbooks))
    # 추천 위한 피클파일
    pickle_file_path = "data/mec_3f_007_matrix.pkl"
    with open(pickle_file_path, "rb") as file:
        tfidx_matrix = pickle.load(file)

    # "읽은책" 의 책'객체'들 뽑아내기
    endbooks = Reading.objects.all().filter(user_id=pk)
    # 커뮤니티 참여 책 객체
    result = []
    isbn_list = []
    for book in endbooks:
        result.append(book.book)
    for book in result:
        isbn_list.append(book.book_isbn)
    # 책 리스트 df로
    # DataFrame 만들기
    df = bookdata.df
    ls = getRecommend(df, tfidx_matrix, isbn_list)
    recommendbooks = Book.objects.all().filter(book_isbn__in=ls)
    count = len(endbooks)
    return render(
        request,
        "userpage.html",
        {
            "user": user,
            "name": name,
            "pk": pk,
            "loginuser": loginuser,
            "cate_name": cate_name,
            "randomresult": randomresult,
            "loginuser": loginuser,
            "recommendbooks": recommendbooks,
            "result": result,
            "count": count,
        },
    )


def search(request):
    user = User.objects.get(id=int(request.session.get("user")))
    name = user.user_name
    if "searchword" in request.GET:
        query = request.GET.get("searchword")
        selectbar = request.GET.get("selectbar")
        if selectbar:
            if selectbar == "1":
                users = User.objects.all().filter(Q(user_name__icontains=query))
            elif selectbar == "2":
                users = User.objects.all().filter(Q(user_id__icontains=query))
        return render(
            request,
            "usersearch.html",
            {
                "user": user,
                "name": name,
                "query": query,
                "users": users,
                "selectbar": selectbar,
            },
        )
    else:
        return render(request, "usersearch.html", {"user": user, "name": name})


def reading(request, pk):
    user = User.objects.get(id=pk)
    loginuser = User.objects.get(id=int(request.session.get("user")))
    name = user.user_name
    readings = Reading.objects.all().filter(user_id=pk)
    readingls = []
    for reading in readings:
        readingls.append(reading.book_id)
    selectedbooks = Book.objects.all().filter(id__in=readingls)
    if "delete" in request.GET:
        id = request.GET.get("delete")
        reading = Reading.objects.all().filter(book_id=id).filter(user_id=user)
        reading.delete()
        return redirect(f"/user/userpage/{request.session.get('user')}/reading")

    return render(
        request,
        "reading.html",
        {
            "user": user,
            "name": name,
            "pk": pk,
            "selectedbooks": selectedbooks,
            "loginuser": loginuser,
        },
    )


def wish(request, pk):
    user = User.objects.get(id=pk)
    loginuser = User.objects.get(id=int(request.session.get("user")))
    name = user.user_name
    Wishes = Wish.objects.all().filter(user_id=pk)
    wishls = []
    for wish in Wishes:
        wishls.append(wish.book_id)
    selectedbooks = Book.objects.all().filter(id__in=wishls)
    if "delete" in request.GET:
        id = request.GET.get("delete")
        wish = Wish.objects.all().filter(book_id=id).filter(user_id=user)
        wish.delete()
        return redirect(f"/user/userpage/{request.session.get('user')}/wish")
    return render(
        request,
        "wish.html",
        {
            "user": user,
            "name": name,
            "pk": pk,
            "selectedbooks": selectedbooks,
            "loginuser": loginuser,
        },
    )


def usercommunity(request, pk):
    loginuser = User.objects.get(id=int(request.session.get("user")))
    user = User.objects.get(id=pk)
    name = user.user_name

    Members = Member.objects.all().filter(user=pk)
    membercommunityls = []
    for member in Members:
        membercommunityls.append(member.community_id)
    # 모든 종료된 커뮤니티를 가져오고, 그중 id가 list에 있는것을 가져옴
    allcommunities = Community.objects.all().filter(id__in=membercommunityls)
    endcommunities = allcommunities.filter(is_finished=True)
    doingcommunities = allcommunities.filter(is_finished=False)
    return render(
        request,
        "usercommunity.html",
        {
            "user": user,
            "name": name,
            "pk": pk,
            "endcommunities": endcommunities[::-1],
            "doingcommunities": doingcommunities[::-1],
            "loginuser": loginuser,
        },
    )


# 회원정보 삭제
def delete(request):
    user = User.objects.get(id=int(request.session.get("user")))
    user.delete()
    del request.session["user"]
    return render(request, "main.html")
