from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket
from .serializers import TicketSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def create_ticket(request):
    

    # GET: Fetch tickets for the logged-in user
    if request.method == 'GET':
        tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    # POST: Create a new ticket
    if request.method == 'POST':
        serializer = TicketSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)  # Assign logged-in user to the ticket
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ticket_detail(request, pk):
    try:
        ticket = Ticket.objects.get(pk=pk, user=request.user)  # Ensure it's the correct user's ticket
    except Ticket.DoesNotExist:
        return Response({'detail': 'Ticket not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TicketSerializer(ticket)
    return Response(serializer.data)