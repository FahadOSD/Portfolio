from django.db import models
import json
from django.core.mail import send_mail
from django.conf import settings

class HomeSection(models.Model):
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    welcome_text = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tech_tags = models.TextField(blank=True, null=True, help_text="Comma-separated values")
    social_links = models.TextField(blank=True, null=True, help_text="JSON format: {\"linkedin\": \"url\", \"github\": \"url\", \"twitter\": \"url\", \"email\": \"email\"}")
    location = models.CharField(max_length=100, blank=True, null=True)
    availability_status = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Home Section"
        verbose_name_plural = "Home Section"
    
    def __str__(self):
        return f"Home Section - {self.name or 'Unnamed'}"
    
    def get_tech_tags_list(self):
        """Return tech tags as a list"""
        if self.tech_tags:
            return [tag.strip() for tag in self.tech_tags.split(',') if tag.strip()]
        return []
    
    def get_social_links_dict(self):
        """Return social links as a dictionary"""
        if self.social_links:
            try:
                return json.loads(self.social_links)
            except json.JSONDecodeError:
                return {}
        return {}

class AboutSection(models.Model):
    primary_role = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Python Developer")
    headline = models.CharField(max_length=150, blank=True, null=True, help_text="Main headline about yourself")
    summary = models.TextField(blank=True, null=True, help_text="Detailed description about yourself")
    skills_list = models.TextField(blank=True, null=True, help_text="Comma-separated skills (e.g., Web Development,Data Science,Machine Learning)")
    pdf_resume = models.FileField(upload_to='resumes/', blank=True, null=True, help_text="Upload your resume in PDF format")
    experience_years = models.IntegerField(blank=True, null=True, help_text="Years of professional experience")
    project_count = models.IntegerField(blank=True, null=True, help_text="Number of completed projects")
    education_summary = models.CharField(max_length=250, blank=True, null=True, help_text="e.g., BSc in Computer Science, University Name")
    client_satisfaction = models.CharField(max_length=10, blank=True, null=True, help_text="e.g., 98%")
    years_experience = models.CharField(max_length=10, blank=True, null=True, help_text="e.g., 5+")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"
    
    def __str__(self):
        return f"About Section - {self.primary_role or 'Unnamed'}"
    
    def get_skills_list(self):
        """Return skills as a list"""
        if self.skills_list:
            return [skill.strip() for skill in self.skills_list.split(',') if skill.strip()]
        return []

