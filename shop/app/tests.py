from audioop import reverse
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product, CustomUser, Type, MessageModel, Feedback, Evaluation, AdminSellList, CountProduct


class ProductModelTest(TestCase):

    def setUp(self):
        self.type = Type.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            prise=100.0,
            img_url="http://example.com/image.jpg",
            type=self.type,
            count=50,
            cost_price=80.0
        )

    def test_product_creation(self):
        """Тестирование создания продукта"""
        product = self.product
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.prise, 100.0)
        self.assertEqual(product.count, 50)

    def test_product_save_creates_admin_sell_list(self):
        """Тестируем, что при создании продукта создается AdminSellList"""
        product = Product.objects.create(
            name="New Product",
            prise=150.0,
            img_url="http://example.com/new_image.jpg",
            type=self.type,
            count=30,
            cost_price=120.0
        )
        self.assertTrue(AdminSellList.objects.filter(product=product).exists())


class FeedbackModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password")
        self.product = Product.objects.create(
            name="Test Product",
            prise=100.0,
            img_url="http://example.com/image.jpg",
            type=Type.objects.create(name="Electronics"),
            count=50,
            cost_price=80.0
        )
        self.feedback = Feedback.objects.create(
            user=self.user,
            question="Issue with product",
            description="The product is defective."
        )

    def test_feedback_creation(self):
        """Тестирование создания отзыва"""
        self.assertEqual(self.feedback.user.username, "testuser")
        self.assertEqual(self.feedback.question, "Issue with product")


class EvaluationModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password")
        self.product = Product.objects.create(
            name="Test Product",
            prise=100.0,
            img_url="http://example.com/image.jpg",
            type=Type.objects.create(name="Electronics"),
            count=50,
            cost_price=80.0
        )
        self.evaluation = Evaluation.objects.create(
            product=self.product,
            user=self.user,
            evaluation=4,
            text="Good product"
        )

    def test_evaluation_creation(self):
        """Тестирование создания оценки"""
        self.assertEqual(self.evaluation.evaluation, 4)
        self.assertEqual(self.evaluation.text, "Good product")


class MessageModelTest(TestCase):

    def setUp(self):
        self.sender = CustomUser.objects.create_user(username="sender", password="password")
        self.receiver = CustomUser.objects.create_user(username="receiver", password="password")
        self.message = MessageModel.objects.create(
            user=self.sender,
            recipient=self.receiver,
            body="Hello, how are you?"
        )

    def test_message_creation(self):
        """Тестирование создания сообщения"""
        self.assertEqual(self.message.body, "Hello, how are you?")
        self.assertEqual(self.message.user.username, "sender")
        self.assertEqual(self.message.recipient.username, "receiver")

    def test_message_characters(self):
        """Тестирование метода characters"""
        self.assertEqual(self.message.characters(), len("Hello, how are you?"))


class AdminSellListModelTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            prise=100.0,
            img_url="http://example.com/image.jpg",
            type=Type.objects.create(name="Electronics"),
            count=50,
            cost_price=80.0
        )

    def test_admin_sell_list_creation_on_product_save(self):
        """Тестируем, что AdminSellList создается при сохранении продукта"""
        sell_list = AdminSellList.objects.get(product=self.product)
        self.assertEqual(sell_list.product, self.product)
        self.assertEqual(sell_list.count, 0)


class UserAuthenticationTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.email = 'test@example.com'
        self.user = get_user_model().objects.create_user(username=self.username, email=self.email,
                                                         password=self.password)

    def test_signup(self):
        url = reverse('signup')
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login(self):
        url = reverse('login')
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('logout')
        response = self.client.post(url)
        self.assertRedirects(response, reverse('login'))


class ProfileTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

    def test_profile_access_without_login(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_profile_access_with_login(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
