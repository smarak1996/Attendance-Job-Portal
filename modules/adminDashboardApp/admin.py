from django.contrib import admin
from modules.adminDashboardApp.models import EmployeeProfile, Company, Department, Attendance, Role, EmployeeRole, AdminUserRoles
# Register your models here.
admin.site.register(EmployeeProfile)
admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Attendance)
admin.site.register(Role)
admin.site.register(EmployeeRole)
admin.site.register(AdminUserRoles)