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
present_pos[i,1] <= paper_shape[1] - present_rot(i,1) /\ (present_pos[i,2] <= paper_shape[2] - present_rot(i,2)));

% extensive search in the documentation lead to find the perfect constraint to represent the problem
% predefined global constraints are efficently implemented and have to be privileged
% it expresses the rectangle non-overlapping constraint
constraint diffn(present_pos[1..n,1], present_pos[1..n,2], 
                [present_rot(i,1) | i in 1..n], [present_rot(i,2) | i in 1..n]);


% ======== PARTIAL SUMS IMPLIED CONSTRAINT ========

% tentative custom approach:

% compute the partial sums for each column and row
%array[1..paper_shape[2]] of var int: sum_col = [sum(i in 1..n)(
%if (j >= present_pos[i,1] /\ j < present_pos[i,1] + present_rot(i,1)) then present_rot(i,2) else 0 endif) | j in 1..paper_shape[2]];

%array[1..paper_shape[1]] of var int: sum_row = [sum(i in 1..n)(
%if ( j >= present_pos[i,2] /\ j < present_pos[i,2] + present_rot(i,2)) then present_rot(i,1) else 0 endif) | j in 1..paper_shape[1]];

% constrain the sums to not exceed the respective dimension
%constraint forall(i in 1..paper_shape[2])(sum_col[i] <= paper_shape[2]);
%constraint forall(i in 1..paper_shape[1])(sum_row[i] <= paper_shape[1]);


% global approach:

constraint cumulative(present_pos[1..n,1],
                      present_shape[1..n,1],
                      present_shape[1..n,2],
                      paper_shape[2]);
                      
constraint cumulative(present_pos[1..n,2],
                      present_shape[1..n,2],
                      present_shape[1..n,1],
                      paper_shape[1]);

% symmetry breaking by fixing the first present in the first quadrant

constraint forall(j in 1..2)(present_pos[1,j] < (paper_shape[j])/2);   

%constraint lex_lesseq(present_pos[1..n,1], [paper_shape[1] - present_pos[i,1] + present_shape[i,1]| i in 1..n]);
%constraint lex_lesseq(present_pos[1..n,2], [paper_shape[2] - present_pos[i,2] + present_shape[i,2]| i in 1..n]);
%constraint lex_lesseq(array1d(present_pos[1..n,1..2]),
                      %array1d(array2d(1..n,1..2,[paper_shape[j] - present_pos[i,j] + present_shape[i,j]| j in 1..2, i in 1..n])));
%constraint lex_lesseq(present_pos[1..n,1..2], [paper_shape[1] - present_pos[i,1] + present_shape[i,1]| i in 1..n]);

%constraint lex_lesseq(array1d([present_pos[i,j] | j in 1..2, i in 1..n]),
 %                     array1d(array2d(1..n,1..2,
  %                    [if (j mod 2 == 0 ) then paper_shape[1] - present_pos[i,1] + present_shape[i,1] else                              
   %                   present_pos[i,2] endif | j in 1..2, i in 1..n]))
    %                  );
                      
%constraint lex_lesseq([present_pos[i,j] |i in 1..n, j in 1..2],
 %                     [if (j mod 2 == 1 ) then paper_shape[2] - present_pos[i,2] + present_shape[i,2] else                              
  %                    present_pos[i,1] endif |i in 1..n, j in 1..2 ]);
                      
                      
%constraint lex_lesseq(array1d([present_pos[i,j] |i in 1..n, j in 1..2, ]),
 %                     array1d(array2d(1..n,1..2,
  %                    [if (j mod 2 == 1 ) then paper_shape[1] - present_pos[i,1] + present_shape[i,1] else                              
   %                   present_pos[i,2] endif |i in 1..n, j in 1..2]))
    %                  );                                                                
                      
% second term must be the present_po array with mod x and SAME y

% 6: multiple pieces with same dimension
%array delle posizioni dei pezzi uguali

%array[1..n,1..2] of var 1..2: x;

%x (1,2) (30,4) ok
%x (30,4) (1,2) not ok

%constraint lex_lesseq(x, reverse(x));

% search heuristics
% first fail with indomain_min for each coordinate
% search_ann_y expecially helps due to the great asymmetry of the instancess
ann: search_ann_y;
search_ann_y = int_search(present_pos[1..n,2], first_fail, indomain_min);
ann: search_ann_x;
search_ann_x = int_search(present_pos[1..n,1], first_fail, indomain_min); 

solve :: search_ann_y :: search_ann_x satisfy;

output [ "[\(present_pos[i,1]), \(present_pos[i,2]) \(rotations[i])], " | i in 1..n ];
%output ["\(present_pos[i,j])" | i in 1..n, j in 1..2] 
