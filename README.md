# Present-Wrapping-Problem
### Marco Buiani & Daniele Verì
The Present Wrapping problem can be viewed as finding the position of rectangular pieces in order to fit them into the available rectangular paper shape without overlap and rotation.
In this project we present solutions with MiniZinc Constraint Programming modelling, SMT and SAT modelling with Microsoft Z3 solver.  

<img width="896" alt="Schermata 2022-04-22 alle 13 40 56" src="https://user-images.githubusercontent.com/38630200/164708216-c56a7ca2-bb68-4336-869b-8001ca1ccfbc.png">

**Instructions for launching:**

### CP in MiniZinc:  [Report](cp/report.pdf)

run `cp_solver.mzn` from the Minizinc IDE,
.dzn converted instances are provided inside the `cp/instances/` folder

### SMT in Z3:  [Report](smt/report.pdf)
. `python3 smt/src/smt_solver.py smt/instances/<instance.txt>` produces output to the terminal

. `python3 smt/src/smt_solver.py smt/instances/<instance.txt> -o` creates output file in the same folder as input

. `python3 smt/src/smt_solver.py smt/instances/<instance.txt> --allow_rotations` allows rotation of each present

. `python3 smt/src/smt_solver.py smt/instances/<instance.txt> -v` produces a png image of the solution (requires python pillow)


### SAT in Z3:  [Report](sat/report.pdf)
. `python3 sat/src/sat_solver.py sat/instances/<instance.txt>` produces output to the terminal
