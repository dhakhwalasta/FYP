from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fyp.models import Business, Event, Review, UserProfile

class Command(BaseCommand):
    help = 'Seeds the database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Clear existing data to start fresh
        Review.objects.all().delete()
        Event.objects.all().delete()
        Business.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # --- Create Users ---
        user1, _ = User.objects.get_or_create(username='johndoe', defaults={'password': 'password', 'email': 'john@example.com'})
        user1.set_password('password123')
        user1.save()
        UserProfile.objects.get_or_create(user=user1, defaults={'preferences': ['food', 'books']})

        user2, _ = User.objects.get_or_create(username='janedoe', defaults={'password': 'password', 'email': 'jane@example.com'})
        user2.set_password('password123')
        user2.save()
        UserProfile.objects.get_or_create(user=user2, defaults={'preferences': ['clothing']})

        business_owner, _ = User.objects.get_or_create(username='business_owner', defaults={'password': 'password', 'email': 'owner@example.com'})
        business_owner.set_password('password123')
        business_owner.save()
        UserProfile.objects.get_or_create(user=business_owner, defaults={'preferences': ['food', 'clothing']})

        self.stdout.write('Users created.')

        # --- Create Businesses ---
        biz1, _ = Business.objects.get_or_create(
            name='The Reading Nook',
            defaults={
                'description': 'A cozy bookstore with a great selection of new and used books.',
                'category': 'books',
                'owner': business_owner
            }
        )

        biz2, _ = Business.objects.get_or_create(
            name='Gourmet Burger Kitchen',
            defaults={
                'description': 'The best burgers in town, made with locally sourced ingredients.',
                'category': 'food',
                'owner': business_owner
            }
        )
        
        biz3, _ = Business.objects.get_or_create(
            name='Vintage Threads',
            defaults={
                'description': 'A curated collection of vintage and retro clothing.',
                'category': 'clothing',
                'owner': business_owner
            }
        )

        self.stdout.write('Businesses created.')

        # --- Create Events ---
        Event.objects.get_or_create(
            name='Poetry Reading Night',
            defaults={
                'description': 'An open mic night for local poets.',
                'category': 'books',
                'business': biz1
            }
        )

        Event.objects.get_or_create(
            name='Burger of the Week Special',
            defaults={
                'description': 'Come try our special edition burger, available for one week only!',
                'category': 'food',
                'business': biz2
            }
        )
        
        self.stdout.write('Events created.')

        # --- Create Reviews ---
        Review.objects.get_or_create(
            business=biz1,
            user=user1,
            defaults={'rating': 5, 'comment': 'Absolutely love this place! So many great finds.'}
        )

        Review.objects.get_or_create(
            business=biz2,
            user=user1,
            defaults={'rating': 4, 'comment': 'Great burgers, but the fries were a bit soggy.'}
        )

        Review.objects.get_or_create(
            business=biz2,
            user=user2,
            defaults={'rating': 5, 'comment': 'Best burger I have ever had! Highly recommend.'}
        )
        
        Review.objects.get_or_create(
            business=biz3,
            user=user2,
            defaults={'rating': 5, 'comment': 'Found a beautiful dress here. The owner is so helpful!'}
        )

        self.stdout.write('Reviews created.')
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
