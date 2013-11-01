# Regenerate example HapMap data for pony_blanket_example.py

all: hapmap.txt

HAPMAP_SOURCE = ftp://ftp.ncbi.nlm.nih.gov/hapmap/frequencies/2010-08_phaseII+III/

allele_freqs_chrY_YRI_r28_nr.b36_fwd.txt:
	curl $(HAPMAP_SOURCE)/allele_freqs_chrY_YRI_r28_nr.b36_fwd.txt.gz | gunzip > allele_freqs_chrY_YRI_r28_nr.b36_fwd.txt

# Reduced copy of HapMap data
hapmap.txt: allele_freqs_chrY_YRI_r28_nr.b36_fwd.txt
	cut -f1,12,15 -d\  < allele_freqs_chrY_YRI_r28_nr.b36_fwd.txt > hapmap.txt
