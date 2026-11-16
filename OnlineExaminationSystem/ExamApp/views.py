from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ExamApp.models import QuestionsDb
from ExamApp.serializers import QuestionsDbSerializer

# Create your views here.

class QuestionsCreateListView(APIView):
    def get(self,request):
        qs = QuestionsDb.objects.all()
        serializer_instance = QuestionsDbSerializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance=QuestionsDbSerializer(data = form_data)
        if serializer_instance.is_valid():
            org_data = serializer_instance.validated_data
            QuestionsDb.objects.create(**org_data)
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)


class QuestionsRetrieveUpdateDeleteView(APIView):
    def get(self,request,pk):
        qs = QuestionsDb.objects.get(id=pk)
        serializer_instance = QuestionsDbSerializer(qs)
        return Response(serializer_instance.data)

    def delete(self,request,pk):
        QuestionsDb.objects.filter(id=pk).delete()
        return Response({"message":"Question Deleted!"})

    def put(self,request,pk):
        form_data=request.data
        serializer_instance=QuestionsDbSerializer(data=form_data)
        if serializer_instance.is_valid():
            org_data = serializer_instance.validated_data
            QuestionsDb.objects.filter(id=pk).update(**org_data)
            return Response(serializer_instance.data)