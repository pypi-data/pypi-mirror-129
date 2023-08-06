QuickStart:
===========

.. _installation:

Installation:
-------------

To use hbspark, first install it using pip:

.. code-block:: console

   $ pip install hbspark

Note that correct versioning is required. Please review the `PyPi <https://pypi.org/project/hbspark/>`_ repository to determine compatibility.

.. _examples:

Examples:
---------

Initialization and imports:
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To initialize the connection proper imports and initialization is required. The simplest example is provided:

.. code-block:: python

   import hbspark
   from pyspark.sql import SparkSession

   spark_session = SparkSession.builder.appName('my-spark-app').master('local[1]').getOrCreate()
   
   hbase_host_name = '___.___.___.___'
   hbase_host_name2 = 'hostname_at_dns'

   hbspark.connect(hbaseHostName, spark)


Get all of the tables:
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   #Initialize hbspark as in "Initialization and imports"
   all_tables = hbspark.tables()

   print(all_tables)
   # ['table1', 'table2', ...]

Next Steps:
^^^^^^^^^^^

With your initialized hbspark connection, read the :doc:`api_documentation` in order to work with hbase tables.