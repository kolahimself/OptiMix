"""
Determines the fine aggregate proportion in the concrete mixture.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from core.logic.helpers.computation_helpers import interpolate, create_linear_points, fit_linreg
from core.utils.file_paths import optimix_paths
from core.utils.themes import fig_vi_colors, white_color, graph_colors, BG, transparent, calibri


class FineAggPortioner:
    """
    Determines the right proportion of fine aggregate in a concrete mixture based on maximum aggregate size,
    slump, and water-to-cement ratio.

    Attributes:
        - fwc_ratio (`float`) --> The free-water/cement ratio
        - max_agg (`int`): The maximum aggregate size
        - slump_category (`str`): The slump category
        - perc_passing (`float`): Percentage of aggregate passing a 600-micro-m pore size.

    Methods:
        - _validate_inputs(fwc_ratio, max_agg, slump_category) --> Performs internal error handling
        - generate_appropriate_plots() --> Generates plot points based on the maximum aggregate size and slump category
        - determine_proportion() --> Calculates the fine aggregate proportion using the appropriate plot
        - plot() --> Visualizes the plot with plotly
    """

    def __init__(self, fwc_ratio: float, max_agg: int, slump_category: str, perc_passing: float | int):
        """
        Initializes the class with input parameters.

        :param fwc_ratio (float): Free-water/cement ratio.
        :param max_agg (int): Maximum aggregate size
        :param slump_category (str): Slump category
        :param perc_passing (float): Percentage of aggregate passing a 600-micro-m pore size.
        """

        self.fwc_ratio = fwc_ratio
        self.max_agg = max_agg
        self.slump_category = slump_category
        self.perc_passing = perc_passing
        self.errors = ['N', 'N', 'N']
        self.recommended_plot = None
        self.new_line = None

        # Error handling
        self._validate_inputs(fwc_ratio, max_agg, slump_category)

        # If there's an error, pause, else continue
        if self.errors == ['N', 'N', 'N']:
            # Generate appropriate plots
            self.generate_appropriate_plots()

            # Preset value of the fine aggregate proportion
            self.fine_agg_proportion = 0

        else:
            pass

    def _validate_inputs(self, fwc_ratio, max_agg, slump_category):
        """Error handling of the inputs, parameters are as the function's.

        """
        if not isinstance(fwc_ratio, float):
            self.errors[0] = 'E'
            raise TypeError("fwc_ratio must be a float")

        if max_agg not in (10, 20, 40):
            self.errors[1] = 'E'
            raise ValueError("max_agg must be one of: {}".format((10, 20, 30)))

        if slump_category not in ('60-180mm', '30-60mm', '10-30mm', '0-10mm'):
            self.errors[2] = 'E'
            raise ValueError("slump_category must be one of {}".format(('60-180mm', '30-60mm', '10-30mm', '0-10mm')))

    def generate_appropriate_plots(self):
        """Generates the appropriate plot lines based on the specified maximum aggregate size & slump category

        - Reads plot data from CSV files (hardcoded paths)
        - Organizes data into nested dictionaries
        - Performs linear regression to calculate coefficients
        - Creates plot lines using create_linear_points
        - Selects the appropriate plot and stores it in self.recommended_plot

        self.recommended plot is a dictionary containing this structure:
            figure_6 = {
            10: {
                '0-10mm': [l15, l40, l60, l80, l100],
                '10-30mm': [l15, l40, l60, l80, l100],
                '30-60mm': [l15, l40, l60, l80, l100],
                '60-180mm': [l15, l40, l60, l80, l100]
            },
            20: {
                '0-10mm': [l15, l40, l60, l80, l100],
                '10-30mm': [l15, l40, l60, l80, l100],
                '30-60mm': [l15, l40, l60, l80, l100],
                '60-180mm': [l15, l40, l60, l80, l100]
            },
            40: {
                '0-10mm': [l15, l40, l60, l80, l100],
                '10-30mm': [l15, l40, l60, l80, l100],
                '30-60mm': [l15, l40, l60, l80, l100],
                '60-180mm': [l15, l40, l60, l80, l100]
            }}
        """
        # Retrieve the paths for figure 6's datapoints
        plot_paths = optimix_paths.fagg_prop_plot_paths

        # Figure 6 Recommended proportions of fine aggregate according to percentage passing a 600um sieve
        fig_vi_points = {
            10: {
                '0-10mm': [pd.read_csv(plot) for plot in plot_paths[0]],
                '10-30mm': [pd.read_csv(plot) for plot in plot_paths[1]],
                '30-60mm': [pd.read_csv(plot) for plot in plot_paths[2]],
                '60-180mm': [pd.read_csv(plot) for plot in plot_paths[3]]
            },
            20: {
                '0-10mm': [pd.read_csv(plot) for plot in plot_paths[4]],
                '10-30mm': [pd.read_csv(plot) for plot in plot_paths[5]],
                '30-60mm': [pd.read_csv(plot) for plot in plot_paths[6]],
                '60-180mm': [pd.read_csv(plot) for plot in plot_paths[7]]
            },
            40: {
                '0-10mm': [pd.read_csv(plot) for plot in plot_paths[8]],
                '10-30mm': [pd.read_csv(plot) for plot in plot_paths[9]],
                '30-60mm': [pd.read_csv(plot) for plot in plot_paths[10]],
                '60-180mm': [pd.read_csv(plot) for plot in plot_paths[11]]
            }
        }

        # free water to cement ratio range
        fwc_range = [
            [
                [0.2, 0.8999998527660982],
                [0.2, 1],
                [0.2, 1],
                [0.2, 1]
            ],
            [
                [0.2, 0.8999998527660982],
                [0.2, 1],
                [0.2, 1],
                [0.2, 1]
            ],
            [
                [0.2, 0.8999998527660982],
                [0.2, 1],
                [0.2, 1],
                [0.2, 1]
            ]
        ]

        # Organize the coefficients for the 60 linear functions into a multidimensional list for clarity
        coefficients = []
        for agg_size_index, (category, slump_group) in enumerate(fig_vi_points.items()):
            category_coeffs = []  # Initialize list for coefficients within this category

            # Iterate through each group within the category
            for group_index, (group_name, dataframes) in enumerate(slump_group.items()):
                group_coeffs = []  # Initialize list for coefficients within this group

                # Iterate through each DataFrame in the group
                for df_index, df in enumerate(dataframes):
                    y = df[' y']  # Extract y values from the DataFrame

                    # Access the correct x_range for this DataFrame
                    fwc_range_pair = fwc_range[agg_size_index][group_index]

                    # Apply linear regression using the extracted x_range
                    equation_coeffs = fit_linreg(fwc_range_pair, y)

                    # Append the calculated coefficients to the group's list
                    group_coeffs.append(equation_coeffs)

                # Append the group's coefficients to the category's list
                category_coeffs.append(group_coeffs)

            # Append the category's coefficients to the main list
            coefficients.append(category_coeffs)

        # Slump categories
        slump_categories = ['0-10mm', '10-30mm', '30-60mm', '60-180mm']

        # Aggregate sizes
        agg_sizes = [10, 20, 40]

        # Apply linear regression on the datapoints, the straight lines will be used for further calculations
        figure_vi = {
            agg_size: {
                slump_cat: [
                    create_linear_points(fwc_range[agg_index][group_index], coeffs)
                    for coeffs in coeffs_group
                ]
                for group_index, (slump_cat, coeffs_group) in enumerate(zip(slump_categories, coeffs_group))
            }
            for agg_index, (agg_size, coeffs_group) in enumerate(zip(agg_sizes, coefficients))
        }

        # Pick the appropriate plot
        self.recommended_plot = figure_vi[self.max_agg][self.slump_category]

    def determine_proportion(self):
        """
        Calculates the fine aggregate proportion of the concrete mix using figure 6
        """
        # Percentage passing line tags
        percentage_tags = [15, 40, 60, 80, 100]

        if self.perc_passing < 15:
            line_df = self.recommended_plot[0]
            self.new_line = line_df

            # Determine the fine aggregate proportion
            self.fine_agg_proportion = interpolate(
                x=line_df['x'],
                y=line_df[' y'],
                target_var=self.fwc_ratio
            )

        else:
            # Check if the percentage passing is 15, 40, 60, 80 or 100%
            if self.perc_passing in [15, 40, 60, 80, 100]:

                # Create a dictionary to map self.perc_passing to index in self.recommended_plot
                percent_passing_map = {
                    15: 0,
                    40: 1,
                    60: 2,
                    80: 3,
                    100: 4
                }

                # Get the index corresponding to self.perc_passing
                index = percent_passing_map[int(self.perc_passing)]

                # Get the line_df directly using the index
                line_df = self.recommended_plot[index]

                # Determine the fine aggregate proportion
                self.fine_agg_proportion = interpolate(
                    x=line_df['x'],
                    y=line_df[' y'],
                    target_var=self.fwc_ratio
                )
                self.new_line = line_df

            else:
                # Define the starting and ending x points of the proposed new line
                x_start = 0.2
                x_end = np.max([x_point['x'].max() for x_point in self.recommended_plot])

                # Extract the first and last y values from each dataframe
                first_y_values = [df[' y'].iloc[0] for df in self.recommended_plot]
                last_y_values = [df[' y'].iloc[-1] for df in self.recommended_plot]

                # Calculate the corresponding starting y-value of the specified percentage passing with interpolation
                y_start = interpolate(
                    target_var=self.perc_passing,
                    x=percentage_tags,
                    y=first_y_values
                )

                # Calculate the corresponding ending y-value of the specified percentage passing with interpolation
                y_end = interpolate(
                    target_var=self.perc_passing,
                    x=percentage_tags,
                    y=last_y_values
                )

                # The x coordinates of the new specified percentage passing line
                x_coords = np.linspace(x_start, x_end, 50)
                y_coords = np.linspace(y_start, y_end, 50)

                # Store the new datapoints of the new line for further referencing
                self.new_line = pd.DataFrame({'x': x_coords, ' y': y_coords})

                # Determine the fine aggregate proportion
                self.fine_agg_proportion = interpolate(
                    x=x_coords,
                    y=y_coords,
                    target_var=self.fwc_ratio
                )

    def plot(self):
        """
        Function that makes visualization of figure 6
        :return (plotly.go) fig_vi: Figure 6 from The design of normal concrete mixes.
        """

        # Legend
        legend = ['15% passing', '40% passing', '60% passing', '80% passing', '100% passing']

        # Plot the percentage passing lines for 15, 40, 60, 80 & 100%
        traces = []
        for i in range(5):
            trace = go.Scatter(
                x=self.recommended_plot[i]['x'],
                y=self.recommended_plot[i][' y'],
                mode='lines',
                name=legend[i],
                line=dict(color=fig_vi_colors[i], width=2))

            traces.append(trace)

        # Create figure 6
        fig_vi = go.Figure(data=traces)

        # Plot the appropriate percent passing line
        fig_vi.add_trace(
            go.Scatter(
                x=self.new_line['x'],
                y=self.new_line[' y'],
                mode='lines',
                name=f'Defined percentage passing ({np.round(self.perc_passing, 2)}%)',
                line=dict(color=fig_vi_colors[5], width=3)
            )
        )

        # Make a vertical line that moves from the x-axis to the plot
        fig_vi.add_shape(
            type='line',
            x0=self.fwc_ratio,
            y0=0,
            x1=self.fwc_ratio,
            y1=self.fine_agg_proportion,
            line=dict(color=white_color, width=2.3, dash='dash'))

        # Make a horizontal line that moves from the y-axis to the plot
        fig_vi.add_shape(
            type='line',
            x0=0,
            y0=self.fine_agg_proportion,
            x1=self.fwc_ratio,
            y1=self.fine_agg_proportion,
            line=dict(color=white_color, width=2.3, dash='dash'))

        # Customize the gridlines
        fig_vi.update_xaxes(gridcolor=graph_colors[4])
        fig_vi.update_yaxes(gridcolor=graph_colors[4])

        # Axis titles
        xaxis_title = 'Free-water/cement ratio'
        yaxis_title = 'Proportion of fine aggregate (%)'

        max_y_val = max(self.recommended_plot[0][' y']) + 5

        # Edit the layout
        fig_vi.update_layout(
            width=640,
            height=440,
            autosize=True,
            paper_bgcolor=transparent,
            plot_bgcolor=transparent,
            font_family=calibri,
            margin=dict(l=50, r=50, b=50, t=50, pad=4),
            font_size=13,
            xaxis_title=xaxis_title,
            xaxis_range=[0.2, 0.8],
            yaxis_title=yaxis_title,
            yaxis_range=[10, max_y_val],
            template='plotly_dark')

        # Add the point (fwc_ratio, fine_agg_proportion) as an annotation in the plot
        tag = f"Proportion of fine aggregate = {np.round(self.fine_agg_proportion, 2)}%"
        fig_vi.add_annotation(
            x=self.fwc_ratio,
            y=self.fine_agg_proportion,
            xref='x',
            yref='y',
            text=tag,
            showarrow=True,
            font_family=calibri,
            font_size=13,
            align='center',
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=white_color,
            ax=55,
            ay=-55,
            bordercolor=white_color,
            borderwidth=2,
            borderpad=4,
            bgcolor=BG,
            opacity=0.99123345
        )

        return fig_vi
