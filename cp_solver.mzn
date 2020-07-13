% project present-wrapping-problem
% 
include "globals.mzn";
% cuts indicated with xiyi position of the present by bottom left corner

% a quadruple l,h,x,y suffices to state where the piece is in the paper
% with l,h fixed for each piece, while x,y are the proper variables
% how to implement this in minizinc?

% so in reality the decision variable array is a nx2 with the xy pos of
% and we have a correspondinf nx2 input parameters array + n + l,h of the total paper

array[1..2] of int: paper_shape;
int: n;
array[1..n,1..2] of int: present_shape;

%bottom left corner position for each present
array[1..n,1..2] of var int: present_pos;

% We can check the input for a first global criterion:
% the total area of presents cannot exceed the availabel paper area
int: paper_area = paper_shape[1] * paper_shape[2];
int: paper_needed = sum(i in 1..n)(present_shape[i,1] * present_shape[i,2]);
constraint paper_needed <= paper_area;

% bottom_left corner of each piece can't go outside of the paper
constraint forall(i in 1..n)(0 <= present_pos[i,1] /\ (present_pos[i,1] <= paper_shape[1] - present_shape[i,1]) /\
                             0 <= present_pos[i,2] /\ (present_pos[i,2] <= paper_shape[2] - present_shape[i,2]) );

% extensive search in the documentation lead to find the perfect constraint to represent the problem
% predefined global constraints are fast and have to be privileged
constraint diffn(present_pos[1..n,1], present_pos[1..n,2], present_shape[1..n,1], present_shape[1..n,2]);

% implied constraint
% In any solution, if we draw a vertical line and sum the vertical sides of the traversed pieces, 
% the sum can be at most l. A similar property holds if we draw a horizontal line. 
% Use these implied constraints in both of your CP model and SAT/SMT encoding

% sommare solo le variabili che hanno la x nel dominio analizzato

% forbid small spaces, assuming solution does not allow them
array[1..2] of int: min_shape  = [arg_min(present_shape[1..n,1]), arg_min(present_shape[1..n,2])];

var int: sum1 = sum(i in 1..n)(
if ( i >= present_pos[i,1] /\ i < present_pos[i,1] + present_shape[i,1]) then present_shape[i,2] else 0 endif);

var int: sum2 = sum(i in 1..n)(
if ( i >= present_pos[i,2] /\ i < present_pos[i,2] + present_shape[i,2]) then present_shape[i,1] else 0 endif);

constraint paper_shape[1]-min_shape[1] <sum1 /\ sum1 <= paper_shape[1];
constraint paper_shape[2]-min_shape[2] <sum2 /\ sum2 <= paper_shape[2];

%nope
%constraint lex_lesseq(present_pos[1..n,2], reverse(present_pos[1..n,2]));

% rimuovere tutti gli interstizi
%var array[1..paper_shape[1],1..paper_shape[2]]: row = 

%constraint (sum(i in 1..n)(
%if ( i >= present_pos[i,1] /\ i <=present_pos[i,1] + present_shape[i,1]) then present_shape[i,2] else 0 endif)) <= paper_shape[1];
                                    
%constraint (sum(i in 1..n)(
%if ( i >= present_pos[i,2] /\ i <=present_pos[i,2] + present_shape[i,2]) then present_shape[i,1] else 0 endif)) <= paper_shape[2];


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

ann: restart_ann;
restart_ann = restart_linear(10);
solve :: search_ann satisfy;



output ["\(present_pos)"];


