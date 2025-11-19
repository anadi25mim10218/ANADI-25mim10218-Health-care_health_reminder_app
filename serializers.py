from rest_framework import serializers
from django.contrib.auth.models import User
from dataccess.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
# class DefUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('username','password')

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = [ 'exercise_code', 'exercise_name', 'instructions', 'level']


class DoctorExerciseSerializer(serializers.ModelSerializer):
    exercises = serializers.PrimaryKeyRelatedField(many=True, queryset = Exercise.objects.all())

    class Meta:
        model = Exercise
        fields = ['exerciseId', 'doctorId', 'exercises']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [ 'department', 'designation', 'hospital']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [ 'date_firstVisit', 'date_lastVisit']

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['department', 'designation', 'hospital']


class TreatmentSerializer(serializers.ModelSerializer):
    exercises = serializers.SlugRelatedField(
        many=True,
        queryset=Exercise.objects.all(),
        slug_field='exercise_name'
    )

    class Meta:
        model = Treatment
        fields = ['medicines', 'exercises', 'end_date']


class TreatmentSerializerForPatient(serializers.ModelSerializer):
    exercises = serializers.SlugRelatedField(
        many=True,
        queryset=Exercise.objects.all(),
        slug_field='exercise_name'
    )
    # doctorId = serializers.SerializerMethodField()
    # staff1 = serializers.SerializerMethodField()
    # staff2 = serializers.SerializerMethodField()
    class Meta:
        model = Treatment
        fields = ['treatmentId', 'doctorId', 'start_date', 'end_date', 'medicines', 'exercises', 'staff1', 'staff2']

    # def get_doctorId(self, obj):
    #     p = User.objects.get(username = obj.doctorId)
    #     return p.username

    # def get_doctorId(self, obj):
    #     dr = Doctor.objects.get(user = obj.doctorId)
    #     return dr.username
    # def get_staff1(self, obj):
    #     s1 = User.objects.get(username = obj.staff1)
    #     return s1.username

    # def get_staff2(self, obj):
    #     s1 = User.objects.get(username = obj.staff2)
    #     if s1!=Null:
    #         return s1.username


class TreatmentSerializerParticular(serializers.ModelSerializer):
    exercises = serializers.SlugRelatedField(
        many=True,
        queryset=Exercise.objects.all(),
        slug_field='exercise_name'
    )
    doctorId = serializers.SerializerMethodField()
    staff1 = serializers.SerializerMethodField()
    staff2 = serializers.SerializerMethodField()
    class Meta:
        model = Treatment
        fields = ['doctorId', 'start_date', 'end_date', 'medicines', 'exercises', 'staff1', 'staff2']

    def get_doctorId(self, obj):
        # p = User.objects.get(username = obj.doctorId)
        return obj.doctorId.user.username
    def get_staff1(self, obj):
        # s1 = User.objects.get(username = obj.staff1)
        return obj.staff1.user.username

    def get_staff2(self, obj):
        # s1 = User.objects.get(username = obj.staff2)
        return obj.staff2.user.username

class PatientRelativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['relative1', 'relative2', 'relative3']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['userId', 'treatmentId']

class GetNotificationSerializer(serializers.ModelSerializer):
    patientId = serializers.SerializerMethodField()
    class Meta:
        model = Notification
        fields = ['treatmentId', 'patientId', 'dateNotified']

    def get_patientId(self, obj):
        # p = User.objects.get(username=obj.patientId)
        return obj.patientId.user.username

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['treatmentId', 'confirmationFromRelative1', 'markAsDone']

class TreatmentSerializerForDoctor(serializers.ModelSerializer):
    exercises = serializers.SlugRelatedField(
        many=True,
        queryset=Exercise.objects.all(),
        slug_field='exercise_name'
    )
    patientId = serializers.SerializerMethodField()
    class Meta:
        model = Treatment
        fields = ['treatmentId', 'patientId', 'start_date', 'end_date', 'medicines', 'exercises', 'staff1', 'staff2']
    def get_patientId(self, obj):
        # p = User.objects.get(id=obj.patientId)
        return obj.patientId.user.id



class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['treatmentId', 'date', 'markAsDone']

class Userwa(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']