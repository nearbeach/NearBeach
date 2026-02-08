from rest_framework.throttling import AnonRateThrottle


class AuthMinuteThrottle(AnonRateThrottle):
    scope = 'auth_minute'
