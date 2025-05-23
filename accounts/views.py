from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import (
    HomeSection, AboutSection, WorkExperience,
    Project, SkillEntry, Education, Certification,
    ContactInfo, ContactMessage
)
from .forms import ContactForm

@csrf_exempt
def home_view(request):
    # Home and About Sections
    home_section = HomeSection.objects.first()
    about_section = AboutSection.objects.first()

    # Work Experience
    work_experiences = WorkExperience.objects.all().order_by('-start_year')

    # Projects Filtering
    category_filter = request.GET.get('category', 'all')
    if category_filter == 'all':
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(category=category_filter)

    # Handle AJAX for Projects
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        projects_data = []
        for project in projects:
            projects_data.append({
                'id': project.id,
                'title': project.title,
                'category': project.category,
                'category_display': project.get_category_display_short(),
                'image_url': project.image.url if project.image else '',
                'short_description': project.short_description,
                'tech_stack': project.get_tech_stack_list(),
                'preview_url': project.preview_url,
                'code_url': project.code_url,
            })
        return JsonResponse({'projects': projects_data})

    # Get unique categories
    categories = Project.objects.values_list('category', flat=True).distinct()
    
    # Create a list of tuples with category and display name
    categories_with_display = []
    for category in categories:
        # Create a dummy project to get the display name
        dummy_project = Project(category=category)
        categories_with_display.append((category, dummy_project.get_category_display_short()))

    # Skills
    skills_by_type = {}
    for choice in SkillEntry.TYPE_CHOICES:
        type_key = choice[0]
        skills_by_type[type_key] = SkillEntry.objects.filter(type=type_key).order_by('order', 'name')

    # Education & Certification
    education_entries = Education.objects.all().order_by('-start_year')
    certifications = Certification.objects.all().order_by('order', '-issue_date')

    # Contact Info & Form
    contact_info = ContactInfo.objects.first()
    if request.method == 'POST' and not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            try:
                contact_message.send_notification_email()
            except Exception as e:
                print(f"Failed to send notification email: {e}")
            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    elif request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            form = ContactForm(data)
            if form.is_valid():
                contact_message = form.save()
                try:
                    contact_message.send_notification_email()
                except Exception as e:
                    print(f"Failed to send notification email: {e}")
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you! Your message has been sent successfully.'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred. Please try again.'
            })

    else:
        form = ContactForm()

    context = {
        'home_section': home_section,
        'about_section': about_section,
        'work_experiences': work_experiences,
        'projects': projects,
        'categories': categories,
        'categories_with_display': categories_with_display,
        'active_category': category_filter,
        'skills_by_type': skills_by_type,
        'skill_types': SkillEntry.TYPE_CHOICES,
        'education_entries': education_entries,
        'certifications': certifications,
        'contact_info': contact_info,
        'form': form,
    }

    return render(request, 'index.html', context)
