# 장고가 폼을 잘 관리하도록 제공하는 클래스 forms
from django import forms
# 모델에서 User 데이터베이스를 가져옵니다.
from .models import User
# check_password로 비밀번호를 확인합니다.
from django.contrib.auth.hashers import check_password


# class Modify(forms.Form):
#      user_pw = 



# 로그인폼 작성 
class LoginForm(forms.Form):
    user_id = forms.CharField(
        max_length=15, 
        label='아이디',
        error_messages={'required': "아이디를 입력해 주세요"}
        )
    # widget : input type
    password = forms.CharField(
        max_length=15, 
        label='비밀번호',
        error_messages={'required': "비밀번호를 입력해 주세요"},
        widget=forms.PasswordInput)
    
    
    def clean(self):
                # 기본적인 유효성 검증을 먼저 수행하기 위해 부모 클래스의 clean()을 먼저 실행
                # 값이 모두 들어있는지를 검사합니다.
                # 값이 모두 들어있지 않으면 여기에서 이미 실패처리가 됩니다.
                cleaned_data = super().clean()
            
                # cleaned_data는 부모 클래스의 유효성 검증 결과가 들어 있습니다.
                # form.POST 객체이며, 여기서 사용자가 입력한 데이터를 꺼내올 수 있습니다.
                user_id = cleaned_data.get("user_id")
                password = cleaned_data.get("password")

                # user_id와 패스워드가 모두 존재한다면 Valid = True
                if user_id and password:
                    # 아이디를 가져온다.
                    try:
                        user = User.objects.get(user_id=user_id)
                    # 만약 없으면 
                    except User.DoesNotExist: # 조회된 내용이 없을 경우 발생된 예외를 처리
                        self.add_error("password", "비밀번호 오류 또는 존재하지 않는 아이디입니다.")
                        return # 중단 (자동 clear)
                    if password != user.password:
                        # 비밀번호가 틀리면 에러 메시지 설정
                        self.add_error("password", "비밀번호 오류 또는 존재하지 않는 아이디입니다.")
                    else:
                        # 비밀번호가 맞은 경우 사용자의 pk를 변수에 저장
                        self.user_id=user.id