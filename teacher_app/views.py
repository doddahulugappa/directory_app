from django.shortcuts import render, HttpResponse
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.shortcuts import render, redirect
from .models import Teacher , Subject
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .resources import SubjectResource,TeacherResource
from tablib import Dataset
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from urllib.parse import unquote
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import serializers
import jwt, datetime

from .tasks import test_func

# Create your views here.

def test(request):
    test_func.delay()
    return HttpResponse("Done")

def run_program_on_schedule(request):
    schedule, created =  CrontabSchedule.objects.get_or_create(hour=10, minute=17)
    task = PeriodicTask.objects.create(crontab=schedule,name="add subject-2",task='main_app.tasks.insert_record')
    return HttpResponse("Program Ran")



@login_required(login_url="/login/")
def index(request):
    teachers_record = []
    available_subjects = Subject.objects.all()
    first_names = []
    last_names = []
    teachers = Teacher.objects.all()
    for teacher in teachers:
        if teacher.first_name not in first_names:
            first_names.append(teacher.first_name)
        if teacher.last_name not in last_names:
            last_names.append(teacher.last_name)

    q = unquote(request.META['QUERY_STRING'])
    if q != "":
        key, value = q.split("=")
        if 'first_name' == key:
            teachers = Teacher.objects.filter(
                Q(first_name__exact=value)
            )
        elif 'last_name' == key:
            teachers = Teacher.objects.filter(
                Q(last_name__exact=value)
            )
        elif 'subjects_taught' in key:
            teachers = Teacher.objects.filter(
                Q(subjects_taught__id__exact=value)
            )


    if request.method == "POST":
        searchquery = request.POST.get("searchquery","")
        teachers = Teacher.objects.filter(
            Q(first_name__icontains=searchquery) |
            Q(last_name__icontains=searchquery) |
            Q(phone_number__icontains=searchquery) |
            Q(email_address__icontains=searchquery)
        )




    for teacher in teachers:
        teacher_rec = {}
        teacher_rec["id"] = teacher.id
        teacher_rec["first_name"] = teacher.first_name
        if teacher.first_name not in first_names:
            first_names.append(teacher.first_name)
        teacher_rec["last_name"] = teacher.last_name
        if teacher.last_name not in last_names:
            last_names.append(teacher.last_name)
        teacher_rec["email_address"] = teacher.email_address
        teacher_rec["phone_number"] = teacher.phone_number
        teacher_rec["room_number"] = teacher.room_number
        teacher_rec["profile_picture"] = teacher.profile_picture
        subject_list = ", ".join([x.subject_name for x in teacher.subjects_taught.all()])
        subjects = [x.subject_name for x in teacher.subjects_taught.all()]
        teacher_rec["subjects_taught"] = subject_list
        teacher_rec["subjects"] = subjects
        teachers_record.append(teacher_rec)
    # print(teachers_record)
    return render(request,"index.html",{"records":teachers_record,
                                        "available_subjects":available_subjects,
                                        "first_names":first_names,
                                        "last_names":last_names})

@login_required(login_url="/login/")
def delete_teacher(request,id):
    try:
        Teacher.objects.filter(id=id).delete()
        messages.success(request,"Deleted Successfully")
    except Exception as e:
        print(e)
        messages.warning(request, "Error in Deletion")

    return redirect('index')


@login_required(login_url="/login/")
def export_popup(request):
    print("called pop up")
    return render(request,"export.html",{})

@login_required(login_url="/login/")
def export_data(request):
    print("called download")
    if request.method == 'POST':
        if request.POST.get('download') == "subjects":
            subject_resource = SubjectResource()
            dataset = subject_resource.export()
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="subjects.csv"'
            return response

        if request.POST.get('download') == "teachers":
            teacher_resource = TeacherResource()
            dataset = teacher_resource.export()
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="teachers.csv"'
            return response

