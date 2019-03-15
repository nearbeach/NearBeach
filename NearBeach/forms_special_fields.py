from django import forms
from django.core.validators import ValidationError
from django.utils.encoding import smart_str
from django.forms.renderers import get_default_renderer

from NearBeach.models import \
    product_and_service, \
    list_of_country_region, \
    list_of_country, \
    customer, \
    organisation
from django.utils.html import escape, mark_safe


import gettext


class ConnectCustomerSelect(forms.SelectMultiple):
    """
    We want the ability to render a multiple select in a table format. This will give the use a friendly layout.
    The fields we want are;
    -- Tickbox
    -- Customer First Name
    -- Customer Last Name
    -- Customer organisation (if any)
    """
    def _render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''

        #Get SQL Objects
        customer_results = customer.objects.filter(
            is_deleted="FALSE",
        ).order_by('customer_first_name','customer_last_name')

        #Start the rendering
        output = u'<table class="table table-hover table-striped mt-4">' \
                '<thead><tr>' \
                    '<td> - </td>' \
                    '<td>Customer First Name</td>' \
                    '<td>Customer Last Name</td>' \
                    '<td>Customer Organisation</td>'\
                '<tr></thead>'

        #Render a new row for each customer
        #for idx,item in enumerate(list):
        for idx, row in enumerate(customer_results):
            if row.organisation_id:
                output = output + \
                    u'<tr>'\
                        '<td><input type="checkbox" id="id_customers_%s" name="customers" value="%s"></td>'  % (str(idx),str(row.customer_id)) + \
                        '<td>%s</td>' % (row.customer_first_name) +\
                        '<td>%s</td>' % (row.customer_last_name) + \
                        '<td>%s</td>' % (str(row.organisation_id)) + \
                    '</tr>'
            else:
                output = output + \
                    u'<tr>'\
                        '<td><input type="checkbox" id="id_customers_%s" name="customers" value="%s"></td>' % (str(row.customer_id),str(row.customer_id)) +\
                        '<td>%s</td>' % (row.customer_first_name) + \
                        '<td>%s</td>' % (row.customer_last_name) + \
                        '<td>%s</td>' % (str(row.organisation_id)) + \
                    '</tr>'

        #Finish the rendering
        output = output + \
            u'</table>'

        return output
        # return mark_safe('\n'.join(output))

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


class ConnectOrganisationSelect(forms.SelectMultiple):
    """
    We want the ability to render a multiple select in a table format. This will give the use a friendly layout.
    The fields we want are;
    -- Tickbox
    -- Organisation Name
    -- Organisation Website
    -- Organisation Email
    """
    def _render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''

        #Get SQL Objects
        organisation_results = organisation.objects.filter(
            is_deleted="FALSE",
        ).order_by('organisation_name')

        #Start the rendering
        output = u'<table class="table table-hover table-striped mt-4">' \
                '<thead><tr>' \
                    '<td> - </td>' \
                    '<td>Organisation Name</td>' \
                    '<td>Organisation Website</td>' \
                    '<td>Organisation Email</td>'\
                '<tr></thead>'

        #Render a new row for each customer
        #for idx,item in enumerate(list):
        for idx, row in enumerate(organisation_results):
            output = output + \
                u'<tr>'\
                    '<td><input type="checkbox" id="id_organisations_%s" name="organisations" value="%s"></td>' %(str(row.organisation_id),str(row.organisation_id)) +\
                    '<td>%s</td>' % (row.organisation_name) + \
                    '<td>%s</td>' % (row.organisation_website) + \
                    '<td>%s</td>' % (str(row.organisation_email)) + \
                '</tr>'

        #Finish the rendering
        output = output + \
            u'</table>'

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
