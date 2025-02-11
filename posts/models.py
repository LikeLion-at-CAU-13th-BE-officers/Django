from django.db import models
from accounts.models import User

# Create your models here.
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True) # 객체를 생성할 때 날짜와 시간 저장
    updated = models.DateTimeField(auto_now=True) # 객체를 저장할 때 날짜와 시간 갱신

    class Meta:
        abstract = True


class  Post(BaseModel):

    CHOICES = (
        ('STORED', '보관'),
        ('PUBLISHED', '발행')
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    status = models.CharField(max_length=15, choices=CHOICES, default='STORED')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')

    def __str__(self):
        return self.title
    
class Image(BaseModel):
    id = models.AutoField(primary_key=True)
    image_url = models.URLField(max_length=500)  # S3에 업로드된 이미지의 URL 저장

    def __str__(self):
        return f"Image {self.id}"