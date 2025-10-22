# restaurants/management/commands/seed_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Customer
from restaurants.models import Restaurant, Tag, Item

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with tags and sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database seeding...')
        
        # 1. Create Tags (58 total)
        self.create_tags()
        
        # 2. Create sample owner and restaurants
        self.create_sample_restaurants()
        
        # 3. Create sample customer
        self.create_sample_customer()
        
        self.stdout.write(self.style.SUCCESS('✅ Database seeding completed!'))

    def create_tags(self):
        """Create all 58 predefined tags"""
        self.stdout.write('Creating tags...')
        
        tags = [
            # Cuisine (15 tags)
            'Chinese', 'Japanese', 'Korean', 'Thai', 'Indian',
            'Italian', 'Mexican', 'American', 'Mediterranean', 'French',
            'Vietnamese', 'Greek', 'Eastern Europe', 'African', 'Latin American',
            
            # ProteinType (14 tags)
            'Chicken', 'Beef', 'Pork', 'Lamb', 'Fish',
            'Shrimp', 'Crab', 'Egg', 'Tofu', 'Gluten',
            'Beans', 'Dairy', 'Nuts', 'Mainly Vegetable',
            
            # Spiciness (5 tags)
            'None', 'Mild', 'Medium', 'Hot', 'Extra Hot',
            
            # MealType (4 tags)
            'Combo', 'Drink', 'Main Course', 'Side Dish',
            
            # Flavor (5 tags)
            'Sweet', 'Sour', 'Umami', 'Savory', 'Spicy',
            
            # Allergen (9 tags)
            'Milk', 'Eggs', 'Fish', 'Crustacean Shellfish', 'Tree Nuts',
            'Peanuts', 'Wheat', 'Soybeans', 'Sesame',
            
            # Nutrition (6 tags)
            'High Protein', 'Low Carb', 'Low Sugar', 'Low Fat',
            'High Fiber', 'Low Calorie',
        ]
        
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(f'  ✓ Created tag: {tag_name}')
        
        self.stdout.write(self.style.SUCCESS(f'✅ Created {len(tags)} tags'))

    def create_sample_restaurants(self):
        """Create sample restaurants with mock data"""
        self.stdout.write('Creating sample restaurants...')
        
        # Create owner user
        owner_user, created = User.objects.get_or_create(
            username='owner1',
            defaults={
                'type': 'owner',
                'email': 'owner@example.com'
            }
        )
        if created:
            owner_user.set_password('password123')
            owner_user.save()
            self.stdout.write('  ✓ Created owner user')
        
        # Sample restaurants (Seattle area)
        restaurants_data = [
            {
                'name': 'Healthy Bites',
                'google_place_id': 'ChIJ_sample_healthy_bites',
                'latitude': 47.7623,
                'longitude': -122.2054,
                'address': '10116 Main St, Bothell, WA 98011',
                'description': 'Fresh, healthy meals with a focus on nutrition',
            },
            {
                'name': 'Dragon Palace',
                'google_place_id': 'ChIJ_sample_dragon_palace',
                'latitude': 47.6062,
                'longitude': -122.3321,
                'address': '456 Pike St, Seattle, WA 98101',
                'description': 'Authentic Chinese cuisine',
            },
            {
                'name': 'Thai Spice',
                'google_place_id': 'ChIJ_sample_thai_spice',
                'latitude': 47.6101,
                'longitude': -122.2015,
                'address': '789 Bellevue Way, Bellevue, WA 98004',
                'description': 'Traditional Thai dishes with authentic flavors',
            },
        ]
        
        for rest_data in restaurants_data:
            restaurant, created = Restaurant.objects.get_or_create(
                google_place_id=rest_data['google_place_id'],
                defaults={
                    'user': owner_user,
                    'name': rest_data['name'],
                    'latitude': rest_data['latitude'],
                    'longitude': rest_data['longitude'],
                    'address': rest_data['address'],
                    'description': rest_data['description'],
                }
            )
            
            if created:
                self.stdout.write(f'  ✓ Created restaurant: {rest_data["name"]}')
                self.create_menu_items(restaurant)
        
        self.stdout.write(self.style.SUCCESS('✅ Created sample restaurants'))

    def create_menu_items(self, restaurant):
        """Create sample menu items for a restaurant"""
        
        if 'Healthy' in restaurant.name:
            # Healthy Bites menu
            items_data = [
                {
                    'name': 'Grilled Chicken Salad',
                    'description': 'Fresh greens with grilled chicken breast',
                    'price': 12.99,
                    'totalprotein': 35,
                    'totalgreens': 150,
                    'totalcarb': 20,
                    'totalfat': 10,
                    'totalcalories': 320,
                    'tags': ['American', 'High Protein', 'Low Carb', 'Chicken', 'Main Course', 'None']
                },
                {
                    'name': 'Quinoa Buddha Bowl',
                    'description': 'Quinoa with roasted vegetables and tahini',
                    'price': 11.99,
                    'totalprotein': 15,
                    'totalgreens': 200,
                    'totalcarb': 65,
                    'totalfat': 12,
                    'totalcalories': 450,
                    'tags': ['American', 'High Fiber', 'Mainly Vegetable', 'Main Course', 'None']
                },
            ]
        elif 'Dragon' in restaurant.name:
            # Dragon Palace menu
            items_data = [
                {
                    'name': 'Kung Pao Chicken',
                    'description': 'Spicy stir-fried chicken with peanuts',
                    'price': 14.99,
                    'totalprotein': 30,
                    'totalgreens': 80,
                    'totalcarb': 45,
                    'totalfat': 18,
                    'totalcalories': 480,
                    'tags': ['Chinese', 'Chicken', 'Spicy', 'Hot', 'Peanuts', 'Main Course']
                },
                {
                    'name': 'Vegetable Fried Rice',
                    'description': 'Classic fried rice with mixed vegetables',
                    'price': 9.99,
                    'totalprotein': 8,
                    'totalgreens': 100,
                    'totalcarb': 70,
                    'totalfat': 10,
                    'totalcalories': 400,
                    'tags': ['Chinese', 'Mainly Vegetable', 'Savory', 'None', 'Main Course']
                },
            ]
        else:
            # Thai Spice menu
            items_data = [
                {
                    'name': 'Pad Thai',
                    'description': 'Stir-fried rice noodles with shrimp',
                    'price': 13.99,
                    'totalprotein': 25,
                    'totalgreens': 60,
                    'totalcarb': 55,
                    'totalfat': 15,
                    'totalcalories': 480,
                    'tags': ['Thai', 'Shrimp', 'Sweet', 'Mild', 'Peanuts', 'Main Course']
                },
                {
                    'name': 'Green Curry',
                    'description': 'Spicy coconut curry with vegetables',
                    'price': 12.99,
                    'totalprotein': 20,
                    'totalgreens': 120,
                    'totalcarb': 40,
                    'totalfat': 20,
                    'totalcalories': 440,
                    'tags': ['Thai', 'Spicy', 'Hot', 'Mainly Vegetable', 'Main Course']
                },
            ]
        
        for item_data in items_data:
            tag_names = item_data.pop('tags')
            item, created = Item.objects.get_or_create(
                restaurant=restaurant,
                name=item_data['name'],
                defaults=item_data
            )
            
            if created:
                # Add tags
                tags = Tag.objects.filter(name__in=tag_names)
                item.tags.set(tags)
                self.stdout.write(f'    ✓ Created item: {item.name}')

    def create_sample_customer(self):
        """Create a sample customer user"""
        self.stdout.write('Creating sample customer...')
        
        customer_user, created = User.objects.get_or_create(
            username='customer1',
            defaults={
                'type': 'customer',
                'email': 'customer@example.com'
            }
        )
        
        if created:
            customer_user.set_password('password123')
            customer_user.save()
            
            Customer.objects.create(
                user=customer_user,
                firstname='John',
                lastname='Doe',
                age=25,
                gender='Male',
                weight=70,
                memo='I want to keep fit and build muscle'
            )
            self.stdout.write(self.style.SUCCESS('  ✓ Created sample customer'))