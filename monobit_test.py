import math
import scipy.special as spc
import csv
import statistics

def monobit(self, bin_data: str):
    """
    Note that this description is taken from the NIST documentation [1]
    [1] http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf
  
    The focus of this test is the proportion of zeros and ones for the entire sequence. The purpose of this test is
    to determine whether the number of ones and zeros in a sequence are approximately the same as would be expected
    for a truly random sequence. This test assesses the closeness of the fraction of ones to 1/2, that is the number
    of ones and zeros ina  sequence should be about the same. All subsequent tests depend on this test.
  
    :param bin_data: a binary string
    :return: the p-value from the test
    """
    count = 0
    # If the char is 0 minus 1, else add 1
    for char in bin_data:
        if char == '0':
            count -= 1
        else:
            count += 1
    # Calculate the p value
    sobs = count / math.sqrt(len(bin_data))
    p_val = spc.erfc(math.fabs(sobs) / math.sqrt(2))
    return p_val

def main():
    '''
    
    In order to find the randomness according to the monobit test, I import
    the pseudo-random numbers in a .csv format. Comprehension is used to
    slice off the \n characters at the end of the numbers. The numbers are
    converted to binary and sent through the monobit test.

    This test determines how random a sequence is by converting the bits to
    0s and 1s and determining the ratio of one to the other. In a truly
    random number, this is expected to approach 0.5

    Randomness is measured in terms of distance from 0.5, and therefore
    the 'weights' added convert the distance from 0.5 into a percentage
    of randomness on a scale of 0% - 100%

    On line 61 the range is set at (1,6) in order to read 5 files with
    the format 'trial{num}.csv', to increase the number of trials to run, simply
    add more trial.csv files and increase the range to run all trials

    '''
    do_print = False
    print_nums = input('Print number lists? (y/n): ')
    if print_nums == 'y':
        do_print = True
    elif print_nums == 'n':
        do_print = False
    else:
        print('Error')
    rows = []
    for num in range(1,3):
        print('*'*100)
        print('Trial',num,':')
        with open('trials/trial'+str(num)+'.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            mylist = [line.rstrip('\n') for line in csv_file]
        if do_print == True:
            for i in mylist:
                print(i)
        else:
            pass
        temp = []
        for i in mylist:
            b = monobit('a', bin(int(i)))
            temp.append(b)
        print('*'*100)
        print('Monobit Avg Before Weight:',statistics.mean(temp))
        if statistics.mean(temp) > 0.5:
            x = statistics.mean(temp)-0.5
            i = (statistics.mean(temp)-(2*x))*2
            print('Monobit Avg:',i)
        else:
            print('Monobit Avg:',statistics.mean(temp)/0.5)

if __name__ == '__main__':
    main()