from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from ordering.models import Supplier, Restaurant, Food, Agents, Customer, OrderDetails, Feedback, OrderItem
import datetime


class RestaurantFoodOrderingSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.today = datetime.date.today()

        # Create base test records
        self.supplier = Supplier.objects.create(supplier_name="Test Supplier Ltd")
        self.restaurant = Restaurant.objects.create(
            restaurant_name="Test Bistro",
            restaurant_ph_no="9876543210",
            restaurant_adrs="123 Test Street",
            rating=Decimal("4.5"),
            supplier=self.supplier
        )
        self.food = Food.objects.create(
            food_name="Test Burger",
            food_price=Decimal("150.00"),
            food_rating=Decimal("4.6"),
            restaurant=self.restaurant
        )
        self.agent = Agents.objects.create(
            agent_name="Test Agent",
            agent_ph_number="9123456789",
            supplier=self.supplier
        )
        self.customer = Customer.objects.create(
            cust_name="Test Customer",
            cust_adrs="456 Test Lane",
            cust_ph_no="9898989898"
        )
        self.order = OrderDetails.objects.create(
            customer=self.customer,
            supplier=self.supplier,
            order_date=self.today,
            quantity=1,
            price=Decimal("150.00")
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            food=self.food,
            quantity=1,
            item_price=Decimal("150.00")
        )
        self.feedback = Feedback.objects.create(
            customer=self.customer,
            rating=5,
            message="Great test food!",
            feedback_date=self.today
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "System Dashboard")
        self.assertContains(response, "Test Customer")

    def test_restaurant_crud(self):
        # List
        res = self.client.get(reverse('restaurant_list'))
        self.assertEqual(res.status_code, 200)

        # Create
        res_post = self.client.post(reverse('restaurant_create'), {
            'restaurant_name': 'New Cafe',
            'restaurant_ph_no': '9192939495',
            'restaurant_adrs': '789 Market Rd',
            'rating': '4.2',
            'supplier': self.supplier.supplier_id
        })
        self.assertEqual(res_post.status_code, 302)
        self.assertTrue(Restaurant.objects.filter(restaurant_name='New Cafe').exists())

        # Update
        new_cafe = Restaurant.objects.get(restaurant_name='New Cafe')
        res_update = self.client.post(reverse('restaurant_update', args=[new_cafe.restaurant_id]), {
            'restaurant_name': 'New Cafe Premium',
            'restaurant_ph_no': '9192939495',
            'restaurant_adrs': '789 Market Rd Updated',
            'rating': '4.9',
            'supplier': self.supplier.supplier_id
        })
        self.assertEqual(res_update.status_code, 302)
        new_cafe.refresh_from_db()
        self.assertEqual(new_cafe.restaurant_name, 'New Cafe Premium')

        # Delete
        res_del = self.client.post(reverse('restaurant_delete', args=[new_cafe.restaurant_id]))
        self.assertEqual(res_del.status_code, 302)
        self.assertFalse(Restaurant.objects.filter(pk=new_cafe.restaurant_id).exists())

    def test_food_crud(self):
        res = self.client.get(reverse('food_list'))
        self.assertEqual(res.status_code, 200)

        res_create = self.client.post(reverse('food_create'), {
            'food_name': 'Garlic Bread',
            'food_price': '120.00',
            'food_rating': '4.4',
            'restaurant': self.restaurant.restaurant_id
        })
        self.assertEqual(res_create.status_code, 302)
        self.assertTrue(Food.objects.filter(food_name='Garlic Bread').exists())

    def test_order_creation_with_items(self):
        res = self.client.post(reverse('order_create'), {
            'customer': self.customer.cust_id,
            'supplier': self.supplier.supplier_id,
            'order_date': self.today.strftime('%Y-%m-%d'),
            'quantity': 2,
            'price': '300.00',
            'item_food_id[]': [str(self.food.food_id)],
            'item_quantity[]': ['2'],
            'item_price[]': ['150.00'],
        })
        self.assertEqual(res_post:=res.status_code, 302)
        latest_order = OrderDetails.objects.latest('order_id')
        self.assertEqual(latest_order.quantity, 2)
        self.assertEqual(latest_order.items.count(), 1)

    def test_dbms_queries_demo_page(self):
        res = self.client.get(reverse('dbms_queries_demo'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "DBMS SQL Concepts Demonstration")

    def test_rest_api_dashboard_stats(self):
        res = self.client.get(reverse('api_dashboard_stats'))
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn('counts', data)
        self.assertIn('aggregates', data)
        self.assertGreaterEqual(data['counts']['restaurants'], 1)
