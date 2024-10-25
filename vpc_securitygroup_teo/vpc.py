import json
import time
from typing import List

from tencentcloud.common import credential
from tencentcloud.common.exception import TencentCloudSDKException
from tencentcloud.vpc.v20170312 import models, vpc_client

from vpc_securitygroup_teo.config import Config


class VPC:
    """
    VPC Client
    """

    def __init__(self):
        self.client = vpc_client.VpcClient(
            credential=credential.Credential(Config.secret_id, Config.secret_key),
            region=Config.security_group_region,
            profile=None,
        )

    def list_all_address_templates(self) -> List[str]:
        """
        拉取所有IP模板
        """
        templates = []
        finished = False
        offset = 0
        limit = 5
        while not finished:
            # 调用API
            try:
                request = models.DescribeAddressTemplatesRequest()
                request.from_json_string(
                    json.dumps({"NeedMemberInfo": False, "Limit": str(limit), "Offset": str(offset)})
                )
                response = self.client.DescribeAddressTemplates(request)
                print(
                    "Load Address Template Partial Success: "
                    f"{len(templates) + len(response.AddressTemplateSet)}/{response.TotalCount}"
                )
            except TencentCloudSDKException as err:
                print(f"Load Address Template Failed => {err}")
                raise err
            time.sleep(1.0 / Config.vpc_api_qps)
            # 解析数据
            if not response.AddressTemplateSet:
                break
            templates.extend(
                [
                    template.AddressTemplateId
                    for template in response.AddressTemplateSet
                    if template.AddressTemplateName.startswith(Config.tmpl_name_prefix)
                ]
            )
            offset += limit
        print(f"Load Address Template Success: {len(templates)}")
        return templates

    def create_address_template(self, date: str, index: int, ips: List[str]) -> str:
        """
        创建IP模板
        """
        try:
            request = models.CreateAddressTemplateRequest()
            params = {
                "AddressTemplateName": Config.tmpl_name_format.format(
                    prefix=Config.tmpl_name_prefix, date=date, index=index
                ),
                "Addresses": ips,
            }
            request.from_json_string(json.dumps(params))
            response = self.client.CreateAddressTemplate(request)
            print(f"Create Address Template Success => {response.AddressTemplate.AddressTemplateId}")
            return response.AddressTemplate.AddressTemplateId
        except TencentCloudSDKException as err:
            print(f"Create Address Template Failed => {err}")
            raise err

    def delete_address_template(self, address_template_id: str) -> None:
        """
        删除IP地址模板
        """
        try:
            request = models.DeleteAddressTemplateRequest()
            request.from_json_string(json.dumps({"AddressTemplateId": address_template_id}))
            self.client.DeleteAddressTemplate(request)
            print(f"Delete Address Template Success => {address_template_id}")
        except TencentCloudSDKException as err:
            print(f"Delete Address Template Failed => {err}")
            raise err

    def create_security_group_policy(self, address_tmpl_ids: List[str]) -> None:
        """
        创建安全组规则
        """
        try:
            request = models.CreateSecurityGroupPoliciesRequest()
            params = {
                "SecurityGroupId": Config.security_group_id,
                "SecurityGroupPolicySet": {
                    "Ingress": [
                        {
                            "Action": "ACCEPT",
                            "Port": "80,443",
                            "Protocol": "TCP",
                            "AddressTemplate": {"AddressId": tmpl_id},
                        }
                        for tmpl_id in address_tmpl_ids
                    ],
                    "Egress": [],
                },
            }
            request.from_json_string(json.dumps(params))
            self.client.CreateSecurityGroupPolicies(request)
            print("Create SG Policy Success")
        except TencentCloudSDKException as err:
            print(f"Create SG Policy Failed => {err}")
            raise err
