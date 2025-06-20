from rest_framework import serializers
from django.contrib.auth.models import User
from .models import EmployeeProfile, Skill, Education, Certification, Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        # Ensure the skill belongs to a profile owned by the current user
        profile = validated_data['profile']
        if profile.owner != self.context['request'].user:
            raise serializers.ValidationError("You can only add skills to your own profile.")
        return super().create(validated_data)

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        # Ensure the education belongs to a profile owned by the current user
        profile = validated_data['profile']
        if profile.owner != self.context['request'].user:
            raise serializers.ValidationError("You can only add education to your own profile.")
        return super().create(validated_data)

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        # Ensure the certification belongs to a profile owned by the current user
        profile = validated_data['profile']
        if profile.owner != self.context['request'].user:
            raise serializers.ValidationError("You can only add certifications to your own profile.")
        return super().create(validated_data)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        # Ensure the project belongs to a profile owned by the current user
        profile = validated_data['profile']
        if profile.owner != self.context['request'].user:
            raise serializers.ValidationError("You can only add projects to your own profile.")
        return super().create(validated_data)

class EmployeeProfileDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with all related data"""
    owner = UserSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    education = EducationSerializer(many=True, read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    
    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'owner', 'bio', 'position', 'joined_at',
            'skills', 'education', 'certifications', 'projects'
        ]
        read_only_fields = ['id', 'owner', 'joined_at']

class EmployeeProfileListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list view"""
    owner = UserSerializer(read_only=True)
    skills_count = serializers.SerializerMethodField()
    projects_count = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'owner', 'bio', 'position', 'joined_at',
            'skills_count', 'projects_count'
        ]
        read_only_fields = ['id', 'owner', 'joined_at']
    
    def get_skills_count(self, obj):
        return obj.skills.count()
    
    def get_projects_count(self, obj):
        return obj.projects.count()

class EmployeeProfileSerializer(serializers.ModelSerializer):
    """Basic serializer for create/update operations"""
    owner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = EmployeeProfile
        fields = ['id', 'owner', 'bio', 'position', 'joined_at']
        read_only_fields = ['id', 'owner', 'joined_at']