import boto3
import time

EC2_INSTANCES = {
    "Ubuntu-20" : "i-04b95ec15429c7be8",
}

ec2_client = boto3.client('ec2')
ec2_res = boto3.resource('ec2')

instances = []
instances.append(EC2_INSTANCES["Ubuntu-20"])

try:
    response = ec2_client.start_instances(InstanceIds=instances, DryRun=False)
    print(response, "\n")
except ClientError as e:
    print(e)

try:
    while True:
        print("Active EC2 Instances: ")
        for instance in ec2_res.instances.all():
            if instance.state['Name'] != 'stopped':
                print(
                    "Id: {0}\nPlatform: {1}\nType: {2}\nPublic IPv4: {3}\nAMI: {4}\nState: {5}\n".format(
                    instance.id, instance.platform, instance.instance_type, instance.public_ip_address, instance.image.id, instance.state
                    )
                )
        time.sleep(5)
except KeyboardInterrupt:
    try:
        response = ec2_client.stop_instances(InstanceIds=instances, DryRun=False)
        print(response)
    except ClientError as e:
        print(e)