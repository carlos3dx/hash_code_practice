#Hash Code 2021 practice example
This project is my attempt to solve the parctice round in 2021 Google's Hash Code competition (https://codingcompetitions.withgoogle.com/hashcode)

The provided files are inside the `doc` folder.

In this attempt I've tried to use an implementation of a genetic algorithm to solve each one of the proposed problems.

This program requires Python 3.9

The genetic algorithm approach can be executed with `python genetic_approach.py`

```
  -h, --help            show this help message and exit
  -i INPUT_FILE, --file INPUT_FILE
                        The file provided with the challenge as an input
  -f POPULATION_FILE, --initial POPULATION_FILE
                        The file with the initial population. Result of previous executions can be used.
  -x INITIAL_POP, --initial_pop INITIAL_POP
                        If not specified the file with the initial population, set the number of individuals to generate
  -m MAX_ITERATIONS, --max_iterations MAX_ITERATIONS
                        Number of iterations the program can be running
  -n NO_IMPROVE_STOP, --no_improve_stop NO_IMPROVE_STOP
                        If provided, the program will stop after n iterations without an improvement
  -s MAX_POP, --max_pop MAX_POP
                        Maximum number of individuals, if reachad, the ones with least score are removed
  -e EVOLUTION, --evolution EVOLUTION
                        Number between 0 and 100, probability of mutation
  -r OUTPUT_FILE, --result OUTPUT_FILE
                        Output file with the best result
  -p POPULATION_OUTPUT_FILE, --population POPULATION_OUTPUT_FILE
                        Output file with the population

```

Because the harder the problem, the longer it takes to compute, in each iteration of the algorithm the current best solution and population is saved.
