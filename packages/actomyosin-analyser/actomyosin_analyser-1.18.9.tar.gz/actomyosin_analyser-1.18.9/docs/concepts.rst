
Key Concepts
************

``Analyser``
============

The :class:`~actomyosin_analyser.analysis.analyser.Analyser`
class provides the unified user interface to the
analysis methods of the package. The interface is unified in the
sense, that reading the raw data is externalized to
implementations of the abstract
:class:`~actomyosin_analyser.file_io.data_reader.DataReader` class (see next section).

For many data that take a lot of time for computing or converting in desired formats,
the :class:`~actomyosin_analyser.analysis.analyser.Analyser` is designed to
compute/convert those data only once, then store them in the provided analysis file, and read them
upon next request of that data.
The user need only use the ``get`` methods for that, internally
the reading is delegated to a matching private ``_read``
method if the requested data is present, or
to a ``_compute`` method if it is not. The underscore denotes a private method which is not
meant to be used outside of the class it belongs to.

In this design where many data are computed only once,
compute times can be heavily reduced, but the trade-off is
that more disk space will be occupied.
For some aggregated results like MSDs (see section~\ref{sec:theory-msd}),
the benefit of saving time outweighs the draw-back that additional disk
space is occupied by far. In other cases, the benefits are debatable.

The :class:`~actomyosin_analyser.analysis.analyser.Analyser` will store
a copy of all trajectories in the analysis file when
they are retrieved from the :class:`~actomyosin_analyser.file_io.data_reader.DataReader`
for the first time. This can up to double the disk space
per simulation.
But for all simulation frameworks for which compatible ``DataReader``\ s were implemented
(cytosim, ``bead_state_model``), this was found to decrease the compute times a lot.

``DataReader``
==============

The :class:`~actomyosin_analyser.analysis.analyser.Analyser` works
independently of the raw data format. The goal is a unified
analysis interface, no matter how the raw data was created. This is achieved by
externalizing the raw data reading to implementations
of the :class:`~actomyosin_analyser.file_io.data_reader.DataReader` class.
In the ``actomyosin_analyser`` package, :class:`~actomyosin_analyser.file_io.data_reader.DataReader`
is a abstract base class.
This base class needs to be implemented to match the respective raw data. Implementations
of :class:`~actomyosin_analyser.file_io.data_reader.DataReader` exist for ``bead_state_model`` (in the ``bead_state_model`` package) and
for ``cytosim``
(in the ``cytosim_reader`` `package <https://gitlab.gwdg.de/ikuhlem/cytosim_reader>`_).
Technically, these implementations do not inherit from the base class
:class:`~actomyosin_analyser.file_io.data_reader.DataReader`, as I did not
want to make ``actomyosin_analyser`` a dependency for either one.


Example
=======

.. code:: python

   from actomyosin_analyser.analysis.analyser import Analyser

   # create instance of a DataReader implementation
   dr = ...

   a = Analyser(dr,'analysis.h5')

   # access filament trajectories:
   coords = a.get_filament_trajectories(minimum_image=True)
   # minimum image projection is used, to project filament segments exceeding a
   # periodic boundary box back into the extent of the simulation box.

   # access mean-squared displacements of the centers of mass of filaments:
   com_msds = a.get_filament_center_of_mass_msds(skip=0)
   # skip specifies how many initial frames should be skipped
   # (if system is not in relevant state from the start on, e.g. cross-links
   # are still forming, system is not equilibrated, etc.)


Analyzing Sets of Simulations
=============================

``actomyosin_analyser`` offers some means to deal with sets of simulations, where one or multiple
parameters were varied across simulations. Namely, these means
are the ``ExperimentIterator`` class and analysis pipelines. The ``ExperimentIterator`` is
generated from a ``pandas`` table with information on parameter values for each simulation.
Simulations are then grouped by matching parameters. Pipelines make use of these groups,
and can  largely automated compute results of ensembles of simulations.

Examples were not yet included in this documentation. For more information, you have
to look into the code of ``actomyosin_analyser.pipeline`` package directly. 
