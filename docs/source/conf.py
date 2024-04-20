# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from datetime import date
import os
from os.path import relpath, dirname
import re
from sphinx.util import inspect
import sys

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
    'numpydoc',
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
html_css_files = ["metalattice.css"]
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

# -----------------------------------------------------------------------------
# Source code links
# -----------------------------------------------------------------------------

# Not the same as from sphinx.util import inspect and needed here
import inspect  # noqa: E402

for name in ['sphinx.ext.linkcode', 'linkcode', 'numpydoc.linkcode']:
    try:
        __import__(name)
        extensions.append(name)
        break
    except ImportError:
        pass
else:
    print("NOTE: linkcode extension not found -- no links to source generated")


def linkcode_resolve(domain, info):
    """
    Determine the URL corresponding to Python object
    """
    if domain != 'py':
        return None

    modname = info['module']
    fullname = info['fullname']

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split('.'):
        try:
            obj = getattr(obj, part)
        except Exception:
            return None

    # Use the original function object if it is wrapped.
    while hasattr(obj, "__wrapped__"):
        obj = obj.__wrapped__
    # # SciPy's distributions are instances of *_gen. Point to this
    # # class since it contains the implementation of all the methods.
    # if isinstance(obj, (rv_generic, multi_rv_generic)):
    #     obj = obj.__class__
    try:
        fn = inspect.getsourcefile(obj)
    except Exception:
        fn = None
    if not fn:
        try:
            fn = inspect.getsourcefile(sys.modules[obj.__module__])
        except Exception:
            fn = None
    if not fn:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except Exception:
        lineno = None

    if lineno:
        linespec = "#L%d-L%d" % (lineno, lineno + len(source) - 1)
    else:
        linespec = ""

    startdir = os.path.abspath(os.path.join(dirname(metalattice.__file__), '..'))
    fn = relpath(fn, start=startdir).replace(os.path.sep, '/')

    if fn.startswith('metalattice/'):
        fn = os.path.join("src", fn)
        m = re.match(r'^.*dev0\+([a-f0-9]+)$', metalattice.__version__)
        base_url = "https://github.com/huang-lihao/metalattice/blob"
        if m:
            return f"{base_url}/{m.group(1)}/{fn}{linespec}"
        elif 'dev' in metalattice.__version__:
            return f"{base_url}/main/{fn}{linespec}"
        else:
            return f"{base_url}/v{metalattice.__version__}/{fn}{linespec}"
    else:
        return None



# Napoleon settings
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_keyword = True
napoleon_use_rtype = True
napoleon_preprocess_types = True