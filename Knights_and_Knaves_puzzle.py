# Written by BI XI
# Knights and Knaves Puzzle

import sys
import re

try:
    filename = input('Which text file do you want to use for the puzzle? ')
    if '.txt' in filename:
        with open(filename) as f:
            sentences = f.read()
    else:
        raise ValueError
  
except FileNotFoundError:
    print('No such file or directory, giving up')
    sys.exit()
except ValueError:
    print('Incorrect input, giving up')
    sys.exit()


# the function extract_name() is to get the name from the file.txt given
def extract_name(sentences):
    # replace the '\n' with the space
    sentences = re.sub(r'\n',' ',sentences)
    name_list = []
    final_list = []
    result_of_search = 1
    strings = sentences[0:]
    standard = re.compile(r'Sirs?\s+[A-Z]([a-z])+(,\s+(Sir\s)?[A-Z]([a-z])+)*(,\s+(Sir\s)?[A-Z]([a-z])+)?(,?\s+((and)|(or))\s+(Sir\s)?[A-Z]([a-z])+)?')
    while result_of_search:
        result_of_search = standard.search(strings)
        if result_of_search:
            group_result = result_of_search.group()
            span = result_of_search.span()
            name_list.append(group_result)
            strings = strings[span[1]:]
        else:
            continue
# Get a list which contain all the Sir names(some one may repeat)
    new_strings = ' '.join(name_list)
    new_list = re.split(r'[\s+,]',new_strings)
    for i in new_list:
        if i == 'Sirs' or i == 'and' or i == 'Sir' or i == 'or' or i == '' or i == ' ':
            continue
        elif i not in final_list:
            final_list.append(i)
    final_list.sort()
    return final_list

# the function solutions() is to judge wether there is a solution for this puzzle
# and if there is solution, is the solution is unique
def solutions(sentences):
    sentences = re.sub(r'\n',' ',sentences)
    participants = extract_name(sentences)
    strings = sentences[0:]
    result_of_search = 1
    statement_list = []
    statements = [dict((participants[i],m >> i & 1) for i in range(len(participants))) for m in range(2**len(participants))]
    # the statements will contain all the situations that the persons could be
    # 0 means the knave and 1 means the knight
    # So the statements is like [{'A':0,'B':1,...},{...}]
    # two match models below: one is (A:"XXXX."), another is ("XXXX,"A.)
    s1 = re.compile(r'(([A-Z][A-Za-z\s,]+)?(Sirs?){1}\s[A-Za-z\s,]+:?\s*"[A-Za-z\s,]+[.?!]\s*")|("[A-Za-z\s,.]+"\s+([A-Za-z\s,]+)?(Sirs?){1}([A-Za-z\s,]+)?[.!?])') 
    while result_of_search:
        result_of_search = s1.search(strings)
        if result_of_search:
            group_result = result_of_search.group()
            span = result_of_search.span()
            statement_list.append(group_result)
            strings = strings[span[1]:]
        else:
            continue
    # get a list that contains participants' statements
    s2 = re.compile(r'"[A-Za-z\s,]+[.,!?]"')
    # the s2 standard is to get the contents surrounded by " "
    s3 = re.compile(r'Sir\s+[A-Z]([a-z])+\s+is\s{1,2}a\s+Kn[a-z]+')
    # the s3 standard is to get the single Sir
    s4 = re.compile(r'(Sir\s+[A-Z][a-z]+)(,\s+Sir\s+[A-Z][a-z]+)*\sand((\s+Sir\s+[A-Z][a-z]+)|(\s+I\s))')
    # the s4 standard is to get the conjunction_of_Sirs
    s5 = re.compile(r'(Sir\s+[A-Z][a-z]+)(,\s+Sir\s+[A-Z][a-z]+)*\sor((\s+Sir\s+[A-Z][a-z]+)|(\s+I\s))')
    # the s5 standard is to get the disjunction_of_Sirs
    s6 = re.compile(r'[Aa]t\s+least\s+one\s+of')
    # get the at least one
    s7 = re.compile(r'one\s+of\s+us')
    # one of us
    s8 = re.compile(r'[Aa]ll\s+of\s+us')
    # all of us
    s9 = re.compile(r'[Aa]t\s+most\s+one\s+of')
    # at most one of us
    s10= re.compile(r'I\s+am\s+')
    # I am...
    s11= re.compile(r'Sir\s+[A-Z][a-z]+')
    # get the name
    s12= re.compile(r'[Ee]xactly\s+one\s+of')
    # get the 'exactly/Exactly one of'
    solution_num = 0
    solution_methods = 0
    name_and_say = []
    for index_2 in statement_list:
        temp = s2.search(index_2)
        if temp:
            words = temp.group()
            c = temp.span()
            speaker = s11.search(index_2[0:c[0]]+index_2[c[1]:])
            speaker = speaker.group()
            speaker = re.split(r'\s+',speaker)
            for i in speaker:
                if i != 'Sir' and i != 'Sirs':
                    name_and_say.append([i,words])
                    
    for index_0 in statements:
        feedback = []
        for nas in name_and_say:
            partial_feedback = []
            if s6.search(nas[1]):
