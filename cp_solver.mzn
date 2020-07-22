% project present-wrapping-problem
% 
include "globals.mzn";

% cuts indicated with xiyi position of the present by bottom left corner

% a quadruple l,h,x,y suffices to state where the piece is in the paper
% with l,h fixed for each piece, while x,y are the proper variables
% how to implement this in minizinc?

% so in reality the decision variable array is a nx2 with the xy pos of
% and we have a correspondinf nx2 input parameters array + n + l,h of the total paper

% input intake
array[1..2] of int: paper_shape;
int: n;
array[1..n,1..2] of int: present_shape;


%bottom left corner position for each present
array[1..n,1..2] of var 0..max(paper_shape): present_pos;

% each rectagle can have just 2 possible rotations
array[1..n] of var bool: rotations = [false | i in 1..n];
% TODO stop squares rotation by fixing tots to 1

% We can check the input for a first global criterion:
% the total area of presents cannot exceed the availabel paper area
int: paper_area = paper_shape[1] * paper_shape[2];
int: paper_needed = sum(i in 1..n)(present_shape[i,1] * present_shape[i,2]);
constraint assert(paper_needed <= paper_area,"Paper area isn't sufficient!");
                            
function var int : present_rot(int: i, int: j) = if rotations[i] then present_shape[i, 3-j] else present_shape[i,j] endif;


% bottom_left corner of each piece can't go outside of the paper
constraint forall(i in 1..n)(
present_pos[i,1] <= paper_shape[1] - present_rot(i,1) /\ (present_pos[i,2] <= paper_shape[2] - present_rot(i,2)) );

% extensive search in the documentation lead to find the perfect constraint to represent the problem
% predefined global constraints are fast and have to be privileged
constraint diffn(present_pos[1..n,1], present_pos[1..n,2], 
                [present_rot(i,1) | i in 1..n], [present_rot(i,2) | i in 1..n]);

%constraint all_different(  [pow(2,present_pos[i,1]) * pow(3,present_pos[i,2]) | i in 1..n]   );

%constraint all_different([{present_pos[i,j] | j in 1..2} | i in 1..n]);


%set of int: '..'(present_pos[i,1],present_pos[i,2])
% implied constraint
% In any solution, if we draw a vertical line and sum the vertical sides of the traversed pieces, 
% the sum can be at most l. A similar property holds if we draw a horizontal line. 
% Use these implied constraints in both of your CP model and SAT/SMT encoding

% sommare solo le variabili che hanno la x nel dominio analizzato

% somme parziali sulle colonne
array[1..paper_shape[2]] of var int: sum_col = [sum(i in 1..n)( % y
if (j >= present_pos[i,1] /\ j < present_pos[i,1] + present_rot(i,1)) then present_rot(i,2) else 0 endif) | j in 1..paper_shape[2]];

array[1..paper_shape[1]] of var int: sum_row = [sum(i in 1..n)( % x
if ( j >= present_pos[i,2] /\ j < present_pos[i,2] + present_rot(i,2)) then present_rot(i,1) else 0 endif) | j in 1..paper_shape[1]];

%array[1..n] loadx of var int = [paper_shape[1] | i in 1..n];
 
%constraint bin_packing_load(loadx,
%                           array [int] of var int: bin,
%                           array [int] of int: w)

% scorrelati allora non migliori niente
constraint forall(i in 1..paper_shape[2])(trace("\(i) ",sum_col[i] <= paper_shape[2]));
constraint forall(i in 1..paper_shape[1])(sum_row[i] <= paper_shape[1]);

% predicate bin_packing(int: c,
%                      array [int] of var int: bin, la colonna...
%                     array [int] of int: w)

% global implied attempt
% constraint bin_packing(paper_shape[1], present_pos[1..n,1], present_shape[1..n,1]); 
% constraint bin_packing(paper_shape[2], present_pos[1..n,2], present_shape[1..n,2]);

% ognuna delle somme non può superare una capacity


% forbid small spaces, assuming solution does not allow them
%la somma di ogni riga non deve fare 0<paper_shape - minshape
%constraint forall(i in 1..paper_shape[2])(paper_shape[2] - sum2[i] <= min_shape[2] \/ paper_shape[2] - sum2[i] =0)

%array[1..2] of int: min_shape  = [arg_min(present_shape[1..n,1]), arg_min(present_shape[1..n,2])];

%nope
%constraint lex_lesseq([present_pos[i,1]| i in 1..n], 
%                      [(paper_shape[1] - present_shape[i,1] - present_pos[i,1])| i in 1..n]);

%constraint lex_lesseq([present_pos[i,2]| i in 1..n], 
%                      [(paper_shape[2] - present_shape[i,2] - present_pos[i,2])| i in 1..n]);

% to chose a specific part is heuristic in itself

constraint present_pos[1,1] < (paper_shape[1] - present_rot(1,1))/2;
constraint present_pos[1,2] < (paper_shape[2] - present_rot(1,2))/2;    



%constraint lex_lesseq([present_pos[i,j]| i in 1..n ,j in 1..2], 
%                      [present_pos[i,j]| i in 1..n ,j in 1..2]);

% rimuovere tutti gli interstizi
%var array[1..paper_shape[1],1..paper_shape[2]]: row = 


% rettangoli adiacenti: ogni x di vertice deve essere almeno una xur


% search heuristics

ann: search_ann;
%search_ann = int_search(present_pos, input_order, indomain_min); % 12x12 44674
%search_ann = int_search(present_pos[1..n,1], input_order, indomain_min); %12x12 24825 | 14x14-404442
%search_ann = int_search(present_pos[1..n,2], input_order, indomain_min); %12x12 628280 | 14x14-6204
%search_ann = int_search(present_pos, first_fail, indomain_min); %f359473
search_ann = int_search(present_pos[1..n,2], first_fail, indomain_min);

%search_ann = int_search(present_pos, dom_w_deg, indomain_min); % 350814
%search_ann = int_search(present_pos, input_order, indomain_random); %53793
%search_ann = int_search(present_pos, dom_w_deg, indomain_random); %408105
ann: search_ann2;
search_ann2 = int_search(present_pos[1..n,1], first_fail, indomain_min); 

ann: restart_ann;
restart_ann = restart_linear(10);

solve :: search_ann :: search_ann2 satisfy;

output [ "[\(present_pos[i,1]), \(present_pos[i,2]) \(rotations[i])], " | i in 1..n ];


