import pandas as pd
import plotly.graph_objects as go
import squarify

# ---------------------------------------
# 1) LOAD & PREPARE DATA
# ---------------------------------------
df = pd.read_csv('nasdaq100_data.csv')
df = df.sort_values('market_cap', ascending=False).reset_index(drop=True)

# ---------------------------------------
# 2) DEFINE A COLOR GRADIENT FUNCTION
# ---------------------------------------
def gradient_color(change):
    """Returns an RGBA color based on percent_change."""
    # Clamp change to -3%...+3% for coloring
    if change > 0:
        green_intensity = int(100 + 155 * min(change, 3)/3)
        return f'rgba(0,{green_intensity},0,0.9)'
    elif change < 0:
        red_intensity = int(100 + 155 * min(abs(change), 3)/3)
        return f'rgba({red_intensity},0,0,0.9)'
    else:
        # Neutral gray for 0%
        return 'rgba(128,128,128,0.8)'

df['color'] = df['percent_change'].apply(gradient_color)

# ---------------------------------------
# 3) SQUARIFY TO GET RECTANGLE COORDS
# ---------------------------------------
sizes = squarify.normalize_sizes(df['market_cap'], 100, 100)
rects = squarify.squarify(sizes, x=0, y=0, dx=100, dy=100)

# ---------------------------------------
# 4) BUILD FIGURE & ADD RECTANGLES
# ---------------------------------------
fig = go.Figure()

for idx, rect in enumerate(rects):
    ticker = df.loc[idx, 'ticker']
    percent = df.loc[idx, 'percent_change']
    market_cap = df.loc[idx, 'market_cap']
    color = df.loc[idx, 'color']
    
    # Adaptive font sizing based on rectangle area
    rect_area = rect['dx'] * rect['dy']
    font_size = max(min(rect_area * 0.3, 20), 9)
    
    # Draw rectangle BELOW the text
    fig.add_shape(
        type="rect",
        x0=rect['x'],
        y0=rect['y'],
        x1=rect['x'] + rect['dx'],
        y1=rect['y'] + rect['dy'],
        line=dict(color="white", width=1),
        fillcolor=color,
        layer='below'  # ensures shapes go underneath text
    )
    
    # OPTIONAL: Add a shadow (darker offset text) behind the main text
    fig.add_trace(go.Scatter(
        x=[rect['x'] + rect['dx']/2 + 0.1],  # small offset
        y=[rect['y'] + rect['dy']/2 + 0.1],
        text=f"{ticker}<br>{percent:+.2f}%",
        mode="text",
        textfont=dict(color='rgba(0,0,0,0.5)', size=font_size),
        hoverinfo="none",  # no hover for the shadow
        showlegend=False
    ))
    
    # Main text in white, centered
    fig.add_trace(go.Scatter(
        x=[rect['x'] + rect['dx']/2],
        y=[rect['y'] + rect['dy']/2],
        text=f"{ticker}<br>{percent:+.2f}%",
        mode="text",
        textfont=dict(color='white', size=font_size),
        hoverinfo="text",
        hovertext=(
            f"<b>{ticker}</b><br>"
            f"Change: {percent:+.2f}%<br>"
            f"Market Cap: ${market_cap:,.0f}"
        ),
        showlegend=False
    ))

# ---------------------------------------
# 5) LAYOUT & AXES
# ---------------------------------------
fig.update_layout(
    title="NASDAQ-100 Daily Performance Heatmap",
    title_font=dict(color='white', size=20),
    title_x=0.5,
    plot_bgcolor='#121212',
    paper_bgcolor='#121212',
    margin=dict(l=5, r=5, t=50, b=50),
    xaxis=dict(visible=False),
    yaxis=dict(showgrid=False, visible=False, autorange='reversed')
)

# ---------------------------------------
# 6) FINVIZ-STYLE COLOR SCALE LEGEND
# ---------------------------------------
legend_labels = ["-3%", "-2%", "-1%", "0%", "+1%", "+2%", "+3%"]
legend_values = [-3, -2, -1, 0, 1, 2, 3]
legend_colors = [gradient_color(v) for v in legend_values]

# Positioning for the legend squares
box_width = 10
box_height = 4
legend_y = -8  # negative means it's below the main chart; adjust as needed

for i, color in enumerate(legend_colors):
    x0 = 5 + i*(box_width + 2)
    x1 = x0 + box_width
    y0 = legend_y
    y1 = y0 + box_height
    
    # Colored rectangle
    fig.add_shape(
        type="rect",
        x0=x0, y0=y0,
        x1=x1, y1=y1,
        fillcolor=color,
        line=dict(width=0),
        layer='above'  # these small boxes can be above or below
    )
    # Corresponding label
    fig.add_annotation(
        x=(x0 + x1)/2,
        y=(y0 + y1)/2,
        text=legend_labels[i],
        showarrow=False,
        font=dict(color="white", size=12),
        xanchor='center',
        yanchor='middle'
    )

fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
fig.update_yaxes(showgrid=False, zeroline=False, visible=False, autorange="reversed")

# ---------------------------------------
# 7) WRITE TO HTML
# ---------------------------------------
fig.write_html('nasdaq_heatmap.html', auto_open=True)
