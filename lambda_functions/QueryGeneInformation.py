import json
import urllib3

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
                    return 200, csq["gene_symbol"], csq['gene_id']
                except KeyError:
                    pass
        return 200, None, None 
    return None, None, None

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
    status, gene, gene_id = get_gene_symbol(notation)
    if gene_id:
        summary = get_summary(gene_id)
    else:
        summary = {'status': 204, 'summary': 'Gene Id not found', 'symbol': None}
    summary['gene'] = gene
    summary['gene_id'] = gene_id
    return {
        'statusCode': status,
        'body': json.dumps(summary)
    }
