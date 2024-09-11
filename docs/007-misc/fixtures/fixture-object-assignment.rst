.. _fixture-object-assignment:

Fixture Object Assignment
=========================

The below table describes each object and who can gain access to that object.

+--------------------+----+----------+---------+
| Object             | ID | Group(s) | User(s) |
+====================+====+==========+=========+
| Organisation       | 1  | __all__  | __all__ |
+--------------------+----+----------+---------+
| Customer           | 1  | __all__  | __all__ |
+--------------------+----+----------+---------+
| Kanban Board       | 1  | Admin    | Admin   |
+--------------------+----+----------+---------+
| Kanban Board       | 2  | QA Team  | __all__ |
+--------------------+----+----------+---------+
| Project            | 1  | Admin    | Admin   |
+--------------------+----+----------+---------+
| Project            | 2  | QA Team  | __all__ |
+--------------------+----+----------+---------+
| Requirement        | 1  | Admin    | Admin   |
+--------------------+----+----------+---------+
| Requirement        | 2  | QA Team  | __all__ |
+--------------------+----+----------+---------+
| Task               | 1  | Admin    | Admin   |
+--------------------+----+----------+---------+
| Task               | 2  | QA Team  | __all__ |
+--------------------+----+----------+---------+
| Request for Change | 1  | Admin    | Admin   |
+--------------------+----+----------+---------+
| Request for Change | 2  | QA Team  | __all__ |
+--------------------+----+----------+---------+

.. note::

    The `__all__` defines that every single user will have access.


.. note::

    In the near future - __all__ will need to be change to each individual user. Because there will be some users that have no access

The below table defines the SUB objects, and what object they are connected to above. These objects will inherit the permissions above.

+--------+----+---------------+-----------+
| Object | ID | Parent Object | Parent ID |
+========+====+===============+===========+
| Card   | 1  | Kanban Board  | 1         |
+--------+----+---------------+-----------+
| Card   | 2  | Kanban Board  | 2         |
+--------+----+---------------+-----------+
| R Item | 1  | Requirement   | 1         |
+--------+----+---------------+-----------+
| R Item | 2  | Requirement   | 2         |
+--------+----+---------------+-----------+
