from django.db import models


# Create your models here.

# 도서
class Book(models.Model):
    book_isbn = models.BigIntegerField(verbose_name="ISBN"
    )
    book_title = models.CharField(max_length=500, verbose_name="도서명")
    book_author = models.CharField(max_length=500, verbose_name="저자")
    book_description = models.CharField(max_length=1000, verbose_name="책소개")
    book_cover = models.CharField(max_length=400, verbose_name="책표지")
    book_publishdate = models.DateField(verbose_name="출간일")
    book_page = models.IntegerField(verbose_name="페이지 수")
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, verbose_name="카테고리"
    )

    def __str__(self):
        return "%s"%self.book_title

    # db_table의 이름을 "tb_user로 설정"
    class Meta:
        db_table = "tb_book"

# 도서 카테고리
class Category(models.Model):
    category = models.CharField(max_length=20, unique=True, verbose_name="카테고리명")

    def __str__(self):
        return self.category

    class Meta:
        db_table = "tb_category"

# 라벨링 붙은 알라딘 리뷰
class Review(models.Model):
    book = models.ForeignKey(
        "book.Book",
        blank=False,
        on_delete=models.CASCADE,
        verbose_name="도서",
    )
    label= models.IntegerField(verbose_name='긍부정라벨')

    def __str__(self):
        return self.book

    class Meta:
        db_table = "tb_review"

# 유저가 작성한 리뷰
class reviewUser(models.Model):
    book = models.ForeignKey(
        "book.Book",
        blank=False,
        on_delete=models.CASCADE,
        verbose_name="도서",
    )
    review = models.CharField(max_length=2000, verbose_name='리뷰')

    def __str__(self):
        return self.book

    class Meta:
        db_table = "tb_reviewUser"

