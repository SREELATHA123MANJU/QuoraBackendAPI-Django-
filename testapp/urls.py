
from django.urls import path,include
# import everything from views 
from testapp import views
  


urlpatterns = [ 
    path('register/',views.CreateUserView.as_view()),           #Signup a user
    path('login/',views.LoginView.as_view()),                   # Login user
    path('question/<slug:query>',views.Questioning.as_view()),     #Search query for questions using keywords  
    path('question/',views.Questioning.as_view()),                  #To get all the questions
    path('answer/',views.AnswersViewClass.as_view()),               #returnns [] if GET
    path('answer/<slug:qid>',views.AnswersViewClass.as_view()),         #answer/question_id wil give the answer for given quesion
    path('upvote/<int:aid>',views.upvote),                          # To vote for the answer
    path('user/questions/',views.questionsAskedByMe),      #questions asked by user
    path('user/answers/',views.anwersGivenByMe),              #answrs givn by me
    path('user/upvotes/',views.upvotesGivenByMe),     #upvotes givn by me
    path('upvote/user/<int:aid>',views.answerUpvotedUsers),      #users upvoted for an answer
    path('question/details/',views.questionDetails)                     #question regarding detail
]



  
