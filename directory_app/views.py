from django.shortcuts import render, redirect
from .models import Teacher , Subject
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .resources import SubjectResource,TeacherResource
from tablib import Dataset
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage

@login_required(login_url="/login/")
def index(request):
    teachers_record = []
    teachers = Teacher.objects.all()
    available_subjects = Subject.objects.all()
    for teacher in teachers:
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
        teachers_record.append(teacher_rec)
    # print(teachers_record)
    return render(request,"index.html",{"records":teachers_record,"available_subjects":available_subjects})

@login_required(login_url="/login/")
def delete_teacher(request,id):
    # print(id,"--------------")
    Teacher.objects.filter(id=id).delete()

    # teachers_record = []
    # teachers = Teacher.objects.all()
    # for teacher in teachers:
    #     teacher_rec = {}
    #     teacher_rec["id"] = teacher.id
    #     teacher_rec["first_name"] = teacher.first_name
    #     teacher_rec["last_name"] = teacher.last_name
    #     teacher_rec["email_address"] = teacher.email_address
    #     teacher_rec["phone_number"] = teacher.phone_number
    #     teacher_rec["room_number"] = teacher.room_number
    #     teacher_rec["profile_picture"] = teacher.profile_picture
    #     subject_list = ", ".join([x.subject_name for x in teacher.subjects_taught.all()])
    #     teacher_rec["subjects_taught"] = subject_list
    #     teachers_record.append(teacher_rec)
    # print(teachers_record)
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
                messages.warning(request, "Not allowed select more than 5 subjects")
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

            record.subjects_taught.set(subjects_id)

            image = request.FILES["image"]
            fss = FileSystemStorage()
            fss.save(image.name,image)
            record.profile_picture = image.name
            record.save()

            messages.success(request,"Record Successfully Saved")
        except Exception as e:
            print(e)
            messages.warning(request, "Error In Saving Record")
            return render(request, "add_teacher.html", {'available_subjects': available_subjects,'record':form_data})

        return redirect("index")

