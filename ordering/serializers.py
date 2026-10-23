from rest_framework import serializers
from .models import Supplier, Restaurant, Food, Agents, Customer, OrderDetails, Feedback, OrderItem


class SupplierSerializer(serializers.ModelSerializer):
    restaurant_count = serializers.IntegerField(source='restaurants.count', read_only=True)
    agent_count = serializers.IntegerField(source='agents.count', read_only=True)

    class Meta:
        model = Supplier
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.supplier_name', read_only=True)
    food_count = serializers.IntegerField(source='food_items.count', read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'


class FoodSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.restaurant_name', read_only=True)

    class Meta:
        model = Food
        fields = '__all__'


class AgentsSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.supplier_name', read_only=True)

    class Meta:
        model = Agents
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    order_count = serializers.IntegerField(source='orders.count', read_only=True)
    feedback_count = serializers.IntegerField(source='feedbacks.count', read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source='food.food_name', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderDetailsSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.cust_name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.supplier_name', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = OrderDetails
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.cust_name', read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'
