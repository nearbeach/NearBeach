from silk.profiling.profiler import silk_profile


class SilkProfileAllRequestsMiddleware:
    """
    Dev only. Wraps every request in a silk_profile block so that the Silk
    "Profiling" tab is populated without decorating each view.
    Must sit directly after silk.middleware.SilkyMiddleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/silk/'):
            return self.get_response(request)

        with silk_profile(name=f'{request.method} {request.path}'):
            return self.get_response(request)
