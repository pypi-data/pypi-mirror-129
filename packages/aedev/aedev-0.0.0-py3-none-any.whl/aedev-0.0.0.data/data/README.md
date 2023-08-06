<!-- THIS FILE IS EXCLUSIVELY MAINTAINED by the project de_tpl_namespace_root V0.2.4 -->
# __de__ namespace-root project

de namespace-root: root of de namespace portions, providing development tools for Python projects.

## de namespace root package use-cases

this project is maintaining all the portions (modules and sub-packages) of the de namespace to:

* update and deploy common outsourced files, optionally generated from templates
* merge docstrings of all portions into a single combined and cross-linked documentation
* publish documentation via Sphinx onto [ReadTheDocs](https://de.readthedocs.io "de on RTD")
* refactor multiple or all portions of this namespace simultaneously using the grm portions actions

this namespace-root package is only needed for development tasks, so never add it to the installation requirements
file (requirements.txt) of a project.

to ensure the update and deployment of outsourced files generated from the templates provided by this root package via
the [git repository manager tool](https://github.com/degroup/de_git_repo_manager), add this root package to the
development requirements file (dev_requirements.txt) of a portion project of this namespace.

the following portions are currently included in this namespace:

* [de_git_repo_manager](https://pypi.org/project/de_git_repo_manager "de namespace portion de_git_repo_manager")
* [de_setup_project](https://pypi.org/project/de_setup_project "de namespace portion de_setup_project")
* [de_tpl_namespace_root](https://pypi.org/project/de_tpl_namespace_root "de namespace portion de_tpl_namespace_root")
* [de_tpl_project](https://pypi.org/project/de_tpl_project "de namespace portion de_tpl_project")

