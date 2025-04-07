import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date", parse_dates=True)

# Clean data
df = df[(df["value"] >= df["value"].quantile(0.025)) & (df["value"] <= df["value"].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    df_lines = df.copy()
    
    fig, ax = plt.subplots(figsize=(10, 5), layout='constrained')
    ax.plot(df_lines)
    ax.set(xlabel='Date', ylabel='Page Views', title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')




    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Draw bar plot
    df_bar_sum = df_bar.resample('MS').mean()
    df_bar_sum['year'] = [d.year for d in df_bar_sum.index.date]
    df_bar_sum['month'] = [d.strftime('%b') for d in df_bar_sum.index.date]
    df_bar_sum_wide = pd.pivot(df_bar_sum, index='year', columns='month', values='value')
    df_bar_ord = df_bar_sum_wide.iloc[:, [4, 3, 7, 0, 8, 6, 5, 1, 11, 10, 9, 2]]
    df_bar_ord[df_bar_ord.isnull()] = 0
    fig, ax = plt.subplots(layout='constrained')
    x = np.arange(len(df_bar_ord.index))
    width = 0.06
    multiplier = -5.5
    for month in df_bar_ord.columns:
        offset = width*multiplier
        ax.bar(x+offset, month, width, data = df_bar_ord)
        multiplier += 1

    ax.set(xlabel='Years', ylabel='Average Page Views')
    ax.set_xticks(x, df_bar_ord.index)
    plt.legend(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])




    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    month_ord = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), layout='constrained')
    sns.boxplot(data = df_box, x='year', y='value', hue='year', ax=ax1, legend=False)
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax1.set_title('Year-wise Box Plot (Trend)')
    sns.boxplot(data = df_box, x='month', y='value', hue='month', ax=ax2, order = month_ord, flierprops={"marker": ".", 'markersize': 2}, legend=False)
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    ax2.set_title('Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
