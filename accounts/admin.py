from django.contrib import admin
from .models import HomeSection, AboutSection, WorkExperience, Project, SkillEntry, Education, Certification, ContactInfo, ContactMessage
from django.db.models.functions import ExtractYear


@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'title', 'description')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('profile_image', 'welcome_text', 'name', 'title', 'description')
        }),
        ('Technical Skills', {
            'fields': ('tech_tags',)
        }),
        ('Social & Contact', {
            'fields': ('social_links', 'location', 'availability_status')
        }),
    )

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('primary_role', 'headline', 'experience_years', 'project_count', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('primary_role', 'headline', 'summary')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('primary_role', 'headline', 'summary')
        }),
        ('Skills & Resume', {
            'fields': ('skills_list', 'pdf_resume')
        }),
        ('Experience & Stats', {
            'fields': ('experience_years', 'project_count', 'education_summary')
        }),
        ('Display Stats', {
            'fields': ('client_satisfaction', 'years_experience'),
            'description': 'These fields are for display purposes in the stats section'
        }),
    )


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'role', 'start_year', 'end_year', 'created_at')
    list_filter = ('start_year', 'end_year', 'created_at')
    search_fields = ('company_name', 'role', 'description')
    list_editable = ('start_year', 'end_year')
    
    fieldsets = (
        ('Job Information', {
            'fields': ('company_name', 'role', 'description')
        }),
        ('Timeline', {
            'fields': ('start_year', 'end_year')
        }),
        ('Achievements', {
            'fields': ('highlights',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            start_year_only=ExtractYear('start_year')
        ).order_by('-start_year_only')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'order', 'preview_url', 'code_url', 'created_at')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('title', 'short_description', 'tech_stack')
    list_editable = ('category', 'is_featured', 'order')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'image', 'short_description')
        }),
        ('Technical Details', {
            'fields': ('tech_stack',)
        }),
        ('Links', {
            'fields': ('preview_url', 'code_url')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'order')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('order', '-created_at')


@admin.register(SkillEntry)
class SkillEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'level', 'percentage', 'order', 'created_at')
    list_filter = ('type', 'level', 'created_at')
    search_fields = ('name',)
    list_editable = ('type', 'level', 'percentage', 'order')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'type')
        }),
        ('Proficiency Details', {
            'fields': ('level', 'percentage'),
            'description': 'Level and percentage are mainly for Languages, Frameworks, and Tools'
        }),
        ('Display Options', {
            'fields': ('order',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('type', 'order', 'name')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_year', 'end_year', 'created_at')
    list_filter = ('start_year', 'end_year', 'institution', 'created_at')
    search_fields = ('degree', 'institution', 'description')
    list_editable = ('start_year', 'end_year')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('degree', 'institution', 'description')
        }),
        ('Timeline', {
            'fields': ('start_year', 'end_year')
        }),
        ('Achievements', {
            'fields': ('achievements',),
            'description': 'Comma-separated achievements (e.g., GPA: 3.8/4.0, Dean\'s List: 6 semesters)'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-start_year')

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'institution', 'issue_date', 'certificate_url', 'order', 'created_at')
    list_filter = ('institution', 'issue_date', 'created_at')
    search_fields = ('title', 'institution', 'description')
    list_editable = ('order',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'institution', 'description')
        }),
        ('Certificate Details', {
            'fields': ('certificate_url', 'issue_date')
        }),
        ('Display Options', {
            'fields': ('order',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('order', '-issue_date')

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'address', 'availability_status', 'updated_at')
    search_fields = ('email', 'phone', 'address')
    
    fieldsets = (
        ('Basic Contact Information', {
            'fields': ('address', 'email', 'phone', 'timezone')
        }),
        ('Social Media Links', {
            'fields': ('linkedin', 'github', 'twitter', 'stack_overflow', 'dribbble')
        }),
        ('Additional Information', {
            'fields': ('availability_status', 'additional_info', 'map_url')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one ContactInfo instance
        return not ContactInfo.objects.exists()

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'subject', 'message', 'created_at')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