# At/at least one of Conjunction_of_Sirs/us is a Knight/Knave
                if s7.search(nas[1]):
                    if 'Knight' in nas[1] or 'Knights' in nas[1]:
                        for i in participants:
                            partial_feedback.append(index_0[i] == 1)
                        if index_0[nas[0]] == 0:
                            feedback.append(not (partial_feedback.count(True) >= 1))
                        else:
                            feedback.append(partial_feedback.count(True) >= 1)
                        if feedback.count(False) >= 1:
                            break
                        
                    else:
                        for i in participants:
                            partial_feedback.append(index_0[i] == 0)
                        if index_0[nas[0]] == 0:
                            feedback.append(not (partial_feedback.count(True) >= 1))
                        else:
                            feedback.append(partial_feedback.count(True) >= 1)
                        if feedback.count(False) >= 1:
                            break
                else:
                    if 'Knight' in nas[1] or 'Knights' in nas[1]:
                        for i in participants:
                            if i in nas[1]:
                                partial_feedback.append(index_0[i] == 1)
                        if ' I ' in nas[1]:
                            partial_feedback.append(index_0[nas[0]] == 1)
                        if index_0[nas[0]] == 0:
                            feedback.append(not (partial_feedback.count(True) >= 1))
                        else:
                            feedback.append(partial_feedback.count(True) >= 1)
                        if feedback.count(False) >= 1:
                            break
                    else:
                        for i in participants:
                            if i in nas[1]:
                                partial_feedback.append(index_0[i] == 0)
                        if ' I ' in nas[1]:
                            partial_feedback.append(index_0[nas[0]] == 0)
                        if index_0[nas[0]] == 0:
                            feedback.append(not (partial_feedback.count(True) >= 1))
                        else:
                            feedback.append(partial_feedback.count(True) >= 1)
                        if feedback.count(False) >= 1:
                            break
# aim to the first form of eight statements

            elif s9.search(nas[1]):
# At/at most one of Conjunction_of_Sirs/us is a Knight/Knave
                if s7.search(nas[1]):
                    if 'Knights' in nas[1] or 'Knight' in nas[1]:
                        for i in participants:
                            partial_feedback.append(index_0[i] == 1)
                        if index_0[nas[0]] == 0:
                            feedback.append(not (partial_feedback.count(True) <= 1))
                        else:
                            feedback.append(partial_feedback.count(True) <= 1)
                        if feedback.count(False) >= 1:
                            break
                    else:
                        for i in participants:
                            partial_feedback.append(index_0[i] == 0)
                        if index_0[nas[0]] == 0:
                            feedback.append(not (partial_feedback.count(True) <= 1))
                        else:
                            feedback.append(partial_feedback.count(True) <= 1)
                        if feedback.count(False) >= 1:
                            break
                else:
                    if 'Knights' in nas[1] or 'Knight' in nas[1]:
                        for i in participants:
                            if i in nas[1]:
                                partial_feedback.append(index_0[i] == 1)
                        if ' I ' in nas[1]:
                            partial_feedback.append(index_0[nas[0]] == 1)
                        if index_0[nas[0]] == 0:
                            feedback.append(not (partial_feedback.count(True) <= 1))
                        else:
                            feedback.append(partial_feedback.count(True) <= 1)
                        if feedback.count(False) >= 1:
                            break
                    else:
                        for i in participants:
                            if i in nas[1]:
                                partial_feedback.append(index_0[i] == 0)
                        if ' I ' in nas[1]:
                            partial_feedback.append(index_0[nas[0]] == 0)
                        if index_0[nas[0]] == 0:
                            feedback.append(not (partial_feedback.count(True) <= 1))
                        else:
                            feedback.append(partial_feedback.count(True) <= 1)
                        if feedback.count(False) >= 1:
                            break


            elif s12.search(nas[1]):
# Exactly/exactly one of Conjunction_of_Sirs/us is a Knight/Knave
                if s7.search(nas[1]):
                    if 'Knights' in nas[1] or 'Knight' in nas[1]:
                        for i in participants:
                            partial_feedback.append(index_0[i] == 1)
                        if index_0[nas[0]] == 0:
                            feedback.append(not (partial_feedback.count(True) == 1))
                        else:
                            feedback.append(partial_feedback.count(True) == 1)
                        if feedback.count(False) >= 1:
                            break
                    else:
                        for i in participants:
                            partial_feedback.append(index_0[i] == 0)
                        if index_0[nas[0]] == 0:
                            feedback.append(not (partial_feedback.count(True) == 1))
                        else:
                            feedback.append(partial_feedback.count(True) == 1)
                        if feedback.count(False) >= 1:
                            break
                else:
                    if 'Knights' in nas[1] or 'Knight' in nas[1]:
                        for i in participants:
                            if i in nas[1]:
                                partial_feedback.append(index_0[i] == 1)
                        if ' I ' in nas[1]:
                            partial_feedback.append(index_0[nas[0]] == 1)
                        if index_0[nas[0]] == 0:
                            feedback.append(not (partial_feedback.count(True) == 1))
                        else:
                            feedback.append(partial_feedback.count(True) == 1)
                        if feedback.count(False) >= 1:
                            break
                    else:
                        for i in participants:
                            if i in nas[1]:
                                partial_feedback.append(index_0[i] == 0)
                        if ' I ' in nas[1]:
                            partial_feedback.append(index_0[nas[0]] == 0)
                        if index_0[nas[0]] == 0:
                            feedback.append(not (partial_feedback.count(True) == 1))
                        else:
                            feedback.append(partial_feedback.count(True) == 1)
                        if feedback.count(False) >= 1:
                            break
        

            elif s8.search(nas[1]):
# All/all of us are Knights/Knaves
                if 'Knights' in nas[1] or 'Knight' in nas[1]:
                    for i in participants:
                        partial_feedback.append(index_0[i] == 1)
                    if index_0[nas[0]] == 0:
                        feedback.append(not (partial_feedback.count(True) == len(participants)))
                    else:
                        feedback.append(partial_feedback.count(True) == len(participants))
                    if feedback.count(False) >= 1:
                            break
                else:
                    for i in participants:
                        partial_feedback.append(index_0[i] == 0)
                    if index_0[nas[0]] == 0:
                        feedback.append(not (partial_feedback.count(True) == len(participants)))
                    else:
                        feedback.append(partial_feedback.count(True) == len(participants))
                    if feedback.count(False) >= 1:
                            break

                
            elif s10.search(nas[1]):
# I am a Knight/Knave
                if 'Knights' in nas[1] or 'Knight' in nas[1]:
                    partial_feedback.append(index_0[nas[0]] == 1)
                else:
                    partial_feedback.append(index_0[nas[0]] == 0)
                if index_0[nas[0]] == 0:
                    feedback.append(not partial_feedback[0])
                else:
                    feedback.append(partial_feedback[0])
                if feedback.count(False) >= 1:
                            break


            elif s3.search(nas[1]) and 'or' not in nas[1]:
# Sir Sir_Name is a Knight/Knave
                if 'Knights' in nas[1] or 'Knight' in nas[1]:
                    for i in participants:
                        if i in nas[1]:
                            partial_feedback.append(index_0[i] == 1)
                            if index_0[nas[0]] == 0:
                                feedback.append(not partial_feedback[0])
                            else:
                                feedback.append(partial_feedback[0])
                            if feedback.count(False) >= 1:
                                break
                else:
                    for i in participants:
                        if i in nas[1]:
                            partial_feedback.append(index_0[i] == 0)
                            if index_0[nas[0]] == 0:
                                feedback.append(not partial_feedback[0])
                            else:
                                feedback.append(partial_feedback[0])
                            if feedback.count(False) >= 1:
                                break
                                
            elif s5.search(nas[1]):
# Disjunction_of_Sirs is a Knight/Knave
                name_words = s5.search(nas[1])
                disjunction_names = name_words.group()
                if 'Knights' in nas[1] or 'Knight' in nas[1]:
                    for i in participants:
                        if i in disjunction_names:
                            partial_feedback.append(index_0[i] == 1)
                    if ' I ' in disjunction_names:
                        partial_feedback.append(index_0[nas[0]] == 1)
                    if index_0[nas[0]] == 0:
                        feedback.append(not (partial_feedback.count(True) >= 1))
                    else:
                        feedback.append(partial_feedback.count(True) >= 1)
                    if feedback.count(False) >= 1:
                            break
                else:
                    for i in participants:
                        if i in disjunction_names:
                            partial_feedback.append(index_0[i] == 0)
                    if ' I ' in disjunction_names:
                        partial_feedback.append(index_0[nas[0]] == 0)
                    if index_0[nas[0]] == 0:
                        feedback.append(not (partial_feedback.count(True) >= 1))
                    else:
                        feedback.append(partial_feedback.count(True) >= 1)
                    if feedback.count(False) >= 1:
                            break


            elif (s4.search(nas[1]) and 'least one' not in nas[1] and 'most one' not in nas[1] and 'Exactly one' not in nas[1] and 'exactly one' not in nas[1]):
# Conjunction_of_Sirs are Knights/Knaves
                name_num = 0
                name_words = s4.search(nas[1])
                conjunction_names = name_words.group()
                if 'Knights' in nas[1] or 'Knight' in nas[1]:
                    for i in participants:
                        if i in conjunction_names:
                            name_num = name_num + 1
                            partial_feedback.append(index_0[i] == 1)
                    if ' I ' in conjunction_names:
                        name_num = name_num + 1
                        partial_feedback.append(index_0[nas[0]] == 1)
                    if index_0[nas[0]] == 0:
                        feedback.append(not (partial_feedback.count(True) == name_num))
                    else:
                        feedback.append(partial_feedback.count(True) == name_num)
                    if feedback.count(False) >= 1:
                            break
                else:
                    for i in participants:
                        if i in conjunction_names:
                            name_num = name_num + 1
                            partial_feedback.append(index_0[i] == 0)
                    if ' I ' in conjunction_names:
                        name_num = name_num + 1
                        partial_feedback.append(index_0[nas[0]] == 0)
                    if index_0[nas[0]] == 0:
                        feedback.append(not (partial_feedback.count(True) == name_num))
                    else:
                        feedback.append(partial_feedback.count(True) == name_num)
                    if feedback.count(False) >= 1:
                            break
        if feedback.count(False) == 0:
            solution_methods = index_0
            solution_num = solution_num + 1
        else:
            continue
    return solution_methods, solution_num


                            
people_name = extract_name(sentences)
method, num_of_methods = solutions(sentences)
if len(people_name) != 0:
    print('The Sirs are: ',end = '')
    length = len(people_name)
    for i in range(length - 1):
        print(people_name[i],end = ' ')
    print(people_name[length - 1],end='')
else:
    print('There is no Sir in this puzzle.')
print('')
if num_of_methods == 0:
    print('There is no solution.')
elif num_of_methods == 1:
    print('There is a unique solution:')
    for sol in method:
        if method[sol] == 1:
            method[sol] = 'Knight'
        else:
            method[sol] = 'Knave'
        print(f'Sir {sol} is a {method[sol]}.')
elif num_of_methods > 1:
    print(f'There are {num_of_methods} solutions.')





