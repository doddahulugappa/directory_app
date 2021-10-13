from django.shortcuts import render, redirect
from .models import Teacher , Subject
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from .resources import SubjectResource,TeacherResource
from tablib import Dataset

@login_required(login_url="/login/")
def index(request):
    teachers_record = []
    teachers = Teacher.objects.all()
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
        teacher_rec["subjects_taught"] = subject_list
        teachers_record.append(teacher_rec)
    # print(teachers_record)
    return render(request,"index.html",{"records":teachers_record})

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



def export_popup(request):
    print("called pop up")
    return render(request,"export.html",{})

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

def upload_data(request):

    if request.method == 'POST':
        dataset = Dataset()

        if request.POST.get('upload') == "subjects":
            subject_resource = SubjectResource()
            new_subjects = request.FILES['myfile']

            imported_data = dataset.load(new_subjects.read().decode(),format='csv', headers=True)
            result = subject_resource.import_data(imported_data, dry_run=True)  # Test the data import

            if not result.has_errors():
                subject_resource.import_data(imported_data, dry_run=False)  # Actually import now

        if request.POST.get('upload') == "teachers":
            teacher_resource = TeacherResource()
            new_teachers = request.FILES['myfile']

            imported_data = dataset.load(new_teachers.read().decode(), format='csv', headers=True)
            result = teacher_resource.import_data(imported_data, dry_run=True)  # Test the data import

            if not result.has_errors():
                teacher_resource.import_data(imported_data, dry_run=False)  # Actually import now


        return redirect("index")
    else:
        return render(request,"import.html",{})
