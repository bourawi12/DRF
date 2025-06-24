from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import EmployeeProfile, Skill, Education, Certification, Project
from .serializers import (
    EmployeeProfileSerializer, 
    EmployeeProfileDetailSerializer,
    EmployeeProfileListSerializer,
    SkillSerializer, 
    EducationSerializer, 
    CertificationSerializer, 
    ProjectSerializer
)
from .permissions import IsOwnerOrReadOnly, IsProfileOwnerOrReadOnly, CanEditOwnProfileOnly

class EmployeeProfileViewSet(viewsets.ModelViewSet):
    queryset = EmployeeProfile.objects.all().select_related('owner').prefetch_related(
        'skills', 'education', 'certifications', 'projects'
    )
    permission_classes = [IsAuthenticated, CanEditOwnProfileOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeProfileListSerializer
        elif self.action == 'retrieve':
            return EmployeeProfileDetailSerializer
        return EmployeeProfileSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # Return all profiles for viewing, but filtering will be handled by permissions
        return self.queryset

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_profile(self, request):
        """Get current user's profile"""
        try:
            profile = EmployeeProfile.objects.get(owner=request.user)
            serializer = EmployeeProfileDetailSerializer(profile)
            return Response(serializer.data)
        except EmployeeProfile.DoesNotExist:
            return Response(
                {'detail': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )


    @action(detail=False, methods=['post', 'put', 'patch'])
    def my_profile_update(self):
        """Create or update current user's profile"""
        try:
            profile = EmployeeProfile.objects.get(owner=self.request.user)
            serializer = EmployeeProfileSerializer(
                profile, 
                data=self.request.data, 
                partial=self.request.method == 'PATCH'
            )
        except EmployeeProfile.DoesNotExist:
            serializer = EmployeeProfileSerializer(data=self.request.data)
        
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().select_related('profile__owner')
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        profile_id = self.request.query_params.get('profile', None)
        if profile_id is not None:
            queryset = queryset.filter(profile=profile_id)
        return queryset

    @action(detail=False, methods=['get'])
    def my_skills(self):
        """Get current user's skills"""
        try:
            profile = EmployeeProfile.objects.get(owner=self.request.user)
            skills = Skill.objects.filter(profile=profile)
            serializer = SkillSerializer(skills, many=True)
            return Response(serializer.data)
        except EmployeeProfile.DoesNotExist:
            return Response(
                {'detail': 'Profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all().select_related('profile__owner')
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        profile_id = self.request.query_params.get('profile', None)
        if profile_id is not None:
            queryset = queryset.filter(profile=profile_id)
        return queryset

    @action(detail=False, methods=['get'])
    def my_education(self):
        """Get current user's education"""
        try:
            profile = EmployeeProfile.objects.get(owner=self.request.user)
            education = Education.objects.filter(profile=profile)
            serializer = EducationSerializer(education, many=True)
            return Response(serializer.data)
        except EmployeeProfile.DoesNotExist:
            return Response(
                {'detail': 'Profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all().select_related('profile__owner')
    serializer_class = CertificationSerializer
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        profile_id = self.request.query_params.get('profile', None)
        if profile_id is not None:
            queryset = queryset.filter(profile=profile_id)
        return queryset

    @action(detail=False, methods=['get'])
    def my_certifications(self):
        """Get current user's certifications"""
        try:
            profile = EmployeeProfile.objects.get(owner=self.request.user)
            certifications = Certification.objects.filter(profile=profile)
            serializer = CertificationSerializer(certifications, many=True)
            return Response(serializer.data)
        except EmployeeProfile.DoesNotExist:
            return Response(
                {'detail': 'Profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().select_related('profile__owner')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        profile_id = self.request.query_params.get('profile', None)
        if profile_id is not None:
            queryset = queryset.filter(profile=profile_id)
        return queryset

    @action(detail=False, methods=['get'])
    def my_projects(self):
        """Get current user's projects"""
        try:
            profile = EmployeeProfile.objects.get(owner=self.request.user)
            projects = Project.objects.filter(profile=profile)
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)
        except EmployeeProfile.DoesNotExist:
            return Response(
                {'detail': 'Profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
class ProfileSkillsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, profile_id):
        # Try to get the profile by id
        try:
            profile = EmployeeProfile.objects.get(id=profile_id)
        except EmployeeProfile.DoesNotExist:
            return Response({'detail': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        # Filter skills by the profile
        skills = Skill.objects.filter(profile=profile)
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)