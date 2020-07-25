% present-wrapping-problem cp solver
include "globals.mzn";

% read inputs from .dzn file
array[1..2] of int: paper_shape;
int: n;
array[1..n,1..2] of int: present_shape;

% bottom left corner position for each present
% domain constrained to be a positive int below paper dimensions
array[1..n,1..2] of var 0..max(paper_shape): present_pos;

% each rectagle can have just 2 possible rotations
array[1..n] of var bool: rotations = [false | i in 1..n]; % uncomment to disallow rotations

% check input for a first global area criterion:
% the total area of presents cannot exceed the available paper area
int: paper_area = paper_shape[1] * paper_shape[2];
int: paper_needed = sum(i in 1..n)(present_shape[i,1] * present_shape[i,2]);
constraint assert(paper_needed <= paper_area,"Paper area isn't sufficient!");
          
% returns the present measure according to the rotation state
function var int : present_rot(int: i, int: j) = if rotations[i] then present_shape[i, 3-j] else present_shape[i,j] endif;


% ======== CORE PROBLEM CONSTRAINTS ========
% presents cannot fall outside of the paper
constraint forall(i in 1..n)(
present_pos[i,1] <= paper_shape[1] - present_rot(i,1) /\ (present_pos[i,2] <= paper_shape[2] - present_rot(i,2)) );

% extensive search in the documentation lead to find the perfect constraint to represent the problem
% predefined global constraints are efficently implemented and have to be privileged
% it expresses the rectangle non-overlapping constraint
constraint diffn(present_pos[1..n,1], present_pos[1..n,2], 
                [present_rot(i,1) | i in 1..n], [present_rot(i,2) | i in 1..n]);


% ======== SUGGESTED IMPLIED CONSTRAINT ========

% compute the partial sums for each column and row
array[1..paper_shape[2]] of var int: sum_col = [sum(i in 1..n)(
if (j >= present_pos[i,1] /\ j < present_pos[i,1] + present_rot(i,1)) then present_rot(i,2) else 0 endif) | j in 1..paper_shape[2]];

array[1..paper_shape[1]] of var int: sum_row = [sum(i in 1..n)(
if ( j >= present_pos[i,2] /\ j < present_pos[i,2] + present_rot(i,2)) then present_rot(i,1) else 0 endif) | j in 1..paper_shape[1]];

% constrain the sums to not exceed the respective dimension
constraint forall(i in 1..paper_shape[2])(sum_col[i] <= paper_shape[2]);
constraint forall(i in 1..paper_shape[1])(sum_row[i] <= paper_shape[1]);

% symmetry breaking by fixing the first present in the first quadrant
constraint present_pos[1,1] < (paper_shape[1] - present_rot(1,1))/2;
constraint present_pos[1,2] < (paper_shape[2] - present_rot(1,2))/2;    


% search heuristics
% first fail with indomain_min for each coordinate
% search_ann_y expecially helps due to the great asymmetry of the instancess
ann: search_ann_y;
search_ann_y = int_search(present_pos[1..n,2], first_fail, indomain_min);
ann: search_ann_x;
search_ann_x = int_search(present_pos[1..n,1], first_fail, indomain_min); 

solve :: search_ann_y :: search_ann_x satisfy;

output [ "[\(present_pos[i,1]), \(present_pos[i,2]) \(rotations[i])], " | i in 1..n ];
