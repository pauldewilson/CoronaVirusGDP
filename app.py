from models.df_corona_gdp import DF_Corona_GDP
import plotly.graph_objs as go
import plotly.offline as pyo

# note: can have different data and chart types since df_corona model has this ability
# however this was a one time exercise and so the function was not built

df = DF_Corona_GDP().return_main_df()

if __name__ == '__main__':
    data = []
    for country in df.index.values:
        df_filt = df[df.index == country]
        data.append(
            go.Scatter(
                x=df_filt['Deaths_Capita'],
                y=df_filt['GDP_Capita'],
                mode='markers',
                name=country,
                marker=dict(
                    size=15
                )
            )
        )

    layout = go.Layout(
        title=dict(
            text='Deaths from Covid-19 against GDP (note: GDP figures are open to debate, naturally)'
        ),
        xaxis=dict(
            title=dict(
                text='Total Deaths by Covid-19 Per 100,000'
            )
        ),
        yaxis=dict(
            title=dict(
                text='GDP Per Capita'
            )
        ),
        yaxis_type='log',
        xaxis_type='log'
    )

    fig = go.Figure(data=data,
                    layout=layout)

    pyo.plot(fig,
             filename='output_plot.html')
