import pandas as pd
import plotly.graph_objects as go
import squarify
import numpy as np

# Load data from CSV
df = pd.read_csv('nasdaq100_data.csv')

# Sort data by market cap descending
df = df.sort_values('market_cap', ascending=False).reset_index(drop=True)

# Define colors gradient based on performance
def gradient_color(change):
    if change > 0:
        # Green gradient
        return f'rgba(0,{int(100 + 155 * (min(change,5)/5))},0,0.9)'
    elif change < 0:
        # Red gradient
        return f'rgba({int(100 + 155 * (min(abs(change),5)/5))},0,0,0.9)'
    else:
        # Neutral color for zero change
        return 'rgba(128,128,128,0.6)'

df['color'] = df['percent_change'].apply(gradient_color)

# Normalize sizes for squarify
sizes = squarify.normalize_sizes(df['market_cap'], 100, 100)
rects = squarify.squarify(sizes=sizes, x=0, y=0, dx=100, dy=100)

# Create plotly heatmap figure
fig = go.Figure()

for idx, rect in enumerate(rects):
    ticker = df.loc[idx, 'ticker']
    percent = df.loc[idx, 'percent_change']
    market_cap = df.loc[idx, 'market_cap']
    color = df.loc[idx, 'color']

    # Adaptive font sizing
    rect_area = rect['dx'] * rect['dy']
    font_size = max(min(rect_area * 0.3, 24), 10)

    # Rectangle shapes
    fig.add_shape(
        type="rect",
        x0=rect['x'],
        y0=rect['y'],
        x1=rect['x'] + rect['dx'],
        y1=rect['y'] + rect['dy'],
        line=dict(color="white", width=1),
        fillcolor=color,
    )

    # Ticker Labels added to rectangles
    fig.add_trace(go.Scatter(
        x=[rect['x'] + rect['dx']/2],
        y=[rect['y'] + rect['dy']/2],
        text=f"{ticker}<br>{percent}%",
        mode="text",
        textfont=dict(color="white", size=font_size),
        hoverinfo="text",
        hovertext=f"{ticker}<br>Change: {percent}%<br>Market Cap: ${market_cap:,.0f}"
    ))

fig.update_layout(
    title="NASDAQ-100 Daily Performance Heatmap",
    plot_bgcolor='black',
    paper_bgcolor='black',
    margin=dict(l=5, r=5, t=40, b=5),
    xaxis=dict(showgrid=False, visible=False),
    yaxis=dict(showgrid=False, visible=False),
    showlegend=False,
)

fig.update_yaxes(autorange="reversed")

fig.show()
