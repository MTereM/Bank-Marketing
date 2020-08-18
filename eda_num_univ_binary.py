import ipywidgets as widgets
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from IPython.core.display import display, HTML

'''This function will return 4 tables: overview, descriptive stats, frequency top and frequency bottom and two graphs: histogram and boxplot for each numerical feature'''


def eda_num_univ_binary(dataset):
    '''dataset:pd.DataFrame'''
    dataset_num = dataset.select_dtypes(exclude='object')
    if len(dataset_num[dataset_num.columns.values[-1]].unique())==2:
        dataset_num = dataset_num.iloc[:,:-1]
    else:
        dataset_num = dataset.select_dtypes(exclude='object')
        
    tab_contents = [i for i in dataset_num.columns.values]
    children = [widgets.Output() for value in tab_contents]
    tab = widgets.Tab(children=children)
    [tab.set_title(num,name) for num,name in enumerate(tab_contents)]
    display(tab)

    for i,k in enumerate(dataset_num.columns.values):
        # overview table
        count_num = dataset_num[k].count()
        distinct_count_num = dataset_num[k].nunique()
        unique_num = round(100*(dataset[k].nunique()/len(dataset)),2)
        missing_num = dataset_num[k].isnull().sum().sum()
        missing_num_perc = 100*(missing_num/len(dataset_num))
        zeros_num_count = (dataset_num[k]==0).sum()
        zeros_num_count_perc = 100*(zeros_num_count/len(dataset))
        
        df1_num = pd.DataFrame([count_num,distinct_count_num,unique_num,missing_num,missing_num_perc,zeros_num_count,zeros_num_count_perc],columns=[''],
                         index=['Total count','Distinct count','Unique (%)','Missing','Missing (%)','Zeros','Zeros (%)'])
        df1_num.index.name = 'Overview'
        # descriptive stats table
        df2_num = pd.DataFrame(dataset_num[k].describe().round(2))
        df2_num.columns = ['']
        df2_num = df2_num.drop('count')
        df2_num.loc['kurtosis'] = dataset_num[k].kurtosis(axis=0)
        df2_num.loc['skew'] = dataset_num[k].skew(axis=0)
        df2_num.index.name = 'Descriptive Statistics'
        df2_num = df2_num.style.set_precision(2)
        # Frequency top 7
        freq_top = pd.DataFrame(dataset_num[k].value_counts().sort_values(ascending=False).head(10)).rename(columns={k:'Frequency'}).reset_index()
        freq_top['Frequency (%)'] = 100*(freq_top['Frequency']/len(dataset))
        freq_top = freq_top.rename(columns={'index':k,'Frequency':'Frequency'})
        freq_top = freq_top.style.hide_index().set_caption("Frequency top").set_precision(2)
    
        # Frequency bottom 7
        freq_bottom = pd.DataFrame(dataset_num[k].value_counts().sort_values(ascending=False).tail(10)).rename(columns={k:'Frequency'}).reset_index()
        freq_bottom['Frequency (%)'] = 100*(freq_bottom['Frequency']/len(dataset))
        freq_bottom = freq_bottom.rename(columns={'index':k,'Frequency':'Frequency'})
        freq_bottom = freq_bottom.style.hide_index().set_caption("Frequency bottom").set_precision(3)
    
        out1 = widgets.Output()
        out2 = widgets.Output()
        out3 = widgets.Output()
        out4 = widgets.Output()
        with out1:
            display(df1_num)
        with out2:
            display(df2_num)
        with out3:
            display(freq_top)
        with out4:
            display(freq_bottom)
        hbox = widgets.HBox([out1,out2,out3,out4])
    
        with children[i]:
            display(hbox)
        
            x_titles = list(dataset_num.columns)
    
            fig1=px.histogram(dataset_num,x=dataset_num[k],labels={'x':x_titles[i],'y':'count'},histnorm='percent')
            fig2=px.box(dataset_num,y=dataset_num[k],labels={'x':x_titles[i],'y':'percent'})
        
            trace1 = fig1['data'][0]
            trace2 = fig2['data'][0]
            fig = make_subplots(rows=1,cols=2,subplot_titles=['Histogram','Box plot'])
            fig.layout["xaxis"].title.text = k
            fig.layout["xaxis2"].title.text = ''
            fig.layout["yaxis"].title.text = 'percent'
            fig.layout["yaxis2"].title.text = k
        
            fig.add_trace(trace1,1,1)
            fig.add_trace(trace2,1,2)
            fig.update_layout(template='plotly_dark')
            fig.show()