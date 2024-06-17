.. _fixture_standards:

=================
Fixture Standards
=================

The following document is to outline the structure of the fixtures. 
So if we need to expand the fixtures, it can easily be matched 
with the unit tests.


---------------------------------
Objects Assiged to Administrators
---------------------------------

Any Objects with an ID of 1, will be assigned to just the
Administrators (admin group). No other use shall have access
to these objects.

This applies for the following objects

#. Kanban Board
#. Project
#. Request for Change
#. Requirement
#. Task

Tests should be used to determine other users do not have 
access

-------------------------------
Objects Assiged to Team Members
-------------------------------

Any Objects with an ID 2, will be assigned to Team Members 
group. Any user that is assigned to this team members group
will be able to access the object.

This applies to the following objects

#. Kanban Board
#. Project
#. Request for Change
#. Requirement
#. Task

Test should be used to determine;

#. Administrators can access the objects
#. Any user in the team members group can access the objects
#. Any user who is not assigned to the team members (excluding admin)
, can NOT access objects


------------------------------
Object Assigned to Empty Group
------------------------------

Any Objects with an ID of 3, will be assigned to an empty group
where there are no users assigned.

This applies to the following objects

#. Kanban Board
#. Project
#. Request for Change
#. Requirement
#. Task

Test should be used to determine;

#. Administrators can access the objects
#. Any user not in the empty group can NOT access the objects


----------
Misc Notes
----------

The following objects are excluded from the rules;

#. Cards
#. Notes
#. Requirement items
#. Any sub object