import django
import NearBeach


def django_version(request):
    return {
        'django_version': django.get_version(),
    }


def nearbeach_version(request):
    return {
        'nearbeach_version': NearBeach.__version__
    }
