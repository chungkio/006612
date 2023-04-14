from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Code, Status
from django.contrib.auth.models import User
from .serializers import DiscountCodeSerializer


class ViewDiscountCode(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        items = Code.objects.all().order_by('-id')
        paginator = Paginator(items, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serializer = DiscountCodeSerializer(page_obj, many=True)
        # Serialize the data manually
        data = {
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'results': serializer.data,
        }
        # Return the serialized data as JSON response
        return JsonResponse(data, safe=False)



class ViewDetailDiscountCode(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            item = Code.objects.get(id=pk)
            serializer = DiscountCodeSerializer(item)
            if item:
                return Response({'status': 1, 'results':serializer.data})
        except Code.DoesNotExist:
            pass

        return Response({'status': 0, 'error': f'Code matching query does not exist for ID {pk}'},
                        status=status.HTTP_404_NOT_FOUND)


class CreatePostDiscountCode(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = DiscountCodeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Create a new Discount successful!', 'status':status.HTTP_201_CREATED})

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Some field is required!', 'errors': serializer.errors})


class UpdatePostDiscountCode(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        DiscountCode = get_object_or_404(Code, id=pk)
        serializer = DiscountCodeSerializer(DiscountCode, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': status.HTTP_200_OK, 'message': 'Update Discount successful!'})

        return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Update Discount unsuccessful!', 'errors': serializer.errors})

class DeletePostDiscountCode(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        ids_str = request.data.get('ids')
        if not ids_str:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'No IDs provided!'})

        codes_to_delete = Code.objects.filter(id__in=ids_str)
        num_deleted, _ = codes_to_delete.delete()

        if num_deleted == 0:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'No codes found to delete!'})
        
        return Response({'status': status.HTTP_200_OK, 'message': f'{num_deleted} codes deleted successfully!'})
       

class GetUserDiscountStatus(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Retrieve all users from the auth_user table
        users = User.objects.all()

        # Retrieve all discount statuses from the DiscountStatus table
        discount_statuses = Status.objects.all()

        # Create an empty list to hold the results
        results = []

        # Loop through all users
        for user in users:
            # Create a dictionary for this user
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'discount_statuses': [],
            }

            # Loop through all discount statuses for this user
            for discount_status in discount_statuses:
                # If the user_id in the discount status matches the user id in the auth_user table
                if discount_status.user_id == user.id:
                    # Add the discount status data to the user's dictionary
                    user_data['discount_statuses'].append({
                        'paid': discount_status.paid,
                        'status': discount_status.status,
                    })

            # Append the user's dictionary to the results list
            results.append(user_data)

        # Paginate the results and limit the number of items per page to 12
        paginator = Paginator(results, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Serialize the data manually
        data = {
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'results': list(page_obj),
        }

        # Return the serialized data as JSON response
        return JsonResponse(data)


class UserIdDiscountStatus(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        # Retrieve the user with the given id from the auth_user table
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': f'User with id {user_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Retrieve all discount statuses for the user from the DiscountStatus table
        discount_statuses = Status.objects.filter(user_id=user_id)
        
        # Create a dictionary for the user
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'discount_statuses': [],
        }
        
        # Loop through all discount statuses for the user
        for discount_status in discount_statuses:
            # Add the discount status data to the user's dictionary
            user_data['discount_statuses'].append({
                'paid': discount_status.paid,
                'status': discount_status.status,
            })
        
        # Return the user's dictionary
        return Response(user_data)


class FilterUserDiscountByStatus(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve the optional parameters from the query string
        paid = request.query_params.get('paid')
        status = request.query_params.get('status')

        # Retrieve all users from the auth_user table
        users = User.objects.all()

        # Retrieve all discount statuses from the DiscountStatus table
        discount_statuses = Status.objects.all()

        # Create an empty list to hold the results
        results = []

        # Loop through all users
        for user in users:
            # Create a dictionary for this user
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'discount_statuses': [],
            }

            # Loop through all discount statuses for this user
            for discount_status in discount_statuses:
                # If the user_id in the discount status matches the user id in the auth_user table
                if discount_status.user_id == user.id:
                    # Check if the paid and status fields match the optional parameters
                    if (paid is None or discount_status.paid == paid) and (status is None or discount_status.status == status):
                        # Add the discount status data to the user's dictionary
                        user_data['discount_statuses'].append({
                            'paid': discount_status.paid,
                            'status': discount_status.status,
                        })

            # Append the user's dictionary to the results list if it has any matching discount statuses
            if len(user_data['discount_statuses']) > 0:
                results.append(user_data)

        # Paginate the results and limit the number of items per page to 12
        paginator = Paginator(results, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Serialize the data manually
        data = {
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'results': list(page_obj),
        }

        # Return the serialized data as JSON response
        return Response( data )