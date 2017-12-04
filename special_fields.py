from django import forms
from django.core.validators import ValidationError
from django.utils.encoding import smart_unicode
from NearBeach.models import products_and_services
from django.utils.html import escape, mark_safe

import gettext


"""
			'placeholder': "Choose the users(s)",
			'class': 'chosen-select',
			'multiple tabindex': '4',
			'width': '500px',
"""

class ProductOrServiceSelect(forms.Select):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''

        #Get SQL Objects
        row_results = products_and_services.objects\
            .filter(is_deleted='FALSE')\
            .order_by('product_or_service','product_name')

        #Start the rendering
        output = u'<select name="product_or_service" id="id_product_or_service" class="chosen-select"><option value="------">------</option>'
        output = output + u'<optgroup label="Products">'


        #Render the PRODUCTS
        for option in row_results.filter(product_or_service='Product'):
            option_value = smart_unicode(option.product_id)
            option_label = smart_unicode(option.product_name)
            output = output + u'<option value="%s">%s</option>' % (escape(option_value), escape(option_label))

        #Close off the optgroup PRODUCTS, start the optgroup SERVICES
        output = output + u'</optgroup><optgroup label="Services">'

        #Render the Services
        for option in row_results.filter(product_or_service='Service'):
            option_value = smart_unicode(option.product_id)
            option_label = smart_unicode(option.product_name)
            output = output + u'<option value="%s">%s</option>' % (escape(option_value), escape(option_label))

        #Close everything off
        output = output + u'</optgroup></option>'
        #return mark_safe('\n'.join(output))
        return output

    def clean(self, value):

        value = super(forms.ChoiceField, self).clean(value)
        if value in (None, ''):
            value = u''
        value = forms.util.smart_unicode(value)
        if value == u'':
            return value
        valid_values = []
        for group_label, group in self.choices:
            valid_values += [str(k) for k, v in group]
        if value not in valid_values:
            raise ValidationError(gettext(u'Select a valid choice. That choice is not one of the available choices.'))
        return value
