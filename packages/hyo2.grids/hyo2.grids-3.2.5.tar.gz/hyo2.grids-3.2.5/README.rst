HydrOffice Grids
================

General Info
------------

.. image:: https://www.hydroffice.org/img/hyo2.grids.png
    :alt: logo

HydrOffice is a research development environment for ocean mapping. It provides a collection of hydro-packages, each of them dealing with a specific issue of the field.
The main goal is to speed up both algorithms testing and research-2-operation.

The Grids hydro-package provides means to manage hydrographic surfaces (Caris CSAR SDK 2.1.0 and Open Navigation Surface BAG).

It is currently composed of 3 modules:

* *OcBase* is a collection of helper tools (e.g., thread-safe exceptions and logging)
* *Grids* abtracts the access to the underline Caris CSAR and ONS BAG formats, both VR and SR.
* *Gappy* detects data holidays in gridded data.


.. note:: The LGPLv3 license applies only to the repository C++ and Python code.
          Refer to the Caris' EULA for the *restrictive* licensing conditions of the CSAR SDK
          (see `caris_csar_sdk_eula.txt <https://bitbucket.org/giumas/hyo_gridder/raw/master/cxx/licenses/caris_csar_sdk_eula.txt>`_).

Dependencies
------------

For the libraries, you will need:

* `Eigen <http://eigen.tuxfamily.org/index.php?title=Main_Page>`_ 

For the *Gappy* module, you will also need:

* `OpenCV <http://opencv.org/>`_

For the Python binding, you will need:

* `Python <https://www.python.org/>`_ *[>=3.5]*
* `NumPy <http://www.numpy.org/>`_

For running some of the example scripts, you might also need:
* `Matplotlib <http://matplotlib.org/>`_


Other info
----------

* GitHub: `https://github.com/hydroffice/hyo_grids <https://github.com/hydroffice/hyo_grids>`_
* Project page: `http://www.hydroffice.org <http://www.hydroffice.org>`_
* License: LGPLv3 license (See `LICENSE <https://github.com/hydroffice/hyo_grids/raw/master/py/LICENSE>`_)
