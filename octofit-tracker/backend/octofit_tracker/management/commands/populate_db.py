from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, User, Activity, Workout, Leaderboard
from django.db import transaction
from datetime import date

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.SUCCESS('Deleting old data...'))
            for model in [Leaderboard, Activity, Workout, User, Team]:
                for obj in model.objects.all():
                    if getattr(obj, 'id', None) is not None:
                        obj.delete()

            self.stdout.write(self.style.SUCCESS('Creating teams...'))
            marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
            dc = Team.objects.create(name='DC', description='DC superheroes')

            self.stdout.write(self.style.SUCCESS('Creating users...'))
            tony = User.objects.create(name='Tony Stark', email='tony@marvel.com', team=marvel)
            steve = User.objects.create(name='Steve Rogers', email='steve@marvel.com', team=marvel)
            bruce = User.objects.create(name='Bruce Wayne', email='bruce@dc.com', team=dc)
            clark = User.objects.create(name='Clark Kent', email='clark@dc.com', team=dc)

            self.stdout.write(self.style.SUCCESS('Creating activities...'))
            Activity.objects.create(user=tony, type='Running', duration=30, calories=300, date=date.today())
            Activity.objects.create(user=steve, type='Cycling', duration=45, calories=400, date=date.today())
            Activity.objects.create(user=bruce, type='Swimming', duration=60, calories=500, date=date.today())
            Activity.objects.create(user=clark, type='Flying', duration=120, calories=1000, date=date.today())

            self.stdout.write(self.style.SUCCESS('Creating workouts...'))
            w1 = Workout.objects.create(name='Super Strength', description='Strength workout for heroes')
            w2 = Workout.objects.create(name='Endurance', description='Endurance workout for heroes')
            w1.suggested_for.set([tony, bruce])
            w2.suggested_for.set([steve, clark])

            self.stdout.write(self.style.SUCCESS('Creating leaderboard...'))
            Leaderboard.objects.create(user=tony, score=1500)
            Leaderboard.objects.create(user=steve, score=1200)
            Leaderboard.objects.create(user=bruce, score=1800)
            Leaderboard.objects.create(user=clark, score=2000)

            self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
