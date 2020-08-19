#!/usr/bin/env python

import boto3
import paramiko
import sys
import time
import threading

ec2_client = boto3.client('ec2')
d = int(input("Enter d: "))
print (d)
N = input("Enter N:")
print (N)
#d = int(sys.argv[2])
input_number = min(int(N), 20)

response_123 = ec2_client.describe_instances()
#print(response_123)

ImageId = ""
InstanceType =""
group_id = ""
KeyName =""

for r in response_123["Reservations"]:
    for instance in r["Instances"]:

        if(instance["State"]["Name"] !="terminated"):
            group_id = instance["SecurityGroups"][0]["GroupId"]
            ImageId = instance["ImageId"]
            InstanceType = instance["InstanceType"]
            KeyName = instance["KeyName"]
            #instance_ids = list(map(lambda x: x['InstanceId'], instances))
def create_instances():
    response = ec2_client.run_instances(
        ImageId=ImageId,
        MinCount=input_number,
        MaxCount=input_number,
        InstanceType=InstanceType,
        KeyName=KeyName,
        SecurityGroupIds=[group_id],
    )
    instances = response['Instances']
    instance_ids = list(map(lambda x: x['InstanceId'], instances))
    return instance_ids
def list_instances():
    print('Listing EC2 instances...')
    for instance in ec2_client.instances.all():
        print(instance.id, instance.state)
        # print(ec2.meta.client.describe_instances(InstanceIds=[instance.id]))
def kill_all_instances(iids):
    ec2_client.terminate_instances(InstanceIds=iids)


def check_status(iid):
    time.sleep(10)
    while 1:
        time.sleep(10)
        response = ec2_client.describe_instances(InstanceIds=[iid])
        instance = response['Reservations'][0]['Instances'][0]
        if instance['State']['Name'] == 'running':
            time.sleep(30)
            return instance


def worker(worker_params):
    # input
    index, difficulty, max_instances, instance_id = worker_params
    instance = check_status(instance_id)
    print('Instance ready ', index)
    # ssh
    ssh = paramiko.SSHClient()
    key = paramiko.RSAKey.from_private_key_file('Cloud_Computing.pem')
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=instance['PublicIpAddress'], username='ubuntu', pkey=key)

    sftp = ssh.open_sftp()
    sftp.put('pow.py', 'pow.py')

    cmd = 'python3 pow.py -d ' + str(difficulty) + ' -i ' + str(index) + ' -n ' + str(max_instances)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    for line in lines:
        print(line)
    ssh.close()
    return


def main():
    print("Cloud Nonce Discovery - Start")
    start_time = time.time()
    instance_list = create_instances()

    worker_params = [(instance_list.index(iid), d, len(instance_list), iid) for iid in instance_list]


    # worker(worker_params[0])
    threads = []
    for i in range(input_number):
        t = threading.Thread(target=worker, args=(worker_params[i],))
        threads.append(t)
        t.setDaemon(True)
        t.start()

    flag = 1
    while flag == 1:
        time.sleep(1)
        for t in threads:
            if not t.isAlive():
                flag = 0

    kill_all_instances(instance_list)
    end_time = time.time()
    print('Total Time: ', end_time - start_time)
    print('Nonce Discovered Finished')
    exit()


if __name__ == '__main__':
    main()
