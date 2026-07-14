"""
Wildfire & Power Grid Monitoring - 最小 Dash 骨架
用于先跑通界面结构，之后把 load_data() 换成读取真实的 Vivado CSV 即可。
"""

import numpy as np
import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go


# ---------------------------------------------------------------------------
# 1. 数据加载区
#    现在用随机模拟数据，之后换成: df = pd.read_csv("你的vivado输出.csv")
#    真实CSV建议至少包含这些列: time, raw_signal, conditioned_signal, threshold, alarm
# ---------------------------------------------------------------------------
def load_data():
    n = 500
    t = np.arange(n) * 0.001  # 假设采样间隔 1ms

    raw = np.sin(2 * np.pi * 5 * t) + np.random.normal(0, 0.15, n)
    conditioned = np.convolve(raw, np.ones(8) / 8, mode="same")  # 简单模拟平滑滤波

    threshold = 0.6
    alarm = (np.abs(conditioned) > threshold).astype(int)

    df = pd.DataFrame({
        "time": t,
        "raw_signal": raw,
        "conditioned_signal": conditioned,
        "threshold": threshold,
        "alarm": alarm,
    })
    return df


df = load_data()


# ---------------------------------------------------------------------------
# 2. 构建图表
# ---------------------------------------------------------------------------
def build_signal_figure(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["time"], y=df["raw_signal"],
        mode="lines", name="Raw Signal", opacity=0.5
    ))
    fig.add_trace(go.Scatter(
        x=df["time"], y=df["conditioned_signal"],
        mode="lines", name="Conditioned Signal", line=dict(width=2)
    ))
    fig.add_hline(
        y=df["threshold"].iloc[0], line_dash="dash", line_color="red",
        annotation_text="Threshold"
    )
    fig.update_layout(
        title="Raw vs Conditioned Signal",
        xaxis_title="Time (s)",
        yaxis_title="Amplitude",
        template="plotly_white",
        height=400,
    )
    return fig


# ---------------------------------------------------------------------------
# 3. 报警状态指示灯（颜色随 alarm 列变化）
# ---------------------------------------------------------------------------
def alarm_indicator(df):
    is_alarm = df["alarm"].iloc[-1] == 1
    color = "#e74c3c" if is_alarm else "#2ecc71"
    text = "ALARM" if is_alarm else "NORMAL"
    return html.Div(
        text,
        style={
            "backgroundColor": color,
            "color": "white",
            "padding": "12px 24px",
            "borderRadius": "8px",
            "display": "inline-block",
            "fontWeight": "bold",
            "fontSize": "18px",
        },
    )


# ---------------------------------------------------------------------------
# 4. 页面布局
# ---------------------------------------------------------------------------
app = Dash(__name__)

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "margin": "30px"},
    children=[
        html.H1("野火 & 电网监测 - 信号显示"),
        html.Div(alarm_indicator(df), style={"marginBottom": "20px"}),
        dcc.Graph(figure=build_signal_figure(df)),
    ],
)


# ---------------------------------------------------------------------------
# 5. 启动
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)