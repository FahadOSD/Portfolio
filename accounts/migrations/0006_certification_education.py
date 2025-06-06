# Generated by Django 5.2 on 2025-05-22 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_skillentry_alter_project_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Certificate title', max_length=150)),
                ('institution', models.CharField(help_text='Issuing institution/organization', max_length=150)),
                ('description', models.TextField(blank=True, help_text='Brief description of the certification')),
                ('certificate_url', models.URLField(blank=True, help_text='URL to view the certificate', null=True)),
                ('issue_date', models.DateField(blank=True, help_text='Date when certificate was issued', null=True)),
                ('order', models.IntegerField(default=0, help_text='Display order (lower numbers first)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Certification',
                'verbose_name_plural': 'Certifications',
                'ordering': ['order', '-issue_date', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(help_text='e.g., BSc in Computer Science', max_length=150)),
                ('institution', models.CharField(help_text='e.g., University of Dhaka', max_length=150)),
                ('start_year', models.IntegerField(help_text='Year when you started')),
                ('end_year', models.IntegerField(blank=True, help_text='Year when you completed (leave blank if ongoing)', null=True)),
                ('description', models.TextField(blank=True, help_text='Brief description of your studies')),
                ('achievements', models.TextField(blank=True, help_text="Comma-separated achievements (e.g., GPA: 3.8/4.0, Dean's List: 6 semesters)")),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Education',
                'verbose_name_plural': 'Education',
                'ordering': ['-start_year'],
            },
        ),
    ]
