import fetch_data  # Import your data-fetching module
import pandas as pd
import plotly.graph_objects as go
import squarify

# Update the CSV with fresh NASDAQ-100 data
nasdaq_df = fetch_data.fetch_nasdaq_data(fetch_data.nasdaq_100_tickers)
nasdaq_df.to_csv('nasdaq100_data.csv', index=False)

# 1) LOAD & PREPARE DATA
df = pd.read_csv('nasdaq100_data.csv')
df = df.sort_values('market_cap', ascending=False).reset_index(drop=True)

# 2) FORMAT MARKET CAP
def format_market_cap(value):
    abs_val = abs(value)
    if abs_val >= 1_000_000_000_000:  # trillion
        return f"${value/1_000_000_000_000:.2f}T"
    elif abs_val >= 1_000_000_000:    # billion
        return f"${value/1_000_000_000:.2f}B"
    elif abs_val >= 1_000_000:        # million
        return f"${value/1_000_000:.2f}M"
    else:
        return f"${value:,.0f}"

# 3) DEFINE COLOR GRADIENT
def gradient_color(change):
    # Clamp the change to a maximum of 3 (or -3 for negatives)
    if change > 0:
        norm = min(change, 3) / 3
        # Apply a non-linear scaling (exponent < 1 expands lower values)
        norm = norm ** 0.8
        green_intensity = round(100 + 155 * norm)
        return f'rgba(0,{green_intensity},0,0.9)'
    elif change < 0:
        norm = min(abs(change), 3) / 3
        norm = norm ** 0.8
        red_intensity = round(100 + 155 * norm)
        return f'rgba({red_intensity},0,0,0.9)'
    else:
        return 'rgba(128,128,128,0.8)'

df['color'] = df['percent_change'].apply(gradient_color)

# 4) SQUARIFY
sizes = squarify.normalize_sizes(df['market_cap'], 100, 100)
rects = squarify.squarify(sizes, x=0, y=0, dx=100, dy=100)

# 5) BUILD FIGURE & ADD RECTANGLES
fig = go.Figure()

for idx, rect in enumerate(rects):
    ticker = df.loc[idx, 'ticker']
    full_name = df.loc[idx, 'full_name']  # New column with full company name
    percent = df.loc[idx, 'percent_change']
    market_cap = df.loc[idx, 'market_cap']
    color = df.loc[idx, 'color']
    
    rect_area = rect['dx'] * rect['dy']
    font_size = max(min(rect_area * 0.3, 20), 9)
    
    # Draw rectangle
    fig.add_shape(
        type="rect",
        x0=rect['x'], y0=rect['y'],
        x1=rect['x'] + rect['dx'], y1=rect['y'] + rect['dy'],
        line=dict(color="white", width=1),
        fillcolor=color,
        layer='below'
    )
    
    # Shadow text for readability
    fig.add_trace(go.Scatter(
        x=[rect['x'] + rect['dx']/2 + 0.1],
        y=[rect['y'] + rect['dy']/2 + 0.1],
        text=f"{ticker}<br>{percent:+.2f}%",
        mode="text",
        textfont=dict(color='rgba(0,0,0,0.5)', size=font_size),
        hoverinfo="none",
        showlegend=False
    ))
    
    # Main white text with updated hovertext that includes the full company name
    fig.add_trace(go.Scatter(
    x=[rect['x'] + rect['dx']/2],
    y=[rect['y'] + rect['dy']/2],
    text=f"{ticker}<br>{percent:+.2f}%",
    mode="text",
    textfont=dict(color='white', size=font_size, family='Arial Black'),
    hoverinfo="text",
    hovertext=(
        f"<b>{ticker} - {full_name}</b><br>"
        f"Change: {percent:+.2f}%<br>"
        f"Market Cap: {format_market_cap(market_cap)}"
    ),
    showlegend=False
    ))


# 6) LAYOUT & AXES
fig.update_layout(
    title="NASDAQ-100 Daily Performance Heatmap",
    title_font=dict(color='white', size=26, family='Arial Black'),
    title_x=0.5,
    plot_bgcolor='#121212',
    paper_bgcolor='#121212',
    margin=dict(l=50, r=50, t=50, b=50),
    xaxis=dict(visible=False),
    yaxis=dict(showgrid=False, visible=False, autorange='reversed')
)

# 7) COLOR SCALE LEGEND: BOTTOM-RIGHT (no gaps between rectangles)
legend_labels = ["-3%", "-2%", "-1%", "0%", "+1%", "+2%", "+3%"]
legend_values = [-3, -2, -1, 0, 1, 2, 3]
legend_colors = [gradient_color(v) for v in legend_values]

# Each rectangle is 0.04 wide in paper coords; no gap
box_width = 0.04
box_height = 0.04
start_x = 0.68   # left edge of the legend row
start_y = -0.02   # bottom

for i, color in enumerate(legend_colors):
    x0 = start_x + i * box_width
    x1 = x0 + box_width
    y0 = start_y
    y1 = y0 + box_height
    
    # Colored rectangle
    fig.add_shape(
        type="rect",
        xref='paper', yref='paper',
        x0=x0, y0=y0,
        x1=x1, y1=y1,
        fillcolor=color,
        line=dict(width=0),
        layer='above'
    )
    # Label in the middle of the rectangle
    fig.add_annotation(
        x=(x0 + x1)/2,
        y=(y0 + y1)/2,
        xref='paper',
        yref='paper',
        text=legend_labels[i],
        showarrow=False,
        font=dict(color="white", size=12),
        xanchor='center',
        yanchor='middle'
    )

# 8) WATERMARK / BRANDING: LOWER-LEFT
fig.add_annotation(
    x=0.01,   # slightly in from the left edge
    y=-0.01,  # aligned with the gradient legend
    xref='paper',
    yref='paper',
    text="© Harasoft LLC",
    showarrow=False,
    font=dict(size=20, color="white"),
    xanchor='left',
    yanchor='bottom',
    opacity=0.7
)

fig.write_html('app/index.html', auto_open=True)
