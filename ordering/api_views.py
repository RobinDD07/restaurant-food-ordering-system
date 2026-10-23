from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count

from .models import Supplier, Restaurant, Food, Agents, Customer, OrderDetails, Feedback, OrderItem
from .serializers import (
    SupplierSerializer, RestaurantSerializer, FoodSerializer, AgentsSerializer,
    CustomerSerializer, OrderDetailsSerializer, FeedbackSerializer, OrderItemSerializer
)


@api_view(['GET'])
def dashboard_stats_api(request):
    """
    Returns live database statistics for the dashboard.
    Demonstrates COUNT, SUM, AVG aggregate functions.
    """
    total_restaurants = Restaurant.objects.count()
    total_food = Food.objects.count()
    total_suppliers = Supplier.objects.count()
    total_agents = Agents.objects.count()
    total_customers = Customer.objects.count()
    total_orders = OrderDetails.objects.count()
    total_feedback = Feedback.objects.count()

    # Aggregate calculations
    total_sales = OrderDetails.objects.aggregate(total=Sum('price'))['total'] or 0
    total_items_sold = OrderDetails.objects.aggregate(total=Sum('quantity'))['total'] or 0
    avg_order_value = OrderDetails.objects.aggregate(avg=Avg('price'))['avg'] or 0
    avg_restaurant_rating = Restaurant.objects.aggregate(avg=Avg('rating'))['avg'] or 0
    avg_customer_rating = Feedback.objects.aggregate(avg=Avg('rating'))['avg'] or 0

    return Response({
        'counts': {
            'restaurants': total_restaurants,
            'food_items': total_food,
            'suppliers': total_suppliers,
            'agents': total_agents,
            'customers': total_customers,
            'orders': total_orders,
            'feedback': total_feedback,
        },
        'aggregates': {
            'total_sales': float(total_sales),
            'total_items_sold': int(total_items_sold),
            'avg_order_value': round(float(avg_order_value), 2),
            'avg_restaurant_rating': round(float(avg_restaurant_rating), 1),
            'avg_customer_rating': round(float(avg_customer_rating), 1),
        }
    })


@api_view(['GET'])
def food_by_restaurant_api(request, restaurant_id):
    """
    Fetch food items offered by a specific restaurant.
    Used dynamically in order creation.
    """
    food_items = Food.objects.filter(restaurant_id=restaurant_id)
    serializer = FoodSerializer(food_items, many=True)
    return Response(serializer.data)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.select_related('supplier').all()
    serializer_class = RestaurantSerializer


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.select_related('restaurant').all()
    serializer_class = FoodSerializer


class AgentsViewSet(viewsets.ModelViewSet):
    queryset = Agents.objects.select_related('supplier').all()
    serializer_class = AgentsSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class OrderDetailsViewSet(viewsets.ModelViewSet):
    queryset = OrderDetails.objects.select_related('customer', 'supplier').prefetch_related('items__food').all()
    serializer_class = OrderDetailsSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.select_related('customer').all()
    serializer_class = FeedbackSerializer
