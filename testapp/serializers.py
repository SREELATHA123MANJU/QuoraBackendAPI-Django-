from rest_framework import serializers,exceptions
from django.contrib.auth import get_user_model,authenticate
from testapp.models import Question,Tower




class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    def create(self,Validated_data):
        user=get_user_model().objects.create(
            username=Validated_data['username']
            )
        user.set_password(Validated_data['password'])
        user.save()
        return user


    class Meta:
        model=get_user_model()
        fields=['username','password']

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self,data):
        username=data.get("username"," ")
        password=data.get("password"," ")
        if username and password:
                user=authenticate(username=username,password=password)
                if user:
                    if user.is_active:
                        data["user"]=user
                    else:
                        msg="user is deactivated."
                        raise exceptions.ValidationError(msg)
                else:
                    msg="unable to login with given credentials"
                    raise exceptions.ValidationError(msg)
        else:
                msg="Must provide username and password both"
                raise exceptions.ValidationError(msg)

        return data

    class Meta:
        fields=['username','password']

class QuestionSerializer(serializers.ModelSerializer):
     
    class Meta: 
        model = Question 
        fields = ('id','question','count')

    def create(self, validated_data):
        
        ques = Question(user = self.context["request"].user,question=validated_data['question'])
        ques.save()

        return ques 


#Class t return question object for given question id
class CustomForeignKeyField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        return self.queryset

    def to_representation(self, value):
        value = super().to_representation(value)
        question = Question.objects.get(pk=value)
        return QuestionSerializer(question).data

#cass to get all answers for the given question id
class CustomAnswerForeignKeyField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        return self.queryset

    def to_representation(self, value):
        value = super().to_representation(value)
        question = Question.objects.get(pk=value)
        return QuestionSerializer(question).data

class AnswersSerializer(serializers.ModelSerializer):

    question = CustomForeignKeyField(required=False, queryset=Question.objects.all() )



    class Meta: 
        model = Tower
        fields = ('id','question','answer','upvotes')

    def validate(self,data):
        valid_data = {}

        print(data['question'])
        if Question.objects.filter(id=data['question']).count() == 1 :
            print(Question.objects.filter(id=data['question']))
            valid_data['question'] = Question.objects.get(id=data['question'])
        else:
            msg="Question with gven id not found"
            raise exceptions.ValidationError(msg)
        
        if len(data['answer']) > 0:
            valid_data['answer'] = data['answer']
        else:
            msg="Question with gven id not found"
            raise exceptions.ValidationError(msg)
        
        
        return valid_data


    def create(self,data,user): 
            print(data['question'])
            ans =  Tower.objects.create(user = user, question = data['question'], answer = data['answer'])
            ans.save()
            return AnswersSerializer(ans).data

   


class AnswerQuestionSerializer(serializers.Serializer):
    class Meta:
        model = Tower
        fields = ('id','answer','upvotes')

        
      