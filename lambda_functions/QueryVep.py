import json
import urllib3
from collections import defaultdict, Counter

tools = {
        "BayesDel_addAF_score": {
            "help": ("BayesDel (AF) is a deleteriousness meta-score. The range of the score is from -1.29334 to 0.75731. "
                     "The higher the score, the more likely the variant is pathogenic. "
                     "Scores above 0.06 are considered pathogenic."),
            "threshold": 0.06,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "BayesDel (AF)"},
        "BayesDel_noAF_score":{
            "help": ("BayesDel is a deleteriousness meta-score. The range of the score is from -1.29334 to 0.75731. "
                     "The higher the score, the more likely the variant is pathogenic.  "
                     "Scores above -0.0570105 are considered pathogenic."),
            "threshold": -0.0570105,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "BayesDel (No AF)"},
        "clinpred_score": {
            "help": ("ClinPred is a deleteriousness meta-score combining in-silico predictions and AFs. The range of the score is from 0 to 1. "
            "The higher the score, the more likely the variant is pathogenic. Scores above 0.5 are considered pathogenic."),
            "threshold": 0.5,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "ClinPred"},
        "MetaLR_score": {
            "help": ("MetaLR is a deleteriousness meta-score derived using logistic regression to integrate nine tools. The range of the score is from 0 to 1. "
                     "The higher the score, the more likely the variant is pathogenic. Values greater than 0.5 are considered pathogenic. (PMID:25552646)"),
            "threshold": 0.5,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "MetaLR"},
        "MetaRNN_score": {
            "help": ("MetaRNN is a deleteriousness meta-score derived using a recurrent neural network to integrate nine tools. The range of the score is from 0 to 1. "
                     "The higher the score, the more likely the variant is pathogenic. Values greater than 0.5 are considered pathogenic."),
            "threshold": 0.5,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "MetaRNN"},
        "MetaSVM_score": {
            "help": ("MetaSVM is a deleteriousness meta-score derived using a support vector machine to integrate nine tools. "
                    "The range of the score is from 0 to 1. "
                     "The higher the score, the more likely the variant is pathogenic. Values greater than 0.5 are considered pathogenic. (PMID:25552646)"),
            "threshold": 0.5,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "MetaSVM"},
        "SIFT_score": {
            "help": ("SIFT predicts pathogenicity based on sequence homology and the physico-chemical similarity between the alternate amino acid. "
                    "Scores nearer zero are more likely to be deleterious. Scores of less than 0.05 are considered pathogenic. (PMID: 12824425)"),
            "threshold": 0.05,
            "threshold_type" : "max",
            "scores": [],
            "classifications": [],
            "toolname": "SIFT"},
        "polyphen_score": {
            "help": ("Polyphen predicts the effect of an amino acid substitution using sequence homology, Pfam annotations and 3D structures from PDB. The range of the score is from 0 to 1.  "
                     "The higher the score, the more likely the variant is pathogenic. Values greater than 0.446 are considered pathogenic."),
            "threshold": 0.446,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "Polyphen"},
        "DANN_score": {
            "help": ("DANN uses a neural network to integrate genomic features used by CADD for predicting variant deleteriousness. The range of the score is from 0 to 1. "
            "The higher the score, the more likely the variant is pathogenic. Values greater than 0.5 are considered pathogenic. (PMID:25338716)"),
            "threshold": 0.5,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "DANN"},
        "fathmm-MKL_coding_score": {
            "help": ("FATHMM-MKL uses a classifier based on multi-kernel learning to incorporate information on sequence conservation and ENCODE-derived functional data. The range of "
            "the score is from 0 to 1. The higher the score, the more likely the variant is pathogenic. Values greater than 0.26 are considered pathogenic. (PMID: 25583119)"),
            "threshold": 0.26,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "FATHMM-MKL"
        },
        "MutationTaster_score": {
            "help": ("Mutation Taster is a deleteriousness meta-score derived by aggregating tools using a Naive Bayes approach. The range of the score is from 0 to 1. "
                    "The higher the score, the more likely the variant is pathogenic. Values greater than 0.5 are considered pathogenic"),
            "threshold": 0.5,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "Mutation Taster"},
        "PROVEAN_score": {
            "help": ("Provean predicts the deleteriousness of a variant by considering alignment of a variant with homologous proteins. The lower the value, "
                        "the more likely the variant is pathogenic. Values smaller than -2.282 are considered pathogenic to maximise overall balanced accuracy. (PMID: 23056405)"),
            "threshold": -2.282,
            "threshold_type": "max",
            "scores": [],
            "classifications": [],
            "toolname": "Provean"},
        "MutPred_score": {
            "help": ("MutPred predicts the deleteriousness of a variant using a protein sequence-based model and 14 structural/functional features combined using a Random Forest. The range of the score is "
            "0 to 1. The higher the value, the more likely the variant is pathogenic. Values greater than 0.5 are considered pathogenic. (PMID: 19734154)"),
            "threshold": 0.5,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "MutPred"},
        "CADD_phred": {
            "help": ("CADD is a deleteriousness score derived from 60 features combined with SVM. The range of the score is 1 to 99. "
                    "The higher the value, the more likely the variant is pathogenic. Values greater than 20 (top 1% of variants) are considered pathogenic. (PMID: 30371827) "),
            "threshold": 20,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "CADD"}
            }

def fetch_vep_data(notation):
    # returns None if status code from the Vep API is not 200 or no consequences can be retrieved
    TOOLS = ",".join(tools.keys())
    http = urllib3.PoolManager()
    API_ENDPOINT = f"https://grch37.rest.ensembl.org/vep/human/hgvs/{notation}?CADD=1&dbNSFP={TOOLS}&hgvs=1&maxEntScan=1&refseq=1&content-type=application/json"
    response = http.request('GET', API_ENDPOINT)
    if response.status == 200:
        data = json.loads(response.data)
        try:
            return data[0]['transcript_consequences']
        except (IndexError, KeyError):
            return None
    return None 
def format_response(status_code, body):
    return {'statusCode': status_code,
    'headers': {
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'},
        'body': json.dumps(body)} 

def process_consequence(consequence):
    result_keys = [(x, x.lower()) for x in tools.keys()]
    if consequence.get('hgvsc', 'c.(?)'):
        init = {}
        init['hgvsc'] = consequence.get('hgvsc', 'c.(?)')
        init['hgvsp'] = consequence.get('hgvsp', 'p.(?)')
        total_predictions = 0
        total_pathogenic = 0
        for toolname, toolkey in result_keys:
            try:
                tool_score = consequence[toolname]
                scores = [x for x in set(tool_score.split(",")) if x!="."]
                if scores:
                    total_predictions += 1
                else:
                    pass
            except KeyError:
                tool_score = 'Not provided'
        return init
    return None

def lambda_handler(event, context):   
    param = event["queryStringParameters"]
    notation = param['hgvsg']

    consequences = fetch_vep_data(notation)

    if not consequences:
        return format_response(201, 
                                {"error": "No variant data available from VEP API"})
    else:
        annotations = []
        for consequence in consequences:
            result = process_consequence(consequence)
            annotations.append(result)
        return format_response(200, annotations)
    return format_response(201, 
                            {"error": "Error in processing Vep results"})