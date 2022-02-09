"""Import all libraries that will be used."""
import sys
from contextlib import contextmanager
from io import StringIO
import pytest
from scripts.fasta_validator import inputs, valid_file, dictionary_to_file, main

@contextmanager
def captured_output():
    """Before each test, capture the sys.stdout and sys.stderr."""
    # compare the outputs
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def test_inputs():
    """Test input."""
    infile = 'tests/RAG1_alinhadas.fasta'
    assert infile == inputs(['fasta_validator.py', infile])

def test_inputs_except1():
    """Test input exception."""
    arguments = ['scripts/fasta_validator.py', 'tests/RAG_small.txt']
    with pytest.raises(TypeError):
        inputs(arguments)

def test_inputs_len():
    """Test input length."""
    arguments = ['scripts/fasta_validator.py', 'tests/RAG_small.txt', 'test']
    with pytest.raises(SystemExit):
        inputs(arguments)

def test_valid_file():
    """Test valid file that passes."""
    # opens file RAG1_alinhadas.fasta
    with open('tests/RAG1_alinhadas.fasta', 'r', encoding="utf-8") as file:
        #receives the output
        with captured_output() as (out, err):
            valid_file(file)
        lines = out.getvalue().splitlines()
        #returns that the Fasta file got validated
        assert['The FASTA file was sucessfully validated.'] == lines


def test_valid_file2():
    """Test valid file that passes."""
    # opens file S7RP_alinhadas.fasta
    with open('tests/S7RP_alinhadas.fasta', 'r', encoding="utf-8") as file:
        #receives the output
        with captured_output() as (out, err):
            valid_file(file)
        lines = out.getvalue().splitlines()
        #returns that the Fasta file got validated
        assert['The FASTA file was sucessfully validated.'] == lines

def test_valid_valid_file3():
    """Test valid file that passes."""
    # opens file TBR1_alinhadas.fasta
    with open('tests/TBR1_alinhadas.fasta', 'r', encoding="utf-8") as file:
        #receives the output
        with captured_output() as (out, err):
            valid_file(file)
        lines = out.getvalue().splitlines()
        #returns that the Fasta file got validated
        assert['The FASTA file was sucessfully validated.'] == lines

def test_valid_randomfiles():
    """Test valid file that doesn't pass."""
    # opens file Book.fasta
    with open('tests/Book.fasta', 'r', encoding="utf-8") as file1, \
        open('tests/RAG1_valueerror.fasta', 'r', encoding="utf-8") as file2, \
        open('tests/RAG1_empty.fasta', 'r', encoding="utf-8") as file3, \
        open('tests/RAG1_failed.fasta', 'r', encoding="utf-8") as file4:
        with pytest.raises(TypeError):
            valid_file(file1)
        with pytest.raises(ValueError):
            valid_file(file2)
        with pytest.raises(ValueError):
            valid_file(file3)
        with pytest.raises(TypeError):
            valid_file(file4)

def test_valid_randomfile2():
    """Test valid file that doesn't pass."""
    # opens file RAG1_blanklines.fasta
    with open('tests/RAG_blanklines.fasta', 'r', encoding="utf-8") as file:
        #receives the output
        with captured_output() as (out, err):
            valid_file(file)
        lines = out.getvalue().splitlines()
        #returns that the Fasta file got validated
        assert['The FASTA file was sucessfully validated.'] == lines

def test_dictionary_to_file():
    """Test valid dictionary that passes."""
    dictionary_tests = {'1':'ABCDEFG',
                        '2':'ACTGATCG',
                        '3':'ACHTATCGAA'}
    with captured_output() as (out, err):
        dictionary_to_file(dictionary_tests)
    lines = out.getvalue().splitlines()
    #returns that the Fasta file got validated
    assert['FASTA file created sucessfully.'] == lines

def test_main_fasta_validator():
    """Test valid file that pass."""
    # opens file RAG_small.fasta
    infile = 'tests/RAG_small.fasta'
    # receives the output
    with captured_output() as (out, err):
        main(infile)
    lines = out.getvalue().splitlines()
    #returns that the Fasta file got validated
    assert['The FASTA file was sucessfully validated.', \
        'FASTA file created sucessfully.', 'Validation finished.'] == lines
