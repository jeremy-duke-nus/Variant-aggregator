import json
import urllib3
from collections import defaultdict, Counter

tools = {
        "bayesdel_addaf_score": {
            "help": ("BayesDel (AF) is a deleteriousness meta-score. The range of the score is from -1.29334 to 0.75731. "
                     "The higher the score, the more likely the variant is pathogenic. "
                     "Scores above 0.06 are considered pathogenic."),
            "threshold": 0.06,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "BayesDel (AF)"},
        "bayesdel_noaf_score":{
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
        "metalr_score": {
            "help": ("MetaLR is a deleteriousness meta-score derived using logistic regression to integrate nine tools. The range of the score is from 0 to 1. "
                     "The higher the score, the more likely the variant is pathogenic. Values greater than 0.5 are considered pathogenic. (PMID:25552646)"),
            "threshold": 0.5,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "MetaLR"},
        "metarnn_score": {
            "help": ("MetaRNN is a deleteriousness meta-score derived using a recurrent neural network to integrate nine tools. The range of the score is from 0 to 1. "
                     "The higher the score, the more likely the variant is pathogenic. Values greater than 0.5 are considered pathogenic."),
            "threshold": 0.5,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "MetaRNN"},
        "metasvm_score": {
            "help": ("MetaSVM is a deleteriousness meta-score derived using a support vector machine to integrate nine tools. "
                    "The range of the score is from 0 to 1. "
                     "The higher the score, the more likely the variant is pathogenic. Values greater than 0.5 are considered pathogenic. (PMID:25552646)"),
            "threshold": 0.5,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "MetaSVM"},
        "revel_score": {
            "help": ("REVEL is a deleteriousness meta-score derived by combining 13 tools using a random forest. The higher the score, the more likely the variant is pathogenic. "
                    "The range of the score is from 0 to 1. Scores above 0.5 are considered pathogenic. (PMID: 27666373)"),
            "threshold": 0.5,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "REVEL"},
        "sift_score": {
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
        "dann_score": {
            "help": ("DANN uses a neural network to integrate genomic features used by CADD for predicting variant deleteriousness. The range of the score is from 0 to 1. "
            "The higher the score, the more likely the variant is pathogenic. Values greater than 0.5 are considered pathogenic. (PMID:25338716)"),
            "threshold": 0.5,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "DANN"},
        "fathmm-mkl_coding_score": {
            "help": ("FATHMM-MKL uses a classifier based on multi-kernel learning to incorporate information on sequence conservation and ENCODE-derived functional data. The range of "
            "the score is from 0 to 1. The higher the score, the more likely the variant is pathogenic. Values greater than 0.26 are considered pathogenic. (PMID: 25583119)"),
            "threshold": 0.26,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "FATHMM-MKL"
        },
        "fathmm_score": {
            "help": ("FATHMM uses a hidden markov model to predict the deleteriousness of a substitution considering the functional domain within which the mutation occurs. "
                    "The smaller the value, the more likely the variant is pathogenic. Values smaller than -0.75 are considered pathogenic. (PMID: 23620363)"),
            "threshold": -0.75,
            "threshold_type": "max",
            "scores": [],
            "classifications": [],
            "toolname": "FATHMM"},
        "mutationtaster_score": {
            "help": ("Mutation Taster is a deleteriousness meta-score derived by aggregating tools using a Naive Bayes approach. The range of the score is from 0 to 1. "
                    "The higher the score, the more likely the variant is pathogenic. Values greater than 0.5 are considered pathogenic"),
            "threshold": 0.5,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "Mutation Taster"},
        "provean_score": {
            "help": ("Provean predicts the deleteriousness of a variant by considering alignment of a variant with homologous proteins. The lower the value, "
                        "the more likely the variant is pathogenic. Values smaller than -2.282 are considered pathogenic to maximise overall balanced accuracy. (PMID: 23056405)"),
            "threshold": -2.282,
            "threshold_type": "max",
            "scores": [],
            "classifications": [],
            "toolname": "Provean"},
        "mutpred_score": {
            "help": ("MutPred predicts the deleteriousness of a variant using a protein sequence-based model and 14 structural/functional features combined using a Random Forest. The range of the score is "
            "0 to 1. The higher the value, the more likely the variant is pathogenic. Values greater than 0.5 are considered pathogenic. (PMID: 19734154)"),
            "threshold": 0.5,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "MutPred"},
        "cadd_phred": {
            "help": ("CADD is a deleteriousness score derived from 60 features combined with SVM. The range of the score is 1 to 99. "
                    "The higher the value, the more likely the variant is pathogenic. Values greater than 20 (top 1% of variants) are considered pathogenic. (PMID: 30371827) "),
            "threshold": 20,
            "threshold_type": "min",
            "scores": [],
            "classifications": [],
            "toolname": "CADD"}
            }

def fetch_vep_data(notation):
    http = urllib3.PoolManager()
    API_ENDPOINT = f"https://grch37.rest.ensembl.org/vep/human/hgvs/{notation}?CADD=1&dbNSFP=ALL&hgvs=1&maxEntScan=1&refseq=1&content-type=application/json"
    response = http.request('GET', API_ENDPOINT)
    if response.status == 200:
        data = json.loads(response.data)
        return data
    else:
        return None 

def subset_tool_data(consequence, tools):
    return [consequence.get(tool, {tool: None}) for tool in tools]

def lambda_handler(event, context):   
    param = event["queryStringParameters"]
    notation = param['hgvsg']

    vep_response = fetch_vep_data(notation)
    
    if not vep_response:
        return {'statusCode': 201,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'},
                'body': json.dumps({
                    'error': 'Unable to fetch response from VEP endpoint'
                })}
    
    annotations = []
    try:
        consequences = data[0]['transcript_consequences'] 
        TOOLS = ["polyphen_score", "bayesdel_addaf_score", "bayesdel_noaf_score", "clinpred_score", 
                    "metalr_score", "metarnn_score", "metasvm_score", "mutationtaster_score",
                    "revel_score", 'cadd_phred', 'dann_score', 'fathmm_score',
                    'fathmm-mkl_coding_score',  
                    'mutpred_score', 'provean_score', 'sift_score']
        total_predictions = 0
        for consequence in consequences:
            if consequence.get("hgvsc"):
                consequence_results = {}
                consequence_results["hgvsc"] = consequence.get("hgvsc", "c.(?)")
                consequence_results["hgvsp"] = consequence.get("hgvsp", "p.(?)")
                consequence_results["predictions"] = []

                predictions = subset_tool_data(consequence, TOOLS)
                total_pathogenic = 0
                total_predictions = 0

                for tool, predictions in predictions.items():
                    pass
            annotations.append(consequence_results)
    except KeyError:
            return 
        
            if consequence.get("hgvsc"):
                init = {}
                init["hgvsp"] = consequence.get("hgvsp", "p.(?)")
                init["hgvsc"] = consequence.get("hgvsc", "c.(?)")
                total_predictions = 0
                total_pathogenic = 0
                init["predictions"] = []
                for tool in tool_list:
                    try:
                        if consequence[tool]!="":
                            tool_tmp = {"id": tool,
                                    "name": tools[tool]["toolname"], 
                                    "description": tools[tool]["help"],
                                    "threshold": tools[tool]["threshold"],
                                    "threshold_type": tools[tool]["threshold_type"]
                            }
                            threshold = tools[tool]["threshold"]
                            threshold_type = tools[tool]["threshold_type"]
                            try:
                                score_tmp = set(consequence[tool].split(","))
                                score_tmp = [x for x in score_tmp if x!="."]
                                if score_tmp:
                                    total_predictions += 1
                                    score_tmp = [float(x) for x in score_tmp if x]
                                    tool_tmp["scores"] = ",".join([str(x) for x in score_tmp])
                                    if threshold_type == "min" and score_tmp:
                                        if min(score_tmp) >= threshold:
                                            tool_tmp["classification"] = "pathogenic"
                                            total_pathogenic += 1
                                        else:
                                            tool_tmp["classification"] = "neutral"
                                    elif threshold_type == "max":
                                        if max(score_tmp) <= threshold and score_tmp:
                                            tool_tmp["classification"] = "pathogenic"
                                            total_pathogenic += 1
                                        else:
                                            tool_tmp["classification"] = "neutral"
                                else:
                                    tool_tmp["scores"] = "Not available"
                                    tool_tmp["classification"] = "neutral"
                            except AttributeError:
                                tool_tmp['scores'] = consequence[tool]
                                total_predictions += 1
                                if threshold_type == "min" and float(consequence[tool]) >= threshold:
                                    tool_tmp["classification"] = "pathogenic"
                                    total_pathogenic += 1
                                elif threshold_type == "max" and float(consequence[tool]) <= threshold:
                                    tool_tmp["classification"] = "pathogenic"
                                    total_pathogenic += 1
                                else:
                                    tool_tmp["classification"] = "neutral"
                            except KeyError:
                                tool_tmp['scores'] = "Not available"
                                tool_tmp["classification"] = "neutral"
                        init["predictions"].append(tool_tmp)
                        init['total_predictions'] = total_predictions
                        init['total_pathogenic'] = total_pathogenic
                        init['percent_pathogenic'] = "{:.2f}".format(100*float(total_pathogenic)/float(total_predictions))
                    except KeyError:
                        pass
                annotations.append(init)
        if total_predictions:
            return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'},
                    'body': json.dumps(annotations)
                    } 
        else:
            body = {"error":"No predictions found for variant"}
    except AttributeError:
        body = {'error': 'Server error'}
    return {'statusCode': 201,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'},
            'body': json.dumps(body)}
