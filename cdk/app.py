#!/usr/bin/env python3

from aws_cdk import core
from maintenance_app.maintenance_app_stack import MaintenanceAppStack
from Pipeline import Pipeline
from visit import Visit
from dns import MakerspaceDns
from database import Database
from accounts_config import accounts

namespace = 'unified-makerspace'
app = core.App()

"""
Section 1: Global resources that exist in only one account

The DNS records shared by all of the organization accounts exist in
the Prod account to discourage changing them. This is due to the
security concerns posed by using Route53 NS records. See the
below blog post for details:

https://nabeelxy.medium.com/dangling-dns-records-are-a-real-vulnerability-361f2a29d37f

Also, all Pipeline-related resources go here, because we don't deploy
those directly. Instead, we use the Pipline's self-mutation to update
all the child stacks. So, everything beta/prod goes here.
"""
maintenance_app = MaintenanceAppStack(
    app, f"{namespace}-maintenance-app")

# todo: add Database and Visit to Pipeline...
pipeline = Pipeline(app, f"{namespace}-pipeline", env=accounts['Prod'])
# pipeline.add_dependency(maintenance_app)

dns_stack = MakerspaceDns(app, 'MakerspaceDns', env=accounts['Dns'])


"""
Section 2: Resources that exist within the same account

This section is for the alpha or development environments. For
these, we need to deploy each by hand, and each user should have the
only credentials that deploy to their own dev account. This loop
generates a stack for each user that deploys to their own account.
"""
for user in ['mhall6', 'kejiax']:
    stage = f'Dev-{user}'
    database = Database(app, stage, env=accounts[stage])
    Visit(app, stage, database.table.table_name, env=accounts[stage])

app.synth()
