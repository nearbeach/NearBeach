from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from two_factor.views import LoginView
from .authentication_views import check_first_time_login, check_recaptcha
from django.contrib import auth
from NearBeach.models import UserGroup

# TODO: Add in the recaptcha - investigate costs first


class TwoFactorLoginView(LoginView):
    def __init__(self, **kwargs):
        self.show_no_group_errors = False
        self.show_recaptcha_errors = False
        super().__init__(**kwargs)

    def done(self, form_list, *args, **kwargs):
        # Check recaptcha
        # TODO - Re-implement the recaptcha
        # if not check_recaptcha(self.request.POST):
        #     # User has failed the recaptcha
        #     self.storage.reset()
        #     self.show_recaptcha_errors = True
        #     return self.render_goto_step(self.FIRST_STEP)

        # Always apply the first time loging check
        check_first_time_login(self.request)

        # Check the user has groups
        user_group_count = len(
            UserGroup.objects.filter(
                is_deleted=False,
                username=self.get_user(),
            )
        )
        if user_group_count == 0:
            # User has no groups
            self.storage.reset()
            self.show_no_group_errors = True
            return self.render_goto_step(self.FIRST_STEP)

        # Authenticate user
        auth.login(request=self.request, user=self.get_user())

        return HttpResponseRedirect(reverse("dashboard"))

    def get_form(self, step=None, **kwargs):
        form = super().get_form(step=step, **kwargs)
        if self.show_no_group_errors:
            form.cleaned_data = getattr(form, "cleaned_data", {})
            form.add_error(
                None,
                ValidationError("User currently not setup with any groups. Please contact system admin")
            )
        if self.show_recaptcha_errors:
            form.cleaned_data = getattr(form, "cleaned_data", {})
            form.add_error(
                None,
                ValidationError("Recaptcha Failed")
            )
        return form
