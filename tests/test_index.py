from unittest import TestCase
from moto import mock_cloudformation, mock_s3
from src.index import Stack
import cfntest
import boto3
import os

class TestConstructor(TestCase):
  @mock_cloudformation
  @mock_s3
  def test_initialize(self):
    setup()
    context = cfntest.get_context()
    event = cfntest.get_create_event({
      "Parameters": {
        "Name": "test",
        "Value": "1",
      },
      "TemplateURL": "https://hixi.s3.amazonaws.com/resource.yaml",
      "Region": "us-east-1",
    })
    c = Stack(event, context)
    print(c.stack_name)
    self.assertEqual(len(c.unique_key), 12)
    self.assertEqual(c.id, "us-east-1:https://hixi.s3.amazonaws.com/resource.yaml")
    self.assertDictEqual(c._parameters, {"Name":"test", "Value":"1"})
    self.assertCountEqual(c.parameters, [
      {
        "ParameterKey": "Name",
        "ParameterValue": "test",
      },
      {
        "ParameterKey": "Value",
        "ParameterValue": "1",
      },
    ])

def setup():
  s3 = boto3.client('s3')
  s3.create_bucket(Bucket='hixi')
  s3.upload_file(os.path.dirname(__file__)+'/resource.yaml', 'hixi', 'resource.yaml')

def descibe_stack(stack_name):
  return self._cfn.describe_stacks(StackName=stack_name)

class TestScenario(TestCase):
  @mock_cloudformation
  @mock_s3
  def test_default(self):
    setup()
    create_physical_resource_id = ''
    if True:
      event = cfntest.get_create_event({
        "Parameters": {
          "Name": "test",
          "Value": "1",
        },
        "TemplateURL": "https://hixi.s3.amazonaws.com/resource.yaml",
        "Region": "us-east-1",
      })
      c = Stack(event, cfntest.get_context())
      c.run()
      create_physical_resource_id = c.response.physical_resource_id
      self.assertEqual(c.response.get_data('Outputs.OutputName'), 'test')
      self.assertEqual(c.response.get_data('Outputs.OutputValue'), '1')

    update_phycical_resource_id = ''
    if True:
      event = cfntest.get_update_event({
        "ParentStackName": "Parent",
        "ParentStackRegion": "ap-northeast-1",
        "Parameters": {
          "Name": "test2",
          "Value": "1",
        },
        "TemplateURL": "https://hixi.s3.amazonaws.com/resource.yaml",
        "Region": "us-east-1",
      })
      c = Stack(event, cfntest.get_context())
      c.run()
      update_physical_resource_id = c.response.physical_resource_id
      create_physical_resource_id = c.response.physical_resource_id
      self.assertEqual(c.response.get_data('Outputs.OutputName'), 'test2')
      self.assertEqual(c.response.get_data('Outputs.OutputValue'), '1')

    self.assertEqual(create_physical_resource_id, update_physical_resource_id)

    if True:
      event = cfntest.get_delete_event({
        "ParentStackName": "Parent",
        "ParentStackRegion": "ap-northeast-1",
        "Parameters": {
          "Name": "test2",
          "Value": "1",
        },
        "TemplateURL": "https://hixi.s3.amazonaws.com/resource.yaml",
        "Region": "us-east-1",
      })
      c = Stack(event, cfntest.get_context())
      c.run()
