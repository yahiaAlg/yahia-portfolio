from django.core.management.base import BaseCommand
from pages.models import Project, SkillCategory, Skill, Experience, Certification


class Command(BaseCommand):
    help = 'Seed portfolio with Yahia Lakhfif CV data'

    def handle(self, *args, **kwargs):
        self._seed_skills()
        self._seed_experience()
        self._seed_certifications()
        self._seed_projects()
        self.stdout.write(self.style.SUCCESS('Portfolio seeded successfully!'))

    def _seed_skills(self):
        categories = [
            ('Backend',          'server',        ['Django','Flask','Laravel','Python','PHP','Java']),
            ('Frontend',         'monitor',        ['Bootstrap 5','Material CSS','React','PWA','HTML5','CSS3','JavaScript']),
            ('Desktop & Mobile', 'smartphone',     ['C++ Qt','JavaFX','WinDev','Android','Flutter']),
            ('Embedded',         'cpu',            ['C for STM32 (ARM Cortex-M)']),
            ('AI / ML',          'brain',          ['Machine Learning','Deep Learning','Data Mining','Business Intelligence']),
            ('LLM & Agents',     'bot',            ['LangChain','LlamaIndex','Pinecone','OpenAI Agents API']),
            ('Databases',        'database',       ['MySQL','PostgreSQL','Oracle DBMS']),
            ('Networking',       'network',        ['Windows Server','Active Directory','pfSense','VMware ESXi','LAN']),
            ('DevOps',           'git-branch',     ['Git','REST APIs','Docker','Linux']),
            ('Design',           'pen-tool',       ['Adobe XD','Adobe Illustrator','Figma','Photoshop','Blender','SolidWorks']),
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
                 description='Server & DB admin · WinDev clinic software development · LAN config · hardware maintenance',
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
            ('Label Projet Innovant', 'National Startup Committee, Algeria', 'Feb 2025', 'award'),
            ('Adobe XD UI/UX Design', 'Adobe', '2024', 'pen-tool'),
            ('UI/UX Design Coaching', 'University Business Incubator, Sétif 1', 'May 2024', 'graduation-cap'),
        ]
        for i, (title, issuer, date, icon) in enumerate(certs):
            Certification.objects.get_or_create(title=title, defaults={
                'issuer': issuer, 'date': date, 'icon': icon, 'order': i
            })
        self.stdout.write('  ✓ Certifications seeded')

    def _seed_projects(self):
        projects = [
            dict(title='ISI Management System', slug='isi-management-system',
                 category='saas', client='EEMS — Excellence Management Solutions',
                 description='Dual-business-line platform (training + consulting) covering client management, invoicing, equipment tracking, attestation generation, and financial reporting.',
                 tech_stack='Django, Bootstrap 5, PostgreSQL, JavaScript',
                 live_url='https://excellance-ms.dz/', featured=True, order=0),
            dict(title='Lab Waste & Invoice System', slug='lab-waste-invoice',
                 category='saas', client='Madre Tierra Clinical Lab',
                 description='Invoicing and hazardous waste tracking system with Algerian tax compliance (TVA, timbre) and client/supplier management.',
                 tech_stack='Django, Bootstrap 5, SQLite, JavaScript',
                 live_url='https://madre-tierra-dz.com', featured=True, order=1),
            dict(title='HB China Cars SaaS', slug='hb-china-cars',
                 category='saas', client='HB China Cars, Sétif',
                 description='Vehicle inventory, sales transaction workflow, CRM, commission tracking, and analytics dashboard for a car reselling bureau.',
                 tech_stack='Django, Bootstrap 5, Chart.js, SQLite',
                 live_url='https://hb-china-car-webapp.onrender.com/', featured=True, order=2),
            dict(title='Glass Workshop SaaS', slug='glass-workshop-saas',
                 category='saas', client='Local Glass Workshop, Sétif',
                 description='Full SaaS invoicing, expense tracking, equipment management, inventory control, and reporting for a glass retail business.',
                 tech_stack='Django, Bootstrap 5, SQLite, Chart.js',
                 live_url='https://glass-workshop-management.onrender.com', featured=False, order=3),
            dict(title='Reservili', slug='reservili',
                 category='saas', client='Tourism Platform (client awarded Startup Label)',
                 description='All-in-one Algerian tourism reservation platform for hotels, cars, and restaurants with real-time booking and user dashboards.',
                 tech_stack='Django, Bootstrap 5, PostgreSQL, JavaScript',
                 live_url='https://reservili-startup-project.onrender.com/', featured=True, order=4),
            dict(title='HassoubDZ', slug='hassoubdz',
                 category='elearning', client='EdTech Startup',
                 description='Game-based financial literacy e-learning platform for children aged 5–13 with reward systems, progress tracking, and parental supervision.',
                 tech_stack='Django, Bootstrap 5, JavaScript, SQLite',
                 live_url='https://www.hassoubdz.com/', featured=True, order=5),
            dict(title='Rafadz', slug='rafadz',
                 category='elearning', client='Audiovisual Vocational Training',
                 description='Audiovisual vocational training platform with structured multimedia courses, progress tracking, and certification for film, audio, and media production.',
                 tech_stack='Django, Bootstrap 5, JavaScript, SQLite',
                 live_url='https://rafadz.com/', featured=False, order=6),
            dict(title='Mobtakir', slug='mobtakir',
                 category='ai', client='Startup — Label Projet Innovant, Feb 2025',
                 description='AI project recognized with the national Label Projet Innovant by Algeria\'s National Startup Committee. AI-powered system built with Python and LangChain.',
                 tech_stack='Python, LangChain, Machine Learning, OpenAI API',
                 live_url='', featured=True, order=7),
            dict(title='Desktop Inventory Apps', slug='desktop-inventory-apps',
                 category='desktop', client='Multiple Local Businesses',
                 description='Multiple standalone inventory management applications built for local businesses with full CRUD, reporting, and print functionality.',
                 tech_stack='Java, JavaFX, C++ Qt, SQLite',
                 live_url='', featured=False, order=8),
        ]
        for p in projects:
            Project.objects.get_or_create(slug=p['slug'], defaults=p)
        self.stdout.write('  ✓ Projects seeded')
