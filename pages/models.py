from django.db import models


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
        return f"{self.category} — {self.name}"


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
    tech_stack  = models.CharField(max_length=300, help_text="Comma-separated: Django, Bootstrap 5, ...")
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
        return f"{self.title} @ {self.organization}"

    @property
    def period(self):
        return f"{self.start_date} – {self.end_date or 'Present'}"


class Certification(models.Model):
    title  = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date   = models.CharField(max_length=30)
    icon   = models.CharField(max_length=50, default='award', help_text="Lucide icon name")
    image  = models.ImageField(
        upload_to='certifications/', blank=True, null=True,
        help_text="Upload a scan/photo of the certificate"
    )
    link   = models.URLField(
        blank=True,
        help_text="External verification URL. If both image and link are set, image opens in lightbox AND a link button appears."
    )
    order  = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
