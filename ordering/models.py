from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Supplier(models.Model):
    """
    SUPPLIER Table
    Primary Key: supplier_id
    Attributes: supplier_name
    """
    supplier_id = models.AutoField(primary_key=True, db_column='supplier_id')
    supplier_name = models.CharField(max_length=120, db_column='supplier_name', verbose_name="Supplier Name")

    class Meta:
        db_table = 'supplier'
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['supplier_id']

    def __str__(self):
        return f"{self.supplier_name} (ID: {self.supplier_id})"


class Restaurant(models.Model):
    """
    RESTAURANT Table
    Primary Key: restaurant_id
    Attributes: restaurant_name, restaurant_ph_no, restaurant_adrs, rating, supplier_id
    Foreign Key: supplier_id references SUPPLIER(supplier_id)
    """
    restaurant_id = models.AutoField(primary_key=True, db_column='restaurant_id')
    restaurant_name = models.CharField(max_length=150, db_column='restaurant_name', verbose_name="Restaurant Name")
    restaurant_ph_no = models.CharField(max_length=20, db_column='restaurant_ph_no', verbose_name="Phone Number")
    restaurant_adrs = models.CharField(max_length=255, db_column='restaurant_adrs', verbose_name="Address")
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        db_column='rating', 
        verbose_name="Rating (0.0 - 5.0)"
    )
    supplier = models.ForeignKey(
        Supplier, 
        on_delete=models.CASCADE, 
        db_column='supplier_id',
        related_name='restaurants',
        verbose_name="Supplier"
    )

    class Meta:
        db_table = 'restaurant'
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'
        ordering = ['restaurant_id']

    def __str__(self):
        return f"{self.restaurant_name} (ID: {self.restaurant_id})"


class Food(models.Model):
    """
    FOOD Table
    Primary Key: food_id
    Attributes: food_name, food_price, food_rating, restaurant_id
    Foreign Key: restaurant_id references RESTAURANT(restaurant_id)
    """
    food_id = models.AutoField(primary_key=True, db_column='food_id')
    food_name = models.CharField(max_length=150, db_column='food_name', verbose_name="Food Name")
    food_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)],
        db_column='food_price', 
        verbose_name="Price (₹/$)"
    )
    food_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        db_column='food_rating', 
        verbose_name="Food Rating (0.0 - 5.0)"
    )
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.CASCADE, 
        db_column='restaurant_id',
        related_name='food_items',
        verbose_name="Restaurant"
    )

    class Meta:
        db_table = 'food'
        verbose_name = 'Food Item'
        verbose_name_plural = 'Food Items'
        ordering = ['food_id']

    def __str__(self):
        return f"{self.food_name} - {self.food_price} ({self.restaurant.restaurant_name})"


class Agents(models.Model):
    """
    AGENTS Table
    Primary Key: agent_id
    Attributes: agent_name, agent_ph_number, supplier_id
    Foreign Key: supplier_id references SUPPLIER(supplier_id)
    """
    agent_id = models.AutoField(primary_key=True, db_column='agent_id')
    agent_name = models.CharField(max_length=120, db_column='agent_name', verbose_name="Agent Name")
    agent_ph_number = models.CharField(max_length=20, db_column='agent_ph_number', verbose_name="Phone Number")
    supplier = models.ForeignKey(
        Supplier, 
        on_delete=models.CASCADE, 
        db_column='supplier_id',
        related_name='agents',
        verbose_name="Supplier"
    )

    class Meta:
        db_table = 'agents'
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'
        ordering = ['agent_id']

    def __str__(self):
        return f"{self.agent_name} (Supplier: {self.supplier.supplier_name})"


class Customer(models.Model):
    """
    CUSTOMER Table
    Primary Key: cust_id
    Attributes: cust_name, cust_adrs, cust_ph_no
    """
    cust_id = models.AutoField(primary_key=True, db_column='cust_id')
    cust_name = models.CharField(max_length=120, db_column='cust_name', verbose_name="Customer Name")
    cust_adrs = models.CharField(max_length=255, db_column='cust_adrs', verbose_name="Address")
    cust_ph_no = models.CharField(max_length=20, db_column='cust_ph_no', verbose_name="Phone Number")

    class Meta:
        db_table = 'customer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['cust_id']

    def __str__(self):
        return f"{self.cust_name} (ID: {self.cust_id})"


class OrderDetails(models.Model):
    """
    ORDER_DETAILS Table
    Primary Key: order_id
    Attributes: cust_id, supplier_id, order_date, quantity, price
    Foreign Key: cust_id references CUSTOMER(cust_id)
    Foreign Key: supplier_id references SUPPLIER(supplier_id)
    """
    order_id = models.AutoField(primary_key=True, db_column='order_id')
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        db_column='cust_id',
        related_name='orders',
        verbose_name="Customer"
    )
    supplier = models.ForeignKey(
        Supplier, 
        on_delete=models.CASCADE, 
        db_column='supplier_id',
        related_name='orders',
        verbose_name="Supplier"
    )
    order_date = models.DateField(db_column='order_date', verbose_name="Order Date")
    quantity = models.IntegerField(validators=[MinValueValidator(1)], db_column='quantity', verbose_name="Total Quantity")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)],
        db_column='price', 
        verbose_name="Total Price"
    )

    class Meta:
        db_table = 'order_details'
        verbose_name = 'Order Details'
        verbose_name_plural = 'Order Details'
        ordering = ['-order_id']

    def __str__(self):
        return f"Order #{self.order_id} - {self.customer.cust_name} (₹{self.price})"


class Feedback(models.Model):
    """
    FEEDBACK Table
    Primary Key: feedback_id
    Attributes: cust_id, rating, message, feedback_date
    Foreign Key: cust_id references CUSTOMER(cust_id)
    """
    feedback_id = models.AutoField(primary_key=True, db_column='feedback_id')
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        db_column='cust_id',
        related_name='feedbacks',
        verbose_name="Customer"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        db_column='rating', 
        verbose_name="Rating (1-5)"
    )
    message = models.TextField(db_column='message', verbose_name="Feedback Message")
    feedback_date = models.DateField(db_column='feedback_date', verbose_name="Feedback Date")

    class Meta:
        db_table = 'feedback'
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
        ordering = ['-feedback_id']

    def __str__(self):
        return f"Feedback #{self.feedback_id} - {self.customer.cust_name} ({self.rating}★)"


class OrderItem(models.Model):
    """
    ORDER_ITEMS Table (Supplementary table as requested in specification)
    Allows an order in ORDER_DETAILS to associate with specific food items from FOOD table.
    Primary Key: order_item_id
    Attributes: order_id, food_id, quantity, item_price
    Foreign Key: order_id references ORDER_DETAILS(order_id)
    Foreign Key: food_id references FOOD(food_id)
    """
    order_item_id = models.AutoField(primary_key=True, db_column='order_item_id')
    order = models.ForeignKey(
        OrderDetails, 
        on_delete=models.CASCADE, 
        db_column='order_id', 
        related_name='items',
        verbose_name="Order"
    )
    food = models.ForeignKey(
        Food, 
        on_delete=models.CASCADE, 
        db_column='food_id', 
        related_name='order_items',
        verbose_name="Food Item"
    )
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)], db_column='quantity', verbose_name="Quantity")
    item_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='item_price', verbose_name="Unit Price")

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        ordering = ['order_item_id']

    @property
    def subtotal(self):
        return self.quantity * self.item_price

    def __str__(self):
        return f"{self.food.food_name} x {self.quantity} (Order #{self.order.order_id})"
