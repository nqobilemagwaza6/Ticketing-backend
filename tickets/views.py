from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket
from .serializers import TicketSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def create_ticket(request):

    # GET: Fetch tickets
    if request.method == 'GET':

        if request.user.is_staff or request.user.role == 'Support':

            # Admin sees ALL tickets
            tickets = Ticket.objects.all().order_by('-created_at')
        else:
            # Normal users see only their tickets
            tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')

        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    # POST: Create a new ticket
    if request.method == 'POST':
        serializer = TicketSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ticket_detail(request, pk):
    try:
        if request.user.is_staff or request.user.role == 'Support':

            ticket = Ticket.objects.get(pk=pk)
        else:
            ticket = Ticket.objects.get(pk=pk, user=request.user)

    except Ticket.DoesNotExist:
        return Response({'detail': 'Ticket not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TicketSerializer(ticket)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def assign_ticket(request, pk):
    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return Response({'detail': 'Ticket not found'}, status=404)

    # Admin assigning a ticket
    if request.user.is_staff and 'assigned_to' in request.data:
        serializer = TicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # This will automatically set status = In Progress
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # Support marking ticket as resolved
    elif ticket.assigned_to == request.user and request.data.get('status') == Ticket.RESOLVED:
        ticket.status = Ticket.RESOLVED
        ticket.save()
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    return Response({'detail': 'Not authorized or nothing to update'}, status=403)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def assigned_tickets(request):
    user = request.user
    tickets = Ticket.objects.filter(assigned_to=user).order_by('-created_at')
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)