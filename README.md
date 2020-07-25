# Present-Wrapping-Problem
### Marco Buiani & Daniele Verì

**Instructions for launching:**

- CP in MiniZinc

run `cp_solver.mzn` from the Minizinc IDE,
.dzn converted instances are provided inside the `Instances_dzn/` folder

- Z3


SMT:  
. `python3 smt_solver.py /Instances_txt/<instance.txt>` produces output to the terminal  

. `python3 smt_solver.py /Instances_txt/<instance.txt> -o` creates output file in the same folder as input  

. `python3 smt_solver.py /Instances_txt/<instance.txt> -v` produces a png image of the solution (requires python pillow)

SAT:
. `python3 sat_solver.py /Instances_txt/<instance.txt>` produces output to the terminal

