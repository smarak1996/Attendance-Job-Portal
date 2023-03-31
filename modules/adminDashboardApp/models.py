from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.utils.crypto import get_random_string
from django.template.defaultfilters import slugify
import uuid


class EmployeeProfile(models.Model):
    GENDER = (
        ('Male', 'male'),
        ('Female', 'female')
    )
    gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=50, choices=GENDER, default='male')
    address = models.CharField(max_length=250)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    contact_number = models.BigIntegerField()

    def _get_unique_slug(self):
        slug = slugify(self.user.first_name[:40 - 2])
        unique_slug = slug
        num = 1
        while EmployeeProfile.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(EmployeeProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name


class Company(models.Model):
    gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)
    company_name = models.CharField(max_length=255)
    company_apartment_num = models.CharField(max_length=255, null=True)
    company_street = models.CharField(max_length=255, null=True)
    company_city = models.CharField(max_length=255, null=True)
    company_state = models.CharField(max_length=255, null=True)
    company_country = models.CharField(max_length=255, null=True)
    company_contact_number = models.BigIntegerField()
    company_email_address = models.EmailField(max_length=255, null=True)

    def _get_unique_slug(self):
        """
        Generate unique slug for the Company object.
        Used by the Company bject save method, while creating new Company
        """
        slug = slugify(self.company_name[:40 - 2])
        unique_slug = slug
        num = 1
        while Company.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.company_name


class Department(models.Model):
    department_choices = (
        ('hr', 'Hr'),
        ('backoffice', 'Backoffice'),
        ('developer', 'Developer'),
        ('designer', 'Designer'),
        ('business_development', 'Business_Development'),
        ('admin', 'Admin')

    )
    gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)
    department_name = models.CharField(
        max_length=250, choices=department_choices, default='hr')
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='employee')
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='company')

    def _get_unique_slug(self):
        """
        Generate unique slug for the Department object.
        Used by the Department bject save method, while creating new Department
        """
        slug = slugify(self.department_name[:40 - 2])
        unique_slug = slug
        num = 1
        while Department.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(Department, self).save(*args, **kwargs)

    def __str__(self):
        return self.employee.first_name + '(' + (self.department_name)+')'


class Attendance(models.Model):
    gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='employeeAttendance')
    date_time = models.DateTimeField(default=timezone.now, null=True)

    def _get_unique_slug(self):
        """
        Generate unique slug for the Attendance object.
        Used by the Attendance bject save method, while creating new Attendance
        """
        slug = slugify(self.employee.first_name[:40 - 2])
        unique_slug = slug
        num = 1
        while Attendance.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(Attendance, self).save(*args, **kwargs)

    def __str__(self):
        return self.employee.first_name


class Role(models.Model):
    gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)
    role_name = models.CharField(max_length=250)

    def _get_unique_slug(self):
        """
        Generate unique slug for the Role object.
        Used by the Role bject save method, while creating new Role
        """
        slug = slugify(self.role_name[:40 - 2])
        unique_slug = slug
        num = 1
        while Role.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(Role, self).save(*args, **kwargs)

    def __str__(self):
        return self.role_name


class EmployeeRole(models.Model):
    gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)
    emp_role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name='empRole')
    emp_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='empUser')

    def _get_unique_slug(self):
        """
        Generate unique slug for the EmployeeRole object.
        Used by the EmployeeRole object save method, while creating new EmployeeRole
        """
        slug = slugify(self.emp_role.role_name[:40 - 2])
        unique_slug = slug
        num = 1
        while EmployeeRole.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(EmployeeRole, self).save(*args, **kwargs)

    def __str__(self):
        return self.emp_role.role_name + " - " + self.emp_user.username


class AdminUserRoles(models.Model):
    gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="admin_user_role")
    roles = models.ForeignKey(
        Permission, on_delete=models.CASCADE, null=True, related_name='roles')

    def _get_unique_slug(self):
        """
        Generate unique slug for the AdminUserRoles object.
        Used by the AdminUserRoles bject save method, while creating new AdminUserRoles
        """
        slug = slugify(self.user.first_name[:40 - 2])
        unique_slug = slug
        num = 1
        while AdminUserRoles.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(AdminUserRoles, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name
