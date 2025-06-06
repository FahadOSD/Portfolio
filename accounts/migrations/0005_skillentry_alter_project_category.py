# Generated by Django 5.2 on 2025-05-22 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkillEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Skill name (e.g., Python, Django, Web Development)', max_length=100)),
                ('type', models.CharField(choices=[('LANGUAGE', 'Programming Languages'), ('FRAMEWORK', 'Frameworks & Libraries'), ('TOOL', 'Tools & Technologies'), ('SPECIALTY', 'Specialty Areas'), ('ADDITIONAL', 'Additional Technologies')], help_text='Category of the skill', max_length=50)),
                ('level', models.CharField(blank=True, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('Expert', 'Expert')], help_text='Proficiency level (optional for specialty/additional skills)', max_length=50, null=True)),
                ('percentage', models.IntegerField(blank=True, help_text='Skill proficiency percentage (0-100, for progress bars)', null=True)),
                ('order', models.IntegerField(default=0, help_text='Display order within category (lower numbers first)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Skill Entry',
                'verbose_name_plural': 'Skill Entries',
                'ordering': ['type', 'order', 'name'],
            },
        ),
        migrations.AlterField(
            model_name='project',
            name='category',
            field=models.CharField(choices=[('web', 'Web Development'), ('python', 'Python'), ('IoT', 'IoT'), ('ml', 'Machine Learning'), ('nlp', 'Natural Language Processing'), ('api', 'API Development'), ('mobile', 'Mobile Development'), ('other', 'Other')], help_text='Project category for filtering', max_length=50),
        ),
    ]
