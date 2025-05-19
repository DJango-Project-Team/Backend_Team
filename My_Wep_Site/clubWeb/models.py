from django.db import models

class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'clubweb_club'  # 명시적으로 테이블 이름 지정

class Application(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20)
    email = models.EmailField()
    motivation = models.TextField()
    experience = models.TextField()

    def __str__(self):
        return f"{self.student_name} - {self.club.name}"

    class Meta:
        db_table = 'clubweb_application'  # 테이블 이름 지정
