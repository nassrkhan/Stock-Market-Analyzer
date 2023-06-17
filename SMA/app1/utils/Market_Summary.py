import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup
import requests

import plotly.graph_objects as go


class Today_Market:
    def __init__(self):

        # url to read market summary
        self.url = "https://www.psx.com.pk/market-summary/"

    @property
    def Scrap_Table(self):

        # read scraped tables
        headers = {
            "User-Agent": "Mozilla/5.0(Window NT 10.0; x64) AppleWebKit/537.36 (KHTML,like gecko) chrome/74.0.3729.169 Safari"}
        req = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(req.content, features="lxml")
        main_tab = soup.find("div", {"id": "marketmainboard"})
        t_table = []
        for word in main_tab.find_all("div", attrs={"class": "table-responsive"}):
            t_table.append(word)
        #header=1 -> column names.    
        scp_table = pd.read_html(str(t_table), header=1)

        # empty Datafrme
        df = pd.DataFrame()

        # loop to access all table
        for i in range(0, len(scp_table)):

            data = scp_table[i]

            #object -> any data type
            tab = np.array(data, dtype=object)
            df1 = pd.DataFrame(tab.tolist())

            # concat Tables , axis =0 -> concatenated along the rows.
            df = pd.concat([df, df1], ignore_index=True, axis=0)

        df.columns = ["SCRIP", "LDCP", "OPEN", "HIGH", "LOW", "CURRENT", "CHANGE", "VOLUME"]

        return df

    # table Design
    def Table_Dsg(self, df):
        try:
            if len(df) != 0:

                df["SCRIP"] = df["SCRIP"].str.replace( r"\[.*?\]", "", regex=True)

                table = {
                    "type": "table",
                    "cells": {
                        "fill": {"color": ["rgb(128, 255, 170)", "rgb(242, 242, 242)"]},

                        "font": {"size": 12, "color": ["rgb(40, 40, 40)"]},
                        
                        "height": 27,
                        "align": ["center"],
                        "format": [None, ", .2f", ", .2f", ",.2f", ",.2f", ", .2f", ", .2f", None],
                        "values": [df.SCRIP, df.LDCP, df.OPEN, df.HIGH, df.LOW, df.CURRENT, df.CHANGE, df.VOLUME],
                    },

                    "header": {
                        "fill": {"color": "rgb(128, 255, 170)"},

                        "font": {"size": 14, "color": ["rgb(45, 45, 45)"]},

                        "height": 40,
                        "align": ["center"],
                        "values": ["<b>SCRIP</b>", "<b>LDCP</b>", "<b>OPEN</b>", "<b>HIGH</b>", "<b>LOW</b>", "<b>CURRENT</b>", "<b>CHANGE</b>", "<b>VOLUME</b>"]
                    },

                    "columnorder": [0, 1, 2, 3, 4, 5, 6, 7],
                    "columnwidth": [100, 25, 25, 25, 25, 30, 30, 30],
                }

                data = table

                layout = {
                    "autosize": False,
                    "width": 1024,
                    "height": 850,
                    "margin": {"t": 40},
                    "plot_bgcolor": "rgba(228, 222, 249, 0.65)"
                }

                fig = go.Figure(data=data, layout=layout)
                config = {"displaylogo": False}
                return fig, config
        except:
            print("There is Problem exist data not found")

    # market chart
    def Market_Dsg(self, df):

        m_volume = {

            "line": {"color": "#4d4d33", "width": 2},

            "fill": "tozerox",

            "mode": "lines",

            "name": "VOLUME",

            "type": "scatter",

            "x": df.SCRIP,
            "y": df.VOLUME,

            "xaxis": "x1",
            "yaxis": "y1"
        }

        m_change = {

            "line": {"color": "#39ac73", "width": 2},

            "fill": "tozerox",

            "mode": "lines",

            "name": "CHANGE",

            "type": "scatter",

            "x": df.SCRIP,
            "y": df.CHANGE,

            "xaxis": "x2",
            "yaxis": "y2"
        }

        m_current = {

            "line": {"color": "#0066ff", "width": 2},

            "fill": "tozerox",

            "mode": "lines",

            "name": "CURRENT",

            "type": "scatter",

            "x": df.SCRIP,
            "y": df.CURRENT,

            "xaxis": "x3",
            "yaxis": "y3"
        }

        m_low = {

            "line": {"color": "#e61919", "width": 2},

            "fill": "tozerox",

            "mode": "lines",

            "name": "LOW",

            "type": "scatter",

            "x": df.SCRIP,
            "y": df.LOW,

            "xaxis": "x4",
            "yaxis": "y4"
        }

        m_high = {

            "line": {"color": "#009933", "width": 2},

            "fill": "tozerox",

            "mode": "lines",

            "name": "HIGH",

            "type": "scatter",

            "x": df.SCRIP,
            "y": df.HIGH,

            "xaxis": "x5",
            "yaxis": "y5"
        }

        m_open = {

            "line": {"color": "#004080", "width": 2},

            "fill": "tozerox",

            "mode": "lines",

            "name": "OPEN",

            "type": "scatter",

            "x": df.SCRIP,
            "y": df.OPEN,

            "xaxis": "x6",
            "yaxis": "y6"
        }

        m_ldcp = {

            "line": {"color": "#996600", "width": 2},

            "fill": "tozerox",

            "mode": "lines",

            "name": "LDCP",

            "type": "scatter",

            "x": df.SCRIP,
            "y": df.LDCP,

            "xaxis": "x7",
            "yaxis": "y7"
        }

        data = [m_volume, m_change, m_current, m_low, m_high, m_open, m_ldcp]

        layout = {
            "width": 900,
            "height": 1024,

            "plot_bgcolor": "#ffffff",

            "margin": {"t": 20, "b": 20, "l": 20},

            "xaxis1": {"anchor": "y1", "domain": [0, 1], "showticklabels": False, "gridcolor": "#d1e0e0"},

            "xaxis2": {"anchor": "y2", "domain": [0, 1], "showticklabels": False, "gridcolor": "#d1e0e0"},

            "xaxis3": {"anchor": "y3", "domain": [0, 1], "showticklabels": False, "gridcolor": "#d1e0e0"},

            "xaxis4": {"anchor": "y4", "domain": [0, 1], "showticklabels": False, "gridcolor": "#d1e0e0"},

            "xaxis5": {"anchor": "y5", "domain": [0, 1], "showticklabels": False, "gridcolor": "#d1e0e0"},

            "xaxis6": {"anchor": "y6", "domain": [0, 1], "showticklabels": False, "gridcolor": "#d1e0e0"},

            "xaxis7": {"anchor": "y7", "domain": [0, 1], "showticklabels": False, "gridcolor": "#d1e0e0"},

            "yaxis1": {"anchor": "x1", "domain": [0, 0.12], "gridcolor": "#d1e0e0"},

            "yaxis2": {"anchor": "x2", "domain": [0.14, 0.26], "gridcolor": "#d1e0e0"},

            "yaxis3": {"anchor": "x3", "domain": [0.28, 0.40], "gridcolor": "#d1e0e0"},

            "yaxis4": {"anchor": "x4", "domain": [0.42, 0.52], "gridcolor": "#d1e0e0"},

            "yaxis5": {"anchor": "x5", "domain": [0.54, 0.66], "gridcolor": "#d1e0e0"},

            "yaxis6": {"anchor": "x6", "domain": [0.68, 0.78], "gridcolor": "#d1e0e0"},

            "yaxis7": {"anchor": "x7", "domain": [0.80, 0.92], "gridcolor": "#d1e0e0"},

            "legend": {"orientation": "h", "yanchor": "bottom", "y": 0.94, "xanchor": "right", "x": 1},
            "modebar_add": ["v1hovermode", "toggleSpikelines"]
        }

        fig = go.Figure(data=data, layout=layout)
        config = {"displaylogo": False}

        return fig, config

    # bullet chart
    def Bullet_Dsg(self, df):

        current = df['CURRENT'].sum()

        ldcp = df['LDCP'].sum()

        volume = df['VOLUME'].sum()

        count = df['CHANGE'].value_counts()[0]

        chng = {
            "type": "indicator",
            "mode": "number+gauge+delta",
            "value": current,
            "delta": {"reference": ldcp},
            "domain": {"x": [0.39, 1], "y": [0.08, 0.25]},
            "title": {"text": "<b>Current/Change</b>"},

            "gauge": {
                    "shape": "bullet",
                    "axis": {"range": [None, current*2]},
                    "threshold": {"line": {"color": "red", "width": 2}, "thickness": 0.75, "value": ldcp},
                    "steps": [{"range": [0, current], "color": "gray"},
                              {"range": [current, current*2], "color": "lightgray"}],
                    "bar": {"color": "black"}
            }
        }

        tot_vol = {
            "type": "indicator",
            "mode": "number+gauge",
                    "value": volume,
                    "domain": {"x": [0.39, 1], "y": [0.4, 0.6]},
                    "title": {"text": "<b>Total Market Volume</b>"},

                    "gauge": {
                        "shape": "bullet",
                        "axis": {"range": [None, volume*2]},
                        "steps": [
                            {"range": [0, volume], "color": "gray"},
                            {"range": [volume, volume*2], "color": "lightgray"}],
                        "bar": {"color": "black"}
                    }
        }

        unchng = {
            "type": "indicator",
            "mode": "number+gauge",
            "value": count,
            "domain": {"x": [0.39, 1], "y": [0.7, 0.9]},
            "title": {"text": "<b>Un-Change Stock companies</b>"},

            "gauge": {
                'shape': "bullet",
                "axis": {"range": [None, len(df)]},
                "steps": [
                    {"range": [0, count], "color": "gray"},
                    {'range': [count, len(df)], "color": "lightgray"}],
                "bar": {"color": "black"}
            }
        }

        data = [chng, tot_vol, unchng]

        layout = {
            "width": 1024,
            "height": 400,
            "margin": {"t": 20, "b": 20, "l": 20},
            "plot_bgcolor": "rgba(228, 222, 249, 0.65)"
        }

        fig = go.Figure(data=data, layout=layout)
        config = {"displaylogo": False, }

        return fig, config

    # pie chart

    def Pie_Dsg(self, df):
        # Define pie chart
        pie = {
            "type": "pie",
            "labels": df.SCRIP,
            "values": df.VOLUME,
            "name": "VOLUME",
            "hoverinfo": "label+percent+name",
            "textposition": "inside"
        }
        data = pie
        layout = {
            "width": 900,
            "height": 400,
            "margin": {"t": 20, "b": 20, "l": 20},
            "plot_bgcolor": "rgba(228, 222, 249, 0.65)",
        }
        fig = go.Figure(data=data, layout=layout)
        config = {"displaylogo": False}

        return fig, config

    # Top 10 Companies  chart
    def Tt_Com_Dsg(self, df):

        df1 = df.nlargest(10, "VOLUME")
        df1 = df1.sort_values(by=["CURRENT"])

        tt_ldcp = {
            "name": "LDCP",
            "type": "bar",

            "x": df1.SCRIP,
            "y": df1.LDCP,

            "xaxis": "x1",
            "yaxis": "y1"
        }

        tt_open = {
            "name": "OPEN",
            "type": "bar",

            "x": df1.SCRIP,
            "y": df1.OPEN,

            "xaxis": "x1",
            "yaxis": "y1"
        }

        tt_high = {
            "name": "HIGH",
            "type": "bar",

            "x": df1.SCRIP,
            "y": df1.HIGH,

            "xaxis": "x1",
            "yaxis": "y1"
        }

        tt_low = {
            "name": "LOW",
            "type": "bar",

            "x": df1.SCRIP,
            "y": df1.LOW,

            "xaxis": "x1",
            "yaxis": "y1"
        }

        tt_current = {
            "name": "CURRENT",
            "type": "bar",

            "x": df1.SCRIP,
            "y": df1.CURRENT,

            "xaxis": "x1",
            "yaxis": "y1"
        }

        tt_change = {
            "name": "CHANGE",
            "type": "bar",

            "x": df1.SCRIP,
            "y": df1.CHANGE,

            "xaxis": "x1",
            "yaxis": "y1"
        }

        tt_volume = {
            "name": "VOLUME",
            "type": "bar",

            "x": df1.SCRIP,
            "y": df1.VOLUME,

            "xaxis": "x2",
            "yaxis": "y2"
        }

        ln_volume = {

            "line": {"color": "#3399ff", "width": 2},

            "mode": "lines+markers",

            "name": "Volume",

            "type": "scatter",

            "x": df1.SCRIP,
            "y": df1.VOLUME,

            "xaxis": "x2",
            "yaxis": "y2"
        }

        data = [tt_ldcp, tt_open, tt_high, tt_low,
                tt_current, tt_change, tt_volume, ln_volume]

        layout = {

            "width": 1000,
            "height": 600,

            "plot_bgcolor": "#ffffff",

            "legend": {"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
            "barmode": "stack",

            "xaxis1": {"anchor": "y1", "domain": [0.0, 0.45], "gridcolor": "#d1e0e0"},

            "xaxis2": {"anchor": "y2", "domain": [0.55, 1.0], "gridcolor": "#d1e0e0"},

            "yaxis1": {"anchor": "x1", "domain": [0.0, 1.0], "gridcolor": "#d1e0e0"},

            "yaxis2": {"anchor": "x2", "domain": [0.0, 1.0], "gridcolor": "#d1e0e0"},

            "modebar_add": ["v1hovermode", "toggleSpikelines"]

        }

        fig = go.Figure(data=data, layout=layout)
        config = {"displaylogo": False}

        return fig, config