@login_required(login_url="/login/")
def upload_data(request):

    if request.method == 'POST':
        dataset = Dataset()
        print(request.POST.get('upload'),"=================")

        if request.POST.get('upload') == "subjects":
            subject_resource = SubjectResource()
            new_subjects = request.FILES['myfile']

            imported_data = dataset.load(new_subjects.read().decode(),format='csv', headers=True)
            result = subject_resource.import_data(imported_data, dry_run=True)  # Test the data import

            if not result.has_errors():
                subject_resource.import_data(imported_data, dry_run=False)  # Actually import now
                messages.success(request, "Imported Subjects Sucessfully")
            else:
                messages.warning(request, "Error in Importing Subjects")


            return redirect("subject_list")

        if request.POST.get('upload') == "teachers":
            teacher_resource = TeacherResource()
            new_teachers = request.FILES['myfile']

            imported_data = dataset.load(new_teachers.read().decode(), format='csv', headers=True)
            result = teacher_resource.import_data(imported_data, dry_run=True)  # Test the data import

            if not result.has_errors():
                teacher_resource.import_data(imported_data, dry_run=False)  # Actually import now
                messages.success(request, "Imported Teachers Sucessfully")
            else:
                messages.warning(request, "Error in Importing Teachers")

            return redirect("index")
    else:
        return render(request,"import.html",{})

@login_required(login_url="/login/")
def edit_teacher(request,id):
    teacher = Teacher.objects.get(id=id)
    teacher_rec = {}
    teacher_rec["id"] = teacher.id
    teacher_rec["first_name"] = teacher.first_name
    teacher_rec["last_name"] = teacher.last_name
    teacher_rec["email_address"] = teacher.email_address
    teacher_rec["phone_number"] = teacher.phone_number
    teacher_rec["room_number"] = teacher.room_number
    teacher_rec["profile_picture"] = teacher.profile_picture
    subject_list = ", ".join([x.subject_name for x in teacher.subjects_taught.all()])
    subjects = [x.subject_name for x in teacher.subjects_taught.all()]
    teacher_rec["subjects_taught"] = subject_list
    teacher_rec["subjects"] = subjects

    available_subjects = Subject.objects.all()
    if request.method == 'GET':
        return render(request,"teacher_details.html",{"record":teacher_rec,"available_subjects":available_subjects})
    if request.method == 'POST':
        try:
            first_name = request.POST.get("first_name","")
            last_name = request.POST.get("last_name","")
            email_address = request.POST.get("email","")
            room_number = request.POST.get("room","")
            phone_number = request.POST.get("phone","")
            subjects_id = request.POST.getlist('subjects')
            subjects_id = list(map(int,subjects_id))
            teacher = Teacher.objects.get(id=id)
            teacher.first_name = first_name
            teacher.last_name = last_name
            teacher.email_address = email_address
            teacher.room_number = room_number
            teacher.phone_number = phone_number
            if len(subjects_id) > 5:
                messages.warning(request, "Not allowed to select more than 5 subjects")
                return render(request,"teacher_details.html",{"record":teacher_rec,"available_subjects":available_subjects})
            teacher.subjects_taught.set(subjects_id)
            try:
                image = request.FILES["image"]
                fss = FileSystemStorage()
                fss.save(image.name, image)
                teacher.profile_picture = image.name
            except Exception as e:
                print(e)
            teacher.save()
            messages.success(request,"Record Successfully Updated")
        except Exception as e:
            print(e)
            messages.warning(request, "Error In Updating Record")

        return redirect("index")

