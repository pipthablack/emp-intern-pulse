from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from .models import Employee, Review
from .serializers import EmployeeSerializer, ReviewSerializer





class EmployeeListCreate(generics.ListCreateAPIView):
    """
    Handles listing active employees and creating new ones.
    """
    queryset = Employee.objects.filter(is_active=True)
    serializer_class = EmployeeSerializer

    def get(self, request, *args, **kwargs):
        """
        Lists all active employees.
        """
        try:
            response = super().get(request, *args, **kwargs)
            return Response({
                'status': 'success',
                'data': response.data,
                'message': 'List of active employees retrieved successfully.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e),
                'details': 'An error occurred while retrieving the employee list.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        """
        Creates a new employee.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'data': serializer.data,
                'message': 'Employee created successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': 'Validation failed.',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class EmployeeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieve, update, and delete operations for individual employees.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_object(self):
        """
        Retrieves the employee object based on the pk in the request URL.
        """
        try:
            obj = super().get_object()
            if not obj.is_active:
                raise NotFound("Employee is deactivated.")
            return obj
        except Exception as e:
            raise NotFound({
                'status': 'error',
                'message': str(e),
                'details': 'The requested employee could not be found.'
            })

    def delete(self, request, *args, **kwargs):
        """
        Deactivates an employee instead of deleting them.
        """
        try:
            self.object = self.get_object()
            self.object.is_active = False
            self.object.save()
            return Response({
                'status': 'success',
                'message': 'Employee deactivated successfully.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e),
                'details': 'An error occurred while deactivating the employee.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewCreate(generics.CreateAPIView):
    """
    Handles creating new reviews for employees.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        """
        Creates a new review for an employee.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            review = serializer.instance
            response_serializer = ReviewSerializer(review)
            return Response({
                'status': 'success',
                'data': response_serializer.data,
                'message': 'Review created successfully.'
            }, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            return Response({
                'status': 'error',
                'message': 'Validation error.',
                'details': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e),
                'details': 'An error occurred while creating the review.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)