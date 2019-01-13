"""
The following code has been sourced from DJANGO-PRIVATE-MEDIA - https://github.com/RacingTadpole/django-private-media
which has been sourced from django-filer.

I have modified some of the code, however most of the recognition should be for both;
-- django-filer
-- django-private-media

I have placed this code into one file for convenience.
"""

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import Http404, HttpResponseNotModified, HttpResponse
from django.utils.http import http_date
from django.views.static import was_modified_since

import mimetypes, os, stat

"""
FUNCTION DESCRIPTION
~~~~~~~~~~~~~~~~~~~~
To return the location of where we are going to store the file. It will
look through the SETTINGS.PY file for the Django project and extract the
variables;
-- PRIVATE_MEDIA_ROOT
-- PRIVATE_MEDIA_URL

These will need to be set in the SETTINGS.PY
"""
class File_Storage(FileSystemStorage):
    def __init__(self, location=None, base_url=None):
        if location is None:
            location = settings.PRIVATE_MEDIA_ROOT
        if base_url is None:
            base_url = settings.PRIVATE_MEDIA_URL
        return super(File_Storage, self).__init__(location, base_url)


"""
FUNCTION DESCRIPTION
~~~~~~~~~~~~~~~~~~~~
To return a TRUE or FALSE result depending if the user has permission
to access the file.

METHOD
~~~~~~
1.) Check to make sure a user is logged in
2.) Download the permission rows for the file
3.) Determine if the user meets either 1 of the 
    following permissions;@login_required(login_url='login')
    -- No restrictions on file
    -- User is in group allocated permission to file
    -- User has been allocated permission
    If user meets at least one condition, then the value
    TRUE is returned, else FALSE
"""
class Check_Permissions(object):
    def has_read_permission(self, request, path):
        #Is user logged in
        user = request.user
        if not user.is_authenticated():
            return False

        #TEMP RETURN LINE
        return True

        """
        The following code can expandable for all different modules that require document
        uploads. It will need to be tested with a very large dataset.
        """
        current_user = request.user

        # Setup connection to the database and query it
        cursor = connection.cursor()

        cursor.execute("""
        SELECT 
        count(project_group.groups_id_id)
        + CASE WHEN document_permission.organisations_id_id IS NULL THEN 0 ELSE 1 END
        + CASE WHEN document_permission.customer_id_id IS NULL THEN 0 ELSE 1 END
        AS PERMISSION
        
        FROM
        user_group
        , document_permission
            left join project_group
              on document_permission.project_id_id = project_group.project_id_id
              AND project_group.groups_id_id = user_group.group_id_id
            left join tasks_group
              on document_permission.task_id_id = tasks_group.tasks_id_id
              AND tasks_group.groups_id_id = user_group.group_id_id
        /*
        MISSING
        ~~~~~~~
        Currently opportunities do not have a limit to. I will need to
        apply this.
        */
        
        
        WHERE 1=1
        -- THE USER INPUT
        AND user_group.username_id = %s
        
        --THE DOCUMENT INPUT
        AND document_permission.document_key_id = %s
        
        -- Make sure the doc is not deleted
        AND document_permission.is_deleted = 'FALSE'
       	""", [current_user.id, object])
        has_permission = cursor.fetchall()

        if not has_permission[0][0] >= 1:
            #User have permission to view the file
            return True
        else:
            return False






"""
Left unchanged
"""
class NginxXAccelRedirectServer(object):
    def serve(self, request, path):
        response = HttpResponse()
        fullpath = os.path.join(settings.PRIVATE_MEDIA_ROOT, path)
        response['X-Accel-Redirect'] = fullpath
        response['Content-Type'] = mimetypes.guess_type(path)[0] or 'application/octet-stream'
        return response

"""
Left unchanged
"""
class ApacheXSendfileServer(object):
    def serve(self, request, path):
        fullpath = os.path.join(settings.PRIVATE_MEDIA_ROOT, path)
        response = HttpResponse()
        response['X-Sendfile'] = fullpath

        # From django-filer (https://github.com/stefanfoulis/django-filer/):
        # This is needed for lighttpd, hopefully this will
        # not be needed after this is fixed:
        # http://redmine.lighttpd.net/issues/2076
        response['Content-Type'] = mimetypes.guess_type(path)[0] or 'application/octet-stream'

        # filename = os.path.basename(path)
        # response['Content-Disposition'] = smart_str(u'attachment; filename={0}'.format(filename))

        return response


"""
Left unchanged
"""
class DefaultServer(object):
    """
    Serve static files from the local filesystem through django.
    This is a bad idea for most situations other than testing.

    This will only work for files that can be accessed in the local filesystem.
    """
    def serve(self, request, path):
        # the following code is largely borrowed from `django.views.static.serve`
        # and django-filetransfers: filetransfers.backends.default
        fullpath = os.path.join(settings.PRIVATE_MEDIA_ROOT, path)
        if not os.path.exists(fullpath):
            raise Http404('"{0}" does not exist'.format(fullpath))
        # Respect the If-Modified-Since header.
        statobj = os.stat(fullpath)
        content_type = mimetypes.guess_type(fullpath)[0] or 'application/octet-stream'
        if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                                  statobj[stat.ST_MTIME], statobj[stat.ST_SIZE]):
            return HttpResponseNotModified(content_type=content_type)
        response = HttpResponse(open(fullpath, 'rb').read(), content_type=content_type)
        response["Last-Modified"] = http_date(statobj[stat.ST_MTIME])
        # filename = os.path.basename(path)
        # response['Content-Disposition'] = smart_str(u'attachment; filename={0}'.format(filename))
        return response

"""
Left unchanged
"""
from importlib import import_module
def get_class(import_path=None):
    """
    Largely based on django.core.files.storage's get_storage_class
    """
    from django.core.exceptions import ImproperlyConfigured
    if import_path is None:
        raise ImproperlyConfigured('No class path specified.')
    try:
        dot = import_path.rindex('.')
    except ValueError:
        raise ImproperlyConfigured("%s isn't a module." % import_path)
    module, classname = import_path[:dot], import_path[dot+1:]
    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' % (module, e))
    try:
        return getattr(mod, classname)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" class.' % (module, classname))


"""
Mostly left unchanged
"""
if settings.DEBUG == True:
    server = DefaultServer(**getattr(settings, 'PRIVATE_MEDIA_SERVER_OPTIONS', {}))
else:
    server = ApacheXSendfileServer(**getattr(settings, 'PRIVATE_MEDIA_SERVER_OPTIONS', {}))
if hasattr(settings,'PRIVATE_MEDIA_PERMISSIONS'):
    permissions = get_class(settings.PRIVATE_MEDIA_PERMISSIONS)(**getattr(settings, 'PRIVATE_MEDIA_PERMISSIONS_OPTIONS', {}))
else:
    permissions = Check_Permissions()

