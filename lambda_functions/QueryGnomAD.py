import json
import urllib3

"""
QueryGnomAD.py
This script defines a Lambda function that queries the gnomAD API for variant data and processes the results to provide population-specific allele frequencies and other relevant information.
Functions:
    replace_null_values(value):
        Replaces null or empty values with a default string or processes the value 
        to uppercase if possible.
    get_population_values(exome, genome, population, exome_faf, genome_faf):
        Retrieves and formats allele frequency data for a specific population from 
        exome and genome datasets.
    extract_variant_data(variant_results):
        Extracts and simplifies variant data from the gnomAD API response, 
        focusing on exome and genome datasets.
    lambda_handler(event, context):
        AWS Lambda handler function that processes incoming API requests, 
        queries the gnomAD API, and returns formatted variant data.
Parameters:
    replace_null_values(value):
        value (any): The value to be processed.
    get_population_values(exome, genome, population, exome_faf, genome_faf):
        exome (dict): Exome dataset results.
        genome (dict): Genome dataset results.
        population (str): Population identifier.
        exome_faf (str): Exome FAF (Filtering Allele Frequency) value.
        genome_faf (str): Genome FAF (Filtering Allele Frequency) value.
    extract_variant_data(variant_results):
        variant_results (dict): The variant data results from the gnomAD API.
    lambda_handler(event, context):
        event (dict): The event data containing query parameters.
        context (object): The context in which the Lambda function is called.
Returns:
    replace_null_values(value):
        any: The processed value or a default string if the value is null or empty.
    get_population_values(exome, genome, population, exome_faf, genome_faf):
        dict: A dictionary containing formatted allele frequency data and population information.
    extract_variant_data(variant_results):
        tuple: A tuple containing simplified exome and genome data, allele frequencies, and FAF values.
    lambda_handler(event, context):
        dict: A dictionary containing the HTTP response with status code, headers, and body.
"""

def replace_null_values(value):
    if value:
        try:
            return value.upper()
        except (AttributeError, ValueError):
            return value
    else:
        return "No value available"

def get_population_values(exome, genome, population, exome_faf, genome_faf):
    color = "neutral-population"
    g = "No genome data available" if not genome else "{:.9f}".format(genome[population])
    e = "No exome data available" if not exome else "{:.9f}".format(exome[population])
    
    if genome and "No" not in str(genome_faf) and float(g) > float(genome_faf):
        color = "pathogenic-population"
    if exome and "No" not in str(exome_faf) and float(e) > float(exome_faf):
        color = "pathogenic-population"
    
    return {"exome": e, "genome": g, "id": population, "color": color}

def extract_variant_data(variant_results):
    exome_results = variant_results['exome']
    genome_results = variant_results['genome']
    
    def simplify_population_data(results, key_prefix):
        if results:
            populations = results['populations']
            simplified = [(x["id"].upper(), x["ac"] / x["an"]) if x["an"] != 0 else (x["id"].upper(), 0) for x in populations]
            simplified = dict([x for x in simplified if "X" not in x[0]])
            af = results[f'{key_prefix}_af']
            faf = results[f'{key_prefix}_faf']
            faf_popmax = replace_null_values(faf['popmax'])
            faf_popmax_population = replace_null_values(faf['popmax_population'])
        else:
            simplified = None
            af = f"Not found in GnomAD {key_prefix}"
            faf = f"Not found in GnomAD {key_prefix}"
            faf_popmax = f"Not found in GnomAD {key_prefix}"
            faf_popmax_population = f"Not found in GnomAD {key_prefix}"
        
        return simplified, af, faf_popmax, faf_popmax_population
    
    simplified_exome, exome_af, exome_faf_popmax, exome_faf_popmax_population = simplify_population_data(exome_results, 'exome')
    simplified_genome, genome_af, genome_faf_popmax, genome_faf_popmax_population = simplify_population_data(genome_results, 'genome')
    
    return (simplified_exome, exome_af, exome_faf_popmax, exome_faf_popmax_population, 
            simplified_genome, genome_af, genome_faf_popmax, genome_faf_popmax_population)

def lambda_handler(event, context):
    param = event["queryStringParameters"]
    chrom = param['chromosome']
    position = param['position']
    ref = param['reference']
    variant = param['variant']
    http = urllib3.PoolManager()
    
    query = ("""
    {variant(variantId:"%s-%s-%s-%s" dataset:gnomad_r2_1) {
    reference_genome
    genome {
      genome_af: af
      genome_ac: ac
      genome_an: an
      genome_ac_hemi: ac_hemi
      genome_ac_hom: ac_hom
      genome_faf: faf99 {
        popmax
        popmax_population
      }
      populations {
        id
        ac
        an
      }
    }
    exome {
      exome_af: af
      exome_ac: ac
      exome_an: an
      exome_ac_hemi: ac_hemi
      exome_ac_hom: ac_hom
      exome_faf: faf99 {
        popmax
        popmax_population
      }
      populations {
        id
        ac
        an
      }
    }
    }
    }
    """)
    
    query = query % (chrom, position, ref.upper(), variant.upper())
    payload = {"query": query}
    API_ENDPOINT = "https://gnomad.broadinstitute.org/api/"
    
    response = http.request('GET', API_ENDPOINT, fields=payload)
    data = json.loads(response.data.decode('utf-8'))
    
    if data["data"]["variant"]:
        variant_results = data['data']['variant']
        simplified_exome, exome_af, exome_faf_popmax, exome_faf_popmax_population, simplified_genome, genome_af, genome_faf_popmax, genome_faf_popmax_population = extract_variant_data(variant_results)
        
        populations = ["EAS", "SAS", "AFR", "AMR", "ASJ", "FIN", "NFE", "OTH"]
        population_results = [get_population_values(simplified_exome, simplified_genome, x, exome_faf_popmax, genome_faf_popmax) for x in populations]
        body = {
                "errors": "",
                "summary": {
                    "exome": {
                        "exome_af": exome_af,
                        "exome_faf_popmax": exome_faf_popmax,
                        "exome_faf_popmax_population": exome_faf_popmax_population
                    },
                    "genome": {
                        "genome_af": genome_af,
                        "genome_faf_popmax": genome_faf_popmax,
                        "genome_faf_popmax_population": genome_faf_popmax_population
                    },
                    "query": {
                        "chromosome": chrom,
                        "position": position,
                        "reference": ref,
                        "variant": variant
                    }
                },
                "populations": population_results
                
            }
    else:
        body = {
                "errors": data.get("errors"),
                "summary": {
                    "exome": {},
                    "genome": {},
                    "query": {
                        "chromosome": chrom,
                        "position": position,
                        "reference": ref,
                        "variant": variant
                        }
                },
                "populations": []
            }
    return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(body)
        }
