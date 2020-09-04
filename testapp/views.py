from rest_framework.permissions import AllowAny,IsAuthenticated
from testapp.serializers import UserSerializer,LoginSerializer
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model,login as django_login
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from testapp.models import Question,Tower
from testapp.serializers import QuestionSerializer,AnswersSerializer,AnswerQuestionSerializer
from django.db.models import Max
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt



from rest_framework.mixins import ListModelMixin,CreateModelMixin
from rest_framework.generics import GenericAPIView,ListAPIView,CreateAPIView

import datetime


class CreateUserView(CreateAPIView):
    model=get_user_model()
    permission_classes = [AllowAny]
    serializer_class=UserSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data["user"]
        django_login(request,user)
        token,created=Token.objects.get_or_create(user=user)
        return Response({"token":token.key},status=200)  

    
  

class UserViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
 
    serializer_class = AnswersSerializer

    queryset = Tower.objects.all()


class Questioning(ListAPIView,CreateAPIView,GenericAPIView):

    permission_classes=[IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    model = Question
            
    def get_queryset(self): 
        print(self.kwargs)
        if len(self.kwargs) == 0:
            return Question.objects.all()
        else:

            return Question.objects.filter(question__icontains = self.kwargs['query'])


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class AnswersViewClass(ListAPIView,GenericAPIView):

    model = Tower
    queryset = Tower.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class = AnswersSerializer

    def get_queryset(self):
        
        if len(self.kwargs) > 0:
            return Tower.objects.filter(question__id=self.kwargs['qid'])
        
        return Tower.objects.filter(question__id=0)

    
    
    def post(self,request, *args, **kwargs):
        print(request.data)
        serializer_class = AnswersSerializer(request,data=request.data)
        print('seri done')
        data = serializer_class.validate(request.data)
        print(data)
        ans = serializer_class.create(data,request.user) 
        return Response(ans)


from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def upvote(request,aid):
    # if answer id is not found
    if Tower.objects.filter(id=aid).count() == 0:
        return Response({'message':'Answer id not found'},status=400)
    
    ans = Tower.objects.get(id=aid)
    #Check if he user have already upvoted the answer
    if User.objects.get(username = request.user) in ans.upvotes.all():
        return Response({'message':'Already voted'},status=201)

    question = ans.question
    question.count = question.count + 1
    question.save()
    
    ans.upvotes.add(User.objects.get(username=request.user))
    ans.save()

    return Response({'status':'Success'},status=200)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def questionsAskedByMe(request):
    user = User.objects.get(username = request.user)
    data = [QuestionSerializer(i).data for i in user.user_question.all()]  
    return Response({'data':data})


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def anwersGivenByMe(request):
    user = User.objects.get(username = request.user)
    data = [AnswersSerializer(i).data for i in user.user_answer.all()]
    return Response(data={'data':data})


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def upvotesGivenByMe(request):
    user = User.objects.get(username = request.user)
    data = [AnswersSerializer(i).data for i in  user.likes.all()] 
    return Response(data={'code':data})    



@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def  answerUpvotedUsers(request,aid):
    # aid is Answer id
    if Tower.objects.filter(id=aid).count() == 0:
        return Response({'message':'Sorry, Answer id is not found'},status=400)
    
    data = [i.username for i in Tower.objects.get(id=aid).upvotes.all()]
    return Response(data={'users':data})



@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def  questionDetails(request):
    overall = Question.objects.all().aggregate(Max('count'))['count__max']
    amongAll = [QuestionSerializer(i).data  for i in Question.objects.filter(count = overall)]
   
    now = datetime.datetime.now()
    earlier = now - datetime.timedelta(hours=1)
    last_hour = Question.objects.filter(date_time__range=(earlier,now)).aggregate(Max('count'))['count__max']
    
    LastHour = None

    if Question.objects.filter(count = last_hour).count() > 0  :
        LastHour = QuestionSerializer(Question.objects.filter(count = last_hour)).data 
    
    return Response(data={'last_hour':LastHour,'overall':amongAll})




 