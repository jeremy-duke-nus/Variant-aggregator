import json
import urllib3

def lambda_handler(event, context):
    param = event["queryStringParameters"]
    chrom = param['chromosome'].replace("chr", "")
    position = int(param['position'])-1

    variant = param['variant']
    reference = param['reference']
    if len(reference) < len(variant):
        # insertions
        variant = f"I{variant[1:]}"
    elif len(reference) > len(variant):
        # Deletions
        position = position + 1
        variant = f"D{len(reference) - len(variant)}"
    else:
        variant = variant
    http = urllib3.PoolManager()
    API_ENDPOINT = f"http://beacon.prism-genomics.org/cgi-bin/ucscBeacon/query?&chromosome={chrom}&position={position}&alternateBases={variant}&format=json"
    response = http.request('GET', API_ENDPOINT)
    data = json.loads(response.data)["response"]
    body = {"results": {
            "exists": data['exists'].capitalize(),
            "query": {"chrom": chrom, "position": position+1, "reference": reference, "variant": variant}
    }}
    return {
            'statusCode': 200,
            'body': json.dumps(body),
            'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'} 
            }
