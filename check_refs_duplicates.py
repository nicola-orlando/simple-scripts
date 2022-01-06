#!/bin/env python        

description = """
Scan the biber output to look for duplicate references based on the title. 
"""

import sys

list_of_titles = [] 

# solution from here https://www.techiedelight.com/find-duplicate-items-python-list/
def check_duplicates(input_list):
    print "Here the duplicates in your bib file"
    dup = [x for i, x in enumerate(input_list) if x in input_list[:i]]
    print(dup)  

def main():
    """
    Pass your biber output as input to the code
    Example of use 
    python check_refs_duplicates.py ../ANA-HDBS-2019-24-PAPER.bbl
    """
    args = sys.argv[1:]
    print "Opening biber output %s"%args[0]
    
    input_file = args[0]
    
    with open(input_file) as file_bib:
        lines = file_bib.readlines()
        for line in lines :
            if "field{title}" in line:
                lenght = len( line.split("title}{{") )
                title_paper=0
                
                # booklets and such (have just one bracket)
                if lenght == 1:
                    title_paper = line.split("title}{")[1].split("}")[0]
                # actual papers
                if lenght == 2: 
                    title_paper = line.split("title}{{")[1].split("}}")[0]
            
                list_of_titles.append(title_paper)

        check_duplicates(list_of_titles)

if __name__ == '__main__':
    main()
