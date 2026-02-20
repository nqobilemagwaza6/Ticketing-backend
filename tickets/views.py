from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket, Comment  # Import from current app
from .serializers import TicketSerializer, CommentSerializer  # Import serializers

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket, Comment
from .serializers import TicketSerializer, CommentSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def create_ticket(request):

    # GET: Fetch tickets with filters
    if request.method == 'GET':
        # Base queryset based on user role
        if request.user.is_staff:
            # Admin sees ALL tickets
            tickets = Ticket.objects.all()
        else:
            # Normal users see only their tickets
            tickets = Ticket.objects.filter(user=request.user)
        
        # Apply status filter if provided
        status_filter = request.query_params.get('status', None)
        if status_filter:
            if status_filter == 'open':
                # Open includes both 'Open' and 'In Progress'
                tickets = tickets.filter(status__in=['Open', 'In Progress'])
            elif status_filter == 'closed':
                # Closed means 'Resolved'
                tickets = tickets.filter(status='Resolved')
        
        # Apply search filter if provided
        search = request.query_params.get('search', None)
        if search:
            tickets = tickets.filter(
                models.Q(title__icontains=search) |
                models.Q(description__icontains=search) |
                models.Q(category__icontains=search) |
                models.Q(id__icontains=search)
            )
        
        # Order by created_at
        tickets = tickets.order_by('-created_at')
        
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
        if request.user.is_staff:
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
    if not request.user.is_staff:
        return Response({'detail': 'Not authorized'}, status=403)

    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return Response({'detail': 'Ticket not found'}, status=404)

    serializer = TicketSerializer(ticket, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

# Add new comment views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def ticket_comments(request, pk):
    try:
        if request.user.is_staff:
            ticket = Ticket.objects.get(pk=pk)
        else:
            ticket = Ticket.objects.get(pk=pk, user=request.user)
    except Ticket.DoesNotExist:
        return Response({'detail': 'Ticket not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        comments = ticket.comments.all().order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ticket=ticket, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)