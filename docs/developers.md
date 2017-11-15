# Developer Guide

To get more information on creating your first APB, take a look at our [getting started guide](https://github.com/ansibleplaybookbundle/ansible-playbook-bundle/blob/master/docs/getting_started.md)

  1. [Explanation of APB Spec File](#apb-spec-file)
  1. [APB Actions](#actions)
  1. [Creating Resources with an APB](#common-resources-to-provision)
     * [Service](#service)
     * [DeploymentConfig](#deployment-config)
     * [Route](#route)
     * [PersistentVolume](#persistent-volume)
     * [Binding Credentials](#asb-encode-binding)
  1. [APB Spec Version](#apb-spec-versioning)
  1. [Tips & Tricks](#tips-and-tricks)
     * [Working with Restricted SCC](#working-with-the-restricted-scc)
     * [Using a ConfigMap](#using-a-configmap-within-an-apb)


## APB Examples
For completed APB examples, take a look at some of the APBs in the [ansibleplaybookbundle org](https://github.com/ansibleplaybookbundle)
* [hello-world-apb](https://github.com/ansibleplaybookbundle/hello-world-apb)
* [hello-world-db-apb](https://github.com/ansibleplaybookbundle/hello-world-db-apbb)
* [pyzip-demo-apb](https://github.com/ansibleplaybookbundle/pyzip-demo-apb)
* [pyzip-demo-db-apb](https://github.com/ansibleplaybookbundle/pyzip-demo-db-apb)
* [nginx-apb](https://github.com/ansibleplaybookbundle/nginx-apb)
* [rocketchat-apb](https://github.com/ansibleplaybookbundle/rocketchat-apb)
* [etherpad-apb](https://github.com/ansibleplaybookbundle/etherpad-apb)
* [hastebin-apb](https://github.com/ansibleplaybookbundle/hastebin-apb)
* [mediawiki123-apb](https://github.com/ansibleplaybookbundle/mediawiki123-apb)
* [jenkins-apb](https://github.com/ansibleplaybookbundle/jenkins-apb)
* [manageiq-apb](https://github.com/ansibleplaybookbundle/manageiq-apb)
* [wordpress-ha-apb](https://github.com/ansibleplaybookbundle/wordpress-ha-apb)
* [thelounge-apb](https://github.com/ansibleplaybookbundle/thelounge-apb)
* [rhscl-postgresql-apb](https://github.com/ansibleplaybookbundle/rhscl-postgresql-apb)
* [rhscl-mariadb-apb](https://github.com/ansibleplaybookbundle/rhscl-mariadb-apb)
* [rhscl-mysql-apb](https://github.com/ansibleplaybookbundle/rhscl-mysql-apb)
* [rds-postgres-apb](https://github.com/ansibleplaybookbundle/rds-postgres-apb)

##### Directory Structure
The following shows an example directory structure of an APB.
```bash
example-apb/
├── Dockerfile
├── apb.yml
└── roles/
│   └── example-apb-openshift
│       ├── defaults
│       │   └── main.yml
│       └── tasks
│           └── main.yml
└── playbooks/
    └── provision.yml
    └── deprovision.yml
    └── bind.yml
    └── unbind.yml
```

# APB Spec File
The APB Spec File (`apb.yml`) is where the outline of your application is declared.  The following is an example APB spec

```yml
version: 1.0
name: example-apb
description: A short description of what this APB does
bindable: True
async: optional
metadata: 
  documentationUrl: <link to documentation>
  imageUrl: <link to URL of image>
  dependencies: ['<registry>/<organization>/<dependency-name-1>', '<registry>/<organization>/<dependency-name-2>']
  displayName: Example App (APB)
  longDescription: A longer description of what this APB does
  providerDisplayName: "Red Hat, Inc."
plans:
  - name: default
    description: A short description of what this plan does
    free: true
    metadata:
      displayName: Default
      longDescription: A longer description of what this plan deploys
      cost: $0.00
    parameters:
      - name: parameter_one
        required: true
        default: foo_string
        type: string
        title: Parameter One
        maxlength: 63
      - name: parameter_two
        required: true
        default: true
        title: Parameter Two
        type: boolean
```
## Top level structure
* `version`: Version of the APB spec. Please see [versioning](#apb-spec-versioning) for more information.
* `name`: Name of the APB.
* `description`: Short description of this APB.
* `bindable`: Boolean option of whether or not this APB can be bound to. Accepted fields are `true` or `false`.
* `async`: Field to determine whether the APB can be deployed asynchronously. Accepted fields are `optional`, `required`, `unsupported`.
* `metadata`: A dictionary field declaring relevant metadata information. Please see the [metadata section](#metadata) for more information.
* `plans`: A list of plans that can be deployed. Please see the [plans section](#plans) for more information.

### Metadata

* `documentationUrl`: URL to the applications documentation.
* `imageUrl`: URL to an image which will be displayed in the WebUI for the Service Catalog.
* `dependencies`: List of images which are consumed from within the APB.
* `displayName`: The name that will be displayed in the WebUI for this APB.
* `longDescription`: Longer description that will be displayed when the APB is clicked in the WebUI.
* `providerDisplayName`: Name of who is providing this APB for consumption.

### Plans
Plans are declared as a list. This section will explain what each field in a plan describes.
* `name`: Unique name of plan to deploy. This will be displayed when the APB is clicked from the Service Catalog.
* `description`: Short description of what will be deployed from this plan.
* `free`: Boolean field to determine if this plan is free or not. Accepted fields are `true` or `false`.
* `metadata`: Dictionary field declaring relevant plan metadata information. Please see the [plan metadata section](#plan-metadata)
* `parameters`: List of parameter dictionaries used as input to the APB. Please see the [parameters section](#parameters)

### Plan Metadata
* `displayName`: Name to display for the plan in the WebUI.
* `longDescription`: Longer description of what this plan deploys.
* `cost`: How much the plan will cost to deploy. Accepted field is `$x.yz`

### Parameters
Each item in the `parameters` section can have several fields.  `name` is required.  The order of the parameters will be displayed in sequential order in the form in the OpenShift UI.
```yaml
parameters:
  - name: my_param
    title: My Parameter
    type: enum
    enum: ['X', 'Y', 'Z']
    required: True
    default: X
    display_type: select
    display_group: Group 1
```
* `name`: Unique name of the parameter passed into the APB
* `title`: Displayed label in the UI.
* `type`: Data type of the parameters as specified by [json-schema](http://json-schema.org/) such as `string`, `number`, `int`, `boolean`, or `enum`.  Default input field type in the UI will be assigned if no `display_type` is assigned.
* `required`: Whether or not the parameter is required for APB execution.  Required field in UI.
* `default`: Default value assigned to the parameter.
* `display_type`: Display type for the UI.  For example, you can override a string input as a `password` to hide it in the UI.  Accepted fields include `text`, `textarea`, `password`, `checkbox`, `select`.
* `display_group`: will cause a parameter to display in groups with adjacent parameters with matching `display_group` fields.  In the above example, adding another field below with `display_group: Group 1` will visually group them together in the UI under the heading "Group 1".

When using a long list of parameters it might be useful to use a shared parameter list. For an example of this, please see [rhscl-postgresql-apb](https://github.com/ansibleplaybookbundle/rhscl-postgresql-apb/blob/master/apb.yml#L4) for an example.

## Actions
An action for an APB is the command that the APB is run with. The 5 standard actions that we support is `provision`, `deprovision`, `bind`, `unbind`, and `test`. For an action to be valid there must be a valid file in the `playbooks` directory named `<action>.yml`. These playbooks can do anything which also means that you can technically create any action you would like. Our [mediawiki-apb](https://github.com/ansibleplaybookbundle/mediawiki123-apb/blob/master/playbooks/update.yml) has an example of creating an action `update`.


# Common Resources to Provision
## Service
The following is a sample ansible task to create a service named `hello-world`. It is worth noting that the `namespace` variable in an APB will be provided by the Ansible Service Broker when launched from the WebUI.
```yml
- name: create hello-world service
  k8s_v1_service:
    name: hello-world
    namespace: '{{ namespace }}'
    labels:
      app: hello-world
      service: hello-world
    selector:
      app: hello-world
      service: hello-world
    ports:
      - name: web
        port: 8080
        target_port: 8080
```

## Deployment Config
The following is a sample ansible task to create a deployment config for the image: `docker.io/ansibleplaybookbundle/hello-world` which maps to service `hello-world`.
```yml
- name: create deployment config
  openshift_v1_deployment_config:
    name: hello-world
    namespace: '{{ namespace }}'
    labels:
      app: hello-world
      service: hello-world
    replicas: 1
    selector:
      app: hello-world
      service: hello-world
    spec_template_metadata_labels:
      app: hello-world
      service: hello-world
    containers:
    - env:
      image: docker.io/ansibleplaybookbundle/hello-world:latest
      name: hello-world
      ports:
      - container_port: 8080
        protocol: TCP
```
### Adding optional variables to an Ansible playbook bundle via environment variables

To pass variables into an APB, you will need to escape the variable substitution in your `.yml` files. For example, the below is a section of the [main.yml](https://github.com/fusor/apb-examples/blob/master/etherpad-apb/roles/provision-etherpad-apb/tasks/main.yml#L89) in the [etherpad-apb](https://github.com/fusor/apb-examples/tree/master/etherpad-apb):

```yml
- name: create mariadb deployment config
  openshift_v1_deployment_config:
    name: mariadb
    namespace: '{{ namespace }}'
    ...
    - env:
      - name: MYSQL_ROOT_PASSWORD
        value: '{{ mariadb_root_password }}'
      - name: MYSQL_DATABASE
        value: '{{ mariadb_name }}'
      - name: MYSQL_USER
        value: '{{ mariadb_user }}'
      - name: MYSQL_PASSWORD
        value: '{{ mariadb_password }}'
```

To define variables, use the `main.yml` file under the `defaults` folder to define/set other variables for your APB.  For example, below is the [defaults/main.yml](https://github.com/fusor/apb-examples/blob/master/etherpad-apb/roles/provision-etherpad-apb/defaults/main.yml) for the `etherpad-apb`:

```yml
---
playbook_debug: no
mariadb_root_password: "{{ lookup('env','MYSQL_ROOT_PASSWORD') | default('admin', true) }}"
mariadb_name: "{{ lookup('env','MYSQL_DATABASE') | default('etherpad', true) }}"
mariadb_user: "{{ lookup('env','MYSQL_USER') | default('etherpad', true) }}"
mariadb_password: "{{ lookup('env','MYSQL_PASSWORD') | default('admin', true) }}"
etherpad_admin_password: "{{ lookup('env','ETHERPAD_ADMIN_PASSWORD') | default('admin', true) }}"
etherpad_admin_user: "{{ lookup('env','ETHERPAD_ADMIN_USER') | default('etherpad', true) }}"
etherpad_db_host: "{{ lookup('env','ETHERPAD_DB_HOST') | default('mariadb', true) }}"
state: present
```

## Route
The following is an example of creating a route named `hello-world` which maps to service `hello-world`.
```yml
- name: create hello-world route
  openshift_v1_route:
    name: hello-world
    namespace: '{{ namespace }}'
    spec_port_target_port: web
    labels:
      app: hello-world
      service: hello-world
    to_name: hello-world
```

## Persistent Volume
The following is an example of creating a persistent volume claim resource.
```yml
- name: create volume claim
  k8s_v1_persistent_volume_claim:
    name: hello-world-db
    namespace: '{{ namespace }}'
    state: present
    access_modes:
      - ReadWriteOnce
    resources_requests:
      storage: 1Gi
```

In addition, we need to add our volume to the deployment config declaration. The following is an example deployment config with a persistent volume.

```yml
- name: create hello-world-db deployment config
  openshift_v1_deployment_config:
    name: hello-world-db
    ---
    volumes:
    - name: hello-world-db
      persistent_volume_claim:
        claim_name: hello-world-db
      test: false
      triggers:
      - type: ConfigChange
```

## ASB Encode Binding
A very useful task to use when creating a bindable APB is the `asb_encode_binding` module. This module should be called at the end of the APBs provision role and it will return bind credentials to the Ansible Service Broker.
```
- name: encode bind credentials
  asb_encode_binding:
    fields:
      EXAMPLE_FIELD: foo
      EXAMPLE_FIELD2: foo2
```

# Tips and Tricks

## Working with the restricted scc
When building an OpenShift image, it is important that we do not have our application running as the root user when at all possible. When running under the restriced security context, the application image is launched with a random UID. This will cause problems if your application folder is owned by the root user. A good way to work around this is to add a user to the root group and make the application folder owned by the root group. A very good article on how to support Arbitrary User IDs is shown [here](https://docs.openshift.org/latest/creating_images/guidelines.html#openshift-origin-specific-guidelines). The following is a Dockerfile example of a node app running in `/usr/src`. This command would be run after the application is installed in `/usr/src` and the associated environment variables set.

```Dockerfile
ENV USER_NAME=haste \
    USER_UID=1001 \
    HOME=/usr/src

RUN useradd -u ${USER_UID} -r -g 0 -M -d /usr/src -b /usr/src -s /sbin/nologin -c "<username> user" ${USER_NAME} \
               && chown -R ${USER_NAME}:0 /usr/src \
               && chmod -R g=u /usr/src /etc/passwd
USER 1001
```

## Using a ConfigMap within an APB
There is a temporary workaround we are using to create configmaps from ansible due to a bug in the Ansible modules.

One common use case for ConfigMaps is when the parameters of an APB will be used within a configuration file of an application or service. The ConfigMap module allows you to mount a ConfigMap into a pod as a volume which can be used to store the config file. This approach allows you to also leverage the power Ansible's `template` module to create a ConfigMap out of APB paramters. The following is an example of creating a ConfigMap from a jinja template mounted into a pod as a volume.

```yaml
- name: Create hastebin config from template
  template:
    src: config.js.j2
    dest: /tmp/config.js

- name: Create hastebin configmap
  shell: oc create configmap haste-config --from-file=haste-config=/tmp/config.js

---snip

- name: create deployment config
  openshift_v1_deployment_config:
    name: hastebin
    namespace: '{{ namespace }}'
    labels:
      app: hastebin
      service: hastebin
    replicas: 1
    selector:
      app: hastebin
      service: hastebin
    spec_template_metadata_labels:
      app: hastebin
      service: hastebin
    containers:
    - env:
      image: docker.io/dymurray/hastebin:latest
      name: hastebin
      ports:
      - container_port: 7777
        protocol: TCP
      volumeMounts:
        - mountPath: /usr/src/haste-server/config
          name: config
    - env:
      image: docker.io/modularitycontainers/memcached:latest
      name: memcached
      ports:
      - container_port: 11211
        protocol: TCP
    volumes:
      - name: config
        configMap:
          name: haste-config
          items:
            - key: haste-config
              path: config.js

```

# APB Spec Versioning
We are using semantic versioning with the format of x.y where x is a major release and y is a minor release.

The current spec version is 1.0.

## Major Version Bump
We will increment the major version whenever an API breaking change is introduced to the APB spec. Some examples include:
* Introduction/deletion of a required field
* Changing the yaml format
* New features

## Minor Version Bump
We will increment the minor version whenever a non-breaking change is introduced to the APB spec. Some examples include:
* Introduction/deletion of an optional field
* Spelling change
* Introduction of new options to an existing field
