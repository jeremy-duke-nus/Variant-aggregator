import boto3
import json
import mysql.connector
import os
import urllib3

def get_oncokb_identifiers():
    """
    get list of RefSeq identifiers from oncokb database
    """
 
    database_host = os.environ['DATABASE_HOST']
    database_name = os.environ['DATABASE_NAME']
    database_password = os.environ['PASSWORD']
    database_user = os.environ['USER']
    
    connector = mysql.connector.connect(host = database_host,
                                        user = database_user, 
                                        password = database_password, 
                                        database = database_name)
    cursor = connector.cursor()
    cursor.execute("SELECT refseq FROM oncokb")
    refseq_ids = cursor.fetchall()
    connector.close()
    refseq_ids = [x[0] for x in refseq_ids]
    return refseq_ids

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

def parse_oncokb_result(oncokb_result, aachange, gene, transcript, hgvsc):
    nononcogene = ('ABI1,AFDN,AFF1,ARFRP1,ARNT,BCL11A,BCL2L2,CAMTA1,CARS1,'
                    "CDX2,CEP43,CLTC,CREB3L1,CREB3L2,DDX10,DDX6,EML4,EPS15,EZR,FCGR2B,FCRL4,FOXO4,FSTL3,"
                    "GAS7,GID4,GPHN,H4C9,HERPUD1,HEY1,HIP1,HLF,HOXA13,HOXA9,"
                    "HOXC11,HOXC13,HOXD11,HOXD13,HSP90AB1,IGH,IGK,IGL,IL21R,ITK,"
                    "KDSR,KIF5B,LASP1,LPP,LYL1,MLF1,MLLT6,MRTFA,MSN,MUC1,MYH9,NCOA2,"
                    "NDRG1,NFKB2,NIN,NUMA1,PAFAH1B2,PBX1,PCM1,PDE4DIP,PER1,PICALM,PLAG1,"
                    "POU2AF1,PRDM16,PRRX1,PSIP1,PTPRO,RABEP1,RAP1GDS1,RHOH,RNF213,RPL22,"
                    "RPN1,RSPO2,SDC4,SH3GL1,SLC34A2,SRSF3,SSX1,SSX2,SSX4,TAF15,TAL2,"
                    "TFG,TPM3,TPM4,TRIM24,TRIP11,USP6,ZBTB16,ZMYM2,ZNF384,ZNF521,"
                    "ZNF703,ACSL3,ACSL6,ACTB,ACVR2A,ADGRA2,AFF3,APH1A,APOBEC3B,"
                    "ASMTL,ASPSCR1,ATG5,ATP2B3,BAX,BCL9L,BTLA,BUB1B,CBLB,CBLC,CCDC6,CCN6,"
                    "CCNB1IP1,CCT6B,CD36,CHCHD7,CHIC2,CHN1,CILK1,CKS1B,CLIP1,CLP1,CNBP,CNOT3,CPS1,"
                    "CRTC1,CRTC3,CSF1,CYP17A1,DCTN1,DDR1,DUSP2,DUSP9,ELP2,EXOSC6,EXT2,FAF1,FAT4,"
                    "FBXO31,FGF12,FIP1L1,FLYWCH1,FNBP1,GADD45B,GMPS,GOLGA5,GOPC,GTSE1,HNRNPA2B1,"
                    "HOOK3,HOXA3,IKBKB,IKZF2,IL2,INPP5D,IRS4,JAZF1,KAT6B,KCNJ5,KDM2B,KDM4C,KLF6,KLK2,"
                    "KNL1,KTN1,LCP1,LIFR,LMNA,LRIG3,LRRK2,MAGED1,MAML2,MAP3K6,MDS2,MIB1,MKNK1,MLLT11,MNX1,"
                    "MTCP1,MYO18A,NAB2,NACA,NBEAP1,NCOA1,NCOA4,NFATC2,NFIB,NFKBIE,NOD1,NONO,NUTM2A,NUTM2B,"
                    "NUTM2D,OLIG2,OMD,PAG1,PAK3,PARP2,PARP3,PASK,PATZ1,PC,PCLO,PCSK7,PDCD11,PHF1,POLQ,"
                    "POU5F1,PPFIBP1,PPP1CB,PRCC,PRF1,PRSS8,PTK6,PTK7,PTPN6,PTPRB,PTPRC,PTPRK,RALGDS,"
                    "RASGEF1A,RMI2,RNF217-AS1,RPL10,RSPO3,RUNX2,S1PR2,SALL4,SBDS,SEC31A,SEPTIN5,SEPTIN6,"
                    "SEPTIN9,SERP2,SFPQ,SFRP4,SIX1,SLC1A2,SLC45A3,SMARCA1,SNCAIP,SND1,SNX29,SOCS2,SS18L1,"
                    "STIL,STRN,TCEA1,TCF12,TEC,TERC,TFEB,TFPT,TFRC,TIPARP,TLL2,TMEM30A,TMSB4XP8,"
                    "TNFRSF11A,TPR,TRIM33,"
                    "TRRAP,TTL,TUSC3,TYRO3,WAS,WDCP,WDR90,WRN,XPA,YPEL5,YWHAE,YY1AP1,ZNF24,ZNF331").split(',')
    if oncokb_result:
        status = oncokb_result.status
        data = json.loads(oncokb_result.data)
        if status == 200:
            geneType = None
            geneSummary = data['geneSummary']
            if gene not in nononcogene:
                geneType = 'known oncogene' 
            if 'tumor suppressor' in geneSummary:
                if not geneType:
                    geneType = 'tumor suppressor'
                else:
                    geneType += ' & tumor suppressor'
            if not geneType:
                geneType = 'gene of other functions excluding oncogene & tumor suppressor'
            drugs = data["treatments"]
            drugs = [{"drug": x["drugs"][0]["drugName"], 
                        "indication": x['levelAssociatedCancerType']['mainType']['name'], 
                        "fda": x['fdaLevel']} for x in drugs]
            results = [{
                'gene': str(gene),
                'aachange': str(aachange),
                'hgvsc': hgvsc,
                'oncogenecity': str(data['oncogenic']),
                'geneType': geneType,
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
    refseq_ids = get_oncokb_identifiers()
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
            status, oncokb_result = parse_oncokb_result(oncokb_response, aachange, genename, transcript, hgvsc)
        except TypeError:
            oncokb_result = [{'message': 'Variant not reported in oncoKb', "code":201}]
            status = 201
        return_json['statusCode'] = json.dumps(status)
        return_json['body'] = json.dumps(oncokb_result)
        return return_json
    return