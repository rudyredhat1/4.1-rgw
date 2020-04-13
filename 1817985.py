#!/usr/bin/python3

import os, sys, random, time
print('enable the epel repo or by default it may be installed')
enable_epel = os.system('yum-config-manager --enable epel')
print(enable_epel)
print("----------------------------------------------------------------------")
install_python2_pip = os.system('yum install python3-pip -y')
print(install_python2_pip)
print("----------------------------------------------------------------------")
upgrade_pip = os.system('pip3 install --upgrade pip')
print(upgrade_pip)
print("----------------------------------------------------------------------")
install_s3cmd = os.system('pip3 install s3cmd')
print(install_s3cmd)
print("----------------------------------------------------------------------")
access_key='12345'
secret_key='67890'
create_user = os.system("radosgw-admin user create --uid=\"operator\" --display-name=\"S3 Operator\" --email=\"operator@example.com\" --access_key={} --secret={}".format(access_key, secret_key))
print(create_user)
print("----------------------------------------------------------------------")
print('It will remove the default /root/.s3cfg file')
s3cmd_configure = os.system('s3cmd --configure --dump-config > /root/.s3cfg')
print(s3cmd_configure)
print("----------------------------------------------------------------------")
print('Make some changes to .s3cfg file')
hostname = os.uname()[1]
port_number='8080'
os.system('sed -i -e \'s,^host_base *=.*,host_base = http://{}:{},;s,host_bucket *=.*,host_bucket = http://{}:{},;s,website_endpoint *=.*,website_endpoint = http://%(bucket)s.{}-%(location)s,;s,access_key *=.*,access_key = {},;s,secret_key *=.*,secret_key = {},;s,use_https *=.*,use_https = False,;s,gpg_command *=.*,gpg_command = /usr/bin/gpg,;s,progress_meter *=.*,progress_meter = True,;s,proxy_port *=.*,proxy_port = 0,\' /root/.s3cfg'.format(hostname, port_number, hostname, port_number, hostname, access_key, secret_key))
s3cmd_work = os.system('s3cmd ls')
exit_status = os.system('echo $?')
if exit_status == 0:
        print(port_number)
else:
        os.system('sed -i -e \'s,^host_base *=.*,host_base = http://{}:80,;s,host_bucket *=.*,host_bucket = http://{}:80,;s,website_endpoint *=.*,website_endpoint = http://%(bucket)s.{}-%(location)s,;s,access_key *=.*,access_key = {},;s,secret_key *=.*,secret_key = {},;s,use_https *=.*,use_https = False,;s,gpg_command *=.*,gpg_command = /usr/bin/gpg,;s,progress_meter *=.*,progress_meter = True,;s,proxy_port *=.*,proxy_port = 0,\' /root/.s3cfg'.format(hostname, hostname, hostname, access_key, secret_key))
s3cmd_work = os.system('s3cmd ls')
print(s3cmd_work)
print("----------------------------------------------------------------------")
print('Create a bucket named kvm')
bkt_name = 'kvm'
bkt_create = os.system('s3cmd mb s3://{}'.format(bkt_name))
print(s3cmd_work)
print('Bucket created with name as {}'.format(bkt_name))
print("----------------------------------------------------------------------")
print('Create a file osd.png of 100 MB')
file_name = 'osd.png'
file_create = os.system('head -c 100MB /dev/zero > {}'.format(file_name))
file_created = os.system('ls -l  {}'.format(file_name))
print(file_created)
print("----------------------------------------------------------------------")
print('Upload osd.png in the created bucket')
os.system('s3cmd put {} s3://{}/{}'.format(file_name, bkt_name, file_name))
print("----------------------------------------------------------------------")
print('Install aws cli to enable bucket versioning')
install_awscli = os.system('pip3 install awscli')
print(install_awscli)
print("----------------------------------------------------------------------")
print('Configure awscli')
os.system('rm -rf /root/.aws; mkdir /root/.aws; cd /root/.aws; touch config credentials')
os.system('echo -e \'[default] \n region = US \n ouput = text\' > /root/.aws/config')
os.system('echo -e \'[default] \n aws_access_key_id = {} \n aws_secret_access_key = {}\' > /root/.aws/credentials'.format(access_key, secret_key))
os.system('cd')
os.system('aws s3 ls --profile default --endpoint http://{}:8080'.format(hostname))
print('aws cli is configured properly with port number 8080')
print("----------------------------------------------------------------------")
print('Enable versioning on kvm bucket')
os.system('aws --endpoint=http://{}:8080 s3api get-bucket-versioning --bucket {}'.format(hostname, bkt_name))
#print('Status is showing 0 means it is disabled')
os.system('aws --endpoint=http://{}:8080 s3api put-bucket-versioning --bucket {} --versioning-configuration Status=Enabled'.format(hostname, bkt_name))
os.system('aws --endpoint=http://{}:8080 s3api get-bucket-versioning --bucket {}'.format(hostname, bkt_name))
print('You can see the versioning is enabled with a enabled status')
print("----------------------------------------------------------------------")
print('Create a file download.txt of 10 MB')
file_name_1 = 'download.txt'
file_create_1 = os.system('head -c 10MB /dev/zero > {}'.format(file_name_1))
file_created_1 = os.system('ls -l  {}'.format(file_name_1))
print(file_created_1)
print("----------------------------------------------------------------------")
print('Upload download.txt in the created bucket')
os.system('s3cmd put {} s3://{}/{}'.format(file_name_1, bkt_name, file_name_1))
print("----------------------------------------------------------------------")
print('List objects versions from the bucket')
os.system('aws --endpoint=http://{}:8080 s3api list-object-versions  --bucket {}'.format(hostname, bkt_name))
print("----------------------------------------------------------------------")
print('List objects inside the bucket')
os.system('radosgw-admin bucket list --bucket {}'.format(bkt_name))
print("----------------------------------------------------------------------")
print('Edit the downlod.txt file and upload same file using s3cmd')
os.system('echo \'hello {}\' >> {}'.format(hostname, file_name_1))
os.system('s3cmd put {} s3://{}/{}'.format(file_name_1, bkt_name, file_name_1))
print("----------------------------------------------------------------------")
print('Check again the object versions and  list of objects')
print('List objects versions from the bucket')
os.system('aws --endpoint=http://{}:8080 s3api list-object-versions  --bucket {}'.format(hostname, bkt_name))
print("----------------------------------------------------------------------")
print('List objects inside the bucket')
os.system('radosgw-admin bucket list --bucket {}'.format(bkt_name))
print("----------------------------------------------------------------------")
print('List the files inside the bucket using s3cmd and remove the download.txt')
os.system('s3cmd ls s3://{}'.format(bkt_name))
os.system('s3cmd rm s3://{}/{}'.format(bkt_name, file_name_1))
os.system('s3cmd ls s3://{}'.format(bkt_name))
print("----------------------------------------------------------------------")
print('Restart the rgw service and check the logs')
os.system('systemctl restart ceph-radosgw@rgw.{}.rgw0.service'.format(hostname))
os.system('tail -30 /var/log/ceph/ceph-rgw-{}.rgw0.log'.format(hostname))
time.sleep(5)
print("----------------------------------------------------------------------")
os.system('s3cmd ls s3://{}'.format(bkt_name))
print("----------------------------------------------------------------------")
os.system('tail -30 /var/log/ceph/ceph-rgw-{}.rgw0.log'.format(hostname))
print("------------------------RGW IO OPERATION DONE---------------------------------")
