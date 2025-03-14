import boto3
      import logging
      import json
      import time
      import os

      ssm = boto3.client('ssm')
      autoscaling = boto3.client('autoscaling')

      log = logging.getLogger()
      log.setLevel(logging.DEBUG)

      def handler(event, context):
          log.debug("Received event {}".format(json.dumps(event)))
          
          command = ssm.send_command(
              InstanceIds=[event['detail']['EC2InstanceId']],
              DocumentName=os.environ['SSM_DOCUMENT_NAME'],
              Comment='Gracefully terminate Cribl Stream worker node',
              Parameters={
                  "commands": ["systemctl disable cribl", "systemctl daemon-reload", "systemctl stop cribl"],
                  "workingDirectory": [""],
                  "executionTimeout": ["3600"]
              },
              CloudWatchOutputConfig={
                  'CloudWatchOutputEnabled': True
              }
          )

          command_id = command['Command']['CommandId']
          for x in range(60):
              time.sleep(10)
              response = ssm.get_command_invocation(
                  CommandId=command_id,
                  InstanceId=event['detail']['EC2InstanceId']
              )
              if response.get('Status') == 'Success':
                  break
              elif response.get('Status') in ['Failed', 'Cancelled', 'TimedOut']:
                  log.error(f"SSM command failed: {response.get('StatusDetails')}")
                  return

          autoscaling.complete_lifecycle_action(
              LifecycleHookName=event['detail']['LifecycleHookName'],
              AutoScalingGroupName=event['detail']['AutoScalingGroupName'],
              LifecycleActionToken=event['detail']['LifecycleActionToken'],
              LifecycleActionResult='CONTINUE',
              InstanceId=event['detail']['EC2InstanceId']
          )