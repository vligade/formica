import sys

import click
from botocore.exceptions import ClientError, WaiterError
from texttable import Texttable

from formica import CHANGE_SET_FORMAT

CHANGE_SET_HEADER = ['Action', 'LogicalId', 'PhysicalId', 'Type', 'Replacement', 'Changed']


class ChangeSet:
    def __init__(self, stack, client):
        self.name = CHANGE_SET_FORMAT.format(stack=stack)
        self.stack = stack
        self.client = client

    def create(self, template, type):
        if type == 'UPDATE':
            self.remove_existing_changeset()
        self.client.create_change_set(StackName=self.stack, TemplateBody=template,
                                      ChangeSetName=self.name, ChangeSetType=type)
        click.echo('Change set submitted, waiting for CloudFormation to calculate changes ...')
        waiter = self.client.get_waiter('change_set_create_complete')
        try:
            waiter.wait(ChangeSetName=self.name, StackName=self.stack)
            click.echo('Change set created successfully')
        except WaiterError as e:
            click.echo(e.last_response['StatusReason'])
            sys.exit(1)

    def describe(self):
        change_set = self.client.describe_change_set(StackName=self.stack, ChangeSetName=self.name)
        table = Texttable(max_width=150)

        table.add_rows([CHANGE_SET_HEADER])

        def __change_detail(change):
            target_ = change['Target']
            attribute = target_['Attribute']
            if attribute == 'Properties':
                return target_['Name']
            else:
                return attribute

        for change in change_set['Changes']:
            resource_change = change['ResourceChange']
            table.add_row(
                [resource_change['Action'],
                 resource_change['LogicalResourceId'],
                 resource_change.get('PhysicalResourceId', ''),
                 resource_change['ResourceType'],
                 resource_change.get('Replacement', ''),
                 ', '.join([__change_detail(c) for c in resource_change['Details']])
                 ])

        click.echo("Changes to be deployed:\n" + table.draw() + "\n")

    def remove_existing_changeset(self):
        try:
            self.client.describe_change_set(StackName=self.stack,
                                            ChangeSetName=self.name)
            click.echo('Removing existing change set')
            self.client.delete_change_set(StackName=self.stack,
                                          ChangeSetName=self.name)
        except ClientError as e:
            if e.response['Error']['Code'] != 'ChangeSetNotFound':
                raise e
