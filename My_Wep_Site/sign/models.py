from django.db import models

#from 이나 model 이나 차이는 없다? 하고싶은데로
#unique는 중복을 걸러내는 로직
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)

    #객체를 문자열로 표현할 때 어떤 값을 보여줄지 정해줌
    def __str__(self):
        return self.username
#위 데이버 베이스는 사용하지 않음

#아래는 회원가입시 필요한 DB
class Sign_Up_Users(models.Model):
    sign_up_email = models.CharField(max_length=50, unique=True)
    sign_up_password = models.CharField(max_length=255)
    sign_up_name = models.CharField(max_length=50)
    sign_up_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.sign_up_name
