from django.contrib import admin
from modules.jobPortalApp.models import JobUsersProfile, Skill, JobDetails, AddressDetails,AppliedJobs, ZoomMeetings, ZoomMeetingsUsers

# Register your models here.
admin.site.register(JobUsersProfile)
admin.site.register(Skill)
admin.site.register(JobDetails)
admin.site.register(AddressDetails)
admin.site.register(AppliedJobs)
admin.site.register(ZoomMeetings)
admin.site.register(ZoomMeetingsUsers)
