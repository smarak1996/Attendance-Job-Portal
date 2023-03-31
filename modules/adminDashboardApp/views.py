from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from modules.adminDashboardApp.models import EmployeeProfile, Company, Department
from modules.adminDashboardApp.serializers import EmployeeProfileSerializer, CompanySerializer, DepartmentSerializer
from rest_framework.views import APIView
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from django.views import View
from weasyprint import HTML, CSS
# import weasyprint
import os

from rest_framework.views import APIView
# from weasyprint import HTML, CSS
# Create your views here.


class EmployeeProfileList(generics.ListCreateAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender']


class EmployeeProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'


class CompanyCreateList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company_name']


class CompanyRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'


class DepartmentCreateList(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department_name']


class DepartmentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'


class JoinLetterAPIView(APIView):
    def get(self, request):
        return render(request, 'joiningLetter/join.html')

# class ConvertPdfAPIView(View):
#     def post(self, request):
#         this_folder = settings.PROJECT_DIR
#         context = {
#             'emp_name': request.POST['emp_name'],
#             'date': request.POST['date'],
#             'position': request.POST['position'],
#             'location': request.POST['location'],
#             'pre_company': request.POST['pre_company'],
#             'guardian': request.POST['guardian'],
#             'image_path':  'file://' + os.path.join(this_folder, 'static', 'images', 'webkrone.png')
#         }
#         html = render_to_string('joiningLetter/pdf_change.html', context)
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'inline:filename= "{}.pdf"'.format(
#             "name")
#         weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
#             CSS(string='body { font-size: 13px }')])
#         return response


class ConvertPdfAPIView(APIView):
    def post(self, request):
        this_folder = settings.PROJECT_DIR
        context = {
            'emp_name': request.data['emp_name'],
            'date': request.data['date'],
            'position': request.data['position'],
            'location': request.data['location'],
            'pre_company': request.data['pre_company'],
            'guardian': request.data['guardian'],
            'image_path': 'file://' + os.path.join(this_folder, 'static', 'images', 'webkrone.png')
        }
        html = render_to_string('joiningLetter/pdf_change.html', context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline:filename= "{}.pdf"'.format(
            "name")
        HTML(string=html).write_pdf(response, stylesheets=[
            CSS(string='body { font-size: 13px }')])
        return response
