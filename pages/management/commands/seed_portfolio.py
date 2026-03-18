from django.core.management.base import BaseCommand
from pages.models import (SiteProfile, ContactLink, Language, TrainingCourse,
                          Project, SkillCategory, Skill, Experience, Certification)


class Command(BaseCommand):
    help = 'Seed portfolio with Yahia Lakhfif CV data'

    def handle(self, *args, **kwargs):
        self._seed_profile()
        self._seed_contacts()
        self._seed_languages()
        self._seed_training()
        self._seed_skills()
        self._seed_experience()
        self._seed_certifications()
        self._seed_projects()
        self.stdout.write(self.style.SUCCESS('Portfolio seeded successfully!'))

    def _seed_profile(self):
        SiteProfile.objects.update_or_create(pk=1, defaults={
            'full_name': 'Lakhfif Yahia Abderraouf',
            'job_title': 'Full-Stack Developer · Data Engineer',
            'location':  'Sétif, Algeria',
            'summary': (
                'Full-Stack Developer and Data Engineer with a Master\'s in Big Data & '
                'Web Technologies (IDTW, Université Sétif 1, July 2024). Delivers production '
                'SaaS platforms across healthcare, automotive, tourism, and education. '
                'Startup Label acquired (Label Projet Innovant). University-level teacher '
                'and clinical IT infrastructure administrator.'
            ),
        })
        self.stdout.write('  ✓ Profile seeded')

    def _seed_contacts(self):
        items = [
            (0, 'email',    'yahiaabdraouflakhfif19alg@gmail.com', 'yahiaabdraouflakhfif19alg@gmail.com'),
            (1, 'phone',    '+213 776 22 64 97',                   '+213776226497'),
            (2, 'github',   'github.com/yahiaAlg',                 'https://github.com/yahiaAlg'),
            (3, 'linkedin', 'linkedin.com/in/abderraouf-lakhfif-1102523b8',
                            'https://www.linkedin.com/in/abderraouf-lakhfif-1102523b8'),
        ]
        for order, link_type, label, url in items:
            ContactLink.objects.update_or_create(
                link_type=link_type,
                defaults={'label': label, 'url': url, 'order': order, 'show_on_cv': True}
            )
        self.stdout.write('  ✓ Contacts seeded')

    def _seed_languages(self):
        langs = [
            (0, 'Arabic',  'Native'),
            (1, 'French',  'Professional Working Proficiency'),
            (2, 'English', 'B2 Upper-Intermediate'),
        ]
        for order, name, level in langs:
            Language.objects.get_or_create(name=name, defaults={'level': level, 'order': order})
        self.stdout.write('  ✓ Languages seeded')

    def _seed_training(self):
        courses = [
            dict(order=0, title='STAI Academy',
                 subtitle='Académie Ambassadeur Technologies & IA',
                 description='Python (Fundamentals → Advanced) · Django Backend Web Development · Bootstrap 5 Frontend',
                 period='2023–2024'),
            dict(order=1, title='UI/UX Design Coaching',
                 subtitle='University Business Incubator, Sétif 1',
                 description='',
                 period='May 2024'),
        ]
        for c in courses:
            TrainingCourse.objects.get_or_create(title=c['title'], defaults=c)
        self.stdout.write('  ✓ Training courses seeded')

    def _seed_skills(self):
        categories = [
            ('Backend',          'server',     ['Django','Flask','Laravel','Python','PHP','Java']),
            ('Frontend',         'monitor',    ['Bootstrap 5','Material CSS','React','PWA','HTML5','CSS3','JavaScript']),
            ('Desktop & Mobile', 'smartphone', ['C++ Qt','JavaFX','WinDev','Android','Flutter']),
            ('Embedded',         'cpu',        ['C for STM32 (ARM Cortex-M)']),
            ('AI / ML',          'brain',      ['Machine Learning','Deep Learning','Data Mining','Business Intelligence']),
            ('LLM & Agents',     'bot',        ['LangChain','LlamaIndex','Pinecone','OpenAI Agents API']),
            ('Databases',        'database',   ['MySQL','PostgreSQL','Oracle DBMS']),
            ('Networking',       'network',    ['Windows Server','Active Directory','pfSense','VMware ESXi','LAN']),
            ('DevOps',           'git-branch', ['Git','REST APIs','Docker','Linux']),
            ('Design',           'pen-tool',   ['Adobe XD','Adobe Illustrator','Figma','Photoshop','Blender','SolidWorks']),
        ]
        for i, (name, icon, skills) in enumerate(categories):
            cat, _ = SkillCategory.objects.get_or_create(name=name, defaults={'icon': icon, 'order': i})
            for j, skill in enumerate(skills):
                Skill.objects.get_or_create(category=cat, name=skill, defaults={'order': j})
        self.stdout.write('  ✓ Skills seeded')

    def _seed_experience(self):
        items = [
            dict(title='IT Specialist & Software Developer', organization='Clinique Les Babors',
                 location='Sétif', start_date='Jun 2025', end_date='Dec 2025',
                 description='Server & DB admin · WinDev clinic software development · LAN config · hardware maintenance & technical support',
                 exp_type='work', order=0),
            dict(title='Honorary Teacher (Vacataire)', organization='Université Ferhat Abbas',
                 location='Sétif 1', start_date='2025', end_date='Present',
                 description='S2 2025: Computer Engineering & Science et Matière (1st yr LMD)\nS2 2026: Science et Matière (Tronc Commun)',
                 exp_type='teach', order=1),
            dict(title="Master's — IDTW (Big Data & Web Technologies)", organization='Université Ferhat Abbas',
                 location='Sétif 1', start_date='2022', end_date='Jul 2024',
                 description='ML I&II · Advanced Databases · Data Warehousing · Cloud · Distributed Systems · Web Security · Web Mining · Advanced AI',
                 exp_type='edu', order=0),
        ]
        for item in items:
            Experience.objects.get_or_create(title=item['title'], organization=item['organization'], defaults=item)
        self.stdout.write('  ✓ Experience seeded')

    def _seed_certifications(self):
        certs = [
            (0, 'Label Projet Innovant',  'National Startup Committee, Algeria', 'Feb 2025',   'award'),
            (1, 'Master Diploma',         'Ferhat Abbas University',             '03/07/2024', 'graduation-cap'),
            (2, 'Work Certificate',       'Clinique Les Babors',                 '18/12/2025', 'briefcase'),
            (3, 'UI/UX Design Coaching',  'University Business Incubator, Sétif 1', 'May 2024','pen-tool'),
            (4, 'Adobe XD UI/UX Design',  'Adobe',                               '2024',       'layers'),
        ]
        for order, title, issuer, date, icon in certs:
            Certification.objects.get_or_create(title=title, defaults={'issuer':issuer,'date':date,'icon':icon,'order':order})
        self.stdout.write('  ✓ Certifications seeded')

    def _seed_projects(self):
        projects = [
            dict(title='ISI Management System', slug='isi-management-system', category='saas',
                 client='EEMS — Excellence Management Solutions',
                 description='Dual-business-line platform (training + consulting) covering client management, invoicing, equipment tracking, attestation generation, and financial reporting.',
                 tech_stack='Django, Bootstrap 5, PostgreSQL, JavaScript',
                 live_url='https://excellance-ms.dz/', featured=True, order=0),
            dict(title='Lab Waste & Invoice System', slug='lab-waste-invoice', category='saas',
                 client='Madre Tierra Clinical Lab',
                 description='Invoicing and hazardous waste tracking with Algerian tax compliance (TVA, timbre) and client/supplier management.',
                 tech_stack='Django, Bootstrap 5, SQLite, JavaScript',
                 live_url='https://madre-tierra-dz.com', featured=True, order=1),
            dict(title='HB China Cars SaaS', slug='hb-china-cars', category='saas',
                 client='HB China Cars, Sétif',
                 description='Vehicle inventory, sales workflow, CRM, commission tracking, and analytics dashboard.',
                 tech_stack='Django, Bootstrap 5, Chart.js, SQLite',
                 live_url='https://hb-china-car-webapp.onrender.com/', featured=True, order=2),
            dict(title='Glass Workshop SaaS', slug='glass-workshop-saas', category='saas',
                 client='Local Glass Workshop, Sétif',
                 description='SaaS invoicing, expense tracking, equipment management, inventory control, and reporting.',
                 tech_stack='Django, Bootstrap 5, SQLite, Chart.js',
                 live_url='https://glass-workshop-management.onrender.com', featured=False, order=3),
            dict(title='Reservili', slug='reservili', category='saas',
                 client='Tourism Platform (client awarded Startup Label)',
                 description='All-in-one Algerian tourism reservation platform for hotels, cars, and restaurants.',
                 tech_stack='Django, Bootstrap 5, PostgreSQL, JavaScript',
                 live_url='https://reservili-startup-project.onrender.com/', featured=True, order=4),
            dict(title='HassoubDZ', slug='hassoubdz', category='elearning',
                 client='EdTech Startup',
                 description='Game-based financial literacy e-learning for children aged 5–13 with rewards and progress tracking.',
                 tech_stack='Django, Bootstrap 5, JavaScript, SQLite',
                 live_url='https://www.hassoubdz.com/', featured=True, order=5),
            dict(title='Rafadz', slug='rafadz', category='elearning',
                 client='Audiovisual Vocational Training',
                 description='Audiovisual vocational training platform with multimedia courses and certification.',
                 tech_stack='Django, Bootstrap 5, JavaScript, SQLite',
                 live_url='https://rafadz.com/', featured=False, order=6),
            dict(title='Mobtakir', slug='mobtakir', category='ai',
                 client='Startup — Label Projet Innovant, Feb 2025',
                 description='AI project recognized with the national Label Projet Innovant by Algeria\'s National Startup Committee.',
                 tech_stack='Python, LangChain, Machine Learning, OpenAI API',
                 live_url='', featured=True, order=7),
            dict(title='Desktop Inventory Apps', slug='desktop-inventory-apps', category='desktop',
                 client='Multiple Local Businesses',
                 description='Standalone inventory management applications with CRUD, reporting, and print functionality.',
                 tech_stack='Java, JavaFX, C++ Qt, SQLite',
                 live_url='', featured=False, order=8),
        ]
        for p in projects:
            Project.objects.get_or_create(slug=p['slug'], defaults=p)
        self.stdout.write('  ✓ Projects seeded')
