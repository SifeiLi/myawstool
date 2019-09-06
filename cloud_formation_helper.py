import boto3
import re


CLOUD_FORMATION = 'cloudformation'
STACK_NAME = 'StackName'
CLOUD_FORMATION_STACK_STATUS = [
    'CREATE_COMPLETE',
    'CREATE_FAILED',
    'CREATE_IN_PROGRESS',
    'DELETE_COMPLETE',
    'DELETE_FAILED',
    'DELETE_IN_PROGRESS',
    'REVIEW_IN_PROGRESS',
    'ROLLBACK_COMPLETE',
    'ROLLBACK_FAILED',
    'ROLLBACK_IN_PROGRESS',
    'UPDATE_COMPLETE',
    'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS',
    'UPDATE_IN_PROGRESS',
    'UPDATE_ROLLBACK_COMPLETE',
    'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS',
    'UPDATE_ROLLBACK_FAILED',
    'UPDATE_ROLLBACK_IN_PROGRESS'
]


class CloudFormationHelper:
    def __init__(self, region, aws_access_key_id, aws_secret_access_key, aws_session_token):
        self.client = boto3.client(CLOUD_FORMATION, region_name=region, aws_access_key_id=aws_access_key_id,
                                   aws_session_token=aws_session_token, aws_secret_access_key=aws_secret_access_key)

    def list_stacks(self, stack_name_regex, stack_status, starting_token):
        """
        List stacks with given status filter and stack name regex pattern. Return list of stack summaries.
        :param stack_name_regex: str
        :param stack_status: str
        :param starting_token: str, A token to specify where to start paginating.
        :return: A list of stack summaries
        """
        list_stacks_args = {}
        if stack_status is not None:
            if stack_status not in CLOUD_FORMATION_STACK_STATUS:
                raise Exception("Stack Status {} is invalid. Allowed stack status: {}."
                                .format(stack_status, CLOUD_FORMATION_STACK_STATUS))
            print("Stack status to use as a filter: {}.".format(stack_status))
            list_stacks_args['StackStatusFilter'] = [stack_status]

        output_stack_summaries = []
        next_token = starting_token

        if next_token is None:
            list_stacks_output = self.client.list_stacks(**list_stacks_args)
            stack_summaries = list_stacks_output.get('StackSummaries')
            next_token = list_stacks_output.get(
                'NextToken')  # This is the NextToken from a previously truncated response.

            if stack_name_regex is not None:
                print("Stack name regex pattern to use as a filter: {}.".format(stack_name_regex))
                pattern = re.compile(stack_name_regex)
                for stack_summary in stack_summaries:
                    if pattern.match(stack_summary[STACK_NAME]):
                        output_stack_summaries.append(stack_summary)
            else:
                output_stack_summaries = stack_summaries

        while next_token is not None:
            list_stacks_args['NextToken'] = next_token
            list_stacks_output = self.client.list_stacks(**list_stacks_args)
            stack_summaries = list_stacks_output.get('StackSummaries')
            next_token = list_stacks_output.get('NextToken')

            if stack_name_regex is not None:
                pattern = re.compile(stack_name_regex)
                for stack_summary in stack_summaries:
                    if pattern.match(stack_summary[STACK_NAME]):
                        output_stack_summaries.append(stack_summary)

            else:
                output_stack_summaries += stack_summaries

        return output_stack_summaries

    def __delete_stacks(self, stacks):
        """
        Delete stacks.
        :param stacks: List of stack_summaries
        :return: None
        """
        delete_stack_args = {}
        for stack in stacks:
            delete_stack_args[STACK_NAME] = stack[STACK_NAME]
            print("Deleting stack {}...".format(stack[STACK_NAME]))
            self.client.delete_stack(**delete_stack_args)

    def delete_specified_stacks(self, stack_name_regex, stack_status):
        """
        Delete stacks with given status filter and stack name regex pattern.
        :param stack_name_regex: str
        :param stack_status: str
        :return: None
        """
        self.__delete_stacks(self.list_stacks(stack_name_regex, stack_status, None))
