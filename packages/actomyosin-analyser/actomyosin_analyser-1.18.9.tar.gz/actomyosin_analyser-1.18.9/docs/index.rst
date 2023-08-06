.. actomyosin_analyser documentation master file, created by
   sphinx-quickstart on Mon Jul  5 10:55:51 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation of ``actomyosin_analyser``
========================================

``actomyosin_analyser`` is a python package that collects
analysis tools for polymer data. It was developed
with a focus on output data of actin simulation frameworks
(especially `bead-state-model <https://gitlab.com/ilyas.k/bead_state_model>`_ and
`cytosim <https://gitlab.com/f-nedelec/cytosim>`_, in early versions
also `AFINES <https://github.com/Simfreed/AFINES>`_).

.. figure:: _static/figures/ovito_filament.svg

   Visualization of a polymer using `ovito <https://www.ovito.org/>`_.
   How to export polymer trajectories to XYZ is described :ref:`here <export>`

The project is being developed in
`this repository <https://gitlab.com/ilyas.k/actomyosin_analyser>`_ on gitlab.com.
Open an issue there if you encounter bugs or for feedback and requests. Contributions
through merge requests are very welcome.
``actomyosin_analyser`` is published as free software under the
`GNU GPLv3 <http://www.gnu.org/licenses/gpl-3.0.en.html>`_ license.

Install
=======

``actomyosin_analyser`` can be installed via pip:

.. code:: bash

   pip install actomyosin-analyser

Docker
------

``actomyosin_analyser`` is also installed in the ``bead_state_model``
`docker image <https://hub.docker.com/r/ilyask/bead_state_model>`_. Details how to install and use it
can be found in the `README <https://gitlab.com/ilyas.k/bead_state_model>`_
and `documentation <http://akbg.uni-goettingen.de/docs/bead_state_model/>`_ of ``bead_state_model``.

Documentation Contents:
=======================

.. toctree::
   :maxdepth: 2

   concepts.rst
   export_xyz.rst
   what.rst
   code.rst
