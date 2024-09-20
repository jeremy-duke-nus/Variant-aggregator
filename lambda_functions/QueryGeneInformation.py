
import json
import urllib3

"""
QueryGeneInformation Module
This module provides functions to query gene information using HGVS notation and retrieve gene summaries from external APIs.
Functions:
    get_gene_symbol(notation: str) -> tuple:
        Extracts the gene symbol and gene ID from the VEP API using the provided HGVS notation.
    get_summary(gene_id: str) -> dict:
        Retrieves a summary of the gene information from the NCBI E-utilities API using the provided gene ID.
    lambda_handler(event: dict, context: object) -> dict:
        AWS Lambda handler function that processes the event, extracts the HGVS notation, retrieves gene information, and returns a summary response.
"""

def get_gene_symbol(notation):
    # extract gene symbol from Vep 
    url = f"https://grch37.rest.ensembl.org/vep/human/hgvs/{notation}?refseq=1&hgvs=1&content-type=application/json"
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    if response.status == 200:
        data = json.loads(response.data.decode('utf-8'))
        consequences = data[0]['transcript_consequences']
        if consequences:
            for csq  in consequences:
                try:
                    return {'status': 200, 
                            'symbol': csq["gene_symbol"], 
                            'entrez':csq['gene_id']}
                except KeyError:
                    pass
        return  {'status': 200, 
                'symbol': None, 
                'entrez': None}
    return None

def get_summary(gene_id):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id={gene_id}&retmode=json"
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    if response.status == 200:
        data = json.loads(response.data.decode('utf-8'))
        try:
            return {'status': 200, 'summary': data['result'][gene_id]['summary']}
        except KeyError:
            return {'status': 204, 'summary': 'No gene information found', 'symbol': None}
    else:
        return {'status': 204, 'summary': 'No gene information found', 'symbol': None}
        
def lambda_handler(event, context):
    param = event["queryStringParameters"]
    notation = param["hgvsg"]
    vep_data = get_gene_symbol(notation)
    if vep_data:
        if vep_data['entrez']: 
            summary = get_summary(vep_data['entrez'])
        else:
            summary = {'status': 204, 'summary': 'Gene Id not found', 'symbol': None}
        summary['gene'] = vep_data['symbol']
        summary['gene_id'] = vep_data['entrez']
    else:
        summary = {'status': 204, 'summary': 'Gene Symbol not found', 'symbol': None}
    return {
        'statusCode': 200 if vep_data else 204,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            
        },
        'body': json.dumps(summary),
    }