
..
    THIS FILE IS EXCLUSIVELY MAINTAINED by the project de_tpl_namespace_root V0.2.4 

namespace portions documentation
################################

welcome to the documentation of the portions (app/service modules and sub-packages) of this freely extendable
de namespace (:pep:`420`).


.. include:: ../features_and_examples.rst


code maintenance guidelines
***************************


portions code requirements
==========================

    * pure python
    * fully typed (:pep:`526`)
    * fully :ref:`documented <de-portions>`
    * 100 % test coverage
    * multi thread save
    * code checks (using pylint and flake8)


design pattern and software principles
======================================

    * `DRY <http://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`_
    * `KISS <http://en.wikipedia.org/wiki/Keep_it_simple_stupid>`_


.. include:: ../CONTRIBUTING.rst


register a new namespace portion
================================

the registration of a new portion to the de namespace has to be done by one of the namespace maintainers.
a registered portion will automatically be included into this `de namespace documentation`, available at
`ReadTheDocs <https://de.readthedocs.io>`_.

follow the steps underneath to register and add a new portion to the `de` namespace:

1. open a console window and change the current directory to the parent folder of your projects.
2. choose a not-existing/unique name for the new portion (referred as `<portion-name>` in the next steps).
3. run ``grm new-module <portion_name> --namespace=de`` to register the portion name within the namespace,
   to create a new project folder `de_<portion-name>` (providing initial project files created from
   templates) and to get a pre-configured git repository (with the remote already set and the initial files committed).
4. run ``cd de_<portion-name>`` to change the current to the new project folder
5. run `pyenv local \<venv_name\> <https://pypi.org/project/pyenv/>`_ to create/prepare a local virtual environment.
6. TDD: add unit tests into the test module `test_de_<portion-name>.py`, prepared within the
   `tests` sub-folder of your new code project folder.
7. extend the file <portion_name>.py situated in the `de` sub-folder to implement the new portion.
8. run ``grm check-integrity`` to run the linting and unit tests (if they fail go one or two steps back).
9. run ``grm commit`` and ``grm push`` to upload your new portion via to your remote/server repository under the project
   name `de_<portion-name>` in the users group `degroup` (at https://gitlab.com/degroup).


.. _de-portions:

registered namespace package portions
*************************************

the following list contains all registered portions of the de namespace.


.. hint::
    portions with no dependencies are at the begin of the following list. the portions that are depending on other
    portions of the de namespace are listed more to the end.


.. autosummary::
    :toctree: _autosummary
    :nosignatures:

    de.git_repo_manager
    de.git_repo_manager.git_repo_manager
    de.setup_project
    de.setup_project.setup_project
    de.tpl_namespace_root
    de.tpl_namespace_root.tpl_namespace_root
    de.tpl_project
    de.tpl_project.tpl_project


indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
* `portion repositories at gitlab.com <https://gitlab.com/degroup>`_
