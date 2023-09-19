# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from datetime import date
import os
import metalattice

version = metalattice.__version__
release = version

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'MetaLattice'
copyright = '2022-%s, Huang Lihao' % date.today().year
author = 'Huang Lihao'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.linkcode',
    'sphinx.ext.napoleon',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinx.ext.todo',
]

templates_path = ['_templates']
exclude_patterns = []




# Define the json_url for our version switcher.
json_url = "https://metalattice.readthedocs.io/en/latest/_static/switcher.json"

# Define the version we use for matching in the version switcher.
version_match = os.environ.get("READTHEDOCS_VERSION")
# If READTHEDOCS_VERSION doesn't exist, we're not on RTD
# If it is an integer, we're in a PR build and the version isn't correct.
# If it's "latest" → change to "dev" (that's what we want the switcher to call it)
if not version_match or version_match.isdigit() or version_match == "latest":
    # For local development, infer the version to match from the package.
    release = metalattice.__version__
    if "dev" in release or "rc" in release:
        version_match = "dev"
        # We want to keep the relative reference if we are in dev mode
        # but we want the whole url if we are effectively in a released version
        json_url = "_static/switcher.json"
    else:
        version_match = "v" + release


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.svg"
todo_include_todos = True

html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/huang-lihao/metalattice",
            "icon": "fa-brands fa-square-github",
            "type": "fontawesome",
        },
    ],
    "switcher": {
        "json_url": json_url,
        "version_match": version_match,
    },
    "navbar_end": ["theme-switcher", "version-switcher", "navbar-icon-links"],
    "show_nav_level": 1,
    "navigation_depth": 1,
}

def linkcode_resolve(domain, info):
    if domain != 'py':
        return None
    if not info['module']:
        return None
    filename = info['module'].replace('.', '/')
    return "https://github.com/huang-lihao/metalattice/%s.py" % filename


# Napoleon settings
napoleon_use_admonition_for_examples = True
napoleon_use_ivar = True
napoleon_preprocess_types = True