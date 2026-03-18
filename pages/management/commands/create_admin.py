from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or update admin superuser (admin/admin123)"

    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_superuser": True,
                "is_staff": True,
            },
        )
        if created or not user.has_usable_password():
            user.set_password("admin123")
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created admin user "admin" (password: admin123)'
                )
            )
        else:
            self.stdout.write(self.style.WARNING('Admin user "admin" already exists'))
