import boto3
import json
import os
import urllib3

def get_oncokb_identifiers():
    """
    get list of RefSeq identifiers from oncokb database
    """
    s3 = boto3.resource('s3')
    obj = s3.Object('variant-aggregator-v2','cancerGeneList_Athena.tsv')
    
    data=obj.get()['Body'].read()
    data = str(data).split('\\r\\n')
    data = [str(x).split('\\t') for x in data]
    dictionary = {}
    refseq = []
    for g in data:
        if len(g) == 6:
            dictionary[g[0]] = {'refseq': g[1].split('.')[0], 'description': g[5]}
            refseq.append(g[1].split('.')[0])
    return dictionary, refseq


def get_vep_annotation(notation):
    """
    perform vep annotation using the g. convention. 
    returns None if VEP is not able to annotate
    the variant.
    """
    http = urllib3.PoolManager()
    API_ENDPOINT = API_ENDPOINT = f"https://grch37.rest.ensembl.org/vep/human/hgvs/{notation}?hgvs=1&refseq=1&content-type=application/json"
    response = http.request('GET', API_ENDPOINT)
    data = json.loads(response.data)

    try:
        consequence = data[0]['transcript_consequences']
    except KeyError:
        raise ValueError("Unable to annotate variant coordinates with VEP")
    else:
        return consequence
    return

def identify_oncokb_transcripts(refseq_ids, 
                                vep_annotations):
    """
    identify transcripts from vep annotations that are in oncokb database.
    returns None if the oncoKb transcript is not found. 
    
    return:
    first dictionary element of vep_annotations that has a refseq id in refseq_ids
    """
    refseq_ids = set(refseq_ids)
    if vep_annotations:
        for annotation in vep_annotations:
            try:
                transcript = annotation['hgvsc'].split('.')[0]
                if transcript in refseq_ids:
                    return annotation, transcript, annotation['hgvsc']
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
        raise ValueError("OncoKB transcript is not found")
    else:   
        return 

def contract_amino_acid_change(aachange):
    """
    contract amino acid change to single letter amino acid code
    """
    code_table = {"Ala": "A", "Arg": "R", "Asn": "N", "Asp": "D", "Cys": "C",  
                  "Gln": "Q", "Glu": "E", "Gly": "G", "His": "H", "Ile": "I",  
                  "Leu": "L", "Lys": "K", "Met": "M", "Phe": "F", "Pro": "P",  
                  "Ser": "S", "Thr": "T", "Trp": "W", "Tyr": "Y", "Val": "V"}
    # We will need 3 passes since we cannot assume that the amino acids will appear in order
    for long, short in code_table.items():
        aachange = aachange.replace(long, short)

    for long, short in code_table.items():
        aachange = aachange.replace(long, short)

    for long, short in code_table.items():
        aachange = aachange.replace(long, short)
    return aachange

def get_oncokb_result(consequence):
    """
    return entire api object to extract status code
    """
    api_key = os.environ['API_KEY']
    if consequence:
        http = urllib3.PoolManager()
        try:
            aachange = consequence['hgvsp'].split("p.")[-1]
            aachange_short = contract_amino_acid_change(aachange)
            genename = consequence['gene_symbol']
            API_ENDPOINT = f"https://www.oncokb.org/api/v1/annotate/mutations/byProteinChange?referenceGenome=GRCh37&hugoSymbol={genename}&alteration={aachange_short}"
            response = http.request('GET', API_ENDPOINT, 
                                    headers = {
                                        "Authorization": f" Bearer {api_key}",
                                        "accept": "application/json"})
            return response, aachange_short, genename
        except KeyError:
            return
    return

def parse_oncokb_result(oncokb_result, aachange, gene, transcript, hgvsc, genedictionary):
    if oncokb_result:
        status = oncokb_result.status
        data = json.loads(oncokb_result.data)
        if status == 200:
            geneType = genedictionary.get(gene, 'not in the list of genes from OncoKb')
            drugs = data["treatments"]
            drugs = [{"drug": x["drugs"][0]["drugName"], 
                        "indication": x['levelAssociatedCancerType']['mainType']['name'], 
                        "fda": x['fdaLevel']} for x in drugs]
            results = [{
                'gene': str(gene),
                'aachange': str(aachange),
                'hgvsc': hgvsc,
                'oncogenecity': str(data['oncogenic']),
                'geneType': geneType['description'],
                'transcript': transcript,
                'hotspot': str(data['hotspot']),
                'effect': str(data['mutationEffect']['knownEffect']),
                'description': str(data['mutationEffect']['description']),
                'sensitivity': data['highestSensitiveLevel'] if data['highestSensitiveLevel'] else "unknown",
                'diagnostic': data['highestDiagnosticImplicationLevel'] if data['highestDiagnosticImplicationLevel'] else 'unknown',
                'fda': data['highestFdaLevel'] if data['highestFdaLevel'] else 'unknown',
                'treatments': [x for x in drugs if x['indication']],
                'code': 200, 
                "linkout": f"https://www.oncokb.org/gene/{gene}/{aachange.replace("p.","")}"
            }]
            return 200, results
        elif status == 401:
            return 401, [{
                'message': 'Authentication error. This likely is due to expired API key. Please refresh the API key and try again.',
                "code":401
            }]
    else:
        return 201, [{
                'message': 'Variant not found in OncoKb',
                "code":201
            }]
def lambda_handler(event, context):
    return_json = {
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                        }
    }
    param = event["queryStringParameters"]
    notation = param['hgvsg']
    gene_dictionary, refseq_ids = get_oncokb_identifiers()
    try:
        vep_annotations = get_vep_annotation(notation)
    except ValueError:
         results = [{'message': 'OncoKB transcript not found in annotations from VEP', "code":201}]
         return_json['body'] = json.dumps(results)
         return_json['statusCode'] = json.dumps(201)
         return return_json
         
    try:
        oncokb_transcript, transcript, hgvsc = identify_oncokb_transcripts(refseq_ids, vep_annotations)
    except ValueError:
        results = [{'message': 'OncoKB transcript not found in annotations from VEP', "code":201}]
        return_json['body'] = json.dumps(results)
        return_json['statusCode'] = json.dumps(201)
        return return_json
    else:
        try:
            oncokb_response, aachange, genename = get_oncokb_result(oncokb_transcript)
            status, oncokb_result = parse_oncokb_result(oncokb_response, aachange, genename, transcript, hgvsc, gene_dictionary)
        except TypeError:
            oncokb_result = [{'message': 'Variant not reported in oncoKb', "code":201}]
            status = 201
        return_json['statusCode'] = json.dumps(status)
        return_json['body'] = json.dumps(oncokb_result)
        return return_json
    return