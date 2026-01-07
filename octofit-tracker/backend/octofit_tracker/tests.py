from django.test import TestCase
from .models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class UserModelTest(TestCase):
    def test_create_user(self):
        team = Team.objects.create(name='Marvel', description='Marvel Team')
        user = User.objects.create(name='Iron Man', email='ironman@marvel.com', team=team, is_superhero=True)
        self.assertEqual(user.name, 'Iron Man')
        self.assertEqual(user.team.name, 'Marvel')

class ActivityModelTest(TestCase):
    def test_create_activity(self):
        team = Team.objects.create(name='DC', description='DC Team')
        user = User.objects.create(name='Batman', email='batman@dc.com', team=team, is_superhero=True)
        activity = Activity.objects.create(user=user, type='Running', duration=30, date=timezone.now().date())
        self.assertEqual(activity.user.name, 'Batman')
        self.assertEqual(activity.type, 'Running')

class WorkoutModelTest(TestCase):
    def test_create_workout(self):
        workout = Workout.objects.create(name='Pushups', description='Upper body workout')
        self.assertEqual(workout.name, 'Pushups')

class LeaderboardModelTest(TestCase):
    def test_create_leaderboard(self):
        team = Team.objects.create(name='Avengers', description='Avengers Team')
        leaderboard = Leaderboard.objects.create(team=team, total_points=100)
        self.assertEqual(leaderboard.team.name, 'Avengers')
        self.assertEqual(leaderboard.total_points, 100)
