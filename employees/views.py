from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from .models import Employee, Review
from .serializers import EmployeeSerializer, ReviewSerializer

class EmployeeListCreate(generics.ListCreateAPIView):
    """
    Handles listing active employees and creating new ones.
    
    Attributes:
        queryset (QuerySet): The default queryset used to filter active employees.
        serializer_class (Serializer): The serializer class used to serialize employee data.
        
    Methods:
        get(): Lists all active employees.
        post(): Creates a new employee.
        
    Returns:
        Response: A successful response containing serialized employee data.
        
    Raises:
        Http404: If an attempt is made to retrieve deactivated employees.
    """
    queryset = Employee.objects.filter(is_active=True)
    serializer_class = EmployeeSerializer
    
    def get(self, request, *args, **kwargs):
        """
        Lists all active employees.
        
        Returns:
            Response: A successful response containing serialized employee data.
            
        Raises:
            Http404: If an attempt is made to retrieve deactivated employees.
        """
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        """
        Creates a new employee.
        
        Args:
            request (Request): The incoming request object.
        
        Returns:
            Response: A successful response containing serialized employee data.
            
        Raises:
            ValidationError: If validation fails during the creation process.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieve, update, and delete operations for individual employees.
    
    Attributes:
        queryset (QuerySet): The default queryset used to filter all employees.
        serializer_class (Serializer): The serializer class used to serialize employee data.
        
    Methods:
        get_object(): Retrieves the employee object based on the pk in the request URL.
        delete(): Deactivates an employee instead of deleting them.
        
    Returns:
        Response: A successful response containing serialized employee data.
        
    Raises:
        Http404: If the requested employee does not exist or is deactivated.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    def get_object(self):
        """
        Retrieves the employee object based on the pk in the request URL.
        
        Returns:
            Employee: The requested employee object.
            
        Raises:
            Http404: If the requested employee does not exist or is deactivated.
        """
        obj = super().get_object()
        if not obj.is_active:
            raise NotFound("Employee is deactivated.")
        return obj

    def delete(self, request, *args, **kwargs):
        """
        Deactivates an employee instead of deleting them.
        
        Args:
            request (Request): The incoming request object.
        
        Returns:
            Response: A successful response containing a message indicating the employee was deactivated.
            
        Raises:
            Http404: If the requested employee does not exist.
        """
        try:
            self.object = self.get_object()
            self.object.is_active = False
            self.object.save()
            return Response({'message': 'Employee deactivated successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReviewCreate(generics.CreateAPIView):
    """
    Handles creating new reviews for employees.
    
    Attributes:
        queryset (QuerySet): The default queryset used to filter all reviews.
        serializer_class (Serializer): The serializer class used to serialize review data.
        
    Methods:
        create(): Creates a new review for an employee.
        
    Returns:
        Response: A successful response containing serialized review data.
        
    Raises:
        ValidationError: If validation fails during the creation process.
        Http404: If the employee associated with the review does not exist.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Creates a new review for an employee.
        
        Args:
            request (Request): The incoming request object.
        
        Returns:
            Response: A successful response containing serialized review data.
            
        Raises:
            ValidationError: If validation fails during the creation process.
            Http404: If the employee associated with the review does not exist.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            # Serialize the review with nested employee details
            review = serializer.instance
            employee_details = EmployeeSerializer(review.employee).data
            
            # Create a custom response with detailed information
            response_data = {
                # "review": ReviewSerializer(review).data,
                "employee": employee_details,
                "message": "Review created successfully."
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)