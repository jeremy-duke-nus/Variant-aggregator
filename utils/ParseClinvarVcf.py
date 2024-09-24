import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', required=True, help="Input Clinvar VCF file")
parser.add_argument('-o', required=True, help="Output file")

def main(args):
    with open(args.o, 'w') as outfile:
        outfile.write(('chrom\tposition\treference\talternate\t'
                        'variation_id\tassertions\treview_status\tdisease\n'))
        try:
            with open(args.i) as infile:
                for line in infile:
                    if not line.startswith('#'):
                        data = line.strip().split('\t')
                        chromosome, position, variant_id, reference, alternate = data[0:5]
                        info = data[7].split(';')
                        review_status = [x.split('=')[1] for x in info if x.startswith('CLNREVSTAT')]
                        assertions = [x.split('=')[1] for x in info if x.startswith('CLNSIG')]
                        conditions = [x.split('=')[1] for x in info if x.startswith('CLNDN')]
                        outline = '\t'.join([chromosome, position, reference, alternate, variant_id, 
                                            ','.join(assertions), ','.join(review_status), ','.join(conditions)])
                        outfile.write(outline + '\n')
        except IOError:
            raise

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)