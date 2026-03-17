from django.contrib import admin
from django.utils.html import format_html
from .models import Project, SkillCategory, Skill, Experience, Certification


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
            return format_html('<a href="{}" target="_blank">🔗 Live</a>', obj.live_url)
        return '—'
    live_link.short_description = 'Live'


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 3


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
    list_display       = ('order', 'cert_thumb', 'title', 'issuer', 'date', 'has_image', 'has_link')
    list_display_links = ('title',)
    list_editable      = ('order',)
    fieldsets = (
        (None, {'fields': ('title', 'issuer', 'date', 'icon', 'order')}),
        ('Media', {'fields': ('image', 'link'),
                   'description': 'Upload a scan/photo and/or add a verification URL. '
                                  'If image is uploaded it opens in a lightbox. '
                                  'If only a link is set, clicking opens the URL directly.'}),
    )

    def cert_thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:44px;width:66px;object-fit:cover;border-radius:4px;">',
                obj.image.url)
        return '—'
    cert_thumb.short_description = 'Preview'

    def has_image(self, obj):
        return format_html('<i>🖼</i>') if obj.image else '—'
    has_image.short_description = 'Image'

    def has_link(self, obj):
        if obj.link:
            return format_html('<a href="{}" target="_blank">🔗</a>', obj.link)
        return '—'
    has_link.short_description = 'Link'
