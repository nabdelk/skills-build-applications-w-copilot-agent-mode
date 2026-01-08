from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Suppression des anciennes données...'))
        Activity.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Création des équipes...'))
        marvel = Team.objects.create(name='Marvel', description='Team Marvel')
        dc = Team.objects.create(name='DC', description='Team DC')

        self.stdout.write(self.style.SUCCESS('Création des utilisateurs...'))
        users = [
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel, is_superhero=True),
            User.objects.create(name='Captain America', email='cap@marvel.com', team=marvel, is_superhero=True),
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel, is_superhero=True),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc, is_superhero=True),
            User.objects.create(name='Superman', email='superman@dc.com', team=dc, is_superhero=True),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc, is_superhero=True),
        ]

        self.stdout.write(self.style.SUCCESS('Création des activités...'))
        Activity.objects.create(user=users[0], type='Running', duration=30, date=timezone.now().date())
        Activity.objects.create(user=users[1], type='Cycling', duration=45, date=timezone.now().date())
        Activity.objects.create(user=users[2], type='Swimming', duration=60, date=timezone.now().date())
        Activity.objects.create(user=users[3], type='Yoga', duration=40, date=timezone.now().date())
        Activity.objects.create(user=users[4], type='Boxing', duration=50, date=timezone.now().date())
        Activity.objects.create(user=users[5], type='Pilates', duration=35, date=timezone.now().date())

        self.stdout.write(self.style.SUCCESS('Création des workouts...'))
        w1 = Workout.objects.create(name='Full Body', description='Full body workout')
        w2 = Workout.objects.create(name='Cardio Blast', description='Intense cardio')
        w1.suggested_for.set(users[:3])
        w2.suggested_for.set(users[3:])

        self.stdout.write(self.style.SUCCESS('Création des leaderboards...'))
        Leaderboard.objects.create(team=marvel, total_points=135)
        Leaderboard.objects.create(team=dc, total_points=125)

        self.stdout.write(self.style.SUCCESS('Création de l’index unique sur email pour la collection users...'))
        with connection.cursor() as cursor:
            cursor.execute('''db.users.createIndex({ "email": 1 }, { unique: true })''')

        self.stdout.write(self.style.SUCCESS('Base de données octofit_db initialisée avec des données de test !'))
