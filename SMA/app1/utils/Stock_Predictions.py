import datetime
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Create the Stacked LSTM model
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import load_model

import plotly.graph_objects as go

# Calculate RMSE performance metrics
from sklearn.metrics import mean_squared_error
from numpy import array


class Prediction:
    def __init__(self, df):
        self.df = df

    @property
    def pre_data(self):

        # convert an array of values into a dataset matrix
        def create_dataset(dataset, time_step):
            dataX, dataY = [], []
            for i in range(len(dataset)-time_step-1):
                a = dataset[i:(i+time_step), 0]  # i=0, 0,1,2,3-----99   100
                dataX.append(a)
                dataY.append(dataset[i + time_step, 0])
            return np.array(dataX), np.array(dataY)

        df = self.df

        df_lst = []
        for i in df.columns:

            if i == "Date":
                last_date = df["Date"].iat[-1]
                nxtdays = 30
                date_1 = datetime.datetime.strptime(str(last_date), "%Y-%m-%d")

                # tolist
                date_list = [ date_1 + datetime.timedelta(days=x) for x in range(nxtdays)]
                df_lst.append(date_list)
                continue
            else:
                # access col
                df2 = df.loc[:, i]

                # scale
                scaler = MinMaxScaler(feature_range=(0, 1))

                # (nR:1C)
                df2 = scaler.fit_transform(np.array(df2).reshape(-1, 1))  

                # splitting dataset into train and test split 70% and 30%
                training_size = int(len(df2)*0.7)
                #slicing R:C 
                train_data, test_data = df2[0:training_size,:],df2[training_size:len(df2), :]

                # reshape into X=t,t+1,t+2,t+3 and Y=t+4
                time_step = 10
                X_train, y_train = create_dataset(train_data, time_step)
                X_test, ytest = create_dataset(test_data, time_step)

                # reshape input to be [samples, time steps, features] which is required for LSTM
                #shape -> no
                X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
                X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

                # model = load_model('staticfiles/Ml_Models/' + i + ".h5")
                model = load_model('F:/5. UNI/1. Fahads Uni/FYP/2. FYP (Part-2)/Stock Market Analyzer (Final)/SMA/static/Ml Models/' + i + ".h5")
                # model.summary()

                lnt = len(test_data)

                pre_tst_data = lnt-time_step

                x_input = test_data[pre_tst_data:].reshape(1, -1)
                x_input.shape

                temp_input = list(x_input)
                temp_input = temp_input[0].tolist()

                # demonstrate prediction for next 30 days
                lst_output = []
                # n_steps=10
                i = 0
                while(i < 30):

                    if(len(temp_input) > 10):
                        x_input = np.array(temp_input[1:])
                        x_input = x_input.reshape(1, -1)
                        x_input = x_input.reshape((1, time_step, 1))

                        yhat = model.predict(x_input, verbose=0)

                        temp_input.extend(yhat[0].tolist())
                        temp_input = temp_input[1:]

                        lst_output.extend(yhat.tolist())
                        i = i+1
                    else:
                        x_input = x_input.reshape((1, time_step, 1))
                        yhat = model.predict(x_input, verbose=0)

                        temp_input.extend(yhat[0].tolist())

                        lst_output.extend(yhat.tolist())
                        i = i+1
                lst_output = scaler.inverse_transform(lst_output)
                lst_output = list(np.concatenate(lst_output).flat)
                df_lst.append(lst_output)
        df3 = pd.DataFrame(data=df_lst).T
        df3.columns = ["Date", "Open", "High", "Low", "Close"]

        # tosort
        df3["Date"] = pd.to_datetime(df3["Date"])
        df3 = df3.sort_values(by="Date")
        df3["Date"] = df3["Date"].dt.strftime("%Y-%m-%d")

        for i in df3.columns:
            if i == "Date":
                continue

            else:
                df3[i] = df3[i].astype(float)
                df3[i] = df3[i].round(decimals=2)
        return df3

    # table Design
    def Pred_Dsg(self, df):

        table = {
            "type": "table",
            "cells": {
                "fill": {"color": ["rgb(128, 255, 170)", "rgb(242, 242, 242)"]},

                "font": { "size": 12, "color": ["rgb(40, 40, 40)"]},

                "height": 27,
                "align": ["center"],
                "format": [None, ", .2f", ", .2f", ",.2f", ",.2f"],

                "values": [df.Date, df.Open, df.High, df.Low, df.Close]
            },

            "domain": {  "x": [0, 1], "y": [0.7, 1] },

            "header": {
                "fill": {"color": "rgb(128, 255, 170)"},

                "font": { "size": 14,  "color": ["rgb(45, 45, 45)"] },

                "height": 40,
                "align": ["center"],
                "values": ["<b>Date</b>", "<b>Open</b>", "<b>High</b>", "<b>Low</b>", "<b>Close</b>"],
            },

            "columnorder": [0, 1, 2, 3, 4],
            "columnwidth": [2, 1, 1, 1, 1]
        }

        bar_open = {
            "name": "OPEN",
            "type": "bar",

            "x": df.Date,
            "y": df.Open,

            "xaxis": "x1",
            "yaxis": "y1"
        }

        bar_high = {
            "name": "HIGH",
            "type": "bar",

            "x": df.Date,
            "y": df.High,

            "xaxis": "x1",
            "yaxis": "y1"
        }

        bar_low = {
            "name": "LOW",
            "type": "bar",

            "x": df.Date,
            "y": df.Low,

            "xaxis": "x1",
            "yaxis": "y1"
        }

        bar_close = {
            "name": "CURRENT",
            "type": "bar",

            "x": df.Date,
            "y": df.Close,

            "xaxis": "x1",
            "yaxis": "y1"
        }

        ln_high = {

            "line": {"color": "#33cc33", "width": 2},

            "mode": "lines+markers",

            "name": "High",

            "type": "scatter",

            "x": df.Date,
            "y": df.High,

            "xaxis": "x2",
            "yaxis": "y2"
        }

        ln_low = {

            "line": {"color": "#cc3300", "width": 2},

            "mode": "lines+markers",

            "name": "Low",

            "type": "scatter",

            "x": df.Date,
            "y": df.Low,

            "xaxis": "x2",
            "yaxis": "y2"
        }

        ln_open = {

            "line": {"color": "#ff9900", "width": 2},

            "mode": "lines+markers",

            "name": "Open",

            "type": "scatter",

            "x": df.Date,
            "y": df.Open,

            "xaxis": "x2",
            "yaxis": "y2"
        }

        ln_close = {

            "line": {"color": "#cc6600", "width": 2},

            "mode": "lines+markers",

            "name": "Close",

            "type": "scatter",

            "x": df.Date,
            "y": df.Close,

            "xaxis": "x2",
            "yaxis": "y2"
        }
        ohlc = {
            "type": "ohlc",
            "name": "OHLC",
            "x": df.Date,
            "low": df.Low,
            "high": df.High,
            "open": df.Open,
            "close": df.Close,

            "xaxis": "x3",
            "yaxis": "y3"
        }

        data = [table, bar_open, bar_high, bar_low, bar_close, ln_high, ln_low, ln_open, ln_close, ohlc]
        layout = {
            "width": 950,
            "height": 800,
            "margin": {"t": 100},
            "xaxis1": {
                "anchor": "y1",
                "domain": [0, 1],
                "mirror": True,
                "ticklen": 4,
                "showgrid": True,
                "showline": True,
                "tickfont": {"size": 10},
                "zeroline": False,
                "gridcolor": "#ffffff",
                "showticklabels": False
            },
            "xaxis2": {
                "anchor": "y2",
                "domain": [0, 1],
                "mirror": True,
                "ticklen": 4,
                "showgrid": True,
                "showline": True,
                "tickfont": {"size": 10},
                "zeroline": False,
                "gridcolor": "#ffffff",
                "showticklabels": False
            },
            "xaxis3": {
                "anchor": "y3",
                "domain": [0, 1],
                "mirror": True,
                "ticklen": 4,
                "showgrid": True,
                "showline": True,
                "tickfont": {"size": 10},
                "zeroline": False,
                "gridcolor": "#ffffff",
                "rangeslider": {"visible": False }
            },
            "yaxis1": {
                "anchor": "x1",
                "domain": [0.46, 0.68],
                "mirror": True,
                "ticklen": 4,
                "showgrid": True,
                "showline": True,
                "tickfont": {"size": 10},
                "zeroline": False,
                "gridcolor": "#ffffff",
            },
            "yaxis2": {
                "anchor": "x2",
                "domain": [0.22, 0.44],
                "mirror": True,
                "ticklen": 4,
                "showgrid": True,
                "showline": True,
                "tickfont": {"size": 10},
                "zeroline": False,
                "gridcolor": "#ffffff",
                "hoverformat": ".2f"
            },
            "yaxis3": {
                "anchor": "x3",
                "domain": [0.0, 0.21],
                "mirror": True,
                "ticklen": 4,
                "showgrid": True,
                "showline": True,
                "tickfont": {"size": 10},
                "zeroline": False,
                "gridcolor": "#ffffff",
                "hoverformat": ".2f"
            },
            "autosize": True,
            "showlegend": True,
            "legend": {
                "orientation": "h",
                "yanchor": "bottom",
                "y": 1.02,
                "xanchor": "right",
                "x": 1
            },
            "barmode": "stack",
            "plot_bgcolor": "#ffffff"
        }
        fig = go.Figure(data=data, layout=layout)
        config = {'modeBarButtonsToAdd': ["v1hovermode", "toggleSpikelines"],
                  "displaylogo": False,
                  "modeBarButtonsToRemove": ["lasso2d", "zoom2d"]}
        return fig, config

# Lets Do the prediction and check performance Metrics   
            
            # train_predict = model.predict(X_train)
            # test_predict = model.predict(X_test)

            # Transformback to original form
            # train_predict = scaler.inverse_transform(train_predict)
            # test_predict = scaler.inverse_transform(test_predict)

            # math.sqrt(mean_squared_error(y_train,train_predict)) 

            # Test Data RMSE
            # math.sqrt(mean_squared_error(ytest,test_predict))

#ML model Function
    # def Pre_model(i,time_step,X_train,y_train,X_test,ytest):
    #     model=Sequential()
    #     #rectified linear activation function
    #     model.add(LSTM(32,return_sequences=False, activation="relu", input_shape=(time_step,1)))#T_S 10
    #     #1 -> previous out shape
    #     model.add(Dense(1))
    #     # Adam -> computationally efficient, low memory requirements, large number of parameters.
    #     model.compile(loss="mean_squared_error",optimizer="adam")

    #     model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=100,batch_size=64,verbose=1)
    #     model.save(i+".h5") #using h5 extension

    #     return print("model saved!!!")

# predictionfunction
#Pr=Pre_model(i,time_step,X_train,y_train,X_test,ytest)