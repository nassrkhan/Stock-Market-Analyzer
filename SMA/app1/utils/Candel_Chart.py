import plotly.graph_objects as go
import pandas as pd
import numpy as np

class Candlestic:
    def __init__(self, df):
        self.df=df
        
    @property
                         
    def can_gph(self):
        
        def movingaverage(interval, window_size=20):
            window = np.ones(int(window_size)) / float(window_size)
            #same -> same outputlike interval
            return np.convolve(interval, window, 'same')
        
        def bbands(price, window_size=20, num_of_std=2):
            rolling_mean = price.rolling(window=window_size).mean()
            rolling_std = price.rolling(window=window_size).std()
            upper_band = rolling_mean + (rolling_std * num_of_std)
            lower_band = rolling_mean - (rolling_std * num_of_std)
            return rolling_mean, upper_band, lower_band
        
        df = self.df
        
        #index for companies in for loop of color
        df = df.set_index('Date')

        mv_y = movingaverage(df.Close)
        mv_x = list(df.index)
        
        # Clip the ends
        mv_x = mv_x[10:-10]
        mv_y = mv_y[10:-10]
                    
        bb_avg, bb_upper, bb_lower = bbands(df.Close)
        
        INCREASING_COLOR = "#00994d"
        DECREASING_COLOR = "#cc0000"

        colors = []
                    
        for i in range(len(df.Close)):
            if i != 0:
                if df["Close"][i] > df.Close[i - 1]:
                    colors.append(INCREASING_COLOR)
                else:
                    colors.append(DECREASING_COLOR)
            else:
                colors.append(DECREASING_COLOR)
        
        can_gph = {
        "name": "Candlestic", 
        "type": "candlestick", 
        "x": df.index,  
        "xaxis": "x", 
        "yaxis": "y", 
        "low": df["Low"], 
        "high": df["High"], 
        "open": df["Open"], 
        "close": df["Close"], 
        "decreasing": {"line": {"color" : DECREASING_COLOR}}, 
        "increasing": {"line": {"color" : INCREASING_COLOR}}
        }

        vol_gph = {
            "name": "Volume", 
            "type": "bar",
            #"width": 10,
            "x": df.index, 
            "y": df.Volume,  
            "xaxis": "x", 
            "yaxis": "y2",
            "marker": {"color" : colors, "line" :{ "color" :colors, "width" :3}, }
        }

        mov_gph = {
            "line": { "color": "#000000", "width": 2, }, 
            "mode": "lines", 
            "name": "Moving Average", 
            "type": "scatter", 
            "x": mv_x, 
            "y": mv_y,  
            "xaxis": "x", 
            "yaxis": "y"
        }

        ubb_gph = {
            "fill": "tonexty", 
            "line": {"dash": "4px", "color": "#737373", "width": 1, }, 
            "mode": "lines", 
            "name": "Upper Bollinger Band", 
            "type": "scatter", 
            "legendgroup":'Bollinger Bands',
            "x": df.index, 
            "y": bb_upper,  
            "xaxis": "x", 
            "yaxis": "y", 
            "fillcolor": "rgba(194, 240, 240, 0.2)"
        }

        std_gph = {
            "line": {"dash": "5px", "color": "#33bbff", "width": 2, }, 
            "mode": "lines", 
            "name": "Middle Band", 
            "type": "scatter", 
            "x": df.index, 
            "y": bb_avg,  
            "xaxis": "x", 
            "yaxis": "y"
        }

        lbb_gph = {
            "fill": "tonexty", 
            "line": {"dash": "4px", "color": "#737373", "width": 1,}, 
            "mode": "lines", 
            "name": "Lower Bollinger Band", 
            "legendgroup":'Bollinger Bands', 
            "showlegend":False,
            "type": "scatter", 
            "x": df.index, 
            "y": bb_lower, 
            "xaxis": "x", 
            "yaxis": "y", 
            "fillcolor": "rgba(194, 240, 240, 0.2)"
        }

        data = [can_gph, vol_gph, mov_gph, std_gph, ubb_gph, lbb_gph]

        layout = {
            "width": 950, 
            "xaxis": { "domain": [0, 0.95], "rangeslider": {"visible": True}, 
            "rangeselector": {"x": 0, "y": 0.9, "font": {"color": "white"}, "bgcolor": "#0099cc", 

            "buttons": [
                {
                    "step": "all", 
                    "count": 1, 
                    "label": "reset"
                },

                {
                  "step": "year", 
                  "count": 1, 
                  "label": "1 Year", 
                  "stepmode": "backward"
                }, 

                {
                  "step": "month", 
                  "count": 1, 
                  "label": "1 Month", 
                  "stepmode": "backward"
                }, 

                {
                  "step": "month", 
                  "count": 3, 
                  "label": "3 Month", 
                  "stepmode": "backward"
                }, 

                {
                  "step": "month", 
                  "count": 6, 
                  "label": "6 Month", 
                  "stepmode": "backward"
                },

                {"step": "all"}
              ]
            }
          }, 

            "yaxis": { "domain": [0.22, 0.9] }, 
            "height": 800, 
            "margin": { "b": 40, "l": 60, "r": 10, "t": 25}, 
            "yaxis2": {"side": "left", "domain": [0, 0.18]}, 

            "dragmode": "zoom", 
            "showlegend": True,
            #"showgrid":False,
            "legend":{"orientation":"h", "yanchor":"bottom", "y":0.93, "xanchor":"right", "x":0.95},

            "plot_bgcolor": "#ffffff",
        }

        fig = go.Figure(data=data, layout=layout)

        config={'modeBarButtonsToAdd':["v1hovermode","toggleSpikelines"],"displaylogo": False,}

        #fig.show(config=config)
        
        return fig,config