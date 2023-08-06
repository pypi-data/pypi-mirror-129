
Source Code Documentation
*************************

This page contains documentation of selection of key
components that I consider most important for users of the package.

.. _analyser:

``Analyser``
============

The :class:`~actomyosin_analyser.analysis.analyser.Analyser` is the essential component
of the ``actomyosin_analyser`` package. It provides a unified interface to apply
analysis tools on your polymer data.

.. autoclass:: actomyosin_analyser.analysis.analyser.Analyser
   :members:
   :inherited-members:
	       
   .. automethod:: __init__

``DataReader``
==============

The ``DataReader`` is an abstract class. Implementations of this class are used
to *tell* the :ref:`analyser`, how to read the raw data. You need to create
your own implementation of this class matching the format of your raw data files.
Implementations of the ``DataReader`` exist for ``bead_state_model``
(in the `bead_state_model package <https://gitlab.com/ilyas.k/bead_state_model>`_) and
for ``cytosim``
(in the `cytosim_reader package <https://gitlab.gwdg.de/ikuhlem/cytosim_reader>`_).

.. autoclass:: actomyosin_analyser.file_io.data_reader.DataReader
   :members:
		   
``GridGenerator``
=================

This class is used to define the grid during evaluation of the
polymer particle densities
(see :py:meth:`~actomyosin_analyser.analysis.analyser.Analyser.get_polymer_density`).

.. autoclass:: actomyosin_analyser.analysis.polymer_density.GridGenerator
   :members:
