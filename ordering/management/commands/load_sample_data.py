import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from ordering.models import Supplier, Restaurant, Food, Agents, Customer, OrderDetails, Feedback, OrderItem


class Command(BaseCommand):
    help = 'Populates MySQL database with realistic sample records for all 7 tables + order_items'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Loading sample data into MySQL database 'restaurant_food_ordering'..."))

        with transaction.atomic():
            # 1. SUPPLIERS
            s1, _ = Supplier.objects.get_or_create(supplier_name="FreshFarm Agro Logistics")
            s2, _ = Supplier.objects.get_or_create(supplier_name="Metro Ocean & Meat Supplies")
            s3, _ = Supplier.objects.get_or_create(supplier_name="Royal Dairy & Baking Goods")
            s4, _ = Supplier.objects.get_or_create(supplier_name="Golden Grain & Spice Co.")

            # 2. RESTAURANTS
            r1, _ = Restaurant.objects.get_or_create(
                restaurant_name="Spice Symphony Bistro",
                defaults={
                    'restaurant_ph_no': "9820123456",
                    'restaurant_adrs': "14 Brigade Road, Bangalore",
                    'rating': Decimal("4.8"),
                    'supplier': s1
                }
            )
            r2, _ = Restaurant.objects.get_or_create(
                restaurant_name="Dragon Wok Asian Kitchen",
                defaults={
                    'restaurant_ph_no': "9833456789",
                    'restaurant_adrs': "22 Indiranagar 100ft Rd, Bangalore",
                    'rating': Decimal("4.5"),
                    'supplier': s2
                }
            )
            r3, _ = Restaurant.objects.get_or_create(
                restaurant_name="Bella Italia Trattoria",
                defaults={
                    'restaurant_ph_no': "9844567890",
                    'restaurant_adrs': "7 Koramangala 4th Block, Bangalore",
                    'rating': Decimal("4.7"),
                    'supplier': s3
                }
            )
            r4, _ = Restaurant.objects.get_or_create(
                restaurant_name="Biryani Darbar Palace",
                defaults={
                    'restaurant_ph_no': "9855678901",
                    'restaurant_adrs': "55 Commercial Street, Bangalore",
                    'rating': Decimal("4.9"),
                    'supplier': s4
                }
            )

            # 3. FOOD ITEMS
            foods_data = [
                (r1, "Paneer Tikka Masala", Decimal("320.00"), Decimal("4.8")),
                (r1, "Dal Makhani Deluxe", Decimal("240.00"), Decimal("4.6")),
                (r1, "Butter Garlic Naan", Decimal("60.00"), Decimal("4.7")),
                (r2, "Kung Pao Chicken", Decimal("380.00"), Decimal("4.5")),
                (r2, "Hakka Noodles Special", Decimal("220.00"), Decimal("4.3")),
                (r2, "Steamed Dim Sums (6 pcs)", Decimal("260.00"), Decimal("4.7")),
                (r3, "Woodfire Margherita Pizza", Decimal("450.00"), Decimal("4.9")),
                (r3, "Creamy Fettuccine Alfredo", Decimal("390.00"), Decimal("4.6")),
                (r3, "Classic Tiramisu", Decimal("250.00"), Decimal("4.8")),
                (r4, "Hyderabadi Dum Biryani", Decimal("350.00"), Decimal("4.9")),
                (r4, "Mutton Galouti Kebab", Decimal("420.00"), Decimal("4.8")),
                (r4, "Shahi Gulab Jamun (2 pcs)", Decimal("120.00"), Decimal("4.5")),
            ]

            created_foods = []
            for rest, name, price, rating in foods_data:
                f, _ = Food.objects.get_or_create(
                    food_name=name,
                    restaurant=rest,
                    defaults={'food_price': price, 'food_rating': rating}
                )
                created_foods.append(f)

            # 4. AGENTS
            a1, _ = Agents.objects.get_or_create(
                agent_name="Rahul Verma",
                supplier=s1,
                defaults={'agent_ph_number': "9112233445"}
            )
            a2, _ = Agents.objects.get_or_create(
                agent_name="Sneha Kulkarni",
                supplier=s2,
                defaults={'agent_ph_number': "9223344556"}
            )
            a3, _ = Agents.objects.get_or_create(
                agent_name="Mohammed Ali",
                supplier=s3,
                defaults={'agent_ph_number': "9334455667"}
            )
            a4, _ = Agents.objects.get_or_create(
                agent_name="Pooja Sharma",
                supplier=s4,
                defaults={'agent_ph_number': "9445566778"}
            )

            # 5. CUSTOMERS
            c1, _ = Customer.objects.get_or_create(
                cust_name="Amit Patel",
                defaults={'cust_adrs': "Flat 302, Palm Meadows, Whitefield", 'cust_ph_no': "9898012345"}
            )
            c2, _ = Customer.objects.get_or_create(
                cust_name="Priya Nair",
                defaults={'cust_adrs': "House 12, Rainbow Layout, HSR Layout", 'cust_ph_no': "9898123456"}
            )
            c3, _ = Customer.objects.get_or_create(
                cust_name="Rohan Gupta",
                defaults={'cust_adrs': "Tower B-401, Prestige Oasis, Electronic City", 'cust_ph_no': "9898234567"}
            )
            c4, _ = Customer.objects.get_or_create(
                cust_name="Ananya Roy",
                defaults={'cust_adrs': "Villa 5, Lakeview Estate, Bellandur", 'cust_ph_no': "9898345678"}
            )

            # 6. ORDER DETAILS & 7. ORDER ITEMS
            today = datetime.date.today()
            order1, created1 = OrderDetails.objects.get_or_create(
                customer=c1,
                supplier=s1,
                order_date=today - datetime.timedelta(days=2),
                defaults={'quantity': 3, 'price': Decimal("620.00")}
            )
            if created1:
                OrderItem.objects.create(order=order1, food=created_foods[0], quantity=1, item_price=Decimal("320.00")) # Paneer Tikka
                OrderItem.objects.create(order=order1, food=created_foods[1], quantity=1, item_price=Decimal("240.00")) # Dal Makhani
                OrderItem.objects.create(order=order1, food=created_foods[2], quantity=1, item_price=Decimal("60.00"))  # Naan

            order2, created2 = OrderDetails.objects.get_or_create(
                customer=c2,
                supplier=s3,
                order_date=today - datetime.timedelta(days=1),
                defaults={'quantity': 2, 'price': Decimal("840.00")}
            )
            if created2:
                OrderItem.objects.create(order=order2, food=created_foods[6], quantity=1, item_price=Decimal("450.00")) # Pizza
                OrderItem.objects.create(order=order2, food=created_foods[7], quantity=1, item_price=Decimal("390.00")) # Fettuccine

            order3, created3 = OrderDetails.objects.get_or_create(
                customer=c3,
                supplier=s4,
                order_date=today,
                defaults={'quantity': 3, 'price': Decimal("890.00")}
            )
            if created3:
                OrderItem.objects.create(order=order3, food=created_foods[9], quantity=2, item_price=Decimal("350.00")) # 2x Biryani (700)
                OrderItem.objects.create(order=order3, food=created_foods[11], quantity=1, item_price=Decimal("120.00")) # Gulab Jamun (120) -> 820

            order4, created4 = OrderDetails.objects.get_or_create(
                customer=c4,
                supplier=s2,
                order_date=today,
                defaults={'quantity': 2, 'price': Decimal("640.00")}
            )
            if created4:
                OrderItem.objects.create(order=order4, food=created_foods[3], quantity=1, item_price=Decimal("380.00")) # Kung Pao
                OrderItem.objects.create(order=order4, food=created_foods[5], quantity=1, item_price=Decimal("260.00")) # Dim Sums

            # 7. FEEDBACK
            Feedback.objects.get_or_create(
                customer=c1,
                feedback_date=today - datetime.timedelta(days=2),
                defaults={
                    'rating': 5,
                    'message': "Outstanding paneer tikka and hot crispy naan! Arrived super fast and fresh."
                }
            )
            Feedback.objects.get_or_create(
                customer=c2,
                feedback_date=today - datetime.timedelta(days=1),
                defaults={
                    'rating': 5,
                    'message': "The woodfire pizza from Bella Italia was authentic and delicious! Great packaging."
                }
            )
            Feedback.objects.get_or_create(
                customer=c3,
                feedback_date=today,
                defaults={
                    'rating': 4,
                    'message': "Dum Biryani flavor was aromatic and well cooked. Delivery was prompt."
                }
            )
            Feedback.objects.get_or_create(
                customer=c4,
                feedback_date=today,
                defaults={
                    'rating': 4,
                    'message': "Good Asian dishes and tasty sauces. Will definitely reorder again."
                }
            )

        self.stdout.write(self.style.SUCCESS("Successfully populated all 7 tables + order_items with realistic sample data!"))
