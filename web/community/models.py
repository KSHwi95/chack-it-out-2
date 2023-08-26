from django.db import models


# Create your models here.

# 독서모임
class Community(models.Model):
    book = models.ForeignKey(
        "book.Book",
        blank=False,
        on_delete=models.CASCADE,
        verbose_name="도서",
    )
    meeting_date = models.DateTimeField(blank=False, verbose_name="모임 날짜")
    meeting_place = models.CharField(max_length=20, blank=False, verbose_name="모임 장소")
    creator= models.ForeignKey(
        "user.User",
        to_field="id",
        blank=False,
        on_delete=models.CASCADE,
        verbose_name="작성자",
    )
    is_finished = models.BooleanField(default=False,verbose_name='종료 여부')
    description = models.TextField(max_length=1000,verbose_name='모임 소개')

    # db_table의 이름을 "tb_user로 설정"
    class Meta:
        db_table = "tb_community"

# 모임 참여 멤버
class Member(models.Model):
    community = models.ForeignKey("Community", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)


    class Meta:
        db_table = "tb_communitymember"

# 모임 후기
class reviewMember(models.Model):
    community = models.ForeignKey("Community", on_delete=models.CASCADE)
    review = models.CharField(max_length=2000, verbose_name='모임후기')

    def __str__(self):
        return self.id

    class Meta:
        db_table = "tb_reviewmember"
