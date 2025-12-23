from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Creates Manager and Developer gropus with initial permissions'

    def handle(self, *args, **options):
        manager_group,_ = Group.objects.get_or_create(name='Manager')
        developer_group,_ = Group.objects.get_or_create(name='Developer')
        try:
            delete_permission = Permission.objects.get(codename='delete_task')
            manager_group.permissions.add(delete_permission)
            self.stdout.write(self.style.SUCCESS('Successfully assigned delete_task to Manager'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.WARNING('Permission delete_task is not found. Run migrations first!'))
