import pandas as pd
import numpy as np
import os
import argparse
##########################################################
class liftOverCorections(object):
    
    def __init__(self, intitial_start_file, output_results, errors):
        self.intitial_start_file = intitial_start_file
        self.output_results = output_results
        self.errors = errors
        
    def strartFile(self):
        self.df_in = pd.read_csv(self.intitial_start_file, header = None)
        return self.df_in
    
    def outputLiftOver(self):
        self.df_out = pd.read_csv(self.output_results, header = None)
        return self.df_out
    
    def errorsLiftOver(self):
        df_errors = pd.read_csv(self.errors, header = None)
        self.df_err1 = df_errors[df_errors[0].str.contains("#") == False]
        error1_list = self.df_err1[0].tolist()
        self.set_error_list = set(error1_list) # Make a set of errors
        
        return self.df_err1, self.set_error_list
    
    def firtTest(self):
        'Testing the length of the initial dataframes. If they are correct the result should be 0'
        self.test1 = len(self.df_out) + len(self.df_err1) - len(self.df_in)
        return self.test1
    
    def listOfNotMatched(self):
        self.common_DF = self.df_in[self.df_in[0].isin(self.set_error_list)]
        self.common_DF.reset_index(inplace=True)
        return self.common_DF
    
    def creatingTheNewTable(self):
        pos_list = list(self.common_DF['index'])
        self.new_df = pd.DataFrame()
        df2 = pd.DataFrame([['Deleted']])
        old_pos = 0
        for pos in pos_list:
            temp_DF = self.df_out[old_pos:pos]
            self.new_df = pd.concat([self.new_df,temp_DF])
            self.new_df = pd.concat([self.new_df, df2])
            old_pos = pos
 
        last_pos = pos_list[-1]
        length = len(self.df_out)
        final_part = self.df_out[last_pos:length]
        self.new_df = pd.concat([self.new_df, final_part])
        self.new_df.reset_index(drop = True, inplace = True)
        return self.new_df
    
    def testingForErrors(self):
        
        def compare_chr(chrs):
            chr1, chr2 = chrs
            schr1 = chr1[:3]
            schr2 = chr2[:3]
            
            if schr1 == schr2:
                return 1
            elif schr1 != schr2:
                return 0
            else:
                print("It shouldn't go here")
        
        df11 = self.new_df[[0]]
        df22 = self.df_in[[0]]
        df33 = pd.concat([df11,df22], axis = 1)
        df33.columns = ['col1','col2']
        df33['Test'] = df33[['col1','col2']].apply(compare_chr, axis = 1)
        negative =  df33[df33['Test'] == 0]
        
        if len(negative) != len(self.df_err1):
            print ('There is an error. The numbers does not match - ' + self.intitial_start_file)
        elif len(negative) == len(self.df_err1):
            print('Passed: ' + self.intitial_start_file)
        else:
            print('You never get in here')
##########################################################
class saveTopickle(object):
    
    def __init__(self, fileName, folderName, df):
        self.fileName = fileName
        self.folderName = folderName
        self.df =  df
        
    def makingDir(self):
        if not os.path.exists(self.folderName):
            os.makedirs(self.folderName)
         
    def savingToPickle(self):
        path = self.folderName + '/' + self.fileName
        print(path)
        self.df.to_pickle(path)
##########################################################
class arguments(object):
        
    def parserMain():
        parser = argparse.ArgumentParser()
        parser.add_argument('-o','--output', help = 'Output File Name (Pickle)')
        parser.add_argument('-d','--directory', help = 'Directory For Output File Storage')
        parser.add_argument('-i','--initial', help = 'Bed File That You Want to Lift Over')
        parser.add_argument('-r','--possitive', help = 'Output File From LiftOver With The Positive Hits')
        parser.add_argument('-e','--errors', help = 'Error File From LiftOver')
        parser.add_argument('-t','--test', help = "Testing if the Results are Correct (Time consuming): 1 test, 0 no test", type = int)
        
        args = parser.parse_args()
        
        return args.output, args.directory, args.initial, args.possitive, args.errors, args.test

##########################################################
if __name__ == '__main__':

    fileName,folderName,intitial_start_file, output_results_liftOver, errors_liftOvers, runTest  = arguments.parserMain()

    
    c = liftOverCorections(intitial_start_file, output_results_liftOver, errors_liftOvers)
    df_start = c.strartFile()
    df_out = c.outputLiftOver()
    df_error, list_of_not_matched = c.errorsLiftOver()
    
    test1 = c.firtTest()
    if test1 != 0:
        print('There is an error. Please check')
        exit(1)
    
    list_of_not_mached = c.listOfNotMatched()
    final_DF = c.creatingTheNewTable()
    
    c1 = saveTopickle(fileName, folderName, final_DF)
    c1.makingDir()
    c1.savingToPickle()
    
    if runTest == True:
        c.testingForErrors()
