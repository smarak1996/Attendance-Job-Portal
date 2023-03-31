from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import uuid
from django.utils import timezone
from modules.adminDashboardApp.models import Company, EmployeeRole
# Create your models here.

CHOICES = (
	('Full Time', 'Full Time'),
	('Part Time', 'Part Time'),
	('Internship', 'Internship'),
	('Remote', 'Remote'),
)


class JobUsersProfile(models.Model):
	gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	slug = models.SlugField( unique=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='job_profile')
	resume = models.FileField(upload_to='resumes', null=True, blank=True)
	higer_secondary_year = models.IntegerField(blank=True)
	secondary_year = models.IntegerField(blank=True)
	grad_year = models.IntegerField(blank=True)
	post_grad_year = models.IntegerField(blank=True)
	looking_for = models.CharField(max_length=30, choices=CHOICES, default='Full Time', null=True)

	def _get_unique_slug(self):
		slug = slugify(self.user.first_name[:40 - 2])
		unique_slug = slug
		num = 1
		while JobUsersProfile.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug=self._get_unique_slug()
		super(JobUsersProfile,self).save(*args,**kwargs)
	
	def __str__(self):
		return self.user.first_name

class Skill(models.Model):
	gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	slug = models.SlugField( unique=True)
	skill = models.CharField(max_length=200)
	user = models.ForeignKey(User, related_name='skills', on_delete=models.CASCADE)

	def _get_unique_slug(self):
		slug = slugify(self.user.first_name[:40 - 2])
		unique_slug = slug
		num = 1
		while Skill.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug=self._get_unique_slug()
		super(Skill,self).save(*args,**kwargs)
	
	def __str__(self):
		return self.user.first_name + ' ' + self.skill


class AddressDetails(models.Model):
	gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	slug = models.SlugField( unique=True)
	street = models.CharField(max_length=255, null=True)
	city = models.CharField(max_length=255, null=True)
	state = models.CharField(max_length=255, null=True)
	country = models.CharField(max_length=255, null=True)
	pincode = models.CharField(max_length=255, null=True)


	def _get_unique_slug(self):
		slug = slugify(self.street[:40 - 2])
		unique_slug = slug
		num = 1
		while AddressDetails.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug=self._get_unique_slug()
		super(AddressDetails,self).save(*args,**kwargs)
	
	def __str__(self):
		return self.street + ' ' + self.city

class JobDetails(models.Model):
	gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	slug = models.SlugField( unique=True)
	company = models.ForeignKey(Company, related_name='Company_job', on_delete=models.CASCADE)
	job_title = models.CharField(max_length=255, null=True)
	job_description = models.CharField(max_length=600, null=True)
	experiance = models.CharField(max_length=255, null=True)
	salary = models.CharField(max_length=255, null=True)
	address = models.ForeignKey(AddressDetails, on_delete=models.CASCADE)
	hiring_members = models.BigIntegerField()
	industry_type = models.CharField(max_length=255, null=True)
	employement_type = models.CharField(max_length=30, choices=CHOICES, default='Full Time', null=True)
	qualification = models.CharField(max_length=255, null=True)
	job_creator = models.ForeignKey(EmployeeRole, related_name='jobdetails_creator', on_delete=models.CASCADE)

	def _get_unique_slug(self):
		slug = slugify(self.company.company_name[:40 - 2])
		unique_slug = slug
		num = 1
		while JobDetails.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug=self._get_unique_slug()
		super(JobDetails,self).save(*args,**kwargs)
	
	def __str__(self):
		return self.company.company_name + " - " + self.job_title


class AppliedJobs(models.Model):
	CHOICE = (
		('Pending', 'Pending'),
		('Completed', 'Completed'),
		('Selected', 'Selected')
	)
	gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	slug = models.SlugField( unique=True)
	job = models.ForeignKey(JobDetails, related_name='applied_job', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='applied_user', on_delete=models.CASCADE)
	date_posted = models.DateTimeField(default=timezone.now)
	status = models.CharField(max_length=30, choices=CHOICE, default='Pending', null=True)
	users_profile = models.ForeignKey(JobUsersProfile, related_name='user_job', on_delete=models.CASCADE, default=None )
	mail_id = models.EmailField(null=True, blank=True)

	def _get_unique_slug(self):
		slug = slugify(self.job.job_title[:40 - 2])
		unique_slug = slug
		num = 1
		while AppliedJobs.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug=self._get_unique_slug()
		super(AppliedJobs,self).save(*args,**kwargs)
	
	def __str__(self):
		return self.job.job_title + " - " + self.user.username


class ZoomMeetings(models.Model):
	gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	slug = models.SlugField( unique=True)
	meeting_topic = models.CharField(max_length=255)
	meeting_date = models.DateField()
	meeting_time = models.TimeField()
	meeting_duration = models.CharField(max_length=100)
	meeting_zoom_link = models.CharField(max_length=600, null=True)
	meeting_zoom_password = models.CharField(max_length=255, null=True)

	def _get_unique_slug(self):
		slug = slugify(self.meeting_topic[:40 - 2])
		unique_slug = slug
		num = 1
		while ZoomMeetings.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug=self._get_unique_slug()
		super(ZoomMeetings,self).save(*args,**kwargs)
	
	def __str__(self):
		return self.meeting_topic

class ZoomMeetingsUsers(models.Model):
	status_choice = (
		('complete', 'Completed'),
		('pending', 'Pending'),
		('cancel', 'Canceled')
	)
	gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	slug = models.SlugField( unique=True)
	zoom_meeting = models.ForeignKey(ZoomMeetings, related_name='zoom_meetings', on_delete=models.CASCADE)
	status = models.CharField(max_length=250, choices=status_choice, default='pending')
	mail_send = models.BooleanField(default=False)
	message = models.CharField(max_length=355, null=True)
	jobs = models.ForeignKey(AppliedJobs, related_name='applied_job', on_delete=models.CASCADE)

	def _get_unique_slug(self):
		slug = slugify(self.message[:40 - 2])
		unique_slug = slug
		num = 1
		while ZoomMeetingsUsers.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug=self._get_unique_slug()
		super(ZoomMeetingsUsers,self).save(*args,**kwargs)
	
	def __str__(self):
		return self.message