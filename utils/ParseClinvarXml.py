"""
ParseClinvarXml.py
This script parses a Clinvar XML file and outputs the parsed content to a specified output file.
Usage:
    python ParseClinvarXml.py -i <input_file> -o <output_file>

Arguments:
    -i  Input Clinvar XML file (required)
    -o  Output file (required)

Functions:
    create_soup(infile)
    extract_variation_id(soup)
        Placeholder function to extract variation IDs from the BeautifulSoup object.
            soup (BeautifulSoup): A BeautifulSoup object representing the parsed XML.
    split_records(soup)
    extract_variation_id(record)
    extract_coordinates(record)
        tuple: The coordinates (chromosome, position, reference allele, alternate allele).
    extract_review_status(record)
        tuple: A tuple containing two lists - classification and review status.
    extract_conditions(record)
        set: A set of conditions.
    process_record(record)
        dict: A dictionary containing the extracted information (variation_id, coordinates, review_status, conditions).
    Main function that parses the input XML file and writes the extracted information to the output file.
        args (argparse.Namespace): Command-line arguments.

"""
import argparse
from bs4 import BeautifulSoup as bs


parser = argparse.ArgumentParser()
parser.add_argument('-i', 
                    help="Input Clinvar XML file", 
                    required=True)
parser.add_argument('-o', 
                    help="Output file", 
                    required=True)

def create_soup(infile):
    """
    Parses an XML file and creates a BeautifulSoup object.

    Args:
        infile (str): The path to the input XML file.

    Returns:
        BeautifulSoup: A BeautifulSoup object representing the parsed XML.

    Raises:
        IOError: If the file cannot be opened.
    """
    try:
        with open(args.i, 'r') as infile:
            contents = infile.read()
    except IOError:
        raise
    else:
        contents = contents.decode('utf-8')
        soup = bs(contents, 'xml')
    return soup
def split_records(soup):
    """
    Extracts all 'VariationArchive' elements from a BeautifulSoup object.
        Xml file uses VariationArchive to demarcate a record
    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing XML data.
    Returns:
        list: A list of 'VariationArchive' elements found in the XML data.
    """
    variation_id = soup.find_all('VariationArchive')
    return variation_id

def extract_variation_id(record):
    """
    Extracts the variation ID from a 'VariationArchive' element.
    Args:
        record (Tag): A 'VariationArchive' element.
    Returns:
        str: The variation ID.
    """
    variation_id = record.get('VariationID')
    return variation_id
def extract_coordinates(record):
    """
    Extracts the coordinates from a 'VariationArchive' element.
    Args:
        record (Tag): A 'VariationArchive' element.
    Returns:
        tuple: The coordinates.
        None if no coordinates are found.
    """
    ASSEMBLY = "GRCh37"
    coordinates = record.find_all('SequenceLocation')
    coordinates = [x for x in coordinates if x.get('Assembly') == ASSEMBLY and \
                    x.get('positionVCF')]
    if coordinates:
        vcf_position = coordinates[0].get('positionVCF')
        vcf_reference = coordinates[0].get('referenceAlleleVCF')
        vcf_alternate = coordinates[0].get('alternateAlleleVCF')
        vcf_chromosome = coordinates[0].get('Chr')
        return (vcf_chromosome, vcf_position, vcf_reference, vcf_alternate)
    return 
def extract_review_status(record):
    """
    Extracts the review status from a 'VariationArchive' element.
    Args:
        record (Tag): A 'VariationArchive' element.
    Returns:
        list: The review status.
    """
    classifications = record.find_all('Classifications')
    review_status = [x.find_all('ReviewStatus') for x in classifications][0]
    review_status = [x.text for x in review_status]

    classification = [x.find_all('Description') for x in classifications][0]
    classification = [x.text for x in classification]

    return (classification, review_status)
def extract_conditions(record):
    """
    Extracts the conditions from a 'VariationArchive' element.
    Args:
        record (Tag): A 'VariationArchive' element.
    Returns:
        set: Conditions.
    """
    conditions = record.find_all('TraitSet')
    conditions = [x.find_all('Trait') for x in conditions]
    conditions = [x for sublist in conditions for x in sublist]
    conditions = [x.find_all('Name') for x in conditions]
    conditions = set([x.text.strip().upper() for sublist in conditions for x in sublist])
    return conditions
def process_record(record):
    """
    Processes a 'VariationArchive' element and extracts relevant information.
    Args:
        record (Tag): A 'VariationArchive' element.
    Returns:
        dict: A dictionary containing the extracted information.
    """
    variation_id = extract_variation_id(record)
    coordinates = extract_coordinates(record)
    review_status = extract_review_status(record)
    conditions = extract_conditions(record)
    return {"variation_id": variation_id,
            "coordinates": coordinates,
            "review_status": review_status,
            "conditions": list(conditions)}
def export_record(record, outfile):
    """
    Exports a record to a file.
    Args:
        record (dict): A dictionary containing the record information.
        outfile (str): The output file handle.
    """
    chrom, position, reference, alterate = record['coordinates']
    variation_id = record['variation_id']
    classification, review_status = record['review_status']
    conditions = record['conditions']
    outline = (f"{chrom}\t{position}\t{reference}\t{alterate}\t{variation_id}\t"
                f"{','.join(classification)}\t{','.join(review_status)}\t"
                f"{','.join(conditions)}\n")
    outfile.write(outline)

def main(args):
    soup = create_soup(args.i)
    variation_ids = split_records(soup)
    TOTAL_RECORDS = len(variation_ids)
    with open(args.o, 'w') as outfile:
        for lineno, var in enumerate(variation_ids, start = 1):
            if not lineno % 1000:
                print(f"Processed {lineno} records of {TOTAL_RECORDS}")
            record = process_record(var)
            export_record(record, outfile)

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)