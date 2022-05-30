import argparse
import multiprocessing
import os
from pathlib import Path
from tqdm import tqdm

from utils import crisprdetect_spacers, crt_spacers, piler_spacers, minced_spacers


def command_spacers(args):

	input_dir = Path(args.input)
	output_dir = Path(args.output)

	output_raw = output_dir.joinpath('output')
	output_fa = output_dir.joinpath('fasta')
	output_raw.mkdir(parents=True, exist_ok = True)
	output_fa.mkdir(parents=True, exist_ok = True)

	if args.method == 'piler':
		print('Runnning Piler..')
		piler_spacers.run_dir(input_dir, output_raw, num_threads=args.threads)
		print('Parsing Piler..')
		piler_spacers.parse_dir(output_raw, output_fa, num_threads=args.threads)

	if args.method == 'crt':
		print('Runnning CRT..')
		crt_spacers.run_dir(input_dir, output_raw, num_threads=args.threads)
		print('Parsing CRT..')
		crt_spacers.parse_dir(output_raw, output_fa, num_threads=args.threads)

	if args.method == 'minced':
		print('Runnning MinCED..')
		minced_spacers.run_dir(input_dir, output_raw, num_threads=args.threads)
		print('Parsing MinCED..')
		minced_spacers.parse_dir(output_raw, output_fa, num_threads=args.threads)

	if args.method == 'crisprdetect':
		print('Runnning CRISPRDetect..')
		crisprdetect_spacers.run_dir(input_dir, output_raw, num_threads=args.threads)
		print('Parsing CRISPRDetect..')
		crisprdetect_spacers.parse_dir(output_raw, output_fa, num_threads=args.threads)

def command_compare(args):

	output_dir = Path(args.output)
	output_dir.mkdir(parents=True, exist_ok=True)

	spacer_dir = output_dir.joinpath('spacers')
	spacer_dir.mkdir(parents=True, exist_ok=True)

	for f in spacer_dir.iterdir():
		f.unlink()

	for spacer_method in args.spacers:
		path = Path(spacer_method)
		print(f'Reading {path.name}..')
		for f in tqdm(list(path.rglob('*'))):
			if f.suffix in ['.fa', '.fna', '.fasta']:
				oh = open(spacer_dir.joinpath(f.name),'a')
				fh = open (f)
				for count, spacer in enumerate(fh,start=1): 
					if count%2 == 0: 
						if len(spacer) >= args.k: 
							oh.write('>\n') 
							oh.write(f'{spacer}') 
				fh.close()
				oh.close()

	for f in spacer_dir.iterdir(): 
		if f.stat().st_size == 0:
			f.unlink()
	
	virus_paths_file = output_dir.joinpath('virus_paths.txt')
	virus_dir = Path(args.viral_genomes)
	oh = open(virus_paths_file,'w')
	for f in virus_dir.iterdir():
		oh.write(f'{f}\n')
	oh.close()

	spacer_paths_file = output_dir.joinpath('host_paths.txt')
	oh = open(spacer_paths_file,'w')
	for f in spacer_dir.iterdir():
		oh.write(f'{f}\n')
	oh.close()

	print('Runnning kmer-db..')
	tool_path = Path(__file__).parent.joinpath('bin/kmer-db/kmer-db')

	print('Creating the virus database..')
	virus_db = output_dir.joinpath('virus.db')
	cmd = f'{tool_path} build -k {args.k} -t {args.threads} {virus_paths_file} {virus_db}'
	os.system(cmd)

	print('Comparison..')
	final_output = output_dir.joinpath('output_kmer-db.csv')
	cmd = f'{tool_path} new2all -t {args.threads} {virus_db} {spacer_paths_file} {final_output}'
	os.system(cmd)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='\'spacers\' - identification and extraction of CRISPR spacers, '\
	'\'compare\' - comparison of k-mers (hosts with bacteriophages)')

parser_spacers = subparsers.add_parser('spacers', description='Identification and extraction of CRISPR spacers',
	help='For more information: \'host4phage.py spacers -h\'')
parser_spacers.add_argument('-i', '--i','-input','--input',  dest='input', required=True,
	help='Input: path to the directory containing bacterial genomes - files with the fa/fna/fasta extension')
parser_spacers.add_argument('-m', '--m', '-method', '--method', dest='method', required=True, 
	help='method: piler/crt/minced/crisprdetect')
parser_spacers.add_argument('-t', '--t', '-threads', '--threads', dest='threads', type=int, 
	default= multiprocessing.cpu_count(), help='Threads: number of threads')
parser_spacers.add_argument('-o', '--o','-output','--output',  dest='output', default='spacers',
	help='Output: path to the directory where output folders will be saved')
parser_spacers.set_defaults(function=command_spacers)

parser_compare = subparsers.add_parser('compare', description='Comparison of k-mers (hosts with bacteriophages)',
	help='For more information: \'host4phage.py compare -h\'')
parser_compare.add_argument('-s', '--s', '-spacers','--spacers', dest='spacers', nargs='+', required=True, 
	help='Bacterial_spacers: path to the directory containing CRISPR spacers found in bacteria - files with the fa/fna/fasta extension')
parser_compare.add_argument('-v', '--v', '-virus','--virus', dest='viral_genomes', required=True,
	help='Virus_genomes: path to the directory containing viral genomes - files with the fa/fna/fasta extension')
parser_compare.add_argument('-k', '--k', dest='k', type=int, default=18,
	help='k-length - viral genomes and CRISPR spacers found in hosts will be divided into sequences of that length')
parser_compare.add_argument('-t', '--t', '-threads', '--threads', dest='threads', type=int, 
	default= multiprocessing.cpu_count(), help='Threads: number of threads')
parser_compare.add_argument('-o', '--o', '-output', '--output', dest='output', default='comparison',
	help='Output: path to the directory where files and output folders will be saved')
parser_compare.set_defaults(function=command_compare)

args = parser.parse_args()

if hasattr(args, 'function'):
	print(f'Available threads: {args.threads}')
	args.function(args)
else:
	parser.print_help()



