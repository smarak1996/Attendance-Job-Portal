from rest_framework import serializers
from modules.adminDashboardApp.models import EmployeeProfile, Company, Department, Attendance, Role, EmployeeRole, AdminUserRoles
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.utils import timezone

class EmployeeProfileSerializer(serializers.ModelSerializer):
    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError("Employee must be 18 or older.")
        return value
    
    class Meta:
        model = EmployeeProfile
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    def validate_company_contact_number(self, value):
        if len(str(value)) != 10:
            raise serializers.ValidationError("Contact number should be of 10 digits.")
        return value
    
    def validate_company_email_address(self, value):
        validate_email(value)
        return value
    
    class Meta:
        model = Company
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    def validate_department_name(self, value):
        valid_names = [choice[0] for choice in Department.department_choices]
        if value not in valid_names:
            raise serializers.ValidationError("Invalid department name.")
        return value
    
    class Meta:
        model = Department
        fields = '__all__'
        

class AttendanceSerializer(serializers.ModelSerializer):
    def validate_date_time(self, value):
        if value > timezone.now():
            raise serializers.ValidationError("Attendance cannot be in the future.")
        return value
    
    class Meta:
        model = Attendance
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['gid', 'slug', 'role_name']


class EmployeeRoleSerializer(serializers.ModelSerializer):
    emp_role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    emp_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = EmployeeRole
        fields = ['gid', 'slug', 'emp_role', 'emp_user']


class AdminUserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUserRoles
        fields = ['gid', 'slug', 'user', 'roles']