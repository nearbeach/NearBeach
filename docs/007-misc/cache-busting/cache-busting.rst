.. cache-busting:

=============
Cache Busting
=============

.. note::

    If you have NearBeach installed through Docker, you will not need to do these steps. This is design for those who have manually installed NearBeach.


If you are hosting your own static files, you'll notice that the old static files will not update after an upgrade due to cache. A hard reset will work, however not ideal. The best solution to fix this would be to `Implement ManifestStaticFilesStorage in the Settings file <https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#django.contrib.staticfiles.storage.ManifestStaticFilesStorage>`_.
Please follow the instructions on the Django Documentation linked.
