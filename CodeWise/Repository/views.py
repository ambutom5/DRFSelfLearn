from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from Repository.models import QuestionsDb,SubmissionDb
from Repository.serializers import QuestionsDbSerializer,SubmissionDbSerializer


# Create your views here.

class QuestionsDbView(APIView):
    def get(self,request):
        qs = QuestionsDb.objects.all()
        serializer_instance = QuestionsDbSerializer(qs, many = True)
        return Response(serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = QuestionsDbSerializer(data = form_data)
        if serializer_instance.is_valid():
            val_data = serializer_instance.validated_data
            QuestionsDb.objects.create(**val_data)
            return Response(
                {"message":"Question Added!"}
            )
        else:
            return Response(serializer_instance.errors)

class QuestionsUpdateDeleteRetrieveView(APIView):
    def put(self,request,pk):
        form_data = request.data
        serializer_instance = QuestionsDbSerializer(data=form_data)
        if serializer_instance.is_valid():
            original_data = serializer_instance.validated_data
            QuestionsDb.objects.filter(id=pk).update(**form_data)
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

    def delete(self,request,pk):
        QuestionsDb.objects.filter(id=pk).delete()
        return Response({"message":"Question Deleted!"})

    def get(self,request,pk):
        qs = QuestionsDb.objects.get(id=pk)
        serializer_instance=QuestionsDbSerializer(qs)
        return Response(serializer_instance.data)

class SubmissionListCreateView(APIView):
    def get(self,request):
        qs = SubmissionDb.objects.all()
        serializer_instance = SubmissionDbSerializer(qs,many=True)
        return Response(serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = SubmissionDbSerializer(data = form_data)
        if serializer_instance.is_valid():
            org_data = serializer_instance.validated_data
            SubmissionDb.objects.create(**org_data)
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)
        

class SubmissionRetrieveUpdateDeleteView(APIView):
    def get(self,request,pk):
        qs = get_object_or_404(SubmissionDb,id=pk)
        serializer_instance = SubmissionDbSerializer(qs)
        return Response(data=serializer_instance.data)

    def delete(self,request,pk):
        SubmissionDb.objects.filter(id=pk).delete()
        return Response({"message":"Deleted!"})

    def put(self,request,pk):
        form_data = request.data
        serializer_instance = SubmissionDbSerializer(data=form_data)
        if serializer_instance.is_valid():
            org_data = serializer_instance.validated_data
            SubmissionDb.objects.filter(id=pk).update(**org_data)
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)


class EvaluateSubmissionView(APIView):
    def put(self,request,pk):
        form_data = request.data
        SubmissionDb.objects.filter(id=pk).update(**form_data)
        return Response({"Message":"Updated!"})