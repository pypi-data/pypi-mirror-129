# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fractopo', 'fractopo.analysis', 'fractopo.tval']

package_data = \
{'': ['*']}

install_requires = \
['click',
 'descartes',
 'geopandas>=0.10.2,<0.11.0',
 'matplotlib',
 'numpy',
 'pandas>=1.3,<1.4',
 'powerlaw',
 'pygeos>=0.12.0,<0.13.0',
 'python-ternary',
 'rich>=10.7.0,<11.0.0',
 'scikit-learn',
 'scipy',
 'seaborn',
 'shapely>=1.8.0,<1.9.0',
 'typer>=0.3.2,<0.4.0']

extras_require = \
{'coverage': ['coverage>=5.0,<6.0', 'coverage-badge'],
 'docs': ['sphinx',
          'sphinx-rtd-theme',
          'nbsphinx',
          'sphinx-gallery',
          'sphinx-autodoc-typehints'],
 'format-lint': ['sphinx',
                 'pylint',
                 'rstcheck',
                 'black',
                 'black-nb',
                 'blacken-docs',
                 'blackdoc',
                 'isort'],
 'logging': ['nialog>=0.0.2,<0.0.3'],
 'typecheck': ['mypy']}

entry_points = \
{'console_scripts': ['fractopo = fractopo.cli:app',
                     'tracevalidate = fractopo.cli:tracevalidate_click']}

setup_kwargs = {
    'name': 'fractopo',
    'version': '0.2.3',
    'description': 'Fracture Network Analysis',
    'long_description': 'fractopo-readme\n===============\n\n|Documentation Status| |PyPI Status| |CI Test| |Coverage| |Binder| |Zenodo|\n\n``fractopo`` is a Python module that contains tools for validating and\nanalysing lineament and fracture trace maps (fracture networks).\n\n.. figure:: https://git.io/JBRuK\n   :alt: Overview of fractopo\n\n   Overview of fractopo\n\n-  Full Documentation is hosted on Read the Docs:\n\n   -  `Documentation <https://fractopo.readthedocs.io/en/latest/index.html#full-documentation>`__\n\nInstallation\n------------\n\n``pip`` and ``poetry`` installation only supported for ``linux`` and\n``MacOS`` based operating systems. For ``Windows`` install using\n``(ana)conda``.\n\nFor ``pip`` and ``poetry``: Omit --dev or [dev] for regular\ninstallation. Keep if you want to test/develop or otherwise install all\ndevelopment python dependencies.\n\nConda\n~~~~~\n\n-  Only supported installation method for ``Windows``!\n\n.. code:: bash\n\n   # Create new environment for fractopo (recommended)\n   conda env create fractopo-env\n   conda activate fractopo-env\n   # Available on conda-forge channel\n   conda install -c conda-forge fractopo\n\nPip\n~~~\n\nThe module is on `PyPI <https://www.pypi.org>`__.\n\n.. code:: bash\n\n   # Non-development installation\n   pip install fractopo\n\nOr locally for development:\n\n.. code:: bash\n\n   git clone https://github.com/nialov/fractopo\n   cd fractopo\n   # Omit [dev] from end if you do not want installation for development\n   pip install --editable .[dev]\n\npoetry\n~~~~~~\n\nFor usage:\n\n.. code:: bash\n\n   poetry add fractopo\n\nFor development:\n\n.. code:: bash\n\n   git clone https://github.com/nialov/fractopo --depth 1\n   cd fractopo\n   poetry install\n\nInput data\n~~~~~~~~~~\n\nReading and writing spatial filetypes is done in ``geopandas`` and you\nshould see ``geopandas`` documentation for more advanced read-write use\ncases:\n\n-  https://geopandas.org/\n\nSimple example with trace and area data in GeoPackages:\n\n.. code:: python\n\n   import geopandas as gpd\n\n   # Trace data is in a file `traces.gpkg` in current working directory\n   # Area data is in a file `areas.gpkg` in current working directory\n   trace_data = gpd.read_file("traces.gpkg")\n   area_data = gpd.read_file("areas.gpkg")\n\nTrace validation\n~~~~~~~~~~~~~~~~\n\nTrace and target area data can be validated for further analysis with a\n``Validation`` object.\n\n.. code:: python\n\n   from fractopo import Validation\n\n   validation = Validation(\n       trace_data,\n       area_data,\n       name="mytraces",\n       allow_fix=True,\n   )\n\n   # Validation is done explicitly with `run_validation` method\n   validated_trace_data = validation.run_validation()\n\nTrace validation is also accessible as a command-line script,\n``fractopo tracevalidate`` which is more straightforward to use than through\nPython calls. Note that all subcommands of ``fractopo`` are available by\nappending them after ``fractopo``.\n\n``tracevalidate`` always requires the target area that delineates trace\ndata.\n\n.. code:: bash\n\n   # Get full up-to-date script help\n\n   fractopo tracevalidate --help\n\n   # Basic usage:\n   # --allow-fix is recommended due to automatic fixing being very minor in effect\n   # currently (default True)\n   # --summary can be given to print out summary data of validation\n   # i.e. error types and error counts (default True)\n   # --output can be omitted. By default the same spatial filetype\n   # as the input is used and the output is saved as e.g.\n   # /path/to/validated/trace_data_validated.shp\n   # i.e. a new folder is created (or used) for validated data\n\n   fractopo tracevalidate /path/to/trace_data.shp /path/to/target_area.shp --fix --output /path/to/output_data.shp\n\n   # Or with automatic saving to validated/ directory\n\n   fractopo tracevalidate /path/to/trace_data.shp /path/to/target_area.shp --fix --summary\n\nGeometric and topological trace network analysis\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nTrace and target area data (``GeoDataFrames``) are passed into a\n``Network`` object which has properties and functions for returning and\nvisualizing different parameters and attributes of trace data.\n\n.. code:: python\n\n   from fractopo import Network\n\n   # Initialize Network object and determine the topological branches and nodes\n   network = Network(\n       trace_data,\n       area_data,\n       # Give the Network a name!\n       name="mynetwork",\n       # Specify whether to determine topological branches and nodes\n       # (Required for almost all analysis)\n       determine_branches_nodes=True,\n       # Specify the snapping distance threshold to define when traces are\n       # snapped to each other\n       snap_threshold=0.001,\n       # If the target area used in digitization is a circle, the knowledge can\n       # be used in some analysis\n       circular_target_area=True,\n       # Analysis on traces can be done for the full inputted dataset or the\n       # traces can be cropped to the target area before analysis (cropping\n       # recommended)\n       truncate_traces=True,\n   )\n\n   # Properties are easily accessible\n   # e.g.\n   network.branch_counts\n   network.node_counts\n\n   # Plotting is done by plot_ -prefixed methods\n   network.plot_trace_lengths()\n\nNetwork analysis is also available as a command-line script but I recommend\nusing a Python interface (e.g. ``jupyter lab``, ``ipython``) when analysing\n``Networks`` to have access to all available analysis and plotting methods. The\ncommand-line entrypoint is opinionated in what outputs it produces. Brief\nexample of command-line entrypoint:\n\n.. code:: bash\n\n   fractopo network traces.gpkg area.gpkg --name mynetwork\\\n      --circular-target-area --truncate-traces\n\n   # Use --help to see all up-to-date arguments and help\n   fractopo network --help\n\nDevelopment status\n------------------\n\n-  Breaking changes are possible and expected.\n-  Critical issues:\n\n   -  Trace validation should be refactored at some point.\n\n      -  Though keeping in mind that the current implementation works\n         well.\n\n   -  ``snap_traces`` in branch and node determination is not perfect.\n      Some edge cases cause artifacts which only sometimes are\n      recognized as error branches. However these cases are very rare.\n\n      -  Reinforces that some amount of responsibility is always in the\n         hands of the digitizer.\n      -  Issue mostly avoided when using a ``snap_threshold`` of 0.001\n\n-----\n\n.. |Documentation Status| image:: https://readthedocs.org/projects/fractopo/badge/?version=latest\n   :target: https://fractopo.readthedocs.io/en/latest/?badge=latest\n.. |PyPI Status| image:: https://img.shields.io/pypi/v/fractopo.svg\n   :target: https://pypi.python.org/pypi/fractopo\n.. |CI Test| image:: https://github.com/nialov/fractopo/workflows/test-and-publish/badge.svg\n   :target: https://github.com/nialov/fractopo/actions/workflows/test-and-publish.yaml?query=branch%3Amaster\n.. |Coverage| image:: https://raw.githubusercontent.com/nialov/fractopo/master/docs_src/imgs/coverage.svg\n   :target: https://github.com/nialov/fractopo/blob/master/docs_src/imgs/coverage.svg\n.. |Binder| image:: http://mybinder.org/badge_logo.svg\n   :target: https://mybinder.org/v2/gh/nialov/fractopo/HEAD?filepath=docs_src%2Fnotebooks%2Ffractopo_network_1.ipynb\n.. |Zenodo| image:: https://zenodo.org/badge/297451015.svg\n   :target: https://zenodo.org/badge/latestdoi/297451015\n',
    'author': 'nialov',
    'author_email': 'nikolasovaskainen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nialov/fractopo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
