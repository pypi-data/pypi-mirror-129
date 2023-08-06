from abc import abstractmethod
from typing import List, Tuple

from common.api.dtos.policy_dto import PolicyDTO
from common.api.dtos.rule_result_dto import IssueItemDTO, RuleResultDTO
from common.api.dtos.assessment_job_dto import IacAssessmentJobDTO, UnknownBlockDTO, InvalidationInfoDTO


class BaseFormatter:
    def __init__(self):
        self._error_rule_name_style = ''
        self._warning_rule_name_style = ''
        self._rule_description_style = ''
        self._resource_style = ''
        self._resource_type_style = ''
        self._evidence_style = ''
        self._reset_style = ''
        self._pseudo_style = ''
        self._checkov_style = ''
        self._no_policy_style = ''
        self._unknown_block_style = ''
        self._invalidation_info_style = ''

    @abstractmethod
    def format(self,
               rule_results: List[RuleResultDTO],
               run_exec: IacAssessmentJobDTO,
               policies: List[PolicyDTO]) -> Tuple[str, str]:
        pass

    def _format_issue_item(self, item: IssueItemDTO) -> List[str]:
        message = []
        exposed_iac_reference = "(Not found in TF)"
        violated_iac_reference = "(Not found in TF)"
        if item.exposed_entity.iac_resource_metadata is not None and item.exposed_entity.iac_resource_metadata.file_name is not None:
            exposed_iac_reference = '(' + item.exposed_entity.iac_resource_metadata.file_name + \
                                    ":" + str(item.exposed_entity.iac_resource_metadata.start_line) + ')'
        if item.violating_entity.iac_resource_metadata is not None and item.violating_entity.iac_resource_metadata.file_name is not None:
            violated_iac_reference = '(' + item.violating_entity.iac_resource_metadata.file_name + \
                                     ":" + str(item.violating_entity.iac_resource_metadata.start_line) + ')'
        message.append(f'   - Exposed Resource: {self._resource_style}[{item.exposed_entity.get_friendly_name()}]'
                       f' {self._resource_type_style}{exposed_iac_reference}')
        message.append(f'     Violating Resource: {self._resource_style}[{item.violating_entity.get_friendly_name()}] '
                       f' {self._resource_type_style}{violated_iac_reference}')
        message.append('')
        message.append('     Evidence:')
        message.append(self._format_evidence(item.evidence))
        return message

    def _format_evidence(self, evidence: str) -> str:
        message = []

        for evidence_line in evidence.split('. '):
            evidence_line = self._replace_backticks(evidence_line)
            if evidence_line.startswith('~') and evidence_line.endswith('~'):
                evidence_line = evidence_line.replace('~', '')
                message.append(f'         {evidence_line}')
            else:
                message.append(f'             | {evidence_line}')

        message.append('')
        return '\n'.join(message)

    def _replace_backticks(self, text: str) -> str:
        while '`' in text:
            text = text.replace('`', self._evidence_style, 1)
            text = text.replace('`', self._reset_style, 1)
        return text

    @staticmethod
    def _issue_item_contains_pseudo_entity(issue_item: IssueItemDTO):
        return issue_item.exposed_entity.is_pseudo or issue_item.violating_entity.is_pseudo

    @property
    def _pseudo_message(self):
        return [self._pseudo_style,
                'Cloudrail has listed "pseudo" objects in the above results.',
                'These are resources that don\'t exist yet, or don\'t show in the Terraform input, '
                'but we know will be created in the real live environment.']

    @property
    def _no_policy_message(self):
        return [self._no_policy_style,
                'Cloudrail ran this assessment without any policies and so all rule violations show as warnings.',
                'You can increase a rule\'s enforcement level by creating a Policy in the Web UI and adding the rule to it.']

    def _get_unknown_block_message(self, unknown_blocks: List[UnknownBlockDTO]):
        message = []

        if unknown_blocks:
            message.extend([self._unknown_block_style,
                            'Some of the data sources blocks you’ve used could not be evaluated during plan time.',
                            'As a result, the contents in these blocks were not included in Cloudrail’s analysis:'])
            for block in unknown_blocks:
                message.append(self._unknown_block_style + '  * {}'.format(block.block_address))

        return message

    def _get_invalidation_message(self, invalidation_info: List[InvalidationInfoDTO], verbose: bool):
        message = []

        if invalidation_info:
            base_msg = f"{self._invalidation_info_style}{len(invalidation_info)} of the resources in your code reference resources that are not " \
                       f"visible to Cloudrail at this time, and as a result, these resources could not be fully analyzed. " \
                       f"This means some rules could not operate on these resources. To solve this, please add the cloud account this " \
                       f"code is targeting and re-run without the '--no-cloud-account' flag"
            if verbose:
                message.append(f"{base_msg}:")
                for invalidation_info_item in invalidation_info:
                    message.append(f'* Resource {invalidation_info_item.invalidated_resource_id} '
                                   f'cannot be analyzed because: {invalidation_info_item.invalidation_reason}')
            else:
                message.append(f"{base_msg}. To see a full list of resources, re-run Cloudrail with '-v'.")

            message.append(self._reset_style)

        return message
