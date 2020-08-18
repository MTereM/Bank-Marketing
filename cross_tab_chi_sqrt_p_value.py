from ipywidgets import widgets
import pandas as pd
from scipy.stats import chi2_contingency
from scipy.stats import chi2
import numpy as np

def cross_tab_chi_sqrt_p_value(dataset,missing_word,target,prob):
    """ dataset = dataframe
        missing_word = missing value that has other name other than NaN (string must be between ' ')
        target = response feature
        prob = probability for the p-value. A prob = 0.99 corresponds to a p-value = 0.01
        
        To call:
        Ex: cross_tab_chi_sqrt_p_value(df,'unknown',df['y'],0.99) """
    
    
    my_word = [missing_word]
    m = dataset.isin(my_word).any() # check if the missing word is in it
    m2 = m.loc[m==True].index.tolist() # list column names that have the missing 'unknown'
    print('')
    print('Columns with missing value {} : {}'.format(my_word,m2))
    print(' ')
    dataset = dataset.loc[:, dataset.columns.isin(m2)] 
    response_var = target
    
    tab_contents = [i for i in m2]
    children = [widgets.Output() for value in tab_contents]
    tab = widgets.Tab(children=children)
    [tab.set_title(num,name) for num,name in enumerate(tab_contents)]
    display(tab)
    
    for i, k in enumerate(dataset.columns.values):
        
        out_cross = widgets.Output()
        out_chi = widgets.Output()
        out_p = widgets.Output()
        out_number_unknown = widgets.Output()
        out_expected = widgets.Output()
        
        dataset_new  = pd.DataFrame(dataset[k].apply(lambda x: 'unknown' if x=='unknown' else 'known'))
        dataset_new['response_var'] = response_var
        pd_cross = pd.crosstab(dataset_new[k],dataset_new['response_var'])
        #pd_cross = pd_cross.drop('Total',axis=0)
        
        stat, p, dof, expected = chi2_contingency(pd_cross)
        #prob = 0.99
        prob = prob
        critical = chi2.ppf(prob, dof)
        
        count_unknown = dataset[k].value_counts()['unknown']
        perc_unknown = (count_unknown/len(dataset))*100
        
        with out_cross:
            #pd_cross_table = pd_cross.copy()
            #pd_cross_table['Proportion Yes'] = 100*(pd_cross_table['yes']/pd_cross_table['no'])
            #pd_cross_table_styled = pd_cross_table.style.set_precision(3)
            print('Contingency Table:')
            print(' ')
            #display(pd_cross_table_styled)
            display(pd_cross)
            
        with out_expected:
            print('Expected frequencies:')
            print(' ')
            expected_df = pd.DataFrame(data=expected, index=pd_cross.index, columns= pd_cross.columns)
            expected_df_styled = expected_df.style.set_precision(3)
            display(expected_df_styled)
        
        with out_chi:
            # interpret test-statistic
            if abs(stat) >= critical:
                print('Dependent (reject H0) -> chi-square : {}'.format(abs(stat).round(3)))
            else:
                print('Independent (fail to reject H0) -> chi_square : {}'.format(abs(stat).round(3)))
            print(' ')
            
        with out_p: 
            # interpret p-value
            alpha = 1.0 - prob
            if p <= alpha:
                print("Dependent (reject H0) -> p-value : {}".format(np.format_float_scientific(p, precision=3)))
            else:
                print('Independent (fail to reject H0) -> p-value : {}'.format(np.format_float_scientific(p, precision=3)))
                
        with out_number_unknown:
            print(' ')
            print('Count of {} : {}'.format(my_word,count_unknown))
            print('Percent of {} : {}%'.format(my_word,perc_unknown.round(3)))
        
        hbox1 = widgets.HBox([out_cross,out_expected])
        hbox2 = widgets.VBox([out_chi,out_p,out_number_unknown])
        hbox = widgets.HBox([hbox1,hbox2])
        
        
        with children[i]:
            display(hbox)