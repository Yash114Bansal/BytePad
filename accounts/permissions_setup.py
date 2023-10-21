from django.contrib.auth.models import Group, Permission

department_head_group, created = Group.objects.get_or_create(name='Department Heads')
faculty_group, created = Group.objects.get_or_create(name='Faculty')
student_group, created = Group.objects.get_or_create(name='Students')