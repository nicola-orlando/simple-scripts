import math

# Proposed exercises and solutions here https://towardsdatascience.com/10-algorithms-to-solve-before-your-python-coding-interview-feb74fb9bc27 
# The solution I wrote here should work but problably are not the most efficient and differ from the original post. 


# Given an integer, return the integer with reversed digits.
# Note: The integer could be either positive or negative.
def solution_problem1(num): 
    converted_int = str(num)
    reversed_int = ''
    # positive case, just using the stride index
    if converted_int[0] != '-':
        print('converting positive number')
        reversed_int = converted_int[::-1]
    # negative case
    else : 
        print('converting negative number')
        reversed_int = converted_int[1:]
        reversed_int = '-'+reversed_int[::-1]
    #Conversion to int ensures the removal of the 0's at the front
    print('Reversed string %i'%int(reversed_int))    
    
    
# For a given sentence, return the average word length. 
# Note: Remember to remove punctuation first.
def solution_problem2(sentence):
    # clean up the sentence
    replace_chars = ['!', ',', ';', '?']
    for element in replace_chars:
        sentence = sentence.replace(element,'')
    list_of_words = sentence.split(' ')
    average = 0
    for word in list_of_words: 
        average = average + len(word)
    average = average / len(list_of_words)
    print('Average of the words lenght is %f'%average)


# Given two non-negative integers num1 and num2 represented as string, return the sum of num1 and num2.
# You must not use any built-in BigInteger library or convert the inputs to integer directly.
def solution_problem3(num1,num2):
    print('Solution for the problem 3: %s' %str(eval(num1)+eval(num2)))


# Given a string, find the first non-repeating character in it and return its index. 
# If it doesn't exist, return -1. # Note: all the input strings are already lowercase.
def solution_problem4(phrase):
    print('Problem 4. Passing as input the word: '+phrase)
    index = -1
    for element in phrase: 
        # Can have at most a match of a word with itself 
        counter_occurence = 0
        found_solution = False
        # Special treatment for last element
        matching_last_two = phrase[-1] == phrase[-2]

        for buffer_element in phrase: 
            if element == buffer_element and element != phrase[-1]:
                index = -1
                counter_occurence = counter_occurence + 1
                # If finds a match of a letter with another (different from itself, break the loop, the returned solution will be index = -1)
                if counter_occurence == 2:
                    break 
            # If we are processing the last letter and no match was found, the last letter matches with itself only, so this is the solution
            elif element == buffer_element and element == phrase[-1] and matching_last_two == False:
                counter_occurence = counter_occurence + 1
                index = phrase.find(element)
                print('Solution for problem 4 is (found match): %i'%index)
                break
            elif element == buffer_element and element == phrase[-1] and matching_last_two == True:
                index = -1
                break
            else: 
                index = phrase.find(element)
                if buffer_element == phrase[-1]:
                    print('Solution for problem 4 is (found match): %i'%index)
                    found_solution = True
                    return 

    if found_solution == False:
        print('Solution for problem 4 is (no solution is found): %i'%index)


# Given a non-empty string s, you may delete at most one character. Judge whether you can make it a palindrome.
# The string will only contain lowercase characters a-z. Palindrome is a word that reads the same forward and backward
def solution_problem5(word):
    status = False
    
    # trivial case
    if word == word[::-1]:
        status = True    
        print('Problem 5: solution is trivial '+word)
        return 

    # remove a character 
    for index in range(len(word)):
        # using slicing 
        word_mod = word[:index]+word[index+1:]
        if word_mod == word_mod[::-1]:
            status = True       
            print('Problem 5: solution truncated '+word_mod)
            return 

    print('Problem 5: Found solution? %i'%int(status))


# Given an array of integers, determine whether the array is monotonic or not.
def solution_problem6(input_array):
    is_monothonic_p = False
    is_monothonic_n = False
    for index in range(len(input_array)-2):

        if input_array[index] >= input_array[index+1] >= input_array[index+2]: 
            if index == 0: 
                is_monothonic_n = True
            else: 
                is_monothonic_n = is_monothonic_n*True
            
        elif input_array[index] <= input_array[index+1] <= input_array[index+2]: 
            if index == 0: 
                is_monothonic_p = True
            else: 
                is_monothonic_p = is_monothonic_n*True
        else: 
            is_monothonic_p = False
            is_monothonic_n = False

    if is_monothonic_p == True: 
        print('Monotonic positive')
    elif is_monothonic_n == True: 
        print('Monotonic negative')
    else: 
        print('Non monotonic')


#Given an array nums, write a function to move all zeroes to the end of it while maintaining the relative order of 
#the non-zero elements.
def solution_problem7(input_array):
    input_array_copy=input_array
    print('Problem 7')
    print(input_array)

    for index in range(len(input_array)): 
        if input_array[index]==0:
            input_array_copy.pop(index)
            input_array_copy.append(0)
    # Probably not necessary using a copy 
    print(input_array_copy)
        
    
# Given an array containing None values fill in the None values with most recent 
# non None value in the array. Does not work if the the first element is None. 
def solution_problem8(input_array):
    print('Problem 8')
    print(input_array)
    for index in range(len(input_array)): 
        if input_array[index]==None: 
            input_array[index] = input_array[index-1]
    print(input_array)
        

#Given two sentences, return an array that has the words that appear in one sentence and not
#the other and an array with the words in common. 
def solution_problem9(sent1, sent2):
    print('Problem 9')
    # clean up sentences 
    replace_chars = ['!', ',', ';', '?']
    for element in replace_chars:
        sent1 = sent1.replace(element,'')
        sent2 = sent2.replace(element,'')
    
    arr1 = sent1.split(' ')    
    arr2 = sent2.split(' ')    

    matching_set = set(arr1).intersection(arr2)
    unmatching_set = []
    # Find the unmatching sentences 

    for el1 in arr1:
        if el1 not in arr2:
            unmatching_set.append(el1)
    for el2 in arr2:
        if el2 not in arr1:
            unmatching_set.append(el2)

    print(matching_set)
    print(unmatching_set)


# Given k numbers which are less than n, return the set of prime number among them
# Note: The task is to write a program to print all Prime numbers in an Interval.
# Definition: A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself. 
def solution_problem10(input_list):
    output_list = []
    print('Solution problem 10, first input list then output')
    print(input_list)
    
    for element in input_list:
        is_prime = True
        for i in range( 1, int(element/2)+1 ):
            #print('Processing index %i'%i)
            if element % i == 0 and i != 1 :
                # Found divider
                is_prime = False
                break
        if is_prime == True:
            output_list.append(element)
    
    print(output_list)


# -------

solution_problem1(-1250)
solution_problem1(123)

solution_problem2('This is this is')

solution_problem3('1','5')

solution_problem4('aaad')

solution_problem5('radkar')

solution_problem6([3,2,1,0])

solution_problem7([0,5,1,0,5,8])

solution_problem8([0,5,None,0,None,8])

sentence1 = 'Today I must sleep well'
sentence2 = 'Today I must write code'
solution_problem9(sentence1, sentence2)

solution_problem10([1,2,3,4,6,7,9,13])
