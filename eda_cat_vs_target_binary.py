import pandas as pd
import ipywidgets as widgets
from IPython.core.display import display, HTML
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def eda_cat_vs_target_binary(dataframe):
    '''dataframe: pd.DataFrame'''
    dataframe_cat = dataframe.select_dtypes(exclude='number') # select cat data
    dataframe_target = pd.DataFrame(dataframe[dataframe.columns.values[-1]]) # get the response col
    
    # check values for the response col
    ### source https://stackoverflow.com/questions/19913659/pandas-conditional-creation-of-a-series-dataframe-column
    values_dict = {'no':0,'yes':1,1:1,2:0}
    values_dict_other = {x:'not_found' for x in dataframe[dataframe.columns.values[-1]].unique() if x not in values_dict}
    values_dict.update(values_dict_other)
    ###
    
    # if the response col is cat, get the cat dataframe and create a new col for the response col called 'conversions' which is binary (0's and 1's).
    # if the response call is numeric, it will not be in the cat dataframe so add the numeric response col to the cat dataframe and again 
    # create a new col called 'conversions' which is binary: 0's and 1's
    if dataframe[dataframe.columns.values[-1]].dtype==object:
        dataframe = dataframe_cat.copy()
        dataframe['conversions'] = dataframe[dataframe.columns.values[-1]].map(values_dict)
    else :
        dataframe = pd.concat([dataframe_cat,dataframe_target],axis=1)
        dataframe['conversions'] = dataframe[dataframe.columns.values[-1]].map(values_dict)
    
    # define the tabs
    tab_contents = [i for i in dataframe.columns[0:-2]] # not including the response col and the 'conversions' col
    children = [widgets.Output() for value in tab_contents]
    tab = widgets.Tab(children=children)
    [tab.set_title(num,name) for num,name in enumerate(tab_contents)]
    display(tab)
    
    
    for i,k in enumerate(dataframe.columns.values[0:-2]): # not including the response col and the 'conversions' col 
        dataframe['conversions']=dataframe_target.copy()
        
        with children[i]:
            
            # out for the dataframes that will be create next
            out_dataframe1 = widgets.Output()
            out_dataframe2 = widgets.Output()
            out_dataframe3 = widgets.Output()
            out_dataframe4 = widgets.Output()
            hbox = widgets.HBox([out_dataframe1,out_dataframe2,out_dataframe3,out_dataframe4])
    
            # Feature summary
            with out_dataframe1:
                dataframe1 = pd.DataFrame(dataframe[k].value_counts()).reset_index()
                dataframe1.columns = [k,'count']
                dataframe1['proportions (%)'] = (dataframe1['count']/len(dataframe)*100)
                #dataframe1 = dataframe1.set_index(k)
                dataframe1 = dataframe1.sort_values(k,ascending=True)
                dataframe1['rank'] = dataframe1[dataframe1.columns[1]].rank(ascending=1)
                dataframe1_styled = dataframe1.style.set_caption('Feature summary').set_precision(2).hide_index().hide_columns(['rank'])
                display(dataframe1_styled) 
                
            # Feature vs target summary
            with out_dataframe2:
                dataframe2 = pd.pivot_table(dataframe,values=dataframe.columns.values[-2],index=k,
                                            columns=dataframe.columns.values[-1],aggfunc=len,margins=True,margins_name='Totals')
                dataframe2 = pd.DataFrame(dataframe2.to_records())
                dataframe2 = dataframe2.set_index(k)
                dataframe2 = dataframe2.drop('Totals',axis=0)
                dataframe2 = dataframe2.reset_index()
                dataframe2 = dataframe2.sort_values(k,ascending=True)
                dataframe2_styled = dataframe2.style.set_caption('Feature vs target summary').set_precision(2).hide_index() 
                display(dataframe2_styled)
                
            # target proportions per category level
            with out_dataframe3:
                dataframe3 = pd.crosstab(dataframe[k],dataframe[dataframe.columns.values[-1]],normalize='index')*100
                dataframe3 = pd.DataFrame(dataframe3.to_records())
                #dataframe3 = dataframe3.set_index(k)
                dataframe3 = dataframe3.sort_values(k,ascending=True)
                dataframe3_styled = dataframe3.style.set_caption('Target proportions (%) per category level (normalization = ''row'')').set_precision(3).hide_index()
                display(dataframe3_styled)
                
            # Proportions category level by response
            with out_dataframe4:
                dataframe4 = pd.crosstab(dataframe[k],dataframe[dataframe.columns.values[-1]],normalize='columns')*100
                dataframe4 = pd.DataFrame(dataframe4.to_records())
                dataframe4 = dataframe4.sort_values(k,ascending=True)
                dataframe4_styled = dataframe4.style.set_caption('Proportion (%) category level by target (normalization = ''col'')').set_precision(3).hide_index()
                display(dataframe4_styled)
            display(hbox)
            
            fig=make_subplots(rows=1,cols=3,shared_xaxes=False,specs=[[{"type": "treemap"},{"type": "bar"},{"type":"bar"}]],
                             subplot_titles=('Category Counts','Category Counts by Target','Target proportions by Category (%)'))
                
            # plot feature summary
            fig1=(px.treemap(dataframe1,path=[k],values='proportions (%)',hover_data=['count'],title='Category Counts'))
            
            #plot feature vs target summary
            fig.add_trace(go.Bar(x=dataframe2[k],y=dataframe2[dataframe2.columns[1]],name=dataframe2.columns[1],marker_color='blue',showlegend=False),row=1,col=2)
            fig.add_trace(go.Bar(x=dataframe2[k],y=dataframe2[dataframe2.columns[2]],name=dataframe2.columns[2],marker_color='orange',showlegend=False),row=1,col=2)
            
            # plot target proportions
            width = (dataframe1[dataframe1.columns.values[3]]/10).to_list() # didn't work well
            fig.add_trace(go.Bar(y=dataframe3[k],x=dataframe3[dataframe3.columns[1]],name=dataframe3.columns[1],marker_color='blue',orientation='h',width=width),row=1,col=3)
            fig.add_trace(go.Bar(y=dataframe3[k],x=dataframe3[dataframe3.columns[2]],name=dataframe3.columns[2],marker_color='orange',orientation='h',width=width),row=1,col=3)
            
            trace1=fig1['data'][0]
            
            #fig['data'][2]['yaxis']['tickformat'] = '%'
            
            fig.append_trace(trace1,row=1,col=1)
            fig.update_layout(template='plotly_dark',barmode='stack')
            fig.update_xaxes(tickformat="%", row=1, col=3)
            
            fig.show()
        