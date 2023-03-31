from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from modules.jobPortalApp.serializers import JobUsersProfileSerializer, SkillSerializer, JobDetailsSerializer, AddressDetailsSerializer, AppliedJobsSerializer, ZoomMeetingsSerializer, ZoomMeetingsUsersSerializer, StatusChangeSerializer
from modules.jobPortalApp.models import JobUsersProfile, Skill, AddressDetails, JobDetails, AppliedJobs, ZoomMeetings, ZoomMeetingsUsers
from modules.adminDashboardApp.models import EmployeeRole
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.mail import send_mail
from zoomus import ZoomClient
from django.conf import settings
from datetime import datetime

# Create views here.


class JobUserProfileCreateAPIView(APIView):
    """
    User can add the profile for getting jobs.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = JobUsersProfileSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobUserProfileListAPIView(APIView):
    """
    API endpoints thats allow to view list of job profiles.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = JobUsersProfileSerializer

    def get(self, request):
        job_profiles = JobUsersProfile.objects.all()
        serializer = self.serializer_class(job_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobUserProfileUpdateAPIView(APIView):
    """
    User can edit the profile for getting jobs.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = JobUsersProfileSerializer

    def get_object(self, slug):
        try:
            return JobUsersProfile.objects.get(slug=slug)
        except JobUsersProfile.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        job_profile = self.get_object(slug)
        serializer = JobUsersProfileSerializer(job_profile)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        job_user_profile = self.get_object(slug)
        serializer = JobUsersProfileSerializer(
            job_user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobUserProfileDeleteAPIView(APIView):
    """
    User can delete their profile for getting jobs.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = JobUsersProfileSerializer

    def get_object(self, slug):
        try:
            return JobUsersProfile.objects.get(slug=slug)
        except JobUsersProfile.DoesNotExist:
            raise Http404

    def delete(self, request, slug, format=None):
        job_user_profile = self.get_object(slug)
        job_user_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SkillCreateAPIView(APIView):
    """
    User can add his/her skills.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SkillSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,  context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SkillListAPIView(APIView):
    """
    API endpoints thats allow to view list of skills.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SkillSerializer

    def get(self, request):
        job_profiles = Skill.objects.all()
        serializer = self.serializer_class(job_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SkillUpdateAPIView(APIView):
    """
    User can edit the skills.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SkillSerializer

    def get_object(self, slug):
        try:
            return Skill.objects.get(slug=slug)
        except Skill.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        skill = self.get_object(slug)
        serializer = SkillSerializer(skill)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        skill = self.get_object(slug)
        serializer = SkillSerializer(
            skill, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SkillDeleteAPIView(APIView):
    """
    User can delete their skills.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SkillSerializer

    def get_object(self, slug):
        try:
            return Skill.objects.get(slug=slug)
        except Skill.DoesNotExist:
            raise Http404

    def delete(self, request, slug, format=None):
        skill = self.get_object(slug)
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobCreateAPIView(APIView):
    """
    Hrs can add the Job for company.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = JobDetailsSerializer
    address_serializer_class = AddressDetailsSerializer

    def post(self, request, format=None):
        serializer = JobDetailsSerializer(data=request.data)
        if serializer.is_valid():
            employee_role = EmployeeRole.objects.get(emp_user=request.user)
            job = serializer.save(job_creator=employee_role)
            serialized_job = self.serializer_class(job)
            return Response(serialized_job.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobListAPIView(APIView):
    """
    HRs can view a list all the jobs.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = JobDetailsSerializer

    def get(self, request, format=None):
        jobs = JobDetails.objects.all()
        serialized_jobs = self.serializer_class(jobs, many=True)
        return Response(serialized_jobs.data)


class JobDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = JobDetailsSerializer

    def get_object(self, slug):
        return get_object_or_404(JobDetails, slug=slug)

    def delete(self, request, slug, format=None):
        self.get_object(slug).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobUpdateAPIView(APIView):
    """
    Hrs can update jobs for company.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = JobDetailsSerializer

    def get_object(self, slug):
        try:
            return JobDetails.objects.get(slug=slug)
        except JobDetails.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        JobDetails = self.get_object(slug)
        serializer = JobDetailsSerializer(JobDetails)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        JobDetails = self.get_object(slug)
        serializer = JobDetailsSerializer(
            JobDetails, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppliedJobsCreateAPIView(APIView):
    """
    Candidates can apply to the jobs.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = AppliedJobsSerializer
    address_serializer_class = JobDetailsSerializer

    def post(self, request, *args, **kwargs):
        serializer = AppliedJobsSerializer(data=request.data)
        if serializer.is_valid():
            if AppliedJobs.objects.filter(user=request.user, job=request.data.get('job')).exists():
                return Response({'message': f'{request.user} has already applied to this job.'}, status=status.HTTP_403_FORBIDDEN)
            else:
                users_profile = JobUsersProfile.objects.filter(
                    user=request.user).first()
                applied_job = serializer.save(
                    user=request.user, users_profile=users_profile)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppliedJobsListAPIView(APIView):
    """
        List of all the jobs applied.
        """

    def get(self, request):
        applied_jobs = AppliedJobs.objects.all()
        serializer = AppliedJobsSerializer(applied_jobs, many=True)
        return Response(serializer.data)


class ZoomMeetingsCreateAPIView(APIView):
    """
    HRs can create zoom meetings.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ZoomMeetingsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ZoomMeetingsListAPIView(APIView):
    """
        List of all the zoom meetings.
        """

    def get(self, request):
        zoom_meetings = ZoomMeetings.objects.all()
        serializer = ZoomMeetingsSerializer(zoom_meetings, many=True)
        return Response(serializer.data)


class ZoomMeetingsUpdateAPIView(APIView):
    """
    Zoom meetings can be updated.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ZoomMeetingsSerializer

    def get_object(self, slug):
        try:
            return ZoomMeetings.objects.get(slug=slug)
        except ZoomMeetings.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        skill = self.get_object(slug)
        serializer = ZoomMeetingsSerializer(skill)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        skill = self.get_object(slug)
        serializer = ZoomMeetingsSerializer(
            skill, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ZoomMeetingsDeleteAPIView(APIView):
    """
    Zoom meetings can be deleted.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ZoomMeetingsSerializer

    def get_object(self, slug):
        return get_object_or_404(ZoomMeetings, slug=slug)

    def delete(self, request, slug, format=None):
        self.get_object(slug).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ZoomMeetingsUsersCreateAPIView(APIView):
    """
    Zoom meetings users can be created.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ZoomMeetingsUsersSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ZoomMeetingsUsersListAPIView(APIView):
    """
        List of all the Zoom meetings users.
        """

    def get(self, request):
        zoom_meetings = ZoomMeetingsUsers.objects.all()
        serializer = ZoomMeetingsUsersSerializer(zoom_meetings, many=True)
        return Response(serializer.data)


class ZoomMeetingsUsersUpdateAPIView(APIView):
    """
    Zoom meetings users can be updated.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ZoomMeetingsUsersSerializer

    def get_object(self, slug):
        try:
            return ZoomMeetingsUsers.objects.get(slug=slug)
        except ZoomMeetingsUsers.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        skill = self.get_object(slug)
        serializer = ZoomMeetingsUsersSerializer(skill)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        skill = self.get_object(slug)
        serializer = ZoomMeetingsUsersSerializer(
            skill, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ZoomMeetingsUsersDeleteAPIView(APIView):
    """
    Zoom meetings users can be deleted.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ZoomMeetingsUsersSerializer

    def get_object(self, slug):
        return get_object_or_404(ZoomMeetingsUsers, slug=slug)

    def delete(self, request, slug, format=None):
        self.get_object(slug).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ZoomLinkAPIView(APIView):
    """
        HRs can send zoom link via mail to all selected candidates.
        """

    def get(self, request, format=None):
        candidates = AppliedJobs.objects.filter(status='Selected')
        serializer = AppliedJobsSerializer(candidates, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        candidates = AppliedJobs.objects.filter(status='Selected')
        client = ZoomClient(settings.ZOOM_API_KEY, settings.ZOOM_API_SECRET)
        response = client.meeting.create(
            user_id='me', topic='Interview Meeting')
        meeting_info = response.json()
        join_url = meeting_info.get('join_url')
        for candidate in candidates:
            subject = 'Interview Round - 1'
            message = f'Here is the link to your Zoom meeting: {join_url}'
            from_email = 'frstlst@email.com'
            recipient_list = [candidate.mail_id]
            send_mail(subject, message, from_email, recipient_list)
        return Response({'message': 'Zoom link sent'})


class StatusChangeAPIView(APIView):
    """
    HRs can change status as per the candidates progression.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = StatusChangeSerializer
    job_serializer_class = AppliedJobsSerializer

    def get_object(self, slug):
        try:
            return AppliedJobs.objects.get(slug=slug)
        except AppliedJobs.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        applied_jobs = self.get_object(slug)
        serializer = AppliedJobsSerializer(applied_jobs)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        applied_jobs = self.get_object(slug)
        serializer = StatusChangeSerializer(applied_jobs, data=request.data, context={
                                            'request': request}, partial=True)
        if serializer.is_valid():
            if request.user == applied_jobs.job.job_creator.emp_user:
                serializer.save(status=request.data.get(
                    'status', applied_jobs.status))
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppliedUsersAPIView(APIView):
    """
    HRs can see list of users who applied to a particular job.
    """

    def get(self, request, slug):
        job = JobDetails.objects.get(slug=slug)
        applied_jobs_list = AppliedJobs.objects.filter(job=job)
        serializer = AppliedJobsSerializer(applied_jobs_list, many=True)
        return Response(serializer.data)


class ZoomLinkIndividualAPIView(APIView):
    """
        HRs can send zoom link via mail to a particular selected candidate individually.
        """
    permission_classes = (IsAuthenticated,)
    serializer_class = ZoomMeetingsSerializer

    def get_object(self, slug):
        try:
            return AppliedJobs.objects.get(slug=slug)
        except AppliedJobs.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        applied_jobs = self.get_object(slug)
        serializer = AppliedJobsSerializer(applied_jobs)
        return Response(serializer.data)

    def post(self, request, slug):
        serializer = ZoomMeetingsSerializer(data=request.data)
        if serializer.is_valid():
            candidate = self.get_object(slug)
            data = serializer.validated_data
            client = ZoomClient(settings.ZOOM_API_KEY,
                                settings.ZOOM_API_SECRET)
            start_time = datetime.combine(
                data['meeting_date'], data['meeting_time'])
            response = client.meeting.create(
                user_id='me', topic=data['meeting_topic'], start_time=start_time)
            meeting_info = response.json()
            join_url = meeting_info.get('join_url')
            Company = candidate.job.company
            subject = 'Interview Round'
            message = f'Here is the link to your Zoom meeting: {join_url}\n\nTopic: {data["meeting_topic"]}\nDate: {start_time.strftime("%m/%d/%Y")}\nTime: {start_time.strftime("%I:%M %p")}\nDuration: {data["meeting_duration"]} \n\n Hiring Team \n {Company} '
            recipient_list = [candidate.mail_id]
            send_mail(subject, message,
                      settings.EMAIL_HOST_USER, recipient_list)
            return Response({'message': 'Zoom link sent'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
