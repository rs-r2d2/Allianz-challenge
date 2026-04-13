from typing import Dict, List
from datetime import date
from app.common.helper_function import logger_depp, session_depp
from .provider_base import ProviderBase

class AWSProvider(ProviderBase):

    def __init__(self, *, logger: logger_depp, boto3: session_depp):
        self._logger = logger
        self.boto3 = boto3
        self.ce_client = self.boto3.client('ce')

    def get_ec2_cost(self, *, start_date: date, end_date: date, service: List[str]):
        """
        :param start_date:
        :param end_date:
        :param service:
        https://docs.aws.amazon.com/boto3/latest/reference/services/ce/client/get_cost_and_usage.html
        :return:
        """
        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%d-%m'),
                'End': end_date.strftime('%Y-%d-%m')
            },
            Granularity='DAILY',
            Filter={
                'Dimensions': {
                    'Key': 'SERVICE',
                    'Values': service
                }
            }
        )
        total = 0
        for day in response['ResultsByTime']:
            cost = float(day['Total']['UnblendedCost']['Amount'])
            print(f"{day['TimePeriod']['Start']} → ${cost:.2f}")
            total += cost
        return total

    def get_compute_cost(self, start_date: date, end_date: date):
        total_cost = self.get_ec2_cost(start_date=start_date, end_date=end_date, service=['Amazon Elastic Compute Cloud - Compute'])
        return total_cost


    def get_storage_list(self) -> List[Dict[str, str]] | None:
        try:
            s3 = self.boto3.client("s3")
            buckets = s3.list_buckets()["Buckets"]
            results = []
            for bucket in buckets:
                name = bucket["Name"]
                results.append({
                    "bucket_name": name,
                    "creation_date": bucket["CreationDate"].isoformat()
                })
            return results
        except Exception as e:
            self._logger.info('Error getting s3 list')
            raise e

    def get_storage_cost(self, start_date: date, end_date: date):
        total_cost = self.get_ec2_cost(start_date=start_date, end_date=end_date, service=['Amazon Simple Storage Service'])
        return total_cost

    def get_compute_list(self) -> List[Dict[str, str]] | None:
        """
        https://docs.aws.amazon.com/boto3/latest/reference/services/ec2/client/describe_regions.html
        https://docs.aws.amazon.com/boto3/latest/reference/services/ec2/client/describe_instances.html
        :return:
        """
        try:
            ec2_client = self.boto3.client('ec2', region_name=os.environ['region'])
            regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
            for region in regions:
                ec2 = self.boto3.resource('ec2', region_name=region)
                instances_data = []
                response = ec2.describe_instances()
                for reservation in response["Reservations"]:
                    for instance in reservation["Instances"]:
                        instances_data.append({
                            "instance_id": instance["InstanceId"],
                            "instance_type": instance["InstanceType"],
                            "state": instance["State"]["Name"],
                            "launch_time": instance["LaunchTime"].isoformat()
                        })
                return instances_data
            return None
        except Exception as e:
            self._logger.info('Error getting s3 list')
            raise e
