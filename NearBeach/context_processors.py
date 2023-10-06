import django
import NearBeach


def django_version(request):
    """Get's the django verion and returns it - used in template rendering."""
    return {
        "django_version": django.get_version(),
    }


def nearbeach_version(request):
    """Get's the NearBeach version and returns it - used in template rendering."""
    return {"nearbeach_version": NearBeach.__version__}
