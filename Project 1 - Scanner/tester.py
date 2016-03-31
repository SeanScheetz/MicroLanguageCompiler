from lexer import lexer
import sys

def main(source_file, token_file):
	for t in lexer(source_file, token_file):
		print(t)

if __name__ == "__main__":
	main(*sys.argv[1:])