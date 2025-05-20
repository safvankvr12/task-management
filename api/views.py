from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from tasks.models import Tasks
from .serializers import *


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Tasks.objects.all()

        try:
            return (
                Tasks.objects.filter(assigned_to__in=user.subordinate_user.assignees.all()) |
                Tasks.objects.filter(assigned_to=user)
            )
        except AttributeError:
            return Tasks.objects.filter(assigned_to=user)


class TaskCompleteAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        task = get_object_or_404(Tasks, pk=pk)
        if task.assigned_to != request.user:
            return Response({"detail": "You do not have permission to complete this task."}, status=status.HTTP_403_FORBIDDEN)
        serializer = TaskCompleteSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            task.status = "completed"
            task.save()
            return Response({"detail": "Task marked as completed."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        if not request.user.is_staff:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        task = get_object_or_404(Tasks, id=id)

        if task.assigned_to not in request.user.subordinate_user.assignees.all():
            return Response({"detail": "Permission Denied. You can only view the reports of your Subordinates"}, status=status.HTTP_400_BAD_REQUEST)


        if task.status != 'completed':
            return Response({"detail": "Report available only for completed tasks."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "completion_report": task.completion_report,
            "worked_hours": task.worked_hours
        })