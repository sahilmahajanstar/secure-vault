import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vault.settings")
import django

django.setup()

from users.models.users import Users
def create_superuser(username, email, password, first_name, last_name, is_staff, is_superuser, email_verified, role):
    if Users.objects.all().filter(username=username).exists():
        print('Superuser already exists')
    else:
        user =Users.objects.all().create(username=username, email=email)
        user.set_password(password)
        user.role = role
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.email_verified = email_verified
        user.save()
        print('user created successfully')


if __name__ == '__main__':
    create_superuser('admin', 'admin@example.com', 'Admin@123', 'Admin', 'User', True, True, True, 'admin')
    create_superuser('testuser', 'testuser@example.com', 'test@123', 'Test', 'User', False, False, False, 'user')
    create_superuser('testuser2', 'testuser2@example.com', 'test@123', 'Test', 'User2', False, False, False, 'user')
    create_superuser('testuser3', 'testuser3@example.com', 'test@123', 'Test', 'User3', False, False, False, 'user')
    
