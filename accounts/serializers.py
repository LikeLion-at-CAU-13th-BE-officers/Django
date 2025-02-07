from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import User

# 회원가입용 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User

        # 필요한 필드값만 지정, 회원가입은 email까지 필요
        fields = ['username', 'email', 'password']
    
    # create() 재정의
    def create(self, validated_data):
    
        # 비밀번호 분리
        password = validated_data.pop('password')

        # user 객체 생성
        user = User(**validated_data)

        # 비밀번호는 해싱해서 저장
        user.set_password(password)
        user.save()

        return user
    
    # 이메일 유효성 검사 함수
    def validate_email(self, value):
        
        # 이메일 형식이 맞는지 검사
        if not "@" in value:
            raise serializers.ValidationError("Invalid email format")
        
        # 이메일 중복 여부 검사
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        
        return value


# 로그인용 시리얼라이저
class AuthSerializer(serializers.ModelSerializer):
    # 시리얼라이저 내부에서 username 필드 직접 정의해서 기존 모델 필드의 unique 옵션 적용X
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    class Meta:
        model = User

        # 로그인은 username과 password만 필요
        fields = ['username', 'password']

    # 로그인 유효성 검사 함수
    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
    
        user = User.get_user_by_username(username=username)

        if user is None:
            raise serializers.ValidationError("User does not exist.")
        else:
            if not user.check_password(password):
                raise serializers.ValidationError("Wrong password.")
        
        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            "user": user,
            "refresh_token": refresh_token,
            "access_token": access_token,
        }

        return data
    
class OAuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username','email']

    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)

        if email is None:
            raise serializers.ValidationError('Email does not exist.')
        
        user = User.get_user_by_email(email=email)
        
        # 존재하지 않는 회원이면 새롭게 가입
        if user is None:
            user = User.objects.create(username=username, email=email)

        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            "user": user,
            "refresh_token": refresh_token,
            "access_token": access_token,
        }

        return data

              
            
