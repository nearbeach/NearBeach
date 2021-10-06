# Import files
from django_seed import Seed

# Import models
from NearBeach.models import *

# Setup the seeder
seeder = Seed.seeder()

#Setup users
seeder.add_entity(group,50)
seeder.add_entity(User,150)
seeder.add_entity(user_group,500)

#Setup basic lists
seeder.add_entity(list_of_amount_type, 5)
seeder.add_entity(list_of_bug_client, 5)
seeder.add_entity(list_of_contact_type, 5)
seeder.add_entity(list_of_country_region, 5)
seeder.add_entity(list_of_country, 5)
seeder.add_entity(list_of_currency, 5)
seeder.add_entity(list_of_lead_source, 5)
seeder.add_entity(list_of_opportunity_stage, 5)
seeder.add_entity(list_of_quote_stage, 5)
seeder.add_entity(list_of_requirement_item_status, 5)
seeder.add_entity(list_of_requirement_item_type, 5)
seeder.add_entity(list_of_requirement_status, 5)


#Setup customers
seeder.add_entity(organisation,1000)
seeder.add_entity(customer,5000)


#Setup objects
seeder.add_entity(requirement,1000)
seeder.add_entity(requirement_item,1000)
seeder.add_entity(project,1000)
seeder.add_entity(task,1000)

#Setup kanban
seeder.add_entity(kanban_board,100)
seeder.add_entity(kanban_column,500)
seeder.add_entity(kanban_level,500)
seeder.add_entity(kanban_card,10000)

#Connect objects and kanban
seeder.add_entity(object_assignment,10000)


# Execute query
inserted_pks = seeder.execute()












