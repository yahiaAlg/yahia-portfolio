from .models import SiteProfile, ContactLink


def portfolio_info(request):
    profile  = SiteProfile.load()
    contacts = ContactLink.objects.all()
    # build a quick-access dict keyed by link_type for templates
    contact_map = {c.link_type: c for c in contacts}
    return {
        'profile':     profile,
        'contacts':    contacts,
        'contact_map': contact_map,
        # backward-compat 'owner' dict so existing templates keep working
        'owner': {
            'name':     profile.full_name,
            'title':    profile.job_title,
            'location': profile.location,
            'email':    contact_map.get('email', None) and contact_map['email'].label or '',
            'phone':    contact_map.get('phone',  None) and contact_map['phone'].label  or '',
            'github':   contact_map.get('github', None) and contact_map['github'].url   or '',
            'linkedin': contact_map.get('linkedin', None) and contact_map['linkedin'].url or '',
        }
    }
