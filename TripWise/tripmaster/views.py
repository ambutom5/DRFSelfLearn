from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from tripmaster.serializers import UserSerializer, TripSerializer, TripMemberSerializer
from django.contrib.auth.models import User
from tripmaster.models import TripDb, TripMemberDb
from rest_framework import authentication,permissions,serializers
from tripmaster import permissions as cpermissions
from rest_framework.exceptions import PermissionDenied
# Create your views here.

class SignUpView(APIView):
    def post(self,request):
        form_data = request.data
        serializer_instance = UserSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

class UserListView(APIView):
    def get(self,request):
        qs = User.objects.all()
        serializer_instance = UserSerializer(qs,many=True)
        return Response(serializer_instance.data)


class TripListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        qs = TripDb.objects.all()
        # qs = TripDb.objects.filter(created_by=request.user)
        serializer_instance = TripSerializer(qs,many=True)
        return Response(serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = TripSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)


class TripRetrieveUpdateDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated,cpermissions.OwnerOnly]

    def get(self,request,pk):
        qs = get_object_or_404(TripDb,id=pk)
        self.check_object_permissions(request, qs)
        # if qs.created_by != request.user:
        #     raise serializers.ValidationError("Permission Denied")
        serializer_instance = TripSerializer(qs)
        return Response(serializer_instance.data)


    def put(self,request,pk):
        qs = get_object_or_404(TripDb,id=pk)
        self.check_object_permissions(request, qs)
        # if qs.created_by != request.user:
        #     raise serializers.ValidationError("Permision Denied!")
        form_data = request.data
        serializer_instance = TripSerializer(qs,data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)


    def delete(self, request, pk):
        qs = get_object_or_404(TripDb, id=pk)
        self.check_object_permissions(request, qs)
        qs.delete()
        return Response({"message": "Trip Deleted!"})


class TripMemberListCreateView(APIView):
    def get(self,request,pk):
        qs = get_object_or_404(TripDb,id=pk)

        is_owner = qs.created_by == request.user
        is_member = TripMemberDb.objects.filter(trip=qs,user=request.user).exists()

        if not (is_owner or is_member):
            raise PermissionDenied("You are not allowed to access this trip!")

        members = TripMemberDb.objects.filter(trip=qs)
        serializer_instance = TripMemberSerializer(members,many=True)
        return Response(serializer_instance.data)


    def post(self,request,pk):
        qs = get_object_or_404(TripDb,id=pk)
        if qs.created_by != request.user:
            raise PermissionDenied("You are not allowed to add members to this trip!")
        form_data = request.data
        serializer_instance = TripMemberSerializer(data=form_data,context={"trip":qs})
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"Member Added!","Details":serializer_instance.data})
        else:
            return Response(serializer_instance.errors)


class TripMemberDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self,request,pk,pkk):
        qs = get_object_or_404(TripDb,id=pk)
        if qs.created_by != request.user:
            raise PermissionDenied("You are not allowed to remove members from this trip!")
        qss = TripMemberDb.objects.filter(id=pkk)
        qss.delete()
        return Response({"Message":"Member removed from the trip!"})

