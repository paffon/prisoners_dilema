import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt


def visualize(components, text_to_display):
    text = '\n'.join(str(text_to_display).split(','))

    df = pd.DataFrame(components)

    df = df.astype(int)

    total = df.iloc[0].sum()

    df = df.apply(lambda value: value/total)

    # df['Tournament #'] = pd.Series([i for i in range(len(df))])

    strategies = ['GoodyTwoShoes', 'Cheater', 'Joker', 'CopyCat', 'CopyKitten', 'Cowboy', 'Businessman']

    # Create a Figure and Axes objects
    fig, ax = plt.subplots()

    # Plot the DataFrame using the 'bar' plot with stacked bars
    df.plot(kind='bar', stacked=True, ax=ax)

    # Add Title and Labels
    ax.set_title('Tournaments composition over time')
    ax.set_xlabel('Tournament #')
    ax.set_ylabel('Composition')

    # Move the legend to the right side
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0.)

    fig.subplots_adjust(right=0.3)

    textbox_props = dict(facecolor='lightgrey', alpha=0.5, boxstyle='round,pad=0.5')
    ax.text(1.4, 0.05, text, transform=ax.transAxes, fontsize=10, verticalalignment='bottom',
            horizontalalignment='left', bbox=textbox_props)

    # Show the plot
    plt.show()

