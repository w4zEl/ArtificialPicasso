import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../artificialpicasso'))

project = 'Artificial Picasso'
copyright = '2022, Howard Ou, Amruth Arunkumar, Adib Raed, Max Lu, Jason Cheng'
author = 'Howard Ou, Amruth Arunkumar, Adib Raed, Max Lu, Jason Cheng'
release = '0.1.1'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary', 'sphinx.ext.napoleon', 'sphinx_autodoc_typehints',
              'sphinx.ext.viewcode', 'sphinx.ext.intersphinx']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'adafruit_motor': ('https://docs.circuitpython.org/projects/motor/en/stable/', None)
}
napoleon_use_param = True
autosummary_generate = True
autodoc_mock_imports = ["board", "adafruit_motor", "adafruit_pca9685"]
typehints_defaults = 'comma'

templates_path = ['_templates']
exclude_patterns = []


html_theme = 'furo'
html_static_path = ['_static']
