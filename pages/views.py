from django.shortcuts import render, get_object_or_404
from .models import (Project, SkillCategory, Experience, Certification,
                     Language, TrainingCourse)


def _base_ctx():
    return {
        'skill_categories': SkillCategory.objects.prefetch_related('skills'),
        'experiences':      Experience.objects.filter(exp_type__in=['work', 'teach']),
        'education':        Experience.objects.filter(exp_type='edu'),
        'certifications':   Certification.objects.all(),
        'languages':        Language.objects.all(),
        'training_courses': TrainingCourse.objects.all(),
    }


def home(request):
    ctx = _base_ctx()
    ctx.update({
        'featured_projects': Project.objects.filter(featured=True),
        'all_projects':      Project.objects.all(),
        'categories':        Project.CATEGORY_CHOICES,
    })
    return render(request, 'pages/home.html', ctx)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related = Project.objects.filter(category=project.category).exclude(pk=project.pk)[:3]
    return render(request, 'pages/project_detail.html', {
        'project': project, 'related': related,
    })


def cv_print(request):
    ctx = _base_ctx()
    ctx['all_projects'] = Project.objects.all()
    return render(request, 'pages/cv_print.html', ctx)
