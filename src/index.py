from cfnprovider import CustomResourceProvider, get_logger
import boto3
import botocore
import os
import hashlib
import binascii
logger = get_logger(__name__)
env = os.environ

class Stack(CustomResourceProvider):
  def init(self):
    self._template_url = self.get('TemplateURL')
    self._parameters = self.get('Parameters', {})
    self._capabilities = self.get('Capabilities', [])
    self._region = self.get('Region', env.get('AWS_REGION'))
    self.parse_stack_id()

    self._cfn = boto3.client('cloudformation', region_name=self._region)

  def parse_stack_id(self):
    parts = self.stack_id.split(':')
    self._parent_stack_region = parts[3]
    self._parent_stack_name = parts[5].split('/')[1]

  @property
  def id(self):
    return "{}:{}".format(self._region, self._template_url)

  @property
  def stack_name(self):
    return "{}-{}-{}-{}".format(self._parent_stack_region, self._parent_stack_name, self.logical_resource_id, self.unique_key)

  @property
  def unique_key(self):
    return hashlib.md5(self.id.encode('utf-8')).hexdigest()[:12].upper()

  @property
  def parameters(self):
    params = []
    for k, v in self._parameters.items():
      params.append({
        "ParameterKey": k,
        "ParameterValue": v,
      })
    return params

  def set_response(self):
    res = self._cfn.describe_stacks(
      StackName=self.stack_name,
    )
    for v in res['Stacks'][0]['Outputs']:
      self.response.set_data("Outputs." + v['OutputKey'], v['OutputValue'])
    self.response.physical_resource_id = res['Stacks'][0]['StackId']

  def create(self, policies):
    res = self._cfn.create_stack(
      StackName=self.stack_name,
      TemplateURL=self._template_url,
      Parameters=self.parameters,
      Capabilities=self._capabilities,
    )
    self._cfn.get_waiter('stack_create_complete').wait(StackName=self.stack_name)
    self.set_response()

  def update(self, policies):
    try:
      res = self._cfn.update_stack(
        StackName=self.stack_name,
        TemplateURL=self._template_url,
        Parameters=self.parameters,
        Capabilities=self._capabilities,
      )
      self._cfn.get_waiter('stack_update_complete').wait(StackName=self.stack_name)
    except botocore.exceptions.ClientError as e:
      m = e.response['Error']['Message']
      if m == 'No updates are to be performed.':
        pass
      else:
        raise e
    self.set_response()

  def delete(self, policies):
    res = self._cfn.delete_stack(
      StackName=self.stack_name,
    )
    self._cfn.get_waiter('stack_delete_complete').wait(StackName=self.stack_name)

def handler(event, context):
  c = Stack(event, context)
  c.handle()
