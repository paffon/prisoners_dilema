import pandas as pd
import matplotlib.pyplot as plt


def preprocess_data(components, text_to_display):
    """
    Preprocesses the data and text for visualization.

    Parameters:
    components (list of lists): The data to be visualized.
    text_to_display (str): The text to be displayed in the plot.

    Returns:
    pd.DataFrame: Preprocessed data in DataFrame format.
    str: Preprocessed text.
    """
    # Join the text by comma, split into lines
    # text = '\n'.join(str(text_to_display).split(','))

    text = 'Tournament parameters {'

    sep = '\n     '

    text += sep + sep.join([f'{k}: {v},' for k, v in text_to_display.items()])

    text += '\n}'

    # Create a DataFrame from the data
    df = pd.DataFrame(components)
    df = df.astype(int)

    # Calculate the total to normalize the data
    total = df.iloc[0].sum()
    df = df.apply(lambda value: value / total)

    return df, text


def create_plot(df):
    """
    Creates a stacked bar plot using the preprocessed data.

    Parameters:
    df (pd.DataFrame): Preprocessed data in DataFrame format.

    Returns:
    tuple: A tuple containing the Figure and Axes objects.
    """
    # Create a Figure and Axes objects with adjusted size
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the DataFrame using the 'bar' plot with stacked bars
    bars = df.plot(kind='bar', stacked=True, ax=ax)

    # Get the legend handles and labels
    handles, labels = ax.get_legend_handles_labels()

    # Add Title and Labels
    ax.set_title('Tournaments composition over time')
    ax.set_xlabel('Tournament #')
    ax.set_ylabel('Composition')

    # Move the legend to the upper right and adjust size
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1.013))

    y_offset = -15
    # For each patch (basically each rectangle within the bar), add a label.
    for i, bar in enumerate(ax.patches):
        print(i+1, '\t', bar.get_height())

    return fig, ax


def add_textbox(fig, ax, text):
    """
    Adds a textbox to the plot with the preprocessed text.

    Parameters:
    fig (matplotlib.figure.Figure): The Figure object.
    ax (matplotlib.axes.Axes): The Axes object.
    text (str): The preprocessed text to be displayed in the textbox.
    """
    textbox_props = dict(facecolor='lightgrey', alpha=0.5, boxstyle='round,pad=0.5')
    ax.text(1.03, 0.0117, text, transform=ax.transAxes, fontsize=12, verticalalignment='bottom',
            horizontalalignment='left', bbox=textbox_props)


def visualize(components, text_to_display):
    """
    Visualizes data and text in a stacked bar plot with a textbox.

    Parameters:
    components (list of lists): The data to be visualized.
    text_to_display (str): The text to be displayed in the plot.
    """
    df, text = preprocess_data(components, text_to_display)
    fig, ax = create_plot(df)
    add_textbox(fig, ax, text)

    # Show the plot
    plt.tight_layout()
    plt.show()
