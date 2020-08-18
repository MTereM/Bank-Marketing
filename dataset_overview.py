import ipywidgets as widgets
import pandas as pd

def dataset_overview(dataset):

    out_overview = widgets.Output()
    out_stats_num = widgets.Output()
    out_stats_cat = widgets.Output()
    out_dtypes = widgets.Output()

    with out_overview:
        num_variables = dataset.shape[1]
        num_observations = dataset.shape[0]
        missing = dataset.isnull().sum().sum()  
        missing_perc = (100*(missing/len(dataset)))
        duplicate_rows = dataset.duplicated().sum()
        duplicate_rows_perc = (100*(duplicate_rows/len(dataset)))
        zeros_count = dataset[dataset==0].count(axis=0).sum()
        zeros_count_perc = 100*(zeros_count/len(dataset))
        data_overview = pd.DataFrame([num_variables,num_observations,missing,missing_perc,duplicate_rows,duplicate_rows_perc,zeros_count,zeros_count_perc],
                          index=['Number of variables','Number of observations','Missing values','Missing values (%)','Duplicate rows','Duplicate rows (%)','Zeros','Zeros (%)'],columns=[''])
        data_overview.index.name='Dataset overview'
    
        data_overview_round=data_overview.T.round(decimals=pd.Series([0, 0, 0, 3, 0, 3,0,3], index=data_overview.index)).T
        data_overview_round = data_overview_round.astype(object) 
        display(data_overview_round)
    
    with out_stats_num:
        data_stats_num = pd.DataFrame(dataset.describe(exclude='object'))
        data_stats_num_round_style = data_stats_num.style.set_caption('Descriptive statistics (numerical)').set_precision(2)
        display(data_stats_num_round_style)
        
    with out_stats_cat:
        data_stats_cat = pd.DataFrame(dataset.describe(exclude='number'))
        data_stats_cat_style = data_stats_cat.style.set_caption('Descriptive statistics (categorical)')
        display(data_stats_cat_style)
        
    with out_dtypes:
        num_dtypes = dataset.select_dtypes(exclude='object').dtypes.count()
        cat_dtypes = dataset.select_dtypes(exclude='number').dtypes.count()
        data_types = pd.DataFrame([num_dtypes,cat_dtypes],index=['Numeric','Categorical'],columns=[''])
        data_types.index.name='Variable types'
        display(data_types)
    
    hbox = widgets.HBox([out_overview,out_dtypes],layout={'border': 'red','width':'100%'})
    hbox2 = widgets.HBox([out_stats_num])
    hbox3 = widgets.HBox([out_stats_cat])
    vbox = widgets.VBox([hbox,hbox2,hbox3])
    
    return display(vbox)
