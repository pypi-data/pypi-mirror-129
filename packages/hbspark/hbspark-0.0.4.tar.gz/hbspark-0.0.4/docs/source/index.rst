.. hbspark documentation master file, created by
   sphinx-quickstart on Sat Oct 30 22:30:31 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to hbspark's documentation!
===================================

Overview:
---------
HbSpark is meant to be a pipelining tool that allows for an efficient transfer of data from HBase to Spark. It relies on the thrift API for HBase to directly convert tables into Spark dataframes which can be then be used for distributed computing. Aftewards, results can be piped back to HBase through this same interface.

Contents:
---------

The quickstart contains useful information about getting up and running with HbSpark:

.. toctree::
   :maxdepth: 2

   quickstart


API
---

It is highly recommended to utilize the API documentation while building your own projects with HbSpark.

.. toctree::

   api_documentation

   
Check out the :doc:`quickstart` section for further information, including how to :ref:`install <installation>` the project.
