% Program: mycode.pl.
% Source: SWI-Prolog (threaded, 64 bits, version 8.0.2).
% Written by BI XI for COMP9414 assignment 1.
% Student Number: 5198280
% Assignment Name: Prolog Programming.
% Purpose: It includes five main functions to deal with five different problems.


% sumsq_even(Numbers,Sum) for question_1 in assignment_1.
% sunsq_even(Numbers,Sum) is to sum the squares of only the even numbers in a list of integers given.

sumsq_even([],0). 
sumsq_even([Head|Tail],Sum) :- sumsq_even(Tail,Sum_even),0 =:= Head mod 2,Sum is Sum_even + Head * Head.
sumsq_even([Head|Tail],Sum) :- sumsq_even(Tail,Sum_even),0 =\= Head mod 2,Sum is Sum_even.


% same_name(Person1,Person2) for question_2 in assignment_1.
% the function male_ancestor(Person1,Person2) is to tell wether the Person1 is the ancestor of Person2,
% and for each pair of persons who are of male_ancestor relationship,the elder one must be the male.
% same_name(Person1,Person2) is to tell wether two people have the same family name by calling the function male_ancestor.


male_ancestor(Person1,Person2) :- male(Person1),parent(Person1,Person2),\+(Person1 = Person2).
male_ancestor(Person1,Person2) :- 
                                male(Person1),parent(Person1,Person3),
                                male_ancestor(Person3,Person2),\+(Person1 = Person2).
same_name(Person1,Person2) :- male_ancestor(Person1,Person2).
same_name(Person1,Person2) :- male_ancestor(Person3,Person1),male_ancestor(Person4,Person2),Person3 == Person4.


% sqrt_list(NumberList, ResultList) for question_3 in assignment_1.
% combine_list([],List,List).
% combine_list([Head|Tail1],List,[Head|Tail2]) :- combine_list(Tail1,List,Tail2).
% At the begining I consider to construct a function which is showed upon that can combine 
% several lists into one list. And after solving the question_4 I find a easy way to deal with question_3
% sqrt_list(NumberList,ResultList) is to bind ResultList to the list of pairs consisting of 
% a number and its square root, for each number in NumberList.

sqrt_list([],[]).
sqrt_list([Head3|Tail3],ResultList) :-
                                        sqrt_list(Tail3,Result),
                                        X is sqrt(Head3),
                                        ResultList = [[Head3,X]|Result].
                                      % combine_list([[Head3,X]],Result,ResultList).



% sign_runs(List, RunList) for question_4 in assignment_1.
% judge_and_pack(A,B,C,D) is to get every sublist of the final RunList in order.
% sign_runs(List,RunList) is to traversal all the elements in the List and eventually
% get the final RunList by calling the function judge_and_pack().

judge_and_pack(X,[],[],[X]).
judge_and_pack(H1,[H3|T3],[H3|T3],[H1]) :- H1 >= 0,H3 < 0.
judge_and_pack(H1,[H3|T3],[H3|T3],[H1]) :- H1 < 0,H3 >= 0.
judge_and_pack(H1,[H3|T1],T3,[H1|T2]) :- H1 >= 0,H3 >= 0,judge_and_pack(H3,T1,T3,T2).
judge_and_pack(H1,[H3|T1],T3,[H1|T2]) :- H1 < 0,H3 < 0,judge_and_pack(H3,T1,T3,T2).

sign_runs([],[]).
sign_runs([H1|T1],[H2|T2]) :- judge_and_pack(H1,T1,T3,H2), sign_runs(T3,T2).


% is_heap(empty or tree(L,Num,R)) for question_5 in assignment_1.
% is_heap(empty or tree(L,Num,R)) is to judge wether a binary tree meet the property given,
% the property is that for every non-leaf node in the tree, the number stored at that node 
% is less than or equal to the number stored at each of its children.

is_heap(empty).
is_heap(tree(empty,_,empty)).
is_heap(tree(tree(L2,Num2,R2),Num1,tree(L3,Num3,R3))) :-  
                                 Num1 =< Num2,
                                 Num1 =< Num3,
                                 is_heap(tree(L2,Num2,R2)),
                                 is_heap(tree(L3,Num3,R3)).
is_heap(tree(empty,Num1,tree(L3,Num3,R3))) :-  
                                 Num1 =< Num3,
                                 is_heap(tree(L3,Num3,R3)).
is_heap(tree(tree(L2,Num2,R2),Num1,empty)) :-  
                                 Num1 =< Num2,
                                 is_heap(tree(L2,Num2,R2)).





                                

                                




                                  
