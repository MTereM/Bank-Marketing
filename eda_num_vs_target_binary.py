import ipywidgets as widgets
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from IPython.core.display import display, HTML


def eda_num_vs_target_binary(dataset):
    dataset_num = dataset.select_dtypes(exclude='object')
    dataset_num_target = pd.DataFrame(dataset[dataset.columns.values[-1]])
    
    if dataset[dataset.columns.values[-1]].dtype==object:
        dataset = pd.concat([dataset_num,dataset_num_target],axis=1)  
    else:
        dataset = dataset_num.copy()
    
    tab_contents = [i for i in dataset.columns.values[0:-1]]
    children = [widgets.Output() for value in tab_contents]
    tab = widgets.Tab(children=children)
    [tab.set_title(num,name) for num,name in enumerate(tab_contents)]
    display(tab)
    
    for i,k in enumerate(dataset.columns.values[0:-1]):
        #dataset['conversions'] = dataset_num_target.copy()
        # descriptive stats table
        dataset1 = pd.DataFrame(dataset[k].describe(exclude='object'))
        dataset1.columns = ['']
        dataset1 = dataset1.drop('count')
        dataset1.loc['missing'] = dataset[k].isnull().sum().sum()
        dataset1.loc['kurtosis'] = dataset[k].kurtosis(axis=0)
        dataset1.loc['skew'] = dataset[k].skew(axis=0)
        dataset1 = dataset1.T
        dataset1.index.name = 'Descriptive Statistics'
        dataset1 = dataset1.style.set_precision(2)
        
        
        out_dataset1 = widgets.Output()
        out_dataset2_styled = widgets.Output()
        with out_dataset1:
            display(dataset1)
        
        hbox = widgets.HBox([out_dataset1])
        
        with children[i]:
            display(hbox)
            
            x_titles = list(dataset.columns)
            
            fig1=px.histogram(dataset,x=dataset[k],color=dataset[dataset.columns.values[-1]],facet_row=dataset[dataset.columns.values[-1]],color_discrete_sequence=['blue','red'])
            fig2=px.box(dataset,y=dataset[k],color=dataset[dataset.columns.values[-1]],color_discrete_sequence=['blue','red'])
        
            trace1 = fig1['data'][0] #fig1 y=n0
            trace2 = fig1['data'][1] #fig1 y=yes
            trace3 = fig2['data'][0]
            trace4 = fig2['data'][1]
            
            fig1['data'][0]['showlegend']=True
            fig1['data'][1]['showlegend']=True
            fig1['data'][0]['showlegend']=False
            fig1['data'][1]['showlegend']=False
            
            
            fig = make_subplots(rows=2,cols=2,subplot_titles=['Histogram','Box plot'],specs=[[{'type':'histogram'},{'type':'box','rowspan':2}],
                                                                                            [{'type':'histogram'},None]])
            fig.layout["xaxis"].title.text = ''
            fig.layout["xaxis2"].title.text = ''
            fig.layout["xaxis3"].title.text = k
            fig.layout["yaxis"].title.text = 'count'
            fig.layout["yaxis2"].title.text = k
            fig.layout["yaxis3"].title.text = 'count'
        
            fig.add_trace(trace1,1,1)
            fig.add_trace(trace2,2,1)
            fig.add_trace(trace3,1,2)
            fig.add_trace(trace4,1,2)
            
            fig.update_layout(template='plotly_dark',boxmode='group')
            fig.show()