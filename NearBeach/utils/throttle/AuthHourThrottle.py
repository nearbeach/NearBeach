from rest_framework.throttling import AnonRateThrottle


class AuthHourThrottle(AnonRateThrottle):
    scope = 'auth_minute'
