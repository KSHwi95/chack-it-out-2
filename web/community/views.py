from django.shortcuts import render, redirect
from .models import Community, Member, reviewMember
from book.models import Book
from user.models import User
import re


# Create your views here.
def community(request):
    # 로그인 정보가 있을 때
    if request.session.get("user"):
        user = User.objects.get(id=int(request.session.get("user")))
        name = user.user_name
        # 현재 진행중인 모임만 출력
        communities = Community.objects.all().filter(is_finished=False)
        endcommunities = Community.objects.all().filter(is_finished=True)
        # 지금까지 도서모임으로 진행했던 책들
        result = []
        for community in endcommunities:
            result.append(community.book)
        return render(
            request,
            "community.html",
            {
                "user": user,
                "name": name,
                "communities": communities[::-1],
                "endcommunities": endcommunities[::-1],
                "result": result[::-1],
            },
        )
    else:
        communities = Community.objects.all()
        members = Member.objects.all()
        return render(
            request, "community.html", {"communities": communities, "members": members}
        )


# 새 모임 만들기
def newcommunity(request):
    if request.method == "GET":
        user = User.objects.get(id=int(request.session.get("user")))
        name = user.user_name
        return render(request, "new.html", {"user": user, "name": name})
    elif request.method == "POST":
        get_book_isbn = request.POST["book"]
        meeting_date = request.POST["meeting_date"]
        meeting_place = request.POST["meeting_place"]
        creator = User.objects.get(id=request.session.get("user"))
        description = request.POST["description"]
        community = Community(
            book=Book.objects.get(book_isbn=get_book_isbn),
            meeting_date=meeting_date,
            meeting_place=meeting_place,
            description=description,
            creator=creator,
        )
        community.save()
        member = Member(
            community=Community.objects.latest("id"),
            user=User.objects.get(id=int(request.session.get("user"))),
        )
        member.save()

        return redirect("/community/")


# 상세 페이지
def detail(request, pk):
    user = User.objects.get(id=int(request.session.get("user")))
    community = Community.objects.get(id=pk)
    book = community.book
    members = Member.objects.all().filter(community_id=pk)
    memberls = []
    for member in members:
        memberls.append(member.user_id)
    # 모임 참여 신청
    if "join" in request.GET:
        member = Member(community=community, user=user)
        member.save()
        return redirect("/community/")
    return render(
        request,
        "detail.html",
        {
            "user": user,
            "pk": pk,
            "community": community,
            "book": book,
            "members": members,
            "memberls": memberls,
        },
    )


def detail2(request, pk):
    user = User.objects.get(id=int(request.session.get("user")))
    community = Community.objects.get(id=pk)
    if "review_input" in request.GET:
        contents = request.GET.get("review_input")
        reviewmember = reviewMember(
            review=contents,
            community=Community.objects.get(id=pk),
        )
        reviewmember.save()
        return redirect(f"/community/detail2/{pk}")
        # 모임의의 전체 리뷰조회
    allreview = reviewMember.objects.all().filter(community_id=pk)
    return render(
        request,
        "detail2.html",
        {"user": user, "pk": pk, "community": community, "allreview": allreview},
    )


# 작성자 권한 : 모임 종료시키기
def quit(request, pk):
    community = Community.objects.get(id=pk)
    community.is_finished = 1
    community.save()
    return redirect("/community/")
