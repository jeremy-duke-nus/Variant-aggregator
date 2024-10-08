import boto3
import botocore
import json
import re
import time

# Reference: https://www.ilkkapeltola.fi/2018/04/simple-way-to-query-amazon-athena-in.html

DATABASE = 'clinvar_vcf'
TABLE = 'current'
OUTPUT = 's3://variant-aggregator-v2/queries/Unsaved/'


client = boto3.client('athena')

def lambda_handler(event, context):
    
    param = event["queryStringParameters"]
    chrom = param['chromosome']
    position = param['position']
    ref = param['reference']
    variant = param['variant']
    query = f"SELECT * FROM {DATABASE}.{TABLE} WHERE chrom = '{chrom}' AND position = '{position}' AND reference = '{ref}' AND alternate = '{variant}'"
  
    query_id =  client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': DATABASE
        },
        ResultConfiguration={
            'OutputLocation': OUTPUT,
        }
    )   
    execution_id = query_id['QueryExecutionId']
    
    STATE = 'RUNNING'

    MAX_EXEC = 10
    
    while (MAX_EXEC > 0 and STATE in ['RUNNING', 'QUEUED']):
        MAX_EXEC = MAX_EXEC - 1
        response = client.get_query_execution(QueryExecutionId = execution_id)
        if 'QueryExecution' in response and \
                'Status' in response['QueryExecution'] and \
                'State' in response['QueryExecution']['Status']:
            STATE = response['QueryExecution']['Status']['State']
            if STATE == 'FAILED':
                return False
            elif STATE == 'SUCCEEDED':
                s3_path = response['QueryExecution']['ResultConfiguration']['OutputLocation']
                results = client.get_query_results(
                    QueryExecutionId = execution_id
                    )

                row = results["ResultSet"]["Rows"]
                if len(row) == 1:
                    # empty result set since the first row is the header
                    return {
                            'statusCode': 200,
                            'headers': {
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                            },
                            'body': json.dumps(
                               {'found': False}
                               )
                            }
                else:
                    results = row[-1]
                    results = results['Data']
                    position, ref, variant, variant_id, clinsig, criteria, disease, ch =  [x["VarCharValue"] for x in results]
                    return {
                            'statusCode': 200,
                            'headers': {
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                            },
                            'body': json.dumps(
                                { 'found': True,
                                    'diseases': disease,
                                    'significance': clinsig, 
                                    'criteria': criteria,
                                    'accession': variant_id,
                                    'linkout': f'https://www.ncbi.nlm.nih.gov/clinvar/variation/{variant_id}'
                                })
                            }
        time.sleep(1)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
        'body': json.dumps(
            {'found': False}
            )
    }