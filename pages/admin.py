from django.contrib import admin
from django.utils.html import format_html
from .models import (SiteProfile, ContactLink, Language, TrainingCourse,
                     Project, SkillCategory, Skill, Experience, Certification)


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Identity', {'fields': ['full_name', 'job_title', 'avatar', 'cv_file', 'location']}),
        ('Bio',      {'fields': ['summary']}),
    ]
    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactLink)
class ContactLinkAdmin(admin.ModelAdmin):
    list_display       = ('order', 'link_type', 'label', 'url', 'show_on_cv')
    list_display_links = ('label',)
    list_editable      = ('order', 'show_on_cv')
    list_filter        = ('link_type', 'show_on_cv')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display       = ('order', 'name', 'level')
    list_display_links = ('name',)
    list_editable      = ('order',)


@admin.register(TrainingCourse)
class TrainingCourseAdmin(admin.ModelAdmin):
    list_display       = ('order', 'title', 'subtitle', 'period')
    list_display_links = ('title',)
    list_editable      = ('order',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display       = ('order', 'thumb', 'title', 'category', 'client', 'featured', 'live_link')
    list_display_links = ('title',)
    list_editable      = ('order', 'featured')
    list_filter        = ('category', 'featured')
    search_fields      = ('title', 'client', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering           = ('order',)

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;">', obj.image.url)
        return '—'
    thumb.short_description = 'IMG'

    def live_link(self, obj):
        if obj.live_url:
            return format_html('<a href="{}" target="_blank">🔗</a>', obj.live_url)
        return '—'
    live_link.short_description = 'Live'


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 2


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display       = ('order', 'name', 'icon')
    list_display_links = ('name',)
    list_editable      = ('order',)
    inlines            = [SkillInline]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display       = ('order', 'title', 'organization', 'exp_type', 'start_date', 'end_date')
    list_display_links = ('title',)
    list_editable      = ('order',)
    list_filter        = ('exp_type',)


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display       = ('order', 'title', 'issuer', 'date')
    list_display_links = ('title',)
    list_editable      = ('order',)
