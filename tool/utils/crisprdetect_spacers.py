from pathlib import Path
import os
from .parallel import Parallel

tool_path = Path(__file__).parent.parent.joinpath('bin/crisprdetect/CRISPRDetect.pl')

def run(args):
	input_file, output_file = args
	oh = open(output_file, 'w')
	cmd = f'perl {tool_path} -f {input_file} -o {output_file} -array_quality_score_cutoff 3 1> /dev/null 2> /dev/null'
	os.system(cmd)
	oh.close()
	return output_file

def parse(args):
	input_file, output_file = args
	fh = open(input_file)
	oh = open(output_file, 'w')
	l=[]
	count_spacers = 1
	for line in fh:
		if line.startswith("  Position"):
			for line in fh:
				if line == '\n':
					break
				if not line.startswith('='):
					column = line.split()
					if (len(column))==6:
						l.append(column[-1])
					if (len(column))==7:
						l.append(column[-2])
					if (len(column))==8:
						l.append(column[-3])
					if (len(column))==9:
						l.append(column[-4])
					if (len(column))==10:
						l.append(column[-5])
			l.pop()
			for spacer in l:
				if len(spacer)>=15:
					accession_number = str(output_file).split('/')[-1].replace('.fa','')
					oh.write (f'>{accession_number}|{count_spacers}\n')
					oh.write (f'{spacer}\n')
					count_spacers += 1
			l=[]
			
	fh.close()
	oh.close()
	if output_file.stat().st_size == 0:
		os.system(f'rm {output_file}')
	return output_file

def run_dir(input_dir, output_dir, num_threads):
	args = []
	for input_file in input_dir.iterdir():
		output_file = output_dir.joinpath(f'{input_file.stem}.txt')
		args.append((input_file, output_file))
	job = Parallel(run, args, n_jobs=num_threads)
	os.system(f'rm {output_dir}/*.fp')
	os.system(f'rm {output_dir}/*.gff')


def parse_dir(input_dir, output_dir, num_threads):
	args = []
	for input_file in input_dir.iterdir():
		output_file = output_dir.joinpath(f'{input_file.stem}.fa')
		args.append((input_file, output_file))
	job = Parallel(parse, args, n_jobs=num_threads)