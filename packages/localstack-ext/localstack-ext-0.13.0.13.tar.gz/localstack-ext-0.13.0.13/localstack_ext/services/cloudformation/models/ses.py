from localstack.services.cloudformation.deployment_utils import generate_default_name_without_stack
ndrHy=staticmethod
ndrHQ=None
ndrHv=all
ndrHG=super
ndrHC=str
ndrHX=classmethod
from localstack.services.cloudformation.service_models import GenericBaseModel
from localstack.utils.aws import aws_stack
class SESTemplate(GenericBaseModel):
 @ndrHy
 def cloudformation_type():
  return "AWS::SES::Template"
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("ses")
  template_name=self.props.get("Template",{}).get("TemplateName")
  tmpl_name=self.resolve_refs_recursively(stack_name,template_name,resources)
  templates=client.list_templates().get("TemplatesMetadata",[])
  template=[t for t in templates if t["Name"]==tmpl_name]
  return(template or[ndrHQ])[0]
 def get_physical_resource_id(self,attribute=ndrHQ,**kwargs):
  return self.props.get("Template",{}).get("TemplateName")
 def update_resource(self,new_resource,stack_name,resources):
  client=aws_stack.connect_to_service("ses")
  new_props=new_resource["Properties"]
  new_template=new_props.get("Template",{})
  template=client.get_template(TemplateName=new_template["TemplateName"])["Template"]
  if ndrHv(template.get(attr,"")==new_template.get(attr,"")for attr in["SubjectPart","TextPart","HtmlPart"]):
   return
  return client.update_template(**new_props)
 @ndrHy
 def get_deploy_templates():
  return{"create":{"function":"create_template"},"delete":{"function":"delete_template","parameters":{"TemplateName":"TemplateName"}}}
class SESReceiptRuleSet(GenericBaseModel):
 @ndrHy
 def cloudformation_type():
  return "AWS::SES::ReceiptRuleSet"
 def get_physical_resource_id(self,attribute=ndrHQ,**kwargs):
  return self.props.get("RuleSetName")
 def get_cfn_attribute(self,attribute):
  return ndrHG(SESReceiptRuleSet,self).get_cfn_attribute(attribute)
 @ndrHy
 def add_defaults(resource,stack_name:ndrHC):
  role=resource["Properties"]
  if not role.get("RuleSetName"):
   role["RuleSetName"]=generate_default_name_without_stack(resource["LogicalResourceId"])
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("ses")
  rule_set_name=self.props.get("RuleSetName")
  rule_set_name=self.resolve_refs_recursively(stack_name,rule_set_name,resources)
  rule_set=client.describe_receipt_rule_set(RuleSetName=rule_set_name)
  return rule_set or ndrHQ
 @ndrHX
 def fetch_details(cls,rule_set_name):
  client=aws_stack.connect_to_service("ses")
  rule=client.describe_receipt_rule_set(RuleSetName=rule_set_name)
  return rule or ndrHQ
 @ndrHy
 def get_deploy_templates():
  return{"create":{"function":"create_receipt_rule_set"},"delete":{"function":"delete_receipt_rule_set"}}
class SESReceiptRule(GenericBaseModel):
 @ndrHy
 def cloudformation_type():
  return "AWS::SES::ReceiptRule"
 def get_physical_resource_id(self,attribute=ndrHQ,**kwargs):
  return self.props.get("Rule",{}).get("Name")
 def get_cfn_attribute(self,attribute):
  return ndrHG(SESReceiptRule,self).get_cfn_attribute(attribute)
 @ndrHX
 def fetch_details(cls,rule_set_name,rule_name):
  client=aws_stack.connect_to_service("ses")
  rule=client.describe_receipt_rule(RuleSetName=rule_set_name,RuleName=rule_name).get("Rule")
  return rule or ndrHQ
 @ndrHy
 def add_defaults(resource,stack_name:ndrHC):
  rule=resource["Properties"]["Rule"]
  if not rule.get("Name"):
   rule["Name"]=generate_default_name_without_stack(resource["LogicalResourceId"])
 @ndrHy
 def get_deploy_templates():
  return{"create":{"function":"create_receipt_rule"},"delete":{"function":"delete_receipt_rule","parameters":{"RuleSetName":"RuleSetName","RuleName":lambda params,**kwargs:params["Rule"]["Name"]}}}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
