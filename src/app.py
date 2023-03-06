import boto3

ec2_client = boto3.client('ec2')
rds_client = boto3.client('rds')

regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

def handler(event, context):
  for region in regions:
    ec2_client = boto3.client('ec2', region)
    all_instances = ec2_client.describe_instances()
    if all_instances:
      print("List all instances:")
      for reservation in all_instances['Reservations']:
        for instance in reservation['Instances']:
          print(instance['InstanceId'] + "-" + instance['State']['Name'])
          if instance['State']['Name'] == 'running':
            print("Stopping ec2: " + instance['InstanceId'])
            ec2_client.stop_instances(InstanceIds=[instance['InstanceId']])

    rds_client = boto3.client('rds', region)

    all_rds = rds_client.describe_db_instances(Filters=[{
      'Name': 'engine',
      'Values': ['mysql','postgres','mariadb','oracle-ee','oracle-ee-cdb','oracle-se2','oracle-se2-cdb','sqlserver-ee','sqlserver-se','sqlserver-ex','sqlserver-web']
    }])

    if all_rds:
      print("List all RDS:")
      for db in all_rds['DBInstances']:
        print(db['DBInstanceIdentifier'] + "-" + db['DBInstanceStatus'])
        if db['DBInstanceStatus'] == 'available':
          print("Stopping RDS : " + db['DBInstanceIdentifier'])
          rds_client.stop_db_instance(DBInstanceIdentifier=db['DBInstanceIdentifier'])

    rds_cluster = rds_client.describe_db_clusters()

    if rds_cluster:
      print("List all RDS Cluster:")
      for cluster in rds_cluster['DBClusters']:
        print(cluster['DBClusterIdentifier'] + "-" + cluster['Status'])
        if cluster['Status'] == 'available':
          print("Stopping RDS cluster : " + cluster['DBClusterIdentifier'])
          rds_client.stop_db_cluster(DBClusterIdentifier=cluster['DBClusterIdentifier'])