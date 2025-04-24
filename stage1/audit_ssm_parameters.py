import boto3
import json

region = "us-west-2"
prefix = "/chx/org/datalake/i8883/"

ssm = boto3.client("ssm", region_name=region)

def list_all_parameters():
    params = []
    next_token = None
    while True:
        response = ssm.describe_parameters(
            ParameterFilters=[{"Key": "Name", "Option": "BeginsWith", "Values": [prefix]}],
            MaxResults=50,
            NextToken=next_token
        ) if next_token else ssm.describe_parameters(
            ParameterFilters=[{"Key": "Name", "Option": "BeginsWith", "Values": [prefix]}],
            MaxResults=50
        )
        params.extend(response["Parameters"])
        next_token = response.get("NextToken")
        if not next_token:
            break
    return params

if __name__ == "__main__":
    all_params = list_all_parameters()
    print(json.dumps(all_params, indent=2))