class WorkExperience(models.Model):
    company_name = models.CharField(max_length=150, help_text="e.g., Tech Innovate Ltd.")
    role = models.CharField(max_length=100, help_text="e.g., Software Developer")
    start_year = models.DateField(help_text="Year when you started the job")
    end_year = models.DateField(blank=True, null=True, help_text="Year when you ended the job (leave blank if current)")
    description = models.TextField(help_text="Brief description of your role and responsibilities")
    highlights = models.TextField(help_text="Comma-separated achievements/highlights (e.g., Built RESTful APIs, Improved performance by 25%)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Work Experience"
        verbose_name_plural = "Work Experiences"
        ordering = ['-start_year']  # Default ordering by start year descending
    
    def __str__(self):
        return f"{self.role} at {self.company_name} ({self.start_year}-{self.end_year or 'Present'})"
    
    def get_highlights_list(self):
        """Return highlights as a list"""
        if self.highlights:
            return [highlight.strip() for highlight in self.highlights.split(',') if highlight.strip()]
        return []
    
    def get_year_range(self):
        """Return formatted year range in 'Mon YYYY - Mon YYYY' or 'Mon YYYY - Present' format"""
        start = self.start_year.strftime('%b %Y') if self.start_year else ""
        end = self.end_year.strftime('%b %Y') if self.end_year else "Present"
        return f"{start} - {end}"

    
    def get_display_year(self):
        """Return the year to display in the timeline badge"""
        if self.start_year:
            if hasattr(self.start_year, 'year'):
                return str(self.start_year.year)
            return str(self.start_year)
        return ""

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web Development'),
        ('python', 'Python'),
        ('data', 'Data Science'),
        ('ml', 'Machine Learning'),
        ('nlp', 'Natural Language Processing'),
        ('api', 'API Development'),
        ('mobile', 'Mobile Development'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=150, help_text="Project title")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, help_text="Project category for filtering")
    image = models.ImageField(upload_to='projects/', help_text="Project screenshot or preview image")
    short_description = models.TextField(help_text="Brief description of the project")
    tech_stack = models.TextField(help_text="Comma-separated technologies (e.g., Django,PostgreSQL,Stripe,AWS)")
    preview_url = models.URLField(blank=True, null=True, help_text="Live demo or preview URL")
    code_url = models.URLField(blank=True, null=True, help_text="Source code URL (GitHub, GitLab, etc.)")
    is_featured = models.BooleanField(default=False, help_text="Mark as featured project")
    order = models.PositiveIntegerField(default=0, help_text="Order of display (lower numbers first)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
    
    def get_tech_stack_list(self):
        """Return tech stack as a list"""
        if self.tech_stack:
            return [tech.strip() for tech in self.tech_stack.split(',') if tech.strip()]
        return []
    
    def get_category_display_short(self):
        """Return short category name for display badges"""
        category_map = {
            'web': 'Web',
            'python': 'Python',
            'data': 'Data',
            'ml': 'ML',
            'nlp': 'NLP',
            'api': 'API',
            'mobile': 'Mobile',
            'other': 'Other'
        }
        return category_map.get(self.category, self.category.upper())


from django.db import models

class SkillEntry(models.Model):
    TYPE_CHOICES = [
        ('LANGUAGE', 'Programming Languages'),
        ('FRAMEWORK', 'Frameworks & Libraries'),
        ('TOOL', 'Tools & Technologies'),
        ('SPECIALTY', 'Specialty Areas'),
        ('ADDITIONAL', 'Additional Technologies'),
    ]
    
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert'),
    ]
    
    name = models.CharField(max_length=100, help_text="Skill name (e.g., Python, Django, Web Development)")
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, help_text="Category of the skill")
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, null=True, blank=True, 
                           help_text="Proficiency level (optional for specialty/additional skills)")
    percentage = models.IntegerField(null=True, blank=True, 
                                   help_text="Skill proficiency percentage (0-100, for progress bars)")
    order = models.IntegerField(default=0, help_text="Display order within category (lower numbers first)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Skill Entry"
        verbose_name_plural = "Skill Entries"
        ordering = ['type', 'order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validate percentage range
        if self.percentage is not None and (self.percentage < 0 or self.percentage > 100):
            raise ValidationError({'percentage': 'Percentage must be between 0 and 100.'})
        
        # For skill bars (LANGUAGE, FRAMEWORK, TOOL), percentage and level should be provided
        if self.type in ['LANGUAGE', 'FRAMEWORK', 'TOOL']:
            if self.percentage is None:
                raise ValidationError({'percentage': f'{self.get_type_display()} skills should have a percentage value.'})
            if not self.level:
                raise ValidationError({'level': f'{self.get_type_display()} skills should have a level.'})



class Education(models.Model):
    degree = models.CharField(max_length=150, help_text="e.g., BSc in Computer Science")
    institution = models.CharField(max_length=150, help_text="e.g., University of Dhaka")
    start_year = models.IntegerField(help_text="Year when you started")
    end_year = models.IntegerField(null=True, blank=True, help_text="Year when you completed (leave blank if ongoing)")
    description = models.TextField(blank=True, help_text="Brief description of your studies")
    achievements = models.TextField(blank=True, help_text="Comma-separated achievements (e.g., GPA: 3.8/4.0, Dean's List: 6 semesters)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Education"
        ordering = ['-start_year']  # Most recent first
    
    def __str__(self):
        return f"{self.degree} - {self.institution} ({self.start_year}-{self.end_year or 'Present'})"
    
    def get_achievements_list(self):
        """Return achievements as a list"""
        if self.achievements:
            return [achievement.strip() for achievement in self.achievements.split(',') if achievement.strip()]
        return []
    
    def get_year_range(self):
        """Return formatted year range"""
        if self.end_year:
            return f"{self.start_year} - {self.end_year}"
        return f"{self.start_year} - Present"
    
    def get_display_year(self):
        """Return the year to display in the timeline badge"""
        if self.end_year is None:
            return str(self.start_year)
        return str(self.end_year)

class Certification(models.Model):
    title = models.CharField(max_length=150, help_text="Certificate title")
    institution = models.CharField(max_length=150, help_text="Issuing institution/organization")
    description = models.TextField(blank=True, help_text="Brief description of the certification")
    certificate_url = models.URLField(blank=True, null=True, help_text="URL to view the certificate")
    issue_date = models.DateField(null=True, blank=True, help_text="Date when certificate was issued")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"
        ordering = ['order', '-issue_date', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.institution}"

class ContactInfo(models.Model):
    address = models.CharField(max_length=255, help_text="Your location/address")
    email = models.EmailField(help_text="Your contact email")
    phone = models.CharField(max_length=20, help_text="Your phone number")
    linkedin = models.URLField(blank=True, null=True, help_text="LinkedIn profile URL")
    github = models.URLField(blank=True, null=True, help_text="GitHub profile URL")
    twitter = models.URLField(blank=True, null=True, help_text="Twitter profile URL")
    stack_overflow = models.URLField(blank=True, null=True, help_text="Stack Overflow profile URL")
    dribbble = models.URLField(blank=True, null=True, help_text="Dribbble profile URL")
    additional_info = models.TextField(blank=True, help_text="Additional availability/contact information")
    map_url = models.URLField(blank=True, null=True, help_text="Google Maps embed URL or location URL")
    timezone = models.CharField(max_length=50, blank=True, help_text="Your timezone (e.g., GMT +6)")
    availability_status = models.CharField(max_length=200, blank=True, help_text="Current availability status")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"
    
    def __str__(self):
        return f"Contact Info - {self.email}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, help_text="Sender's name")
    email = models.EmailField(help_text="Sender's email")
    subject = models.CharField(max_length=200, help_text="Message subject")
    message = models.TextField(help_text="Message content")
    is_read = models.BooleanField(default=False, help_text="Mark as read")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
    
    def send_notification_email(self):
        """Send notification email to admin when new message is received"""
        try:
            admin_email = getattr(settings, 'ADMIN_EMAIL', None)
            if admin_email:
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
                send_mail(
                    subject=f"New Contact Form Submission: {self.subject}",
                    message=f"Name: {self.name}\nEmail: {self.email}\nSubject: {self.subject}\n\nMessage:\n{self.message}",
                    from_email=from_email,
                    recipient_list=[admin_email],
                    fail_silently=True,
                )
                print(f"Notification email sent to {admin_email}")
                return True
            else:
                print("ADMIN_EMAIL not set in settings")
                return False
        except Exception as e:
            print(f"Failed to send notification email: {e}")
            return False
