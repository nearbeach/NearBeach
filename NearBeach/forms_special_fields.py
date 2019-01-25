from django import forms
from django.core.validators import ValidationError
from django.utils.encoding import smart_str
from django.forms.renderers import get_default_renderer

from NearBeach.models import product_and_service, list_of_country_region, list_of_country, customer
from django.utils.html import escape, mark_safe


import gettext


class ProductOrServiceSelect(forms.Select):
    def _render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''

        #Get SQL Objects
        row_results = product_and_service.objects\
            .filter(is_deleted='FALSE')\
            .order_by('product_or_service','product_name')

        #Start the rendering
        output = u'<select name="product_and_service" id="id_products_and_services" class="chosen-select form-control"><option value="------" selected disabled> Add Product or Service </option>'
        output = output + u'<optgroup label="Products">'


        #Render the PRODUCTS
        for option in row_results.filter(product_or_service='Product'):
            option_value = smart_str(option.product_id)
            option_label = smart_str(option.product_name)
            output = output + u'<option value="%s">%s' % (escape(option_value), escape(option_label))
            if ((not option.product_part_number == '') and (not option.product_part_number == None)):
                output = output + u' -- %s' % (escape(smart_str(option.product_part_number)))
            output = output + u'</option>'

        #Close off the optgroup PRODUCTS, start the optgroup SERVICES
        output = output + u'</optgroup><optgroup label="Services">'

        #Render the Services
        for option in row_results.filter(product_or_service='Service'):
            option_value = smart_str(option.product_id)
            option_label = smart_str(option.product_name)
            output = output + u'<option value="%s">%s' % (escape(option_value), escape(option_label))
            if ((not option.product_part_number == '') and (not option.product_part_number == None)):
                output = output + u' -- %s' % (escape(smart_str(option.product_part_number)))
            output = output + u'</option>'

        #Close everything off
        output = output + u'</optgroup></option></select>'
        #return mark_safe('\n'.join(output))
        return output

    def clean(self, value):

        value = super(forms.ChoiceField, self).clean(value)
        if value in (None, ''):
            value = u''
        value = forms.util.smart_str(value)
        if value == u'':
            return value
        valid_values = []
        for group_label, group in self.choices:
            valid_values += [str(k) for k, v in group]
        if value not in valid_values:
            raise ValidationError(gettext(u'Select a valid choice. That choice is not one of the available choices.'))
        return value


class RegionSelect(forms.Select):
    """
    Regional Select is a dropdown widget for selecting both
    - Region
    - Country
    """
    def _render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''

        #Get SQL Objects
        country_results = list_of_country.objects\
            .filter(is_deleted="FALSE")\
            .order_by('country_name')
        region_results = list_of_country_region.objects\
            .filter(is_deleted="FALSE")\
            .order_by('country_id','region_name')


        #Start the rendering
        output = u'<select name="country_and_regions" id="id_country_and_regions" class="chosen-select form-control"><option value="" selected> Select a Country/Region </option>'

        #Render for ALL Countries
        for country in country_results:
            #Country
            output = output + u'<optgroup label="' + country.country_name + '">'

            #Loop to place in the regions
            for region in region_results.filter(country_id=country.country_id):
                option_value = smart_str(region.region_id)
                option_label = smart_str(region.region_name)
                output = output + u'<option value="%s">%s' % (escape(option_value), escape(option_label))
                output = output + u'</option>'


        #Close everything off
        output = output + u'</optgroup></option></select>'
        return output

    def clean(self, value):

        value = super(forms.ChoiceField, self).clean(value)
        if value in (None, ''):
            value = u''
        value = forms.util.smart_str(value)
        if value == u'':
            return value
        valid_values = []
        for group_label, group in self.choices:
            valid_values += [str(k) for k, v in group]
        if value not in valid_values:
            raise ValidationError(gettext(u'Select a valid choice. That choice is not one of the available choices.'))
        return value


class ToEmailSelect(forms.SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''

        # Get SQL Objects
        customer_results = customer.objects.filter(
            is_deleted="FALSE"
        )

        # Start the rendering
        output = u'<select name="to_email" id="id_to_email" class="chosen-select form-control"><option value="------" selected disabled> Select an Email </option>'

        # Render the emails
        for option in customer_results:
            option_value = smart_str(option.customer_id)
            option_label = smart_str(option.customer_email)
            output = output + u'<option value="%s">%s' % (escape(option_value), escape(option_label))
            output = output + u'</option>'

        #Close off select
        output = output + u'</select>'

        return output
    def clean(self, value):

        value = super(forms.ChoiceField, self).clean(value)
        if value in (None, ''):
            value = u''
        value = forms.util.smart_str(value)
        if value == u'':
            return value
        valid_values = []
        for group_label, group in self.choices:
            valid_values += [str(k) for k, v in group]
        if value not in valid_values:
            raise ValidationError(gettext(u'Select a valid choice. That choice is not one of the available choices.'))
        return value
