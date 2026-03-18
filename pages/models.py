from django.db import models


# ── SINGLETON SITE PROFILE ────────────────────────────────────
class SiteProfile(models.Model):
    """Singleton — only one row. Edit via Admin."""
    full_name   = models.CharField(max_length=200, default='Lakhfif Yahia Abderraouf')
    job_title   = models.CharField(max_length=200, default='Full-Stack Developer · Data Engineer')
    summary     = models.TextField(help_text='Short bio shown on CV and portfolio hero')
    location    = models.CharField(max_length=100, default='Sétif, Algeria')
    avatar      = models.ImageField(upload_to='profile/', blank=True, null=True)
    cv_file     = models.FileField(upload_to='cv/', blank=True, null=True,
                    help_text='Upload your CV as PDF or DOCX for the Download button')

    class Meta:
        verbose_name = 'Site Profile'
        verbose_name_plural = 'Site Profile'

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce singleton
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            'summary': (
                'Full-Stack Developer and Data Engineer with a Master\'s in Big Data & '
                'Web Technologies (IDTW, Université Sétif 1, July 2024). Delivers production '
                'SaaS platforms across healthcare, automotive, tourism, and education. '
                'Startup Label acquired (Label Projet Innovant). University-level teacher '
                'and clinical IT infrastructure administrator.'
            )
        })
        return obj


# ── CONTACT LINKS ─────────────────────────────────────────────
class ContactLink(models.Model):
    TYPE_CHOICES = [
        ('email',    'Email'),
        ('phone',    'Phone / WhatsApp'),
        ('github',   'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('website',  'Website'),
        ('other',    'Other'),
    ]
    ICON_MAP = {
        'email':    'mail',
        'phone':    'phone',
        'github':   'github',
        'linkedin': 'linkedin',
        'website':  'globe',
        'other':    'link',
    }

    link_type   = models.CharField(max_length=20, choices=TYPE_CHOICES)
    label       = models.CharField(max_length=100, help_text='Display text e.g. yahiaAlg')
    url         = models.CharField(max_length=300, help_text='Full URL or value (mailto:, tel:, https://...)')
    order       = models.PositiveSmallIntegerField(default=0)
    show_on_cv  = models.BooleanField(default=True, help_text='Include in print CV')

    class Meta:
        ordering = ['order']
        verbose_name = 'Contact Link'

    def __str__(self):
        return f'{self.get_link_type_display()} — {self.label}'

    @property
    def icon(self):
        return self.ICON_MAP.get(self.link_type, 'link')

    @property
    def href(self):
        v = self.url.strip()
        if self.link_type == 'email' and not v.startswith('mailto:'):
            return f'mailto:{v}'
        if self.link_type == 'phone' and not v.startswith('tel:') and not v.startswith('https:'):
            return f'https://wa.me/{v.replace("+","").replace(" ","")}'
        return v


# ── LANGUAGE ──────────────────────────────────────────────────
class Language(models.Model):
    name  = models.CharField(max_length=100)
    level = models.CharField(max_length=100, help_text='e.g. Native, B2 Upper-Intermediate')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.name} — {self.level}'


# ── TRAINING COURSE ───────────────────────────────────────────
class TrainingCourse(models.Model):
    title       = models.CharField(max_length=200)
    subtitle    = models.CharField(max_length=200, blank=True, help_text='Organiser / institution')
    description = models.TextField(blank=True, help_text='Topics covered, comma-separated is fine')
    period      = models.CharField(max_length=60, help_text='e.g. 2023–2024 or May 2024')
    certificate = models.ImageField(upload_to='training/', blank=True, null=True)
    link        = models.URLField(blank=True, help_text='Verification or course URL')
    order       = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


# ── SKILL CATEGORY + SKILL ────────────────────────────────────
class SkillCategory(models.Model):
    name  = models.CharField(max_length=100)
    icon  = models.CharField(max_length=50, help_text="Lucide icon name e.g. 'code-2'")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Skill Categories'

    def __str__(self):
        return self.name


class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name     = models.CharField(max_length=100)
    order    = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.category} — {self.name}'


# ── PROJECT ───────────────────────────────────────────────────
class Project(models.Model):
    CATEGORY_CHOICES = [
        ('saas',      'SaaS / Web App'),
        ('ai',        'AI / ML'),
        ('mobile',    'Mobile'),
        ('desktop',   'Desktop'),
        ('elearning', 'E-Learning'),
        ('other',     'Other'),
    ]
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True)
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='saas')
    client      = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    tech_stack  = models.CharField(max_length=300, help_text='Comma-separated: Django, Bootstrap 5, ...')
    image       = models.ImageField(upload_to='projects/', blank=True, null=True)
    live_url    = models.URLField(blank=True)
    github_url  = models.URLField(blank=True)
    featured    = models.BooleanField(default=False)
    order       = models.PositiveSmallIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]


# ── EXPERIENCE ────────────────────────────────────────────────
class Experience(models.Model):
    title        = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    location     = models.CharField(max_length=100, blank=True)
    start_date   = models.CharField(max_length=30)
    end_date     = models.CharField(max_length=30, blank=True)
    description  = models.TextField(blank=True)
    exp_type     = models.CharField(max_length=10,
                       choices=[('work','Work'),('teach','Teaching'),('edu','Education')],
                       default='work')
    order        = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.title} @ {self.organization}'

    @property
    def period(self):
        return f"{self.start_date} – {self.end_date or 'Present'}"


# ── CERTIFICATION ─────────────────────────────────────────────
class Certification(models.Model):
    title  = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date   = models.CharField(max_length=30)
    icon   = models.CharField(max_length=50, default='award', help_text='Lucide icon name')
    image  = models.ImageField(upload_to='certifications/', blank=True, null=True,
                 help_text='Upload scan/photo of certificate')
    link   = models.URLField(blank=True,
                 help_text='External verification URL')
    order  = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
