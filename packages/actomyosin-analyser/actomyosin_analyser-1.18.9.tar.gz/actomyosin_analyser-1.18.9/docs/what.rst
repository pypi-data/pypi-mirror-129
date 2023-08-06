
What can be Computed?
*********************

I want to list a few examples here, but the list is very incomplete currently.
I will add examples as I need them.

MSDs from Trajectories
======================

``actomyosin_analyser`` provides a general and ``numba``-accelerated
function to compute MSDs from trajectories. Example:

.. code::

   import matplotlib.pyplot as plt
   from actomyosin_analyser.analysis.mean_squared_displacement import compute_msd

   """
   Load your data in a (N, M, d) array, where d = 2 or d = 3 is the dimensionality.
   N is the number of frames, M is the number of particles/trajectories. If you have only one
   particle/trajectory, you can also use a (N, d) array.
   """
   trajectories = ... # load your data into a (N, M, 2)

   msd = copute_msd(trajectories)

   fig, ax = plt.subplots(1, 1)
   ax.plot(msd.lag, msd.msd)
   ax.set(
        xscale='log',
	yscale='log',
	xlabel='lag in frames',
	ylabel='MSD'
   ) 
   plt.show()
   
  
