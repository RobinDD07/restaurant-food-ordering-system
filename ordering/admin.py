from django.contrib import admin
from .models import Supplier, Restaurant, Food, Agents, Customer, OrderDetails, Feedback, OrderItem


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_id', 'supplier_name')
    search_fields = ('supplier_name',)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('restaurant_id', 'restaurant_name', 'restaurant_ph_no', 'rating', 'supplier')
    list_filter = ('supplier', 'rating')
    search_fields = ('restaurant_name', 'restaurant_adrs')


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('food_id', 'food_name', 'food_price', 'food_rating', 'restaurant')
    list_filter = ('restaurant', 'food_rating')
    search_fields = ('food_name',)


@admin.register(Agents)
class AgentsAdmin(admin.ModelAdmin):
    list_display = ('agent_id', 'agent_name', 'agent_ph_number', 'supplier')
    list_filter = ('supplier',)
    search_fields = ('agent_name', 'agent_ph_number')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('cust_id', 'cust_name', 'cust_ph_no', 'cust_adrs')
    search_fields = ('cust_name', 'cust_ph_no')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer', 'supplier', 'order_date', 'quantity', 'price')
    list_filter = ('order_date', 'supplier')
    search_fields = ('customer__cust_name',)
    inlines = [OrderItemInline]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_id', 'customer', 'rating', 'feedback_date', 'message')
    list_filter = ('rating', 'feedback_date')
    search_fields = ('customer__cust_name', 'message')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_item_id', 'order', 'food', 'quantity', 'item_price')
    list_filter = ('food',)
