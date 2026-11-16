from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from Repository.models import QuestionsDb
from Repository.serializers import QuestionDbSerializer

# Create your views here.

class QuestionsView(APIView):
    # def get(self,request):
    #     qs = QuestionsDb.objects.all().values()
    #     result = list(qs)
    #     return Response(result)

    # def post(self,request):
    #     form_data = request.data
    #     QuestionsDb.objects.create(**form_data)
    #     return Response(
    #         {"Message":"Question Added Successfully!"}
    #     )

    def get(self,request):
        qs = QuestionsDb.objects.all()
        serializer_instance = QuestionDbSerializer(qs, many = True)
        return Response(serializer_instance.data)


    def post(self,request):
        form_data = request.data
        serializer_instance = QuestionDbSerializer(data=form_data)
        if serializer_instance.is_valid():
            original_data = serializer_instance.validated_data
            QuestionsDb.objects.create(**original_data)
            return Response(
                {"Message":"Question Added Successfully!"}
            )
        else:
            return Response(serializer_instance.errors)

class QuestionsUpdateDeleteRetrieveView(APIView):
    def get(self,request,pk):
        qs = QuestionsDb.objects.get(id = pk)
        serializer_instance = QuestionDbSerializer(qs)
        return Response(serializer_instance.data)

    def delete(self,request,pk):
        QuestionsDb.objects.filter(id=pk).delete()
        return Response({"message":"Question Deleted!"})

    def put(self,request,pk):
        form_data = request.data
        serializer_instance = QuestionDbSerializer(data = form_data)
        if serializer_instance.is_valid():
            org_data = serializer_instance.validated_data
            QuestionsDb.objects.filter(id=pk).update()
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)