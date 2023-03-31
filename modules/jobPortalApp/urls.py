from django.urls import path
from modules.jobPortalApp.views import JobUserProfileCreateAPIView, JobUserProfileListAPIView, \
    JobUserProfileUpdateAPIView, JobUserProfileDeleteAPIView, SkillCreateAPIView, \
    SkillListAPIView, SkillUpdateAPIView, SkillDeleteAPIView, JobCreateAPIView, \
    JobListAPIView, JobDeleteAPIView, JobUpdateAPIView, AppliedJobsListAPIView,\
    AppliedJobsCreateAPIView, ZoomMeetingsCreateAPIView, ZoomMeetingsListAPIView,\
    ZoomMeetingsUpdateAPIView, ZoomMeetingsDeleteAPIView, ZoomMeetingsUsersCreateAPIView,\
    ZoomMeetingsUsersListAPIView, ZoomMeetingsUsersUpdateAPIView, ZoomMeetingsUsersDeleteAPIView, \
    ZoomLinkAPIView, StatusChangeAPIView, AppliedUsersAPIView, ZoomLinkIndividualAPIView

app_name = 'jobPortalApp'

urlpatterns = [
    path('jobprofile_create/', JobUserProfileCreateAPIView.as_view(),
         name='job_profile_create'),
    path('jobprofile_list/', JobUserProfileListAPIView.as_view(),
         name='job_profile_list'),
    path('jobprofile_update/<slug:slug>/',
         JobUserProfileUpdateAPIView.as_view(), name='job_profile_update'),
    path('jobprofile_delete/<slug:slug>/',
         JobUserProfileDeleteAPIView.as_view(), name='job_profile_delete'),
    path('skill_create/', SkillCreateAPIView.as_view(), name='skill_create'),
    path('skill_list/', SkillListAPIView.as_view(), name='skill_list'),
    path('skill_update/<slug:slug>/',
         SkillUpdateAPIView.as_view(), name='skill_update'),
    path('skill_delete/<slug:slug>/',
         SkillDeleteAPIView.as_view(), name='skill_delete'),
    path('job_create/', JobCreateAPIView.as_view(), name='job_create'),
    path('job_list/', JobListAPIView.as_view(), name='job_list'),
    path('job_delete/<slug:slug>/', JobDeleteAPIView.as_view(), name='job_delete'),
    path('job_update/<slug:slug>/', JobUpdateAPIView.as_view(), name='job_update'),
    path('apply_job_create/', AppliedJobsCreateAPIView.as_view(),
         name='applied_job_create'),
    path('apply_job_list/', AppliedJobsListAPIView.as_view(),
         name='applied_job_list'),
    path('zoom_meetings_create/', ZoomMeetingsCreateAPIView.as_view(),
         name='zoom_meetings_create'),
    path('zoom_meetings_list/', ZoomMeetingsListAPIView.as_view(),
         name='zoom_meetings_list'),
    path('zoom_meetings_update/<slug:slug>/',
         ZoomMeetingsUpdateAPIView.as_view(), name='zoom_meetings_update'),
    path('zoom_meetings_delete/<slug:slug>/',
         ZoomMeetingsDeleteAPIView.as_view(), name='zoom_meetings_delete'),
    path('zoom_meetingsusers_create/', ZoomMeetingsUsersCreateAPIView.as_view(),
         name='zoom_meetingsusers_create'),
    path('zoom_meetingsusers_list/', ZoomMeetingsUsersListAPIView.as_view(),
         name='zoom_meetingsusers_list'),
    path('zoom_meetingsusers_update/<slug:slug>/',
         ZoomMeetingsUsersUpdateAPIView.as_view(), name='zoom_meetingsusers_update'),
    path('zoom_meetingsusers_delete/<slug:slug>/',
         ZoomMeetingsUsersDeleteAPIView.as_view(), name='zoom_meetingsusers_delete'),
    path('zoom_link/', ZoomLinkAPIView.as_view(), name='zoom_link'),
    path('status_change/<slug:slug>/',
         StatusChangeAPIView.as_view(), name='status_change'),
    path('applied_users/<slug:slug>/',
         AppliedUsersAPIView.as_view(), name='applied_users'),
    path('zoom_link_individual/<slug:slug>/',
         ZoomLinkIndividualAPIView.as_view(), name='zoom_link_individual')
]
