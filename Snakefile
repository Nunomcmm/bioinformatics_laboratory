inputfile = os.environ.get("INPUT")
outputdir = os.environ.get("OUTPUTDIR")
#command :  OUTPUTDIR="outputs" INPUT="tests/RAG_small.fasta" snakemake --cores all
#print(inputfile)

rule all:
    input:
        'fasta_validated.fasta',
        'table_of_contents.txt',
        f'{outputdir}/raxml/RAxML_bipartitionsBranchLabels.output_ML',
        f'{outputdir}/iqtree/standard_name.fasta.treefile',
        f'{outputdir}/compare/all_trees.treels',
        f'{outputdir}/mega/M11CC_Out/mega_tree.nwk',
        f'{outputdir}/compare/shimodaira_hasegawa.txt',
        f'{outputdir}/compare/AU_report.txt'
    message:
        'Runs sucessfully. Folders created with the respective files.'

# Clean outputs of previous runs
rule clean:
    shell:
        'rm -rf mega iqtree raxml fastas table_of_contents.txt compare outputs'

# Validate the file
rule valid_file:
    input:
        inputfile
    output:
        'fasta_validated.fasta',
        'table_of_contents.txt'
    shell:
        'python3 scripts/fasta_validator.py {input}'

# Standardize names 
rule standardized_name:
    input:
        'fasta_validated.fasta',
        'table_of_contents.txt'
    output:
        '{outputdir}/fastas/standard_name.fasta'
    run:
        shell(f'mkdir -p {outputdir}/fastas')
        shell('mv table_of_contents.txt {outputdir}')
        shell('sed "s/ .*//g" fasta_validated.fasta > {outputdir}/fastas/standard_name.fasta')

# Create trees raxml
rule create_trees_raxml:
    input:
        '{outputdir}/fastas/standard_name.fasta'
    output:
        '{outputdir}/raxml/RAxML_bipartitionsBranchLabels.output_ML'
    benchmark:
        '{outputdir}/raxml/raxml.bwa.benchmark.txt'
    run:
        shell('mkdir -p {outputdir}/raxml')
        shell('cd {outputdir}/raxml && time raxmlHPC-PTHREADS-SSE3 -T 2 -f a -s ../../{input} -m GTRGAMMA -x 2525 -p 2525 -N 100 -n output_ML')

# Create trees iqtree
rule create_trees_iqtree:
    input:
        '{outputdir}/fastas/standard_name.fasta'
    output:
        '{outputdir}/iqtree/standard_name.fasta.treefile'
    benchmark:
        '{outputdir}/iqtree/iqtree.bwa.benchmark.txt'
    run:
        shell('mkdir -p {outputdir}/iqtree')
        shell('cp {input} {outputdir}/iqtree/standard_name.fasta')
        shell('iqtree -s {outputdir}/iqtree/standard_name.fasta')

# Create trees mega
rule create_trees_mega:
    input:
        '{outputdir}/fastas/standard_name.fasta'
    output:
        '{outputdir}/mega/M11CC_Out/mega_tree.nwk'
    benchmark:
        '{outputdir}/mega/mega.bwa.benchmark.txt'
    run:
        shell('mkdir -p {outputdir}/mega')
        shell('cp {input} {outputdir}/mega/standard_name.fasta')
        shell('megacc -a files/ML_nucleotide.mao -d {outputdir}/mega/standard_name.fasta ML_tree_mega')
        shell('cat {outputdir}/mega/M11CC_Out/*.nwk > {output}')

# Concatenate all tree files
rule concatenate_trees_files:
    input:
        '{outputdir}/mega/M11CC_Out/mega_tree.nwk',
        '{outputdir}/iqtree/standard_name.fasta.treefile',
        '{outputdir}/raxml/RAxML_bipartitionsBranchLabels.output_ML'
    output:
        '{outputdir}/compare/all_trees.treels'
    run:
        shell('mkdir -p {outputdir}/compare')
        shell('cat {input} > {outputdir}/compare/all_trees.treels')

# Compare the trees using IQTree
rule compare_shimodaira_hasegawa:
    input:
        '{outputdir}/compare/all_trees.treels',
        '{outputdir}/fastas/standard_name.fasta'
    output:
        '{outputdir}/compare/shimodaira_hasegawa.txt'
    message:
        "In the eventuality of the AU scores being too similar, in their respective directories, it's accompanied the benchmarks of each tree with the times it took too create them."
        "Every user must consider this data when choosing the best program for themselfs."
    run:
        shell('iqtree -s {outputdir}/fastas/standard_name.fasta -z {outputdir}/compare/all_trees.treels -n 0 -zb 10000 -zw -au > {output}')

# Report of the AU test
rule report_AU:
    input:
        '{outputdir}/compare/shimodaira_hasegawa.txt'
    output:
        '{outputdir}/compare/AU_report.txt'
    message:
        'The results of the Au test'
    run:
        shell('grep "TreeID" -A 5 {input} > {output}')
        shell('printf "1 - MEGA\n2 - IQTREE\n3 - RAxML\n" >> {output}')
        shell('cat {output}')