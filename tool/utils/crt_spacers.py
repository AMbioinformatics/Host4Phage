from pathlib import Path
import os
from .parallel import Parallel

tool_path = Path(__file__).parent.parent.joinpath('bin/crt/crt.jar')

def run(args):
	input_file, output_file = args
	oh = open(output_file, 'w')
	cmd = f'java -cp {tool_path} crt {input_file} {output_file} 1> /dev/null 2> /dev/null'
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
		if line.startswith("POSITION"):
			for line in fh:
				if line == '\n':
					break
				if not line.startswith('-'):
					column = line.split()
					if column[-1] == ']':
						l.append(column[2])
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

def parse_dir(input_dir, output_dir, num_threads):
	args = []
	for input_file in input_dir.iterdir():
		if input_file.stat().st_size != 0:
			output_file = output_dir.joinpath(f'{input_file.stem}.fa')
			args.append((input_file, output_file))
	job = Parallel(parse, args, n_jobs=num_threads)