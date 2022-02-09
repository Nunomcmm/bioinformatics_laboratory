"""Import all libraries that will be used."""
import sys

def valid_file(file):
    """
    Validate a FASTA file chosen by the user. Considers as header lines starting with '>'.

    Args:
        file: FASTA file.

    Raises:
        TypeError: Argument is of wrong type.
        TypeError: There is an invalid character in the sequence.
        ValueError: There are no values in one of the dictionary entries.
        IndexError: When the file wasn't entered as an argument.

    Returns:
        sequences: Returns a dictionary with all the different sequences that
        exist in the input FASTA file.
    """
    # Creating an empty dictionary
    sequences = {}

    # For each line in the file
    for line in file:
        # Copies the line without spaces at the beginning and at the end
        line = line.strip()
        # Check if line starts with '>'
        if line.startswith('>'):
            # Header receive the line
            header = line
            # Check if it already exists in dictionary
            if header not in sequences:
                sequences[header] = ''
                continue
        # Check if the line is blank
        elif line.strip() == '':
            # Remove spaces until next line
            line.lstrip()
            # raise SyntaxError('Many blank lines.')
        else:
            # Allowed characters for sequence Nucleic Acid Codes
            letters = 'ACGTURYKMSWBDHVN-*'
            # For each character in line
            for char in line:
                # Check if in allowed characters
                if char.upper() in letters:
                    continue
                # Raise TypeError if found an invalid character
                raise TypeError(
                    'An invalid character '
                    f'{char} was found in {line}.')
            # Assign sequence to header key
            sequences[header] += line.upper()
    # Check if there any empty value
    if '' in sequences.values():
        # Raise ValueError if exist
        raise ValueError(
            'There is a problem '
            'with one of the values.')
    # Check if dictionary is empty
    if not sequences:
        raise ValueError(
            'This file is empty.')
    # This message will appear when the file passes all previous tests
    print('The FASTA file was sucessfully validated.')
    # Return sequences dictionary
    return sequences


def dictionary_to_file(fasta):
    """
    Pass dictionary to file fasta.

    Args:
        fasta (dictionary): [description]

    Return:
        fasta_validated.fasta
    """
    # Create new file
    with open('fasta_validated.fasta', 'w', encoding='utf-8') as file_validated, \
    open('table_of_contents.txt', 'w', encoding='utf-8') as table_of_contents:
        # For each key, value in the dictionary items write in file
        for count, (key, value) in enumerate(fasta.items(), start=1):
            file_validated.write(f'>TAXA{count}\n{value}\n')
            table_of_contents.write(f'TAXA{count}|{key}\n')
    print('FASTA file created sucessfully.')

# Main
def main(infile):
    """In this function, all program steps will be executed."""
    with open(infile,'r',encoding='utf-8') as myfasta:
        fasta = valid_file(myfasta)
        dictionary_to_file(fasta)
        print('Validation finished.')


def inputs(arguments):
    """
    Check if the inputs are correct.

    Args:
        arguments (List): command line arguments.

    Raises:
        TypeError: when it doesn't have the corret extension.

    Returns:
        [str]: fasta file
    """
    if len(arguments) == 2:
        # Check if the file has the fasta extension
        if not arguments[1].endswith('.fasta' or '.fa'):
            # Raise TypeError when it doesn't have the corret extension
            raise TypeError('Argument is of wrong type.')
    # Check if exist more than two arguments
    elif len(arguments) > 2:
        print('Use only the fasta file as an argument.')
        # Exit the program with errors
        sys.exit(1)
    return arguments[1]


# This block only runs when the python file is called directly
if __name__ == '__main__':
    # Read input file
    try:
        input_file = inputs(sys.argv)
        main(input_file)
    except IndexError:
        print("It's necessary to choose a file.")
        # Exit the program with errors
        sys.exit(1)
    except FileNotFoundError:
        print("It's necessary to choose a file that exists.")
        # Exit the program with errors
        sys.exit(1)
