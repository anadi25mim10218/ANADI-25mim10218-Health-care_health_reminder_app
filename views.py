from django.shortcuts import render          # 
from dataccess.serializers import *     
from rest_framework.views import APIView
from rest_framework import status, generics, permissions, views, authentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from dataccess.permissions import IsOwnerOrReadOnly, IsDoctor, IsStaffMember
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

class RegisterUser(views.APIView):
    permision_classes = []
    authentication_classes = []
    def get(request, format=None):
        user = User.objects.all()
        serializer = UserSerializer(user,many=True)
        return Response(serializer.data)

    # @csrf_exempt    
    def post(self, request, format=None):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def exercise_list(request, format=None):
    if request.method == 'GET':
        exes = Exercise.objects.all()
        serializer = ExerciseSerializer(exes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request)
        data = JSONParser().parse(request)
        serializer = ExerciseSerializer(data = data)
        if serializer.is_valid():
            dr = Doctor.objects.get(user=request.user)
            serializer.save(doctorId=dr)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def exercise_detail(request, pk, format=None):

    try:
        ex = Exercise.objects.get(pk=pk)
    except Exercise.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExerciseSerializer(ex)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ExerciseSerializer(ex, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ex.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorExerciseList(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsDoctor, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(doctorId=self.request.user)

class DoctorExerciseDetail(generics.RetrieveAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsDoctor, IsOwnerOrReadOnly]

class CreateDoctor(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsDoctor]
    def post(instance, request, format=None):
        print(request)
        data = JSONParser().parse(request)
        serializer = DoctorSerializer(data = data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateStaff(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsStaffMember]
    def post(instance, request, format=None):
        print(request)
        data = JSONParser().parse(request)
        serializer = StaffSerializer(data = data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePatient(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def post(instance, request, format=None):
        print(request)
        data = JSONParser().parse(request)
        serializer = PatientSerializer(data = data)
        if serializer.is_valid():
            r1 = None
            r2 = None
            r3 = None
            if data['relative1'] != None:
                r1 = User.objects.get(username=data['relative1'])
            if data['relative2'] != None:
                r2 = User.objects.get(username=data['relative2'])
            if data['relative3'] != None:
                r3 = User.objects.get(username=data['relative3'])
            serializer.save(user=request.user, relative1 = r1, relative2=r2, relative3=r3)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    permision_classes = []
    authentication_classes = []
    def post(self, request, format=None):
        print(request)
        data = request.data
        print(data)

        username = data.get('username', None)
        password = data.get('password', None)
        print(data, username, password)
        user = authenticate(username=username, password=password)
        content = {'status':"Invalid"}
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            print(token.key)
            content['token'] = token.key
            content['status']='Valid'
            return Response(content,status=status.HTTP_200_OK)

        return Response(content,status=status.HTTP_404_NOT_FOUND) 


@api_view(['GET', 'POST'])
def treatment_list(request):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsDoctor]
    print(request)
    if request.method == 'GET':
        uid = Doctor.objects.get(user__username = request.user)
        ts = Treatment.objects.filter(doctorId=uid)
        serializer = TreatmentSerializerForDoctor(ts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TreatmentSerializer(data = request.data)
        pi = Patient.objects.get(user__username = request.data['patientId'])
        di = Doctor.objects.get(user__username = request.user)

        s1=None
        s2=None
        if request.data['staff1']!=None:    
            s1 = Staff.objects.get(user__username = request.data['staff1'])

        if request.data['staff2']!=None:    
            s2 = Staff.objects.get(user__username = request.data['staff2'])

        d = timezone.now()

        if serializer.is_valid():
            serializer.save(doctorId=di, patientId=pi, start_date=d, staff1=s1, staff2=s2)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def treatment_list2(request):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsDoctor]
    uid = Doctor.objects.get(user__username=request.user)
    ts = Treatment.objects.filter(doctorId=uid)
    serializer = TreatmentSerializerForDoctor(ts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def treatment_listPatient(request):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    print(request)
    uid = Patient.objects.get(user__username = request.user)
    ts = Treatment.objects.filter(patientId=uid)
    serializer = TreatmentSerializerForPatient(ts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def treatment_patient(request, treatId):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    uid = Patient.objects.get(user__username = request.user)
    treatment = Treatment.objects.get(treatmentId = treatId, patientId=uid)
    serializer = TreatmentSerializerParticular(treatment)
    return Response(serializer.data)
    # if treatment.patientId == uid:
    #     return Response(serializer.data)
    # else:
    #     return Response(serializer.errors)


@api_view(['GET'])
def relatives_list(request):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    patient = Patient.objects.get(user__username = request.user)
    serializer = PatientRelativeSerializer(patient)
    return Response(serializer.data)

@api_view(['POST'])
def create_notification(request): 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer = NotificationSerializer(data = request.data) # uses id of relative
    patient = Patient.objects.get(user__username = request.user)
    datewa = timezone.now()
    if serializer.is_valid():
        serializer.save(patientId=patient, dateNotified=datewa)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def notification_list(request):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    uid = User.objects.get(username = request.user)
    dtoday = timezone.now()
    n = Notification.objects.filter(userId=uid, dateNotified=dtoday)
    serializer=GetNotificationSerializer(n, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_record(request):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer = RecordSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def treatment_doctor(request, treatId):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    uid = Doctor.objects.get(user__username = request.user)
    # treatment = Treatment.objects.get(treatmentId = treatId, doctorId=uid)
    # serializer = TreatmentSerializerForDoctor(treatment)
    rec = Record.objects.filter(treatmentId=treatId)
    serializer = RecordSerializer(rec, many=True)
    return Response(serializer.data)
    # if treatment.patientId == uid:
    #     return Response(serializer.data)
    # else:
    #     return Response(serializer.errors)

@api_view(['GET'])
def detail(request, userId):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    userwa = User.objects.get(id=userId)
    serializer = Userwa(userwa)