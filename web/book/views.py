from django.shortcuts import render,redirect
from .models import Book,reviewUser,Review
import pandas as pd
from user.models import User,Reading,Wish
from django.db.models import Q
import re
# Create your views here.


def search(request):
    user = User.objects.get(id=int(request.session.get("user")))    
    if "searchword" in request.GET:
        query = request.GET.get("searchword")
        selectbar = request.GET.get("selectbar")
        if selectbar:
            if selectbar == "1":
                books = Book.objects.all().filter(Q(book_title__icontains=query))
            elif selectbar == "2":
                books = Book.objects.all().filter(Q(book_author__icontains=query))
            elif selectbar == "3":
                books = Book.objects.all().filter(Q(book_isbn__icontains=query))
        return render(
            request,
            "Booksearch.html",
            {"user":user,"query": query, "books": books, "selectbar": selectbar},
        )
    else:
        return render(request, "Booksearch.html",{'user':user})


def result(request, pk):
    user = User.objects.get(id=int(request.session.get("user")))    
    # 위에 검색창 검색기능
    if "searchword" in request.GET:
        query = request.GET.get("searchword")
        selectbar = request.GET.get("selectbar")
        if selectbar:
            if selectbar == "1":
                books = Book.objects.all().filter(Q(book_title__icontains=query))
            elif selectbar == "2":
                books = Book.objects.all().filter(Q(book_author__icontains=query))
            elif selectbar == "3":
                books = Book.objects.all().filter(Q(book_isbn__icontains=query))
        return render(
            request,
            "Booksearch.html",
            {"user":user,"query": query, "books": books, "selectbar": selectbar}
        )
    
    # 읽은 책 버튼 추가 기능
    elif "reading" in request.GET:
        reading=Reading(
            user = User.objects.get(id=int(request.session.get("user"))),
            book = Book.objects.get(id=pk)
        )
        reading.save()
        return redirect(f"/user/userpage/{request.session.get('user')}/reading")

    # 위시리스트 버튼 누르면 기능
    elif "wish" in request.GET:
        wish=Wish(
            user = User.objects.get(id=int(request.session.get("user"))),
            book = Book.objects.get(id=pk)
        )
        wish.save()
        return redirect(f"/user/userpage/{request.session.get('user')}/wish")
    else:
        book = Book.objects.get(id=pk)
        return render(request, "result.html", {"user":user,"pk": pk, "book": book})


def result2(request, pk):
    user = User.objects.get(id=int(request.session.get("user")))
    book = Book.objects.get(id=pk)
    # 책의 전체 리뷰
    allreview=reviewUser.objects.all().filter(book_id=book.id)
    aladinreview=Review.objects.all().filter(book_id=pk)
    sum=len(aladinreview)
    neg=0
    pos=0
    negative=0
    positive=0
    if sum >= 1:
        for booklabel in aladinreview:
            if booklabel.label == 0:
                neg += 1
            else:
                pos += 1
        negative=round(neg/sum*100,2)
        positive=round(pos/sum*100,2)

    if "searchword" in request.GET:
        query = request.GET.get("searchword")
        selectbar = request.GET.get("selectbar")
        if selectbar:
            if selectbar == "1":
                books = Book.objects.all().filter(Q(book_title__icontains=query))
            elif selectbar == "2":
                books = Book.objects.all().filter(Q(book_author__icontains=query))
            elif selectbar == "3":
                books = Book.objects.all().filter(Q(book_isbn__icontains=query))
        return render(
            request,
            "Booksearch.html",
            {"user":user,"query": query, "books": books, "selectbar": selectbar},
        )
    
    else:
        user = User.objects.get(id=int(request.session.get("user")))
        book = Book.objects.get(id=pk)
        # 리뷰넣기
        if "comment-input" in request.GET:
            contents = request.GET.get("comment-input")
            reviewuser=reviewUser(
                review=contents,
                book = Book.objects.get(id=pk)
            )
            reviewuser.save()
            return redirect(f"/book/search/result2/{pk}")
    return render(request, "result2.html", {"user":user,"pk": pk, "book": book,"allreview":allreview,"neg":neg,"pos":pos,"negative":negative,"positive":positive})
