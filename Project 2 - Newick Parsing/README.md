Sean Scheetz

## Modified Grammar
I slightly modifed your Grammar to the following:
T -> S;

S -> \w+ | (SLIST)\w+

SLIST -> S {, S}

I did this because it was slightly easier for me to visualize and because you said it was okay if we forced all nodes to be labeled.

## Notes

- api_tester.py is your unit tests

- tester.py is the file I used to tests my methods as I worked

- I was returning the message of the ParserException for my unit tests. You were looking to see if an exception was raised.
I conformed my code to fit yours (only a 1 line change), but if you happen to be curious what my tests were change "raise pe"
in line 62 of parse_newick to "return pe.msg". There is a comment on that line with this same info.

- This does assume the tree at least has 1 node.

- Multiple alphanumeric character labels are accepted, but every node must have a label. I remember you saying that was okay in class.