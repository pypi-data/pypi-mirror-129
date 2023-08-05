# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautobot_golden_config',
 'nautobot_golden_config.api',
 'nautobot_golden_config.management.commands',
 'nautobot_golden_config.migrations',
 'nautobot_golden_config.nornir_plays',
 'nautobot_golden_config.tests',
 'nautobot_golden_config.tests.test_nornir_plays',
 'nautobot_golden_config.tests.test_utilities',
 'nautobot_golden_config.utilities']

package_data = \
{'': ['*'],
 'nautobot_golden_config': ['static/nautobot_golden_config/diff2html-3.4.13/*',
                            'templates/nautobot_golden_config/*']}

install_requires = \
['deepdiff>=5.5.0,<6.0.0',
 'django-pivot>=1.8.1,<2.0.0',
 'matplotlib>=3.3.2,<4.0.0',
 'nautobot-plugin-nornir>=0.9.7']

setup_kwargs = {
    'name': 'nautobot-golden-config',
    'version': '0.9.10',
    'description': 'A plugin for configuration on nautobot',
    'long_description': "# nautobot-golden-config\n\nA plugin for [Nautobot](https://github.com/nautobot/nautobot) that intends to provide context around golden configuration.\n\n# Introduction\n\n## What is the Golden Configuration Plugin?\n\nThe golden configuration plugin is a Nautobot plugin that aims to solve common configuration management challenges.\n\n## Key Use Cases\n\nThis plugin enable four (4) key use cases.\n\n\n1. **Configuration Backups** - Is a Nornir process to connect to devices, optionally parse out lines/secrets, backup the configuration, and save to a Git repository.\n2. **Intended Configuration** - Is a Nornir process to generate configuration based on a Git repo of Jinja files to combine with a GraphQL generated data and a Git repo to store the intended configuration.\n3. **Source of Truth Aggregation** - Is a GraphQL query per device that creates a data structure used in the generation of configuration.\n4. **Configuration Compliance** - Is a process to run comparison of the actual (via backups) and intended (via Jinja file creation) CLI configurations upon saving the actual and intended configuration. This is started by either a Nornir process for cli-like configurations or calling the API for json-like configurations\n\n>Notice: The operator's of their own Nautobot instance are welcome to use any combination of these features. Though the appearance may seem like they are tightly \ncoupled, this isn't actually the case. For example, one can obtain backup configurations from their current RANCID/Oxidized process and simply provide a Git Repo\nof the location of the backup configurations, and the compliance process would work the same way. Also, another user may only want to generate configurations,\nbut not want to use other features, which is perfectly fine to do so.\n\n## Documentation\n- [Installation](./docs/installation.md)\n- [Quick Start Guide](./docs/quick-start.md)\n- [Navigating Overview](./docs/navigating-golden.md)\n- [Navigating Backup](./docs/navigating-backup.md)\n- [Navigating Intended](./docs/navigating-intended.md)\n- [Navigating SoTAgg](./docs/navigating-sot-agg.md)\n- [Navigating Compliance](./docs/navigating-compliance.md)\n- [Navigating JSON Compliance](./docs/navigating-compliance-json.md)\n- [FAQ](./docs/FAQ.md)\n\n## Screenshots\n\nThere are many features and capabilities the plugin provides into the Nautobot ecosystem. The following screenshots are intended to provide a quick visual overview of some of these features.\n\nThe golden configuration is driven by jobs that run a series of tasks and the result is captured in this overview.\n\n![Overview](./docs/img/golden-overview.png)\n\nThe compliance report provides a high-level overview on the compliance of your network.\n![Compliance Report](./docs/img/compliance-report.png)\n\nThe compliance overview will provide a per device and feature overview on the compliance of your network devices.\n![Compliance Overview](./docs/img/compliance-overview.png)\n\nDrilling into a specific device and feature, you can get an immediate detailed understanding of your device.\n![Compliance Device](./docs/img/compliance-device.png)\n\n![Compliance Rule](./docs/img/compliance-rule.png)\n\n# Contributing\n\nPull requests are welcomed and automatically built and tested against multiple versions of Python and Nautobot through TravisCI.\n\nThe project is packaged with a light development environment based on `docker-compose` to help with the local development of the project and to run tests within TravisCI.\n\nThe project is following Network to Code software development guidelines and are leveraging the following:\n- Black, Pylint, Bandit, flake8, and pydocstyle for Python linting and formatting.\n- Django unit test to ensure the plugin is working properly.\n\n## Branching Policy\n\nThe branching policy includes the following tenets:\n\n- The develop branch is the branch of the next major or minor version planned.\n- The `stable-<major>.<minor>` branch is the branch of the latest version within that major/minor version\n- PRs intended to add new features should be sourced from the develop branch\n- PRs intended to address bug fixes and security patches should be sourced from `stable-<major>.<minor>`\n\nNautobot Golden Config will observe semantic versioning, as of 1.0. This may result in an quick turn around in minor versions to keep\npace with an ever growing feature set.\n\n## Release Policy\n\nNautobot Golden Config has currently no intended scheduled release schedule, and will release new feature in minor versions.\n\n## Deprecation Policy\n\nSupport of upstream Nautobot will be announced 1 minor or major version ahead. Deprecation policy will be announced within the\nCHANGELOG.md file, and updated in the table below. There will be a `stable-<major>.<minor>` branch that will be minimally maintained.\nAny security enhancements or major bugs will be supported for a limited time. \n\n| Golden Config Version | Nautobot First Support Version | Nautobot Last Support Version |\n| --------------------- | ------------------------------ | ----------------------------- |\n| 0.9.X                 | 1.0                            | 1.2 [Official]                |\n| 1.0.X                 | 1.2                            | 1.2 [Tentative]               |\n\n## CLI Helper Commands\n\nThe project features a CLI helper based on [invoke](http://www.pyinvoke.org/) to help setup the development environment. The commands are listed below in 3 categories:\n- `dev environment`\n- `utility`\n- `testing`. \n\nEach command can be executed with `invoke <command>`. All commands support the arguments `--nautobot-ver` and `--python-ver` if you want to manually define the version of Python and Nautobot to use. Each command also has its own help `invoke <command> --help`\n\n> Note: to run the mysql (mariadb) development environment, set the environment variable as such `export NAUTOBOT_USE_MYSQL=1`.\n\n### Local Development Environment\n\n```\n  build            Build all docker images.\n  debug            Start Nautobot and its dependencies in debug mode.\n  destroy          Destroy all containers and volumes.\n  restart          Restart Nautobot and its dependencies in detached mode.\n  start            Start Nautobot and its dependencies in detached mode.\n  stop             Stop Nautobot and its dependencies.\n```\n\n### Utility \n\n```\n  cli              Launch a bash shell inside the running Nautobot container.\n  create-user      Create a new user in django (default: admin), will prompt for password.\n  makemigrations   Run Make Migration in Django.\n  nbshell          Launch a nbshell session.\n```\n\n### Testing \n\n```\n  bandit           Run bandit to validate basic static code security analysis.\n  black            Run black to check that Python files adhere to its style standards.\n  flake8           Run flake8 to check that Python files adhere to its style standards.\n  pydocstyle       Run pydocstyle to validate docstring formatting adheres to NTC defined standards.\n  pylint           Run pylint code analysis.\n  tests            Run all tests for this plugin.\n  unittest         Run Django unit tests for the plugin.\n```\n",
    'author': 'Network to Code, LLC',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nautobot/nautobot-golden-config',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
