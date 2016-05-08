import sys
import argparse
import MLparser
import code_generator

def compiler(source, tokens, output):
	t, s = MLparser.parser(source, tokens)
	print(t)
	outfile = open(output, "w")

	stringLitList = {}
	programCountDict = {"count": 0} #used to keep track of subprograms
	ifWhileStack = []

	G = code_generator.traverse_tree(t)
	outfile.write("\t.data\n")  # start of the data section
	outfile.write("prompt_int:\t.asciiz\t\"Enter an int to store in a variable: \"\n")
	for node in G:
		code_generator.generate_data(node, s, outfile, stringLitList)

	G = code_generator.traverse_tree(t)
	outfile.write("\n")
	outfile.write("\t.text\n")  # start of the data section
	for node in G:
		code_generator.generate_text(node, s, outfile, stringLitList, programCountDict, ifWhileStack)

# Only true if compiler.py invoked from the command line
if __name__ == "__main__":

	# e.g. python3.5 compiler.py -t tokens.txt source.txt out.asm
	# Use the argparse library to parse the commandline arguments
	parser = argparse.ArgumentParser(description = "Group10 micro-language compiler")
	parser.add_argument('-t', type = str, dest = 'token_file',
					   help = "Token file", default = 'tokens.txt')
	parser.add_argument('source_file', type = str,
						help = "Source-code file", default = 'source.txt')
	parser.add_argument('output_file', type = str,
						help = 'output file name', default = "out.asm")

	args = parser.parse_args()

	# Call the compiler function
	compiler(args.source_file, args.token_file, args.output_file)