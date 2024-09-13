import json
import urllib3

def replace_null_values(value):
    if value:
        try:
            return value.upper()
        except (AttributeError, ValueError):
            return value
    else:
        return "No value available"
            
def get_genome_exome_values(exome, genome, population, exome_faf, genome_faf):
    color = "neutral-population"
    if not genome:
        g = "No genome data available"
    else:
        g = "{:.9f}".format(genome[population])
        if "No" not in str(genome_faf):
            if float(g) > float(genome_faf):
                color = "pathogenic-population"
    if not exome:
        e = "No exome data available"
    else:
        e = "{:.9f}".format(exome[population])
        if "No" not in str(exome_faf):
            if float(e) > float(exome_faf):
                color = "pathogenic-population"
    return  {"exome": e, "genome": g, "id": population, "color": color}
    
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
    
    response = http.request('GET', API_ENDPOINT, fields =  payload)
    
    data = json.loads(response.data.decode('utf-8'))
    
    if data["data"]["variant"]:
        """
        extract only very specific fields of interest 
        """
        # Get genome and exome data respectively
        variant_results = data['data']['variant']
        exome_results = variant_results['exome']
        genome_results = variant_results['genome']
        
        if genome_results:
            genome_populations = genome_results['populations'] # List of population level dictionary
            # Convert the dictionary to a more searchable format
            simplifed_genome = [(x["id"].upper(), x["ac"]/x["an"]) if x["an"]!=0 else (x["id"].upper(), 0) for x in genome_populations ]
            simplifed_genome = dict([x for x in simplifed_genome if "X" not in x[0]])
            genome_af = genome_results['genome_af']
            genome_faf = genome_results['genome_faf']
            genome_faf_popmax = replace_null_values(genome_faf['popmax']) 
            genome_faf_popmax_population = replace_null_values(genome_faf['popmax_population'])
        else:
            simplifed_genome = None
            genome_af = "Not found in GnomAD genome"
            genome_faf = "Not found in GnomAD genome"
            genome_faf_popmax = "Not found in GnomAD genome"
            genome_faf_popmax_population = "Not found in GnomAD genome"

        if exome_results:
            exome_populations = exome_results['populations'] # List of population level dictionary
            simplified_exome = [(x["id"].upper(), x["ac"]/x["an"]) if x["an"]!=0 else (x["id"].upper(), 0) for x in exome_populations ]
            simplified_exome = dict([x for x in simplified_exome if "X" not in x[0]])
            exome_af = exome_results['exome_af']
            exome_faf = exome_results['exome_faf']
            exome_faf_popmax = replace_null_values(exome_faf['popmax'])
            exome_faf_popmax_population = replace_null_values(exome_faf['popmax_population'])
        else:
            simplified_exome = None
            exome_af = "Not found in GnomAD exome"
            exome_faf = "Not found in GnomAD exome"
            exome_faf_popmax = "Not found in GnomAD exome"
            exome_faf_popmax_population = "Not found in GnomAD exome"
            
        populations = ["EAS", "SAS", "AFR", "AMR", "ASJ", "FIN", "NFE", "OTH"]
        population_results = [get_genome_exome_values(simplified_exome, simplifed_genome, x, exome_faf_popmax, genome_faf_popmax) for x in populations]
        results = {'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            
        },
        'body':json.dumps({
            "summary": {
                "exome": {
                    "exome_af": exome_af,
                    "exome_faf_popmax": exome_faf_popmax,
                    "exome_faf_popmax_population": exome_faf_popmax_population
                },
                "genome":{
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
        })
        }
        return results
    else:
        print (data)
        results = {'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            
        },
        'body':json.dumps({
                "query": {
                    "chromosome": chrom,
                    "position": position, 
                    "reference": ref, 
                    "variant": variant
                },
                "errors": data.get("errors"),
                "populations": []
            })
        }
        return results