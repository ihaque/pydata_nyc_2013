POINTS = 10000000

all: random.txt benchmark_output

clean:
	rm -f random.txt random.h5 random.db random.json

random.txt:
	python generate_random_data.py random $(POINTS)

benchmark_output: random.txt
	python benchmark_reads.py random
