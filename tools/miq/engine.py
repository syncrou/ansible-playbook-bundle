import os
import pdb
import json
import re
import requests
import yaml

class MiqConnect(object):
    """
        MIQ REST API operations
    """

    def __init__(self, opts):
        self._opts = opts
        self._server = opts['server']
        self._service = opts['service']
        self._username = opts['username']
        self._password = opts['password']
        self._validate_certs = opts['validate-certs']
        self._debug = opts['debug'] or None
        self._params = dict()
        self._credentials = (self._username, self._password)
        self._auth = self._build_auth()

    @property
    def url(self):
        """ The URL used to access the REST API """
        return self._build_url()


    def _build_url(self):
        """
            Using any type of href input, build out the correct url
        """

        return "http://" + self._server + '/api/' + self._parse_slug()


    def _parse_slug(self):
        """
            Decode the href_slug
        """
        self._dict = self._service
        if isinstance(self._dict, str):
            slug = self._dict.split("::")
            if len(slug) == 2:
                return slug[1]
            return self._dict


    def _build_auth(self):
        self._headers = {'Content-Type': 'application/json; charset=utf-8'}
        self._params['validate_certs'] = self._validate_certs
        self._params['force_basic_auth'] = True


    def get(self):
        """
            Get any attribute, object from the REST API
        """
        result = requests.get(self.url, auth=self._credentials)
        if result.status_code == 200:
            return result.json()
        else:
            return result.status_code


class ServiceDialog(MiqConnect):
    """
        Service Dialog
    """

    def __init__(self, opts):
        super(ServiceDialog, self).__init__(opts)
        self._dialog_id = opts['dialog_id']


    def _build_url(self):
        """
            Using any type of href input, build out the correct url
        """

        return "http://" + self._server + '/api/service_dialogs/' + self._dialog_id

    def tabs(self):
        """
            Return the Dialog Tabs
        """
        tabs = self.get()
        return tabs


class ReduceToYaml(object):
    """
        Apply the processing to build an apb.yml file
    """
    DIALOG_TYPE = dict(DialogFieldTextBox='dialog_field_text_box',
                       DialogFieldTextAreaBox='dialog_field_text_area_box',
                       DialogFieldCheckBox='dialog_field_check_box',
                       DialogFieldRadioButton='dialog_field_radio_button',
                       DialogFieldDateControl='dialog_field_date_control',
                       DialogFieldDateTimeControl='dialog_field_date_time_control',
                       DialogFieldDropDownList='dialog_field_drop_down_list',
                       DialogFieldTagControl='dialog_field_tag_control')


    CFME_REQUESTER = dict(title='CFME Requester', name='cfme_user',
                          type='string',
                          display_group='CloudForms Credentials')
    CFME_PASSWORD = dict(title='CFME Password', name='cfme_password',
                         type='string', display_type='password',
                         display_group='CloudForms Credentials')

    def __init__(self, service_dialog, service_template):
        self._dialog = service_dialog
        self._template = service_template
        self._svc_dialog_params = list()
        self.initialize_params()


    def initialize_params(self):
        self._svc_dialog_params.append(self.CFME_REQUESTER)
        self._svc_dialog_params.append(self.CFME_PASSWORD)


    def process_tabs(self):
        """ Process all Dialog Tabs """
        tabs = self._dialog.tabs()['content'][0]['dialog_tabs']
        for tab in tabs:
            for section in tab['dialog_groups']:
                self.process_section(tab['label'], section)


    def process_section(self, tab_label, section):
        """ Process each Dialog tab section """
        display_group = "{tab_label}/{section}".format(tab_label=tab_label, section=section['label'])

        for dialog_field in section['dialog_fields']:
            if dialog_field['dynamic']:
                raise "Dynamic fields are not currently supported"
            item = self.initialize_apb_parameter(dialog_field, display_group)
            item = getattr(self, self.DIALOG_TYPE[dialog_field['type']])(dialog_field, item)
            self._svc_dialog_params.append(item)


    def initialize_apb_parameter(self, dialog_field, display_group):
        """
            Build up the base apb paramater list
        """
        item = {}
        item['name'] = dialog_field['name']
        item['title'] = dialog_field['label']
        if not dialog_field['default_value']:
            item['default'] = dialog_field['default_value']

        item['display_group'] = display_group

        if dialog_field['validator_rule']:
            item['pattern'] = dialog_field['validator_rule']

        # type: enum|string|boolean|int|number|bool
        item['type'] = self.set_datatype(dialog_field['data_type'])
        item['required'] = dialog_field['required']
        return item

    def dialog_field_text_box(self, dialog_field, item):
        """
            display_type: password|textarea|text
        """
        if dialog_field['options']['protected']:
            item['display_type'] = 'password'

        # max_length
        # updatable : True/False for enum's where a user can enter a value
        return item

    def dialog_field_text_area_box(self, dialog_field, item):
        item = self.dialog_field_text_box(dialog_field, item)
        item['display_type'] = 'textarea'
        return item


    def dialog_field_check_box(self, dialog_field, item):
        item['type'] = 'boolean'
        if dialog_field['default_value'] == 't':
            item['default'] = 'true'
        else:
            item['default'] = 'false'
        return item

    def dialog_field_radio_button(self, dialog_field, item):
        item['type'] = 'enum'
        item['enum'] = ['this', 'needs', 'to', 'be', 'fixed']
    #  self._dict['enum'] = dialog_field['values'].flat_map { |x| x[1] }
        return item

    def dialog_field_date_control(self, dialog_field, item):
        pass


    def dialog_field_date_time_control(self, dialog_field, item):
        pass

    def dialog_field_drop_down_list(self, dialog_field, item):
        item['type'] = 'enum'
        item['enum'] = ['this', 'needs', 'to', 'be', 'fixed']
    #  self._dict['enum'] = dialog_field['values'].flat_map { |x| x[1] }
        return item

    def dialog_field_tag_control(self, dialog_field, item):
        item['type'] = 'enum'
        item['enum'] = ['this', 'needs', 'to', 'be', 'fixed']
    #  self._dict['enum'] = dialog_field['values'].flat_map { |x| x['name'] }
        return item

    def set_datatype(self, miq_type):
        """ set the datatype """
        if miq_type == "string":
            return "string"
        elif miq_type == "integer":
            return "int"
        return "string"

    def apb_normalized_name(self, name):
    #  "#{name.downcase.gsub(/[()_,. ]/, '-')}-apb"
        return "manageiq-please-fix-me-abp"


    def create_apb_yml(self):
        parameters = self._svc_dialog_params
        svc_template = self._template
        print "Creating apb yaml file apb.yml for service template {name}".format(name=svc_template['name'])
        metadata = dict(displayName="{name} (APB)".format(name=svc_template['name']))
        if 'picture' in svc_template:
            metadata['imageUrl'] = svc_template['picture']['image_href']

        plan_metadata = dict(displayName='Default',
                             longDescription="This plan deploys an instance of {name}".format(name=svc_template['name']),
                             cost='$0.0')

        default_plan = dict(name='default',
                            description="Default deployment plan for {name}-apb".format(name=svc_template['name']),
                            free='true',
                            metadata=plan_metadata,
                            parameters=parameters)
        if 'description' not in svc_template:
            svc_template['description'] = 'No description provided'
        apb = dict(version=1.0,
                   name=self.apb_normalized_name(svc_template['name']),
                   description=(svc_template['description'] or 'No description provided'),
                   bindable='false',
                   async='optional',
                   metadata=metadata,
                   plans=[default_plan])

        with open('apb.yml', 'w') as outfile:
            yaml.safe_dump(apb, outfile, default_flow_style=False)


    def create_vars_yml(self):
        parameters = self._svc_dialog_params
        svc_template = self._template
        print "Creating vars yaml file vars.yml for service template {name}".format(name=svc_template['name'])
        manageiq_vars = dict(api_url='http://localhost:3000/api',
                             service_template_href=svc_template['href'])
        varis = dict(manageiq=manageiq_vars)
        with open('vars.yml', 'w') as outfile:
            yaml.safe_dump(varis, outfile, default_flow_style=False)

class ServiceTemplate(MiqConnect):
    """
        Grab a service template from miq, and parse it
    """

    def __init__(self, opts):
        super(ServiceTemplate, self).__init__(opts)
        self._template = self.get()
        self._config_info = self._template['config_info']
        self._opts['dialog_id'] = self._config_info['provision']['dialog_id']

    @property
    def template(self):
        return self._template


    def dialog(self):
        """
            Returns the Dialog for the Service Template
        """
        dialog = ServiceDialog(self._opts)
        return dialog


    def convert(self, template):
        """
            Convert a ServiceTemplate into an apb.yaml file
        """
        dialog = self.dialog()
        toyaml = ReduceToYaml(dialog, template)
        toyaml.process_tabs()
        toyaml.create_apb_yml()
        toyaml.create_vars_yml()


def check_for_inited_apb():
    """
        Make sure we're in an existing APB directory
    """
    # check for Dockerfile, apb.yml, Makefile
    for fname in ('Dockerfile', 'apb.yml', 'Makefile'):
        if os.path.isfile(fname):
            pass
        else:
            raise Exception("Missing filename: {fname}, Are you running inside an apb directory?".format(fname=fname))



def cmdrun_add(**kwargs):
    """ Run MIQ apb operations """
    check_for_inited_apb()
    svc_template = ServiceTemplate(kwargs)
    svc_template.convert(svc_template.template)