@login_required(login_url="/login/")
def add_teacher(request):
    available_subjects = Subject.objects.all()
    if request.method == 'GET':

        return render(request, "add_teacher.html",{'available_subjects':available_subjects})

    if request.method == 'POST':
        print("Add Teacher Called")
        try:
            first_name = request.POST.get("first_name","")
            last_name = request.POST.get("last_name","")
            email_address = request.POST.get("email","")
            room_number = request.POST.get("room","")
            phone_number = request.POST.get("phone","")
            subjects_id = request.POST.getlist('subjects')
            subjects_id = list(map(int,subjects_id))

            form_data = {
                "first_name":first_name,
                "last_name":last_name,
                "email_address":email_address,
                "room_number":room_number,
                "phone_number":phone_number,
                "subjects_id":subjects_id
            }

            if Teacher.objects.filter(email_address=email_address).exists():
                messages.warning(request, "Email Already exists.")
                raise ValidationError('Email already exists.')



            record = Teacher.objects.create(
            first_name = first_name,
            last_name = last_name,
            email_address = email_address,
            room_number = room_number,
            phone_number = phone_number,

            )
            if len(subjects_id) > 5:
                messages.warning(request, "Error In Saving Record")

                messages.warning(request, "Not allowed to select more than 5 subjects")
                return render(request, "add_teacher.html",
                              {'available_subjects': available_subjects, 'record': form_data})

            record.subjects_taught.set(subjects_id)
            try:
                image = request.FILES["image"]
                fss = FileSystemStorage()
                fss.save(image.name,image)
                record.profile_picture = image.name
            except Exception as e:
                print(e)
            record.save()

            messages.success(request,"Record Successfully Saved")
        except Exception as e:
            print(e)
            messages.warning(request, "Error In Saving Record")
            return render(request, "add_teacher.html", {'available_subjects': available_subjects,'record':form_data})

        return redirect("index")

@login_required(login_url="/login/")
def subject_list(request):
    records = Subject.objects.all()
    subjects = Subject.objects.all()
    q = unquote(request.META['QUERY_STRING'])
    if q != "":
        key, value = q.split("=")
        records = Subject.objects.filter(
            Q(subject_name__exact=value)
        )

    if request.method == "POST":
        searchquery = request.POST.get("searchquery","")
        records = Subject.objects.filter(subject_name__icontains=searchquery)

    return render(request,"subjects.html",{"records":records,"subjects":subjects})

@login_required(login_url="/login/")
def add_subject(request):
    records = Subject.objects.all()
    if request.method == 'GET':
        return render(request, "add_subject.html", {})

    if request.method == 'POST':
        print("Add Subject Called")
        try:
            subject_name = request.POST.get("subject_name", "")

            if Subject.objects.filter(subject_name=subject_name).exists():
                messages.warning(request, "Subject Already exists.")
                raise ValidationError('Subject already exists.')

            record = Subject.objects.create(
                subject_name=subject_name
            )
            record.save()

            messages.success(request, "Record Successfully Saved")
        except Exception as e:
            print(e)
            messages.warning(request, "Error In Saving Record")
            return render(request, "add_subject.html", {"subject":subject_name})


    return redirect('subject_list')

@login_required(login_url="/login/")
def edit_subject(request,id):
    subject = Subject.objects.get(id=id)
    if request.method == "GET":
        return render(request,"subject_details.html",{"record":subject})

    if request.method == "POST":
        try:
            subject_name = request.POST.get("subject_name","")
            subject.subject_name = subject_name
            subject.save()
            messages.success(request,"Updated Successfully")
        except Exception as e:
            print(e)
            messages.warning(request, "Error in Updating")

        return redirect("subject_list")



    # return render(request,"subjects.html",{"records":records})

@login_required(login_url="/login/")
def delete_subject(request,id):
    try:
        Subject.objects.filter(id=id).delete()
        messages.success(request,"Deleted Successfully")
    except Exception as e:
        print(e)
        messages.warning(request,"Error in deletion")

    return redirect("subject_list")


class LoginView(APIView):
    def post(self,request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()
        if user is None:
            print("username is none")
            raise AuthenticationFailed("Incorrect Username")

        if not user.check_password(password):
            print("password error")
            raise AuthenticationFailed("Incorrect Password")

        payload = {
            "id":user.id,
            "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=3),
            "iat":datetime.datetime.utcnow()

        }

        token = jwt.encode(payload,'secret',algorithm='HS256').decode('utf-8')

        response = Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data = {"token":token}


        return response

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

class UserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("UnAuthenticated")

        try:
            payload = jwt.decode(token,'secret',algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("UnAuthenticated")

        user = User.objects.filter(id=payload["id"]).first()
        serializer1 = UserSerializer(user)
        return Response(serializer1.data)

class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message":"Logged Out Successfully"
        }

        return response
