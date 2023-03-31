from rest_framework import serializers
from modules.jobPortalApp.models import JobUsersProfile, Skill, AddressDetails
from modules.jobPortalApp.models import JobDetails, AppliedJobs, ZoomMeetings, ZoomMeetingsUsers


class JobUsersProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobUsersProfile
        fields = ['slug', 'resume', 'higer_secondary_year',
                  'secondary_year', 'grad_year', 'post_grad_year', 'looking_for']

    def validate_higer_secondary_year(self, value):
        if not (2000 <= value <= 2023):
            raise serializers.ValidationError(
                "Higher secondary year must be year between 2000-2023.")
        return value

    def validate_secondary_year(self, value):
        if not (2000 <= value <= 2023):
            raise serializers.ValidationError(
                "Secondary year must be year between 2000-2023.")
        return value

    def validate_grad_year(self, value):
        if not (2000 <= value <= 2023):
            raise serializers.ValidationError(
                "Graduation year must be year between 2000-2023.")
        return value

    def validate_post_grad_year(self, value):
        if not (2000 <= value <= 2023):
            raise serializers.ValidationError(
                "Post graduation year must be year between 2000-2023.")
        return value


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['slug', 'skill']

    def validate_skill(self, value):
        """
        Check that the skill name is at least 2 characters long.
        """
        if len(value) < 2:
            raise serializers.ValidationError(
                "Skill name must be at least 2 characters long.")
        return value


class AddressDetailsSerializer(serializers.ModelSerializer):
    street = serializers.CharField(allow_null=True, allow_blank=True)
    city = serializers.CharField(allow_null=True, allow_blank=True)
    state = serializers.CharField(allow_null=True, allow_blank=True)
    country = serializers.CharField(allow_null=True, allow_blank=True)
    pincode = serializers.CharField(
        allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = AddressDetails
        fields = ('street', 'city', 'state', 'country', 'pincode')

    def validate_pincode(self, value):
        """
        Check that the pincode is 6 digits long.
        """
        if len(value) != 6 and len(value) > 0:
            raise serializers.ValidationError("Pincode must be 6 digits long.")
        return value


class JobDetailsSerializer(serializers.ModelSerializer):
    chose_default_address = serializers.PrimaryKeyRelatedField(
        queryset=AddressDetails.objects.all(), allow_null=True)
    address = AddressDetailsSerializer()

    class Meta:
        model = JobDetails
        fields = ('gid', 'slug',  'chose_default_address', 'company', 'job_title', 'job_description', 'experiance',
                  'salary', 'address', 'hiring_members', 'industry_type', 'employement_type', 'qualification')

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        chose_default_address = validated_data.pop(
            'chose_default_address', None)
        if chose_default_address is None:
            address = AddressDetails.objects.create(**address_data)
        else:
            address = chose_default_address
        job_details = JobDetails.objects.create(
            address=address, **validated_data)
        job_details.chose_default_address = chose_default_address
        job_details.save()
        return job_details

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        chose_default_address = validated_data.pop(
            'chose_default_address', None)
        if chose_default_address is None and address_data is not None:
            instance.address = AddressDetails.objects.update_or_create(
                defaults=address_data,
                **({'slug': instance.address.slug} if instance.address else {})
            )[0]
        elif chose_default_address is not None:
            instance.address = chose_default_address
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def validate_hiring_members(self, value):
        """
        Check that the hiring_members value is greater than 0.
        """
        if value <= 0:
            raise serializers.ValidationError(
                "hiring_members must be greater than 0.")
        return value

    def validate_salary(self, value):
        """
        Check that the salary value is a valid number.
        """
        try:
            float(value)
        except ValueError:
            raise serializers.ValidationError("salary must be a valid number.")
        return value


class AppliedJobsSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='AppliedJobs.status', read_only=True)

    class Meta:
        model = AppliedJobs
        fields = ('slug', 'job', 'user', 'users_profile', 'status', 'mail_id')
        read_only_fields = ('gid', 'user', 'users_profile',
                            'slug', 'date_posted',)

    def validate_user(self, value):
        # Ensure that the user is not already applied to the job
        job = self.initial_data['job']
        applied_jobs = AppliedJobs.objects.filter(job=job, user=value)
        if applied_jobs.exists():
            raise serializers.ValidationError(
                "You have already applied to this job.")
        return value

    def validate_status(self, value):
        # Ensure that the status is either 'Pending' or 'Completed'
        if value not in ('Pending', 'Completed'):
            raise serializers.ValidationError("Invalid status.")
        return value


class ZoomMeetingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoomMeetings
        fields = ('meeting_topic', 'meeting_date',
                  'meeting_time', 'meeting_duration',)


class ZoomMeetingsUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoomMeetingsUsers
        fields = ('slug', 'zoom_meeting', 'status',
                  'mail_send', 'message', 'jobs')


class StatusChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedJobs
        fields = ('status', 'job', 'users_profile', 'mail_id', 'user')
        read_only_fields = ('slug', 'job', 'users_profile', 'mail_id', 'user')
