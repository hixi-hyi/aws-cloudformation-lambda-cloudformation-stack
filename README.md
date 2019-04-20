# cfn-lambda-cloudformation-stack
## Description
The `cfn-lambda-cloudformation-stack` function is `AWS::CloudFormation::Stack` that support `Region`

## When do you use it
* Use region locked resources like `AWS::CertificateManager::Certificate` to use in another region. e.g. We want to use `AWS::CloudFront::Distribution` (the resource is created in us-east-1 and can be defined in another region) but `AWS::CertificateManager::Certificate` can not be defined in another region)

## Caution
* It'is not normally cloudformation's flow. We cannot look like the nested resource.
* The function calls for strong permission to create all of aws resource, but you probably don't have to worry. Because the function can delete only resource defined by itself.
* The function cannot delect changes in child stack. You have to define parameter that are alway change and pass them to the function. (like `--parameter-overrides Date=$(date)`)
* You can not operate the stack for more than 15 minites due to lambda limitation.

## Deploy
[See here](https://github.com/hixi-hyi/aws-cloudformation-lambda#deploy)

## Usage
```
Parameters:
  Date:
    Type: String
Resources:
  Stack:
    Type: Custom::Lambda
    Properties:
      ServiceToken: !ImportValue cfn-lambda-cloudformation-stack:LambdaArn
      TemplateURL: https://{s3resource}/demo.yaml
      Parameters:
        Name: "test"
        Value: 1
      Capabilities:
        - CAPABILITY_IAM
      Region: us-east-1
      DeployAlways: !Ref Date
```

## Parameters
### TemplateURL
- [Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-templateurl)
- ***Required:*** Yes
- ***Update requires:*** Replacement
### Parameters
- [Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-parameters)
- ***Default:*** `{}`
- ***Required:*** No
- ***Update requires:*** Replacement
### Capabilities
- [Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities)
- 
- ***Default:*** `[]`
- ***Required:*** No
- ***Update requires:*** Replacement
### Region
- [Docs](https://docs.aws.amazon.com/general/latest/gr/rande.html)
- The region outside the default are also supported.
- ***Default:*** `!Ref AWS::Region`
- ***Required:*** No
- ***Update requires:*** Replacement

## Return Values
### !Ref
- Returns: the Stack ID.
### !GetAtt Outputs.*NestedStackOutputName*
- Returns: The output value from the specified nested stack where NestedStackOutputName is the name of the output value.

## Contributing
[See here](https://github.com/hixi-hyi/aws-cloudformation-lambda#contributing)
