from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Question(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_question')
    question=models.CharField(max_length=200)
    date_time=models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)
    def __str__(self):
        return "User {} Question {} DATETIME {}".format(self.user.username,self.question,self.date_time)




class Tower(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,null = True,related_name='user_answer')
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer=models.TextField()
    upvotes = models.ManyToManyField(User,related_name='likes')
    date_time=models.DateTimeField(auto_now=True)


class Upvote(models.Model):
    question = models.OneToOneField(Question,on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def __str__(self):
        return "Count {}".format(self.count)

