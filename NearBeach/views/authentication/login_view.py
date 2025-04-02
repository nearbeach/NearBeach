from two_factor.views import LoginView
from django.contrib import auth

# TODO: Add in the done section
# TODO: Add in the errors
# TODO: Add in the profile information two factor urls
# TODO: Fix the templates for the profile information two factor

class TwoFactorLoginView(LoginView):
    def __init__(self, **kwargs):
        self.show_no_group_errors = False
        self.show_recaptcha_errors = False
        super().__init__(**kwargs)

    """
    def done(self, form_list, *args, **kwargs):
        user = self.get_user()
        all_cleaned_data = self.get_all_cleaned_data()
        # self.get_form(self, step="All", **kwargs)

        auth.login(request=self.request, user=self.get_user())

        # if True:
        #     # User has failed either the group stuff or recaptcha
        #     self.storage.reset()
        #     self.show_the_pain = True
        #     return self.render_goto_step(self.FIRST_STEP)

        return HttpResponseRedirect(reverse("homeview"))

        # auth.logout(self.request)

    def get_form(self, step=None, **kwargs):
        form = super().get_form(step=step, **kwargs)
        if self.show_the_pain:
            form.cleaned_data = getattr(form, "cleaned_data", {})
            form.add_error(None, ValidationError("I can feel your pain :'("))
        return form
    """
