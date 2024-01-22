"""
mix_design.py

This module contains the MixDesignAnalyzer class for performing mix design calculations and analysis.
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff

from core.logic.helpers.computation_helpers import *
from core.logic.helpers.output_helpers import plotly_image_converter
from core.logic.reference_data import *
from core.logic.fine_agg_portioner import FineAggPortioner
from core.utils.themes import *
from core.utils.file_paths import optimix_paths

import tkinter as tk
from tkinter import ttk


# noinspection
class MixDesignAnalyzer:
    """
    MixDesignAnalyzer class for performing mix design calculations and analysis.

    Methods:
        - null_check(category, key): Checks whether the stored value == ""
        - sync_input(widget, category, key, var_name=None, option_var=None: Collects data from widgets
        - calculate_k(): Determines the risk factor, k
        - special_check(mode): Special check for k and defective rate
        - plot_k(): Makes a graph showing the relationship between percentage defectiveness and risk factor
        - calculate_sd(): Determines the standard deviation
        - plot_sd(): Plots the graph showing relationship between standard deviation and characteristic strength
        - calculate_margin(mode): Determines the margin
        - calculate_target_mean_strength(mode): Determines the target mean strength of the concrete mix
        - calculate_approx_strength(mode): Checks the value of the approximate compressive strength given a fwc_ratio of 0.5
        - calculate_fwc_ratio(mode): Determines the free-water/cement ratio required for the concrete mix
        - plot_fwc_determination(): Plots the free-water/cement ratio in a visualization
        - check_max_agg(): Retrieves the maximum aggregate size
        - calculate_fw_content(mode): Determines the free-water content
        - calculate_cement_content(mode): Determines the cement content
        - ssd_check(): Checks for the relative density of aggregate at SSD condition
        - compute_wet_conc_density(mode): Calculates the wet concrete density of the mix.
        - plot_figure_v(mode): Plots the visualization showing how the concrete density is determined
        - override_density(): Override the density if a value is specified.
        - compute_total_agg_content(mode): Determines the total aggregate content
        - compute_fine_agg_proportion(mode): Determines the fine aggregate content
        - plot_fine_agg_proportion(mode): Visualizes the determination of the fine aggregate content
        - compute_agg_content(mode): Computes the coarse aggregate content
        - oven_dry_batching(): Performs oven-dry matching
        - proportion_coarse_agg(): Proportions the coarse aggregates to specified sizes
        - summarize_results(mode): Saves the summary of the design results into a list
        - batch_to_desired_volume(mode, mix_design_data): Adjust the batching volume for trial mixes
    """

    def __init__(self):
        # Initialize every data needed for the mix design calculations
        self.data = {
            'Specified variables': {
                'Characteristic Strength': '',
                'Curing Days': '',
                'Defective Rate': '',
                'Air Content': '',
                'Strength Loss': '5.5',
                'Less Than 20 Results': 1,
                'Cement Type': 'OPC',
                'Specified Margin': '',
                'Maximum free water-cement ratio': '',
                'Slump': '0-10mm',
                '10mm': 10,
                '20mm': 20,
                '40mm': 40,
                'Maximum cement content': '',
                'Minimum cement content': '',
                'pfa Proportion': '',
                'ggbs Proportion': ''
            },

            'Additional info': {
                'Standard Deviation': '',
                'Specified k': '',
                'Coarse Aggregate Type': 'Crushed',
                'Fine Aggregate Type': 'Crushed',
                'Relative density of agg': '',
                'Percentage passing 600um sieve': '',
                'Absorption of Fine Aggregate': '',
                'Absorption of Coarse Aggregate': '',
                'Fine Aggregate Reduction': '5',
                'Cementing Efficiency Factor': '0.3',
                'Water Content Reduction': '5'
            },

            'Mix Parameters': {
                'Margin': '',
                'Concrete density': ''
            },

            'Result Tuning': {
                'Batch volume': '',
                'Unit': 'm\u00b3'
            }
        }

        # Data dictionary for calculations and processing
        self.calc_data = {}

        # Dictionary containing final results
        self.design_results = {}

        # User input error callers
        self.min_is_more_than_max = False
        self.innaprop_spec_sd = False
        self.invalid_ssd = False
        self.ssd_value_error = None
        self.perc_pass_aberration = False
        self.feasibility_status = True
        self.calculated_k = False
        self.empty_defective_rate_and_k = False
        self.fig_i_png_image = None
        self.fig_iii_png_image = None
        self.fig_iv_png_image = None
        self.fwc_is_larger = False
        self.different_agg_types = False
        self.cc_status = None
        self.invalid_cc_entry = False
        self.tac_content = {}
        self.specified_conc_density = False
        self.fig_v_png_image = None
        self.graph_temp = {}
        self.portioner = None
        self.fig_vi_png_image = None
        self.odb_status = None
        self.design_batch_results = None

    def null_check(self, category: str, key: str):
        """
        Checks whether the stored value is null.
        Intent is to avoid errors that arise due to float("")
        """

        # Perform null check
        if self.data[category][key].strip() == '':
            return True

        else:
            return False

    def sync_input(self, widget, category, key, var_name=None, option_var=None):
        """
        Collect data from a widget and updates the corresponding value in the data dictionary
        The data collected is stored in the data dictionary with the specified category and key.

        :param option_var: tk.StringVar() variable name if the category is an option menu
        :param var_name: tk.IntVar variable name if the category is a checkbutton
        :param widget: The tkinter or ttk widget to collect data from
        :param category: The category or the section in the data section to update
        :param key: The key or the title of the data entry to update
        """
        if isinstance(widget, tk.Entry):
            value = widget.get()

        elif isinstance(widget, ttk.OptionMenu):
            if option_var:
                value = option_var.get()
            else:
                value = None

        elif isinstance(widget, tk.Checkbutton):
            if var_name:
                value = var_name.get()
            else:
                value = None

        else:
            value = None

        if category in self.data and key in self.data[category]:
            self.data[category][key] = value

    def calculate_k(self):
        """
        Determines the value of k using figure 1, `normal distribution of concrete strengths` unless specified
        """
        p = self.data['Specified variables']['Defective Rate']

        if not p:  # if defective rate is empty
            percent_def = 0.0000001
            self.calc_data['perc_def'] = percent_def
        else:
            # Retrieve the percentage defectiveness
            percent_def = float(self.data['Specified variables']['Defective Rate'])
            self.calc_data['perc_def'] = percent_def

        # Check if the given k is empty, else determine k
        if self.null_check('Additional info', 'Specified k'):

            # Determine k (risk factor) from figure 1
            k = compute_risk_factor(percent_def)

            # Store the calculated k
            self.calc_data['k'] = k

            # Update k's status for retrieval during reporting
            self.calculated_k = True

        else:
            # Store the specified value
            self.calc_data['k'] = float(self.data['Additional info']['Specified k'])

            # Update k's status for retrieval during reporting
            self.calculated_k = False

    def special_check(self, mode: str = 'DOE'):
        """
        Special check to see whether k and defective rate entries are both empty or not,
        a specified margin will allow this check to pass.

        :param mode: (str) ['DOE', 'AEM', 'PFA', 'GGBS'] the concrete mix design mode
        """
        if mode == 'DOE' or mode == 'PFA' or mode == 'GGBS':
            # If defective rate and specified k are both empty, give an error message
            check = [
                self.null_check('Specified variables', 'Defective Rate'),
                self.null_check('Additional info', 'Specified k')]

            if check == [True, True]:
                if not self.null_check('Specified variables', 'Specified Margin'):
                    # Case where there's a specified margin.
                    self.empty_defective_rate_and_k = False
                else:
                    # When margin, k and def rate are all unspecified.
                    self.empty_defective_rate_and_k = True

            else:
                self.empty_defective_rate_and_k = False

        elif mode == 'AEM':
            check = [
                self.null_check('Specified variables', 'Defective Rate'),
                self.null_check('Additional info', 'Specified k'),
                self.null_check('Specified variables', 'Air Content')]

            if check == [True, True, True]:
                if not self.null_check('Specified variables', 'Specified Margin'):
                    # Case where there's a specified margin.
                    self.empty_defective_rate_and_k = False
                else:
                    # When margin, k and def rate are all unspecified.
                    self.empty_defective_rate_and_k = True

            else:
                self.empty_defective_rate_and_k = False

    def plot_k(self):
        """
        Makes a graph for the relationship between percentage defectiveness and risk factor
        """
        # Needed parameters
        d = self.calc_data['perc_def']  # defective rate
        k = self.calc_data['k']  # risk factor
        mean = 40
        sd = 5

        # Generate data for the normal distribution given the mean and sd
        data = norm.ppf(np.linspace(0.001, 0.999, 200), loc=mean, scale=sd)

        # Create figure 1 bell curve, distribution plot
        fig_i = ff.create_distplot([data], group_labels=[''],
                                   show_rug=False, show_hist=False)

        # Filter x-y values for the shaded portion
        x_defective_vals = [xc for xc in fig_i.data[0].x if xc < np.quantile(data, q=d / 100)]
        y_defective_vals = fig_i.data[0].y[:len(x_defective_vals)]

        # Add shaded area trace
        fig_i.add_scatter(x=x_defective_vals, y=y_defective_vals,
                          fill='tozeroy', fillcolor=graph_colors[0],
                          mode=None,
                          fillpattern=dict(fgcolor=graph_colors[0], fillmode='replace', shape='\\'))

        # Defectives annotation
        fig_i.add_annotation(x=np.quantile(data, q=d / 100),
                             y=0.0001,
                             xref='x',
                             yref='y',
                             text=f"{d}% defectives",
                             showarrow=True,
                             arrowhead=3,
                             arrowsize=1,
                             arrowwidth=2,
                             arrowcolor=white_color,
                             font_family=calibri,
                             font_size=13,
                             bordercolor=white_color,
                             borderwidth=2,
                             borderpad=4,
                             bgcolor=BG,
                             opacity=0.99123345,
                             xshift=-10,
                             yshift=10,
                             ay=-85,
                             ax=-38
                             )

        # Mean strength line
        fig_i.add_vline(x=mean,
                        line=dict(color=optimix_variants[4], width=1.8, dash='longdash'),
                        annotation_text='Mean Strength')

        # Illustrate the z-score (risk factor)
        fig_i.add_shape(type="line",
                        x0=np.quantile(data, q=d / 100), y0=0.007,
                        x1=mean, y1=0.007,
                        line=dict(color=graph_colors[7], width=1.4))

        fig_i.add_annotation(x=(np.quantile(data, q=d / 100) + mean) / 2,
                             y=0.007,
                             text=f'{np.round(k, 2)}s',
                             bordercolor=graph_colors[6],
                             borderwidth=2,
                             borderpad=4,
                             bgcolor=BG,
                             opacity=0.99123345,
                             )

        fig_i.update_shapes(dict(xref='x', yref='y'))
        fig_i.update_traces(line=dict(color=white_color, width=3))

        # Customize the gridlines
        fig_i.update_xaxes(gridcolor=graph_colors[4], gridwidth=0.5, linewidth=1.5)
        fig_i.update_yaxes(gridcolor=graph_colors[4], gridwidth=0.2)

        # Edit the layout
        fig_i.update_layout(
            width=580,
            height=380,
            showlegend=False,
            paper_bgcolor=transparent,
            plot_bgcolor=transparent,
            font_family=calibri,
            margin=dict(l=50, r=50, b=50, t=50, pad=4),
            font_size=13,
            yaxis=dict(showticklabels=False),
            xaxis_title='Compressive Strength (N/mm\u00b2)',
            yaxis_range=[0, 0.08],
            template='plotly_dark')

        # Save the figure temporarily
        self.fig_i_png_image = plotly_image_converter(fig_i)

    def calculate_sd(self):
        """
        Determines the standard deviation from figure 3 given that the specified input option is empty
        """
        # Retrieve the characteristic strength
        x_strength = float(self.data['Specified variables']['Characteristic Strength'])

        # Check that the given standard deviation is empty, then determine it
        if self.null_check('Additional info', 'Standard Deviation'):

            # Determine sd from figure 3 if less there are less than 20 samples
            if self.data['Specified variables']['Less Than 20 Results'] == 1:
                sd = interpolate(x=figure_iii['Less than 20']['Characteristic Strength'],
                                 y=figure_iii['Less than 20']['Standard Deviation'],
                                 target_var=x_strength)

            else:
                sd = interpolate(x=figure_iii['More than 20']['Characteristic Strength'],
                                 y=figure_iii['More than 20']['Standard Deviation'],
                                 target_var=x_strength)

            # Store the calculated standard deviation
            self.calc_data['sd'] = sd

        else:
            obtained_sd = interpolate(x=figure_iii['More than 20']['Characteristic Strength'],
                                      y=figure_iii['More than 20']['Standard Deviation'],
                                      target_var=x_strength)

            specified_sd = float(self.data['Additional info']['Standard Deviation'])
            # Keep the sds for reporting purposes
            self.calc_data['specified sd'] = specified_sd
            self.calc_data['init_sd'] = obtained_sd

            # Line B standard deviation check
            if specified_sd < obtained_sd:
                # Create bool for referencing in reporting
                self.innaprop_spec_sd = True

                self.calc_data['sd'] = obtained_sd

            else:
                # Create bool for referencing in reporting
                self.innaprop_spec_sd = False

                # Use the specified sd variable
                self.calc_data['sd'] = specified_sd

    def plot_sd(self):
        """
        Makes figure 3, "Relationship between standard deviation and characteristic strength"
        """
        # Create figure 3
        fig_iii = go.Figure()

        # Retrieve the characteristic strength
        x_strength = float(self.data['Specified variables']['Characteristic Strength'])

        # Ensure that the graph's obtained sd will be displayed, not even the specified one. No matter what
        if self.null_check('Additional info', 'Standard Deviation'):
            graph_sd = self.calc_data['sd']
        else:
            graph_sd = self.calc_data['init_sd']

        # Names
        name_a = '<i>s</i> for less<br> than 20 results'
        name_b = 'Minimum <i>s</i> for 20 or<br> more results'

        # Make the line depicting relationship between sd and strength for less than 20 results
        fig_iii.add_trace(go.Scatter(x=figure_iii['Less than 20']['Characteristic Strength'],
                                     y=figure_iii['Less than 20']['Standard Deviation'],
                                     mode='lines',
                                     name=name_a,
                                     line=dict(color=graph_colors[10], width=4)))

        # Make the line depicting relationship between sd and strength for more than 20 results
        fig_iii.add_trace(go.Scatter(x=figure_iii['More than 20']['Characteristic Strength'],
                                     y=figure_iii['More than 20']['Standard Deviation'],
                                     mode='lines',
                                     name=name_b,
                                     line=dict(color=graph_colors[9], width=4)))

        # Make a vertical line that moves from the x-axis to the plot
        fig_iii.add_shape(
            type='line',
            x0=x_strength,
            y0=0,
            x1=x_strength,
            y1=graph_sd,
            line=dict(color=white_color, width=2.1, dash='dash'))

        # Make a horizontal line that moves from the y-axis to the plot
        fig_iii.add_shape(
            type='line',
            x0=0,
            y0=graph_sd,
            x1=x_strength,
            y1=graph_sd,
            line=dict(color=white_color, width=2.1, dash='dash'))

        fig_iii.update_shapes(dict(xref='x', yref='y'))

        # Customize the gridlines
        fig_iii.update_xaxes(gridcolor=graph_colors[4])
        fig_iii.update_yaxes(gridcolor=graph_colors[4])

        # Axis titles
        xaxis_title = 'Characteristic strength (N/mm' + '<sup>2</sup>' + ')'
        yaxis_title = 'Standard Deviation, s, (N/mm' + '<sup>2</sup>' + ')'

        # Edit the layout
        fig_iii.update_layout(
            width=620,
            height=390,
            paper_bgcolor=transparent,
            plot_bgcolor=transparent,
            font_family=calibri,
            margin=dict(l=50, r=50, b=50, t=50, pad=4),
            font_size=13,
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            template='plotly_dark')

        # Add the point (perc_def, k) as an annotation in the plot
        tag = f"standard deviation = {np.round(graph_sd, 2)} N/mm<sup>2</sup>"
        fig_iii.add_annotation(
            x=x_strength,
            y=graph_sd,
            xref='x',
            yref='y',
            text=tag,
            showarrow=True,
            font_family=calibri,
            font_size=14,
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

        # Save the figure temporarily
        self.fig_iii_png_image = plotly_image_converter(fig_iii)

    def calculate_margin(self, mode: str):
        """
        Determines the margin for mix design unless specified.
        Margin determination also varies with concrete mix design mode

        :param mode: (str) ['DOE', 'AEM', 'PFA', 'GGBS'] the concrete mix design mode
        """
        # Margin calculation for DOE mode
        if mode == 'DOE' or mode == 'AEM' or mode == 'PFA' or mode == 'GGBS':

            # Check if the margin is not specified:
            if self.null_check('Specified variables', 'Specified Margin'):

                # M = k x sd
                margin = self.calc_data['k'] * self.calc_data['sd']

                # Store the calculated value
                self.calc_data['margin'] = margin

            else:
                # Store the specified value
                self.calc_data['margin'] = float(self.data['Specified variables']['Specified Margin'])

    def calculate_target_mean_strength(self, mode: str):
        """
        Calculation C2
        Determines the target mean strength as adjusted by a previously calculated margin

        Methods for determination depend on the design modes
        :param mode: (str) ['DOE', 'AEM', 'PFA', 'GGBS'] the concrete mix design mode
        """
        if mode == 'DOE' or mode == 'PFA' or mode == 'GGBS':
            # Retrieve the characteristic strength
            x_strength = float(self.data['Specified variables']['Characteristic Strength'])

            # Target mean strength
            fm = x_strength + self.calc_data['margin']

            # Store the calculated value
            self.calc_data['fm'] = fm

        elif mode == 'AEM':
            # Retrieve the characteristic strength, air content and percentage strength loss
            x_strength = float(self.data['Specified variables']['Characteristic Strength'])
            a = float(self.data['Specified variables']['Air Content'])
            loss = float(self.data['Specified variables']['Strength Loss'])

            # Compute target mean strength
            initial_fm = x_strength + self.calc_data['margin']
            self.calc_data['initial_fm'] = initial_fm
            fm = initial_fm / (1 - ((loss / 100) * a))

            # Store the calculated value
            self.calc_data['fm'] = fm

    def calculate_approx_strength(self, mode: str):
        """
        Calculates the approximate compressive strength based on the following:
        > Cement type
        > Type of coarse aggregate
        > Target mean strength

        References:
        Table 10 for portland cement/pfa concrete mix mode
        Table 2 for others
        :param mode: (str) ['DOE', 'AEM', 'PFA', 'GGBS'] the concrete mix design mode
        """
        if mode == 'DOE' or mode == 'AEM' or mode == 'PFA' or mode == 'GGBS':
            approx_strength = get_approximate_strength(
                cement_type=self.data['Specified variables']['Cement Type'],
                coarse_agg_type=self.data['Additional info']['Coarse Aggregate Type'],
                curing_days=float(self.data['Specified variables']['Curing Days'])
            )

            self.calc_data['approx_strength'] = approx_strength

    def calculate_fwc_ratio(self, mode: str):
        """
        Calculates the free water to cement ratio from and applies specified limits if defined.

        :param mode: (str) ['DOE', 'AEM', 'PFA', 'GGBS'] the concrete mix design mode
        """
        # Smoothen the plot data
        figure_iv = [sg_filter(curve) for curve in chart_iv]

        if mode == 'DOE' or mode == 'AEM':

            # Starting line using data from table 2
            target_x = 0.5

            # y-values for target_x (y-intercept) for every plot line
            y_values = []

            # loop through the plots in figure 4, append the interception point of target_x to y_values
            for plot in figure_iv:
                # find the nearest x values
                nearest_x = plot['x'].values[np.argsort(np.abs(plot['x'].values - target_x))[0:2]]

                # get the corresponding y-values
                nearest_y = plot.loc[plot['x'].isin(nearest_x), ' y'].values

                # interpolate the y-value for target x
                interpolated_y = interpolate(target_var=target_x,
                                             x=nearest_x,
                                             y=nearest_y)

                # append the interpolated y values to the results tray
                y_values.append(interpolated_y)

            # Re-arrange and find the plot above the mean compressive strength
            nearest_index = np.searchsorted(y_values[::-1], self.calc_data['approx_strength'])

            if nearest_index >= len(y_values[::-1]):
                nearest_plot = figure_iv[9]

            else:
                nearest_plot = figure_iv[::-1][nearest_index]

            if nearest_index == 0:
                index_below = 0
            else:
                index_below = nearest_index - 1

            # Determine the distance between the nearest curve and the potential new curve
            y_nearest = self.calc_data['approx_strength']
            x_nearest = interpolate(target_var=y_nearest,
                                    x=nearest_plot['x'],
                                    y=nearest_plot[' y'],
                                    find_x=True)

            distance = x_nearest - target_x

            # Determine the x and y values of the new curve
            x_parallel, y_parallel = offset_curve(nearest_plot['x'], nearest_plot[' y'], d=distance)

            # Determine the free-water to cement ratio
            fwc_ratio = interpolate(target_var=self.calc_data['fm'],
                                    x=x_parallel,
                                    y=y_parallel,
                                    find_x=True)

            # Keep backup of the free water to cement ratio to show in reporting
            self.calc_data['initial_fwc_ratio'] = fwc_ratio

            # Save plot points for graphical reports
            self.graph_temp['figure iv plot'] = {
                'plot above': nearest_plot,
                'new curve': pd.DataFrame({'x': x_parallel, ' y': y_parallel}),
                'plot below': figure_iv[::-1][index_below]
            }

            # Retrieve the specified free water to cement ratio
            spec_fwc_ratio = self.data['Specified variables']['Maximum free water-cement ratio']

            # Apply limits if defined
            if not self.null_check('Specified variables', 'Maximum free water-cement ratio'):

                # Adjust the limits as specified
                if fwc_ratio > float(spec_fwc_ratio):
                    self.calc_data['fwc_ratio'] = spec_fwc_ratio
                    self.fwc_is_larger = True

                else:
                    self.calc_data['fwc_ratio'] = fwc_ratio
                    self.fwc_is_larger = False

            else:
                self.calc_data['fwc_ratio'] = fwc_ratio
                self.fwc_is_larger = False

        elif mode == 'PFA' or 'GGBS':
            # Starting line using data from table 2
            target_x = 0.5

            # y-values for target_x (y-intercept) for every plot line
            y_values = []

            # loop through the plots in figure 4, append the interception point of target_x to y_values
            for plot in figure_iv:
                # find the nearest x values
                nearest_x = plot['x'].values[np.argsort(np.abs(plot['x'].values - target_x))[0:2]]

                # get the corresponding y-values
                nearest_y = plot.loc[plot['x'].isin(nearest_x), ' y'].values

                # interpolate the y-value for target x
                interpolated_y = interpolate(target_var=target_x,
                                             x=nearest_x,
                                             y=nearest_y)

                # append the interpolated y values to the results tray
                y_values.append(interpolated_y)

            # Re-arrange and find the plot above the mean compressive strength
            nearest_index = np.searchsorted(y_values[::-1], self.calc_data['approx_strength'])

            if nearest_index >= len(y_values[::-1]):
                nearest_plot = figure_iv[9]

            else:
                nearest_plot = figure_iv[::-1][nearest_index]

            if nearest_index == 0:
                index_below = 0
            else:
                index_below = nearest_index - 1

            # Determine the distance between the nearest curve and the potential new curve
            y_nearest = self.calc_data['approx_strength']
            x_nearest = interpolate(target_var=y_nearest,
                                    x=nearest_plot['x'],
                                    y=nearest_plot[' y'],
                                    find_x=True)

            distance = x_nearest - target_x

            # Determine the x and y values of the new curve
            x_parallel, y_parallel = offset_curve(nearest_plot['x'], nearest_plot[' y'], d=distance)

            # Determine the free-water to cement ratio
            fwc_ratio = interpolate(target_var=self.calc_data['fm'],
                                    x=x_parallel,
                                    y=y_parallel,
                                    find_x=True)

            # Keep backup of the free water to cement ratio to show in reporting
            self.calc_data['initial_fwc_ratio'] = fwc_ratio

            # Save plot points for graphical reports
            self.graph_temp['figure iv plot'] = {
                'plot above': nearest_plot,
                'new curve': pd.DataFrame({'x': x_parallel, ' y': y_parallel}),
                'plot below': figure_iv[::-1][index_below]
            }

            # Limit comparison is performed at stage 3

    def plot_fwc_determination(self):
        """
        Plots fig 4, Relationship between compressive strength and free-water/cement ratio
        """
        # Create figure 4
        fig_iv = go.Figure()

        # Make printed line above
        fig_iv.add_trace(go.Scatter(x=self.graph_temp['figure iv plot']['plot above']['x'],
                                    y=self.graph_temp['figure iv plot']['plot above'][' y'],
                                    mode='lines',
                                    line=dict(color=graph_colors[10], width=3.6)))

        # Make the new curve
        fig_iv.add_trace(go.Scatter(x=self.graph_temp['figure iv plot']['new curve']['x'],
                                    y=self.graph_temp['figure iv plot']['new curve'][' y'],
                                    mode='lines',
                                    name='Parallel curve',
                                    line=dict(color=white_color, width=2)))

        # Make the plot below
        fig_iv.add_trace(go.Scatter(x=self.graph_temp['figure iv plot']['plot below']['x'],
                                    y=self.graph_temp['figure iv plot']['plot below'][' y'],
                                    mode='lines',
                                    line=dict(color=graph_colors[8], width=3.6)))

        # Make a horizontal line that moves from the y-axis to the plot
        fig_iv.add_shape(
            type='line',
            x0=0,
            y0=self.calc_data['approx_strength'],
            x1=0.5,
            y1=self.calc_data['approx_strength'],
            line=dict(color=graph_colors[7], width=2.1, dash='dash'))

        # Make a vertical line that moves from the x-axis to the plot
        fig_iv.add_shape(
            type='line',
            x0=self.calc_data['initial_fwc_ratio'],
            y0=0,
            x1=self.calc_data['initial_fwc_ratio'],
            y1=self.calc_data['fm'],
            line=dict(color=graph_colors[6], width=2.1, dash='dash'))

        # Make a horizontal line that moves from the y-axis to the plot
        fig_iv.add_shape(
            type='line',
            x0=0,
            y0=self.calc_data['fm'],
            x1=self.calc_data['initial_fwc_ratio'],
            y1=self.calc_data['fm'],
            line=dict(color=graph_colors[6], width=2.1, dash='dash'))

        fig_iv.update_shapes(dict(xref='x', yref='y'))

        # Customize the gridlines
        fig_iv.update_xaxes(gridcolor=graph_colors[4], gridwidth=0.7)
        fig_iv.update_yaxes(gridcolor=graph_colors[4], gridwidth=0.7)

        # Axis titles
        xaxis_title = 'Free-water/cement ratio'
        yaxis_title = 'Compressive strength (N/mm' + '<sup>2</sup>' + ')'

        # Configure xaxis range and tag placement for rare cases
        if self.calc_data['initial_fwc_ratio'] < 0.3:
            x_range = [0.15, 0.9]
            ax = 105
        elif self.calc_data['initial_fwc_ratio'] > 0.7:
            ax = -45
            x_range = [0.3, 0.9]
        else:
            ax = 105
            x_range = [0.3, 0.9]

        # Edit the layout
        fig_iv.update_layout(
            showlegend=False,
            width=600,
            height=400,
            paper_bgcolor=transparent,
            plot_bgcolor=transparent,
            font_family=calibri,
            margin=dict(l=50, r=50, b=50, t=50, pad=4),
            font_size=13,
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            xaxis_range=x_range,
            yaxis_range=[0, 90],
            template='plotly_dark')

        # Add the point (perc_def, k) as an annotation in the plot
        tag = f"Free-water/cement ratio = {np.round(self.calc_data['initial_fwc_ratio'], 2)}"
        fig_iv.add_annotation(
            x=self.calc_data['initial_fwc_ratio'],
            y=self.calc_data['fm'],
            xref='x',
            yref='y',
            text=tag,
            showarrow=True,
            font_family=calibri,
            font_size=14,
            align='center',
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=white_color,
            ax=ax,
            ay=-55,
            bordercolor=white_color,
            borderwidth=2,
            borderpad=4,
            bgcolor=BG,
            opacity=0.99123345
        )

        # Make a vertical line that moves from the x-axis upwards
        fig_iv.add_vline(x=0.5,
                         line=dict(color=graph_colors[7], width=1),
                         annotation_text=f'Starting line using data\n'
                                         f'from the table above')

        # Save the figure temporarily
        self.fig_iv_png_image = plotly_image_converter(fig_iv)

    def check_max_agg(self):
        """
        Checks for the maximum aggregate size selected in the UI
        """
        # Store the aggregate sizes
        self.calc_data['aggregate_sizes'] = [self.data['Specified variables']['10mm'],
                                             self.data['Specified variables']['20mm'],
                                             self.data['Specified variables']['40mm']]
        max_agg_size = max(self.calc_data['aggregate_sizes'])

        # Store the maximum aggregate size as a specified variable
        self.data['Specified variables']['Max Agg Size'] = max_agg_size
        self.calc_data['max_agg_size'] = max_agg_size

    def calculate_fw_content(self, mode: str):
        """
        Calculates the free water content from table 3, method varies with the design mode.
        :param mode: (str) ['DOE', 'AEM', 'PFA', 'GGBS'] the concrete mix design mode
        """

        if mode == 'DOE':

            # Determine the maximum aggregate size
            self.check_max_agg()
            coarse_agg_type = self.data['Additional info']['Coarse Aggregate Type']
            fine_agg_type = self.data['Additional info']['Fine Aggregate Type']
            max_agg_size = self.calc_data['max_agg_size']
            slump_value = self.data['Specified variables']['Slump']

            # When same aggregate types are used
            if coarse_agg_type == fine_agg_type:
                # To be used when reporting
                self.different_agg_types = False

                self.calc_data['fw_content'] = table_iii_a[(max_agg_size, coarse_agg_type)][slump_value]

            else:
                # To be used when reporting
                self.different_agg_types = True

                # free water content based on fine aggregate type
                wf = table_iii_a[(max_agg_size, fine_agg_type)][slump_value]
                self.calc_data['wf'] = wf

                # free water content based on coarse aggregate type
                wc = table_iii_a[(max_agg_size, coarse_agg_type)][slump_value]
                self.calc_data['wc'] = wc

                # free water content when aggregates are of different types
                self.calc_data['fw_content'] = ((2 / 3) * wf) + ((1 / 3) * wc)

        elif mode == 'AEM':

            # Determine the maximum aggregate size
            self.check_max_agg()
            coarse_agg_type = self.data['Additional info']['Coarse Aggregate Type']
            fine_agg_type = self.data['Additional info']['Fine Aggregate Type']
            max_agg_size = self.calc_data['max_agg_size']

            # Reduction in workability to allow for air
            modified_slump_value = aem_workability_modifier(self.data['Specified variables']['Slump'])
            self.calc_data['modified_slump_value'] = modified_slump_value

            # When same aggregate types are used
            if coarse_agg_type == fine_agg_type:
                # To be used when reporting
                self.different_agg_types = False

                self.calc_data['fw_content'] = table_iii_a[(max_agg_size, coarse_agg_type)][modified_slump_value]

            else:
                # To be used when reporting
                self.different_agg_types = True

                # free water content based on fine aggregate type
                wf = table_iii_a[(max_agg_size, fine_agg_type)][modified_slump_value]
                self.calc_data['wf'] = wf

                # free water content based on coarse aggregate type
                wc = table_iii_a[(max_agg_size, coarse_agg_type)][modified_slump_value]
                self.calc_data['wc'] = wc

                # free water content when aggregates are of different types
                self.calc_data['fw_content'] = ((2 / 3) * wf) + ((1 / 3) * wc)

        elif mode == 'PFA':
            # Determine the maximum aggregate size
            self.check_max_agg()
            coarse_agg_type = self.data['Additional info']['Coarse Aggregate Type']
            fine_agg_type = self.data['Additional info']['Fine Aggregate Type']
            max_agg_size = self.calc_data['max_agg_size']
            slump_value = self.data['Specified variables']['Slump']
            pfa_proportion = float(self.data['Specified variables']['pfa Proportion'])

            # When same aggregate types are used
            if coarse_agg_type == fine_agg_type:
                # To be used when reporting
                self.different_agg_types = False

                self.calc_data['initial_fw_content'] = table_iii_a[(max_agg_size, coarse_agg_type)][slump_value]
                self.calc_data['fw_reduction'] = get_fw_reduction(pfa_proportion, slump_value)
                self.calc_data['fw_content'] = self.calc_data['initial_fw_content'] - self.calc_data['fw_reduction']

            else:
                # To be used when reporting
                self.different_agg_types = True

                # free water content based on fine aggregate type
                wf = table_iii_a[(max_agg_size, fine_agg_type)][slump_value]
                self.calc_data['wf'] = wf

                # free water content based on coarse aggregate type
                wc = table_iii_a[(max_agg_size, coarse_agg_type)][slump_value]
                self.calc_data['wc'] = wc

                # free water content when aggregates are of different types
                self.calc_data['initial_fw_content'] = ((2 / 3) * wf) + ((1 / 3) * wc)
                self.calc_data['fw_reduction'] = get_fw_reduction(pfa_proportion, slump_value)
                self.calc_data['fw_content'] = self.calc_data['initial_fw_content'] - self.calc_data['fw_reduction']

        elif mode == 'GGBS':
            # Determine the maximum aggregate size
            self.check_max_agg()
            coarse_agg_type = self.data['Additional info']['Coarse Aggregate Type']
            fine_agg_type = self.data['Additional info']['Fine Aggregate Type']
            max_agg_size = self.calc_data['max_agg_size']
            slump_value = self.data['Specified variables']['Slump']

            if self.null_check('Additional info', 'Water Content Reduction'):
                reduction = 0
            else:
                reduction = float(self.data['Additional info']['Water Content Reduction'])

            # When same aggregate types are used
            if coarse_agg_type == fine_agg_type:
                # To be used when reporting
                self.different_agg_types = False

                self.calc_data['initial_fw_content'] = table_iii_a[(max_agg_size, coarse_agg_type)][slump_value]
                self.calc_data['fw_reduction'] = reduction
                self.calc_data['fw_content'] = self.calc_data['initial_fw_content'] - self.calc_data['fw_reduction']

            else:
                # To be used when reporting
                self.different_agg_types = True

                # free water content based on fine aggregate type
                wf = table_iii_a[(max_agg_size, fine_agg_type)][slump_value]
                self.calc_data['wf'] = wf

                # free water content based on coarse aggregate type
                wc = table_iii_a[(max_agg_size, coarse_agg_type)][slump_value]
                self.calc_data['wc'] = wc

                # free water content when aggregates are of different types
                self.calc_data['initial_fw_content'] = ((2 / 3) * wf) + ((1 / 3) * wc)
                self.calc_data['fw_reduction'] = reduction
                self.calc_data['fw_content'] = self.calc_data['initial_fw_content'] - self.calc_data['fw_reduction']

    def calculate_cement_content(self, mode: str):
        """
        Determines the cement content by dividing the `fw_content` with the `fwc_ratio`
        :param mode: (str) ['DOE', 'AEM', 'PFA', 'GGBS'] the concrete mix design mode
        """
        if mode == 'DOE' or mode == 'AEM':
            # Calculate and store the cement content
            fw_content = float(self.calc_data['fw_content'])
            fwc_ratio = float(self.calc_data['fwc_ratio'])

            self.calc_data['calc_cement_content'] = fw_content / fwc_ratio

            # Adjust cement content based on limits
            max_content = self.data['Specified variables']['Maximum cement content']
            min_content = self.data['Specified variables']['Minimum cement content']
            cement_content = self.calc_data['calc_cement_content']

            # Preliminary check for valid inputs
            confirmation_list = []
            for entry in [max_content.strip(), min_content.strip()]:
                if entry.isnumeric() or entry.replace('.', '', 1).isnumeric() or entry == '':
                    validity = True
                    confirmation_list.append(validity)

                else:
                    validity = False
                    confirmation_list.append(validity)

            if all(confirmation_list):
                self.invalid_cc_entry = False

            else:
                self.invalid_cc_entry = True

            if not self.invalid_cc_entry:
                if min_content and max_content:
                    # Both min and max values are specified
                    min_value = float(min_content)
                    max_value = float(max_content)

                    # Make a status dict, to be used for case specification in reporting
                    self.cc_status = {
                        "max_content": "Specified",
                        "min_content": "Specified"
                    }

                    if min_value > max_value:
                        # This brings a warning message when the program is running...
                        self.min_is_more_than_max = True

                    if min_value <= cement_content <= max_value:
                        self.calc_data['cement_content'] = cement_content

                        # Update status
                        self.cc_status["cement_content"] = 'Within Range'

                        # Modify the free water to cement ratio
                        self.calc_data['modified_fwc_ratio'] = self.calc_data['fw_content'] / cement_content

                    elif cement_content < min_value:
                        self.calc_data['cement_content'] = min_value

                        # Update status
                        self.cc_status["cement_content"] = "Below Minimum"

                        # Modify the free water to cement ratio
                        self.calc_data['modified_fwc_ratio'] = self.calc_data['fw_content'] / self.calc_data[
                            'cement_content']

                    else:
                        # Given specifications cannot be met bc cement content is more than maximum
                        self.feasibility_status = False

                elif min_content:
                    # Only min value is specified
                    min_value = float(min_content)

                    # Make a status dict, to be used for case specification in reporting
                    self.cc_status = {
                        "max_content": "Unspecified",
                        "min_content": "Specified"
                    }

                    if cement_content < min_value:
                        self.calc_data['cement_content'] = min_value

                        # Update status
                        self.cc_status["cement_content"] = "Below Minimum"

                        # Modify the free water to cement ratio
                        self.calc_data['modified_fwc_ratio'] = self.calc_data['fw_content'] / self.calc_data[
                            'cement_content']

                    else:
                        self.calc_data['cement_content'] = cement_content

                        # Update status
                        self.cc_status["cement_content"] = "Within Range"

                        # Modify the free water to cement ratio
                        self.calc_data['modified_fwc_ratio'] = self.calc_data['fw_content'] / self.calc_data[
                            'cement_content']

                elif max_content:
                    # Only max value is specified
                    max_value = float(max_content)

                    # Make a status dict, to be used for case specification in reporting
                    self.cc_status = {
                        "max_content": "Specified",
                        "min_content": "Unspecified"
                    }

                    if cement_content > max_value:
                        # Given specifications cannot be met bc the calculated cement content is more than the maximum value
                        self.feasibility_status = False

                    else:
                        self.calc_data['cement_content'] = cement_content

                        # Update status
                        self.cc_status["cement_content"] = "Within Range"

                        # Modify the free water to cement ratio
                        self.calc_data['modified_fwc_ratio'] = self.calc_data['fw_content'] / self.calc_data[
                            'cement_content']

                else:
                    # No range values specified, return original cement content
                    self.calc_data['cement_content'] = cement_content

                    # Make a status dict, to be used for case specification in reporting
                    self.cc_status = {
                        "max_content": "Unspecified",
                        "min_content": "Unspecified"
                    }

                    # Modify the free water to cement ratio
                    self.calc_data['modified_fwc_ratio'] = self.calc_data['fw_content'] / self.calc_data[
                        'cement_content']

            else:
                # Invalid input, do not proceed
                pass

        elif mode == 'PFA':

            # Calculate and store the cement content
            fw_content = float(self.calc_data['fw_content'])
            fwc_ratio = float(self.calc_data['initial_fwc_ratio'])
            p = float(self.data['Specified variables']['pfa Proportion'])
            k = float(self.data['Additional info']['Cementing Efficiency Factor'])

            # Calculate portland cement content
            c = ((100 - p) * fw_content) / ((100 - ((1 - k) * p)) * fwc_ratio)
            self.calc_data['init_C'] = c

            # Calculate pfa content
            f = (p * c) / (100 - p)
            self.calc_data['init_F'] = f

            # (Cement + pfa) content; (C + F)
            cement_content = c + f
            self.calc_data['calc_cement_content'] = cement_content

            # Compare the calculated cement contents with the specified limits.
            max_content = self.data['Specified variables']['Maximum cement content']
            min_content = self.data['Specified variables']['Minimum cement content']
            max_wcf_ratio = self.data['Specified variables']['Maximum free water-cement ratio']

            # Preliminary check for valid inputs
            confirmation_list = []
            for entry in [max_content.strip(), min_content.strip(), max_wcf_ratio.strip()]:
                if entry.isnumeric() or entry.replace('.', '', 1).isnumeric() or entry == '':
                    validity = True
                    confirmation_list.append(validity)

                else:
                    validity = False
                    confirmation_list.append(validity)

            if all(confirmation_list):
                self.invalid_cc_entry = False

            else:
                self.invalid_cc_entry = True

            if not self.invalid_cc_entry:
                if min_content and max_content:

                    # Both min and max values are specified
                    min_value = float(min_content)
                    max_value = float(max_content)

                    # Make a status dict, to be used for case specification in reporting
                    self.cc_status = {
                        "max_content": "Specified",
                        "min_content": "Specified"
                    }

                    if min_value > max_value:
                        # This brings a warning message when the program is running...
                        self.min_is_more_than_max = True

                    if min_value <= cement_content <= max_value:
                        self.calc_data['cement_content'] = cement_content

                        # Update status
                        self.cc_status["cement_content"] = "Within Range"

                        # No modifications to the cementitious content
                        self.calc_data["init_ii_C"] = self.calc_data["init_C"]
                        self.calc_data["init_ii_F"] = self.calc_data["init_F"]

                    elif cement_content < min_value:
                        self.calc_data['cement_content'] = min_value

                        # Update status
                        self.cc_status["cement_content"] = "Below Minimum"

                        # Modify cementitious content, share the difference on cement and pfa based on their proportions
                        diff = min_value - cement_content
                        self.calc_data['cc_difference'] = diff
                        self.calc_data["init_ii_C"] = self.calc_data["init_C"] + ((1 - (p / 100)) * diff)
                        self.calc_data["init_ii_F"] = self.calc_data["init_F"] + ((p / 100) * diff)

                    else:
                        # Given specifications cannot be met bc cement content is more than maximum
                        self.feasibility_status = False

                elif min_content:
                    # Only min value is specified
                    min_value = float(min_content)

                    # Make a status dict, to be used for case specification in reporting
                    self.cc_status = {
                        "max_content": "Unspecified",
                        "min_content": "Specified"
                    }

                    if cement_content < min_value:
                        self.calc_data['cement_content'] = min_value

                        # Update status
                        self.cc_status["cement_content"] = "Below Minimum"

                        # Modify cementitious content, share the difference on cement and pfa based on their proportions
                        diff = min_value - cement_content
                        self.calc_data["init_ii_C"] = self.calc_data["init_C"] + ((1 - (p / 100)) * diff)
                        self.calc_data["init_ii_F"] = self.calc_data["init_F"] + ((p / 100) * diff)

                    else:
                        self.calc_data['cement_content'] = cement_content

                        # Update status
                        self.cc_status["cement_content"] = "Within Range"

                        # No modifications to the cementitious content
                        self.calc_data["init_ii_C"] = self.calc_data["init_C"]
                        self.calc_data["init_ii_F"] = self.calc_data["init_F"]

                elif max_content:
                    # Only max value is specified
                    max_value = float(max_content)

                    # Make a status dict, to be used for case specification in reporting
                    self.cc_status = {
                        "max_content": "Specified",
                        "min_content": "Unspecified"
                    }

                    if cement_content > max_value:
                        # Given specifications cannot be met bc the calculated cement content is more than the maximum value
                        self.feasibility_status = False

                    else:
                        self.calc_data['cement_content'] = cement_content

                        # Update status
                        self.cc_status["cement_content"] = 'Within Range'

                        # No modifications to the cementitious content
                        self.calc_data["init_ii_C"] = self.calc_data["init_C"]
                        self.calc_data["init_ii_F"] = self.calc_data["init_F"]

                else:
                    # No range values specified, return original cement content
                    self.calc_data['cement_content'] = cement_content

                    # Make a status dict, to be used for case specification in reporting
                    self.cc_status = {
                        "max_content": "Unspecified",
                        "min_content": "Unspecified"
                    }

                    # No modifications to the cementitious content
                    self.calc_data["init_ii_C"] = self.calc_data["init_C"]
                    self.calc_data["init_ii_F"] = self.calc_data["init_F"]

                if self.feasibility_status:

                    # Determine W / (C + F) ratio;
                    wcf_ratio = fw_content / self.calc_data['cement_content']
                    self.calc_data['calc_wcf_ratio'] = wcf_ratio

                    if max_wcf_ratio == '' or float(max_wcf_ratio) == float(0):
                        limit = 0
                        self.cc_status['limiting wcf'] = 'Unspecified'

                    else:
                        limit = float(max_wcf_ratio)
                        self.cc_status['limiting wcf'] = 'Specified'

                    # Compare to a specified maximum free-water ratio
                    if self.cc_status['limiting wcf'] == 'Specified' and wcf_ratio > limit:
                        # Update the status dict, for reporting
                        self.cc_status['wcf_status'] = 'More than Maximum'

                        # Save to the calc_data dictionary
                        self.calc_data['modified_fwc_ratio'] = limit

                        # Re-calculate the cementitious content.
                        self.calc_data['final_cementitious_content'] = fw_content / self.calc_data['modified_fwc_ratio']
                        diff = self.calc_data['final_cementitious_content'] - self.calc_data['cement_content']
                        self.calc_data["C"] = self.calc_data["init_ii_C"] + ((1 - (p / 100)) * diff)
                        self.calc_data["F"] = self.calc_data["init_ii_F"] + ((p / 100) * diff)

                    elif self.cc_status['limiting wcf'] == 'Specified' and wcf_ratio < limit:
                        # Update the status dict, for reporting
                        self.cc_status['wcf_status'] = 'Less than Maximum'

                        # Save the calc_data dictionary
                        self.calc_data['modified_fwc_ratio'] = wcf_ratio

                        # No modifications to the cementitious content, store data as it is.
                        self.calc_data['final_cementitious_content'] = self.calc_data['cement_content']
                        self.calc_data["C"] = self.calc_data["init_ii_C"]
                        self.calc_data["F"] = self.calc_data["init_ii_F"]

                    elif self.cc_status['limiting wcf'] == 'Unspecified':
                        # Update the status dict, for reporting
                        self.cc_status['wcf_status'] = 'No Limits'

                        # Save the calc_data dictionary
                        self.calc_data['modified_fwc_ratio'] = wcf_ratio

                        # No modifications to the cementitious content, store data as it is.
                        self.calc_data['final_cementitious_content'] = self.calc_data['cement_content']
                        self.calc_data["C"] = self.calc_data["init_ii_C"]
                        self.calc_data["F"] = self.calc_data["init_ii_F"]

                else:
                    # I don't want to go on with the calculations if self.feasibility_status is True
                    pass
            else:
                # Invalid input, do not proceed
                pass

        elif mode == 'GGBS':

            # Calculate and store the cement content
            fw_content = float(self.calc_data['fw_content'])
            fwc_ratio = float(self.calc_data['initial_fwc_ratio'])
            ggbs_prop = float(self.data['Specified variables']['ggbs Proportion'])

            # (Cement + ggbs) content; (C + G)
            cement_content = fw_content / fwc_ratio
            self.calc_data['calc_cement_content'] = cement_content

            # Calculate portland cement content
            c = ((100 - ggbs_prop) / 100) * cement_content
            self.calc_data['init_C'] = c

            # Calculate ggbs content
            g = cement_content - c
            self.calc_data['init_G'] = g

            # Compare the calculated cement contents with the specified limits.
            max_content = self.data['Specified variables']['Maximum cement content']
            min_content = self.data['Specified variables']['Minimum cement content']
            max_wcg_ratio = self.data['Specified variables']['Maximum free water-cement ratio']

            # Preliminary check for valid inputs
            confirmation_list = []
            for entry in [max_content.strip(), min_content.strip(), max_wcg_ratio.strip()]:
                if entry.isnumeric() or entry.replace('.', '', 1).isnumeric() or entry == '':
                    validity = True
                    confirmation_list.append(validity)

                else:
                    validity = False
                    confirmation_list.append(validity)

            if all(confirmation_list):
                self.invalid_cc_entry = False

            else:
                self.invalid_cc_entry = True

            if not self.invalid_cc_entry:
                if min_content and max_content:

                    # Both min and max values are specified
                    min_value = float(min_content)
                    max_value = float(max_content)

                    # Make a status dict, to be used for case specification in reporting
                    self.cc_status = {
                        "max_content": "Specified",
                        "min_content": "Specified"
                    }

                    if min_value > max_value:
                        # This brings a warning message when the program is running...
                        self.min_is_more_than_max = True

                    if min_value <= cement_content <= max_value:
                        self.calc_data['cement_content'] = cement_content

                        # Update status
                        self.cc_status["cement_content"] = "Within Range"

                        # No modifications to the cementitious content
                        self.calc_data["init_ii_C"] = self.calc_data["init_C"]
                        self.calc_data["init_ii_G"] = self.calc_data["init_G"]

                    elif cement_content < min_value:
                        self.calc_data['cement_content'] = min_value

                        # Update status
                        self.cc_status["cement_content"] = "Below Minimum"

                        # Modify cementitious content, share the difference on cement and pfa based on their proportions
                        diff = min_value - cement_content
                        self.calc_data['cc_difference'] = diff
                        self.calc_data["init_ii_C"] = self.calc_data["init_C"] + ((1 - (ggbs_prop / 100)) * diff)
                        self.calc_data["init_ii_G"] = self.calc_data["init_G"] + ((ggbs_prop / 100) * diff)

                    else:
                        # Given specifications cannot be met bc cement content is more than maximum
                        self.feasibility_status = False

                elif min_content:
                    # Only min value is specified
                    min_value = float(min_content)

                    # Make a status dict, to be used for case specification in reporting
                    self.cc_status = {
                        "max_content": "Unspecified",
                        "min_content": "Specified"
                    }

                    if cement_content < min_value:
                        self.calc_data['cement_content'] = min_value

                        # Update status
                        self.cc_status["cement_content"] = "Below Minimum"

                        # Modify cementitious content, share the difference on cement and pfa based on their proportions
                        diff = min_value - cement_content
                        self.calc_data["init_ii_C"] = self.calc_data["init_C"] + ((1 - (ggbs_prop / 100)) * diff)
                        self.calc_data["init_ii_G"] = self.calc_data["init_G"] + ((ggbs_prop / 100) * diff)

                    else:
                        self.calc_data['cement_content'] = cement_content

                        # Update status
                        self.cc_status["cement_content"] = "Within Range"

                        # No modifications to the cementitious content
                        self.calc_data["init_ii_C"] = self.calc_data["init_C"]
                        self.calc_data["init_ii_G"] = self.calc_data["init_G"]

                elif max_content:
                    # Only max value is specified
                    max_value = float(max_content)

                    # Make a status dict, to be used for case specification in reporting
                    self.cc_status = {
                        "max_content": "Specified",
                        "min_content": "Unspecified"
                    }

                    if cement_content > max_value:
                        # Given specifications cannot be met bc the calculated cement content is more than the maximum value
                        self.feasibility_status = False

                    else:
                        self.calc_data['cement_content'] = cement_content

                        # Update status
                        self.cc_status["cement_content"] = 'Within Range'

                        # No modifications to the cementitious content
                        self.calc_data["init_ii_C"] = self.calc_data["init_C"]
                        self.calc_data["init_ii_G"] = self.calc_data["init_G"]

                else:
                    # No range values specified, return original cement content
                    self.calc_data['cement_content'] = cement_content

                    # Make a status dict, to be used for case specification in reporting
                    self.cc_status = {
                        "max_content": "Unspecified",
                        "min_content": "Unspecified"
                    }

                    # No modifications to the cementitious content
                    self.calc_data["init_ii_C"] = self.calc_data["init_C"]
                    self.calc_data["init_ii_G"] = self.calc_data["init_G"]

                if self.feasibility_status:

                    # Determine W / (C + G) ratio;
                    wcg_ratio = fw_content / self.calc_data['cement_content']
                    self.calc_data['calc_wcg_ratio'] = wcg_ratio

                    if max_wcg_ratio == '' or float(max_wcg_ratio) == float(0):
                        limit = 0
                        self.cc_status['limiting wcg'] = 'Unspecified'

                    else:
                        limit = float(max_wcg_ratio)
                        self.cc_status['limiting wcg'] = 'Specified'

                    # Compare to a specified maximum free-water ratio
                    if self.cc_status['limiting wcg'] == 'Specified' and wcg_ratio > limit:
                        # Update the status dict, for reporting
                        self.cc_status['wcg_status'] = 'More than Maximum'

                        # Save to the calc_data dictionary
                        self.calc_data['modified_fwc_ratio'] = limit

                        # Re-calculate the cementitious content.
                        self.calc_data['final_cementitious_content'] = fw_content / self.calc_data['modified_fwc_ratio']
                        diff = self.calc_data['final_cementitious_content'] - self.calc_data['cement_content']
                        self.calc_data["C"] = self.calc_data["init_ii_C"] + ((1 - (ggbs_prop / 100)) * diff)
                        self.calc_data["G"] = self.calc_data["init_ii_G"] + ((ggbs_prop / 100) * diff)

                    elif self.cc_status['limiting wcg'] == 'Specified' and wcg_ratio < limit:
                        # Update the status dict, for reporting
                        self.cc_status['wcg_status'] = 'Less than Maximum'

                        # Save the calc_data dictionary
                        self.calc_data['modified_fwc_ratio'] = wcg_ratio

                        # No modifications to the cementitious content, store data as it is.
                        self.calc_data['final_cementitious_content'] = self.calc_data['cement_content']
                        self.calc_data["C"] = self.calc_data["init_ii_C"]
                        self.calc_data["G"] = self.calc_data["init_ii_G"]

                    elif self.cc_status['limiting wcg'] == 'Unspecified':
                        # Update the status dict, for reporting
                        self.cc_status['wcg_status'] = 'No Limits'

                        # Save the calc_data dictionary
                        self.calc_data['modified_fwc_ratio'] = wcg_ratio

                        # No modifications to the cementitious content, store data as it is.
                        self.calc_data['final_cementitious_content'] = self.calc_data['cement_content']
                        self.calc_data["C"] = self.calc_data["init_ii_C"]
                        self.calc_data["G"] = self.calc_data["init_ii_G"]

                else:
                    # I don't want to go on with the calculations if self.feasibility_status is True
                    pass
            else:
                # Invalid input, do not proceed
                pass

    def ssd_check(self):
        """
        Checks the validity of the relative density of aggregate
        """
        ssd = self.data['Additional info']['Relative density of agg']

        if self.null_check('Additional info', 'Relative density of agg'):
            # If ssd is not entered, code assumes based on aggregates..
            pass
        else:
            try:
                ssd = float(ssd)
                self.ssd_value_error = False

                if 2.4 <= ssd <= 2.9:
                    # When the relative density in ssd is in range
                    self.invalid_ssd = False
                else:
                    # When the relative density in ssd in not in range
                    self.invalid_ssd = True

            except ValueError:
                self.ssd_value_error = True
                self.invalid_ssd = False

    def compute_wet_conc_density(self, mode: str):
        """
        Computes the wet concrete density of the designed mix
        :param mode: (str) ['DOE', 'AEM', 'PFA', 'GGBS'] the concrete mix design mode
        """
        # Calculation parameters
        coarse_agg_type = self.data['Additional info']['Coarse Aggregate Type']
        fine_agg_type = self.data['Additional info']['Fine Aggregate Type']
        fw_content = self.calc_data['fw_content']

        # Generate the datapoints for figure 5
        figure_5 = generate_figure_v()

        if mode == 'DOE' or mode == 'PFA' or mode == 'GGBS':
            if self.null_check('Additional info', 'Relative density of agg'):

                # Status dictionary
                self.tac_content = {'ssd_value': 'unspecified'}

                if coarse_agg_type == fine_agg_type and coarse_agg_type == 'Crushed':
                    # Assumed for crushed aggregate (2.7)
                    self.calc_data['ssd_value'] = 2.7
                    wet_conc_density = interpolate(
                        x=figure_5[3]['x'],
                        y=figure_5[3][' y'],
                        target_var=fw_content
                    )
                    self.calc_data['calc_wet_conc_density'] = wet_conc_density

                    # Update status
                    self.tac_content['Agg_status'] = 'Same types, crushed'

                elif coarse_agg_type == fine_agg_type and coarse_agg_type == 'Uncrushed':
                    # Assumed for crushed aggregate (2.6)
                    self.calc_data['ssd_value'] = 2.6
                    wet_conc_density = interpolate(
                        x=figure_5[2]['x'],
                        y=figure_5[2][' y'],
                        target_var=fw_content
                    )
                    self.calc_data['calc_wet_conc_density'] = wet_conc_density

                    # Update status
                    self.tac_content['Agg_status'] = 'Same types, uncrushed'

                else:
                    # The desired line label
                    desired_line = 2.65
                    self.calc_data['ssd_value'] = desired_line

                    # Find the index of the dataframe that contains the line below the desired line (2.6)
                    lower_index = int((desired_line - 2.4) * 10)

                    # Find the index of the dataframe that contains the line above the desired line (2.7)
                    upper_index = lower_index + 1 if lower_index < 5 else 5

                    # Interpolate the x and y values
                    x_lower = figure_5[lower_index]['x']
                    y_lower = figure_5[lower_index][' y']
                    x_upper = figure_5[upper_index]['x']
                    y_upper = figure_5[upper_index][' y']

                    x_desired = x_lower + (desired_line - (lower_index / 10 + 2.4)) / 0.1 * (x_upper - x_lower)
                    y_desired = y_lower + (desired_line - (lower_index / 10 + 2.4)) / 0.1 * (y_upper - y_lower)

                    # Store these values for further plotting
                    self.graph_temp['ssd_spec_x'] = x_desired
                    self.graph_temp['ssd_spec_y'] = y_desired

                    # Wet concrete density assumed for mixed aggregates (2.65)
                    wet_conc_density = interpolate(x=x_desired, y=y_desired, target_var=fw_content)
                    self.calc_data['calc_wet_conc_density'] = wet_conc_density

                    # Update status
                    self.tac_content['Agg_status'] = 'Diff types'

            else:
                # Status dictionary
                self.tac_content = {'ssd_value': 'specified'}

                # Convert the specified relative density (ssd) value from string to float
                desired_line = float(self.data['Additional info']['Relative density of agg'])
                self.calc_data['ssd_value'] = desired_line

                # Find the index of the dataframe that contains the line below the desired line
                lower_index = int((desired_line - 2.4) * 10)

                # Find the index of the dataframe that contains the line above the desired line
                # Handle the upper limit of 2.9
                upper_index = lower_index + 1 if lower_index < 5 else 5

                # Interpolate the x and y values
                x_lower = figure_5[lower_index]['x']
                y_lower = figure_5[lower_index][' y']
                x_upper = figure_5[upper_index]['x']
                y_upper = figure_5[upper_index][' y']

                x_desired = x_lower + (desired_line - (lower_index / 10 + 2.4)) / 0.1 * (x_upper - x_lower)
                y_desired = y_lower + (desired_line - (lower_index / 10 + 2.4)) / 0.1 * (y_upper - y_lower)

                # Store these values for further plotting
                self.graph_temp['ssd_spec_x'] = x_desired
                self.graph_temp['ssd_spec_y'] = y_desired

                # Calculate the wet concrete density
                wet_conc_density = interpolate(x=x_desired, y=y_desired, target_var=fw_content)
                self.calc_data['calc_wet_conc_density'] = wet_conc_density

        elif mode == 'AEM':
            # Retrieve air content
            a = float(self.data['Specified variables']['Air Content'])

            if self.null_check('Additional info', 'Relative density of agg'):

                # Status dictionary
                self.tac_content = {'ssd_value': 'unspecified'}

                if coarse_agg_type == fine_agg_type and coarse_agg_type == 'Crushed':
                    # Assumed for crushed aggregate (2.7)
                    self.calc_data['ssd_value'] = 2.7
                    wet_conc_density = interpolate(
                        x=figure_5[3]['x'],
                        y=figure_5[3][' y'],
                        target_var=fw_content
                    )

                    # Adjust the wet concrete density to allow for its air content
                    self.calc_data['density_from_plot'] = wet_conc_density
                    self.calc_data['calc_wet_conc_density'] = wet_conc_density - (10 * a * self.calc_data['ssd_value'])

                    # Update status
                    self.tac_content['Agg_status'] = 'Same types, crushed'

                elif coarse_agg_type == fine_agg_type and coarse_agg_type == 'Uncrushed':
                    # Assumed for crushed aggregate (2.6)
                    self.calc_data['ssd_value'] = 2.6
                    wet_conc_density = interpolate(
                        x=figure_5[2]['x'],
                        y=figure_5[2][' y'],
                        target_var=fw_content
                    )

                    # Adjust the wet concrete density to allow for its air content
                    self.calc_data['density_from_plot'] = wet_conc_density
                    self.calc_data['calc_wet_conc_density'] = wet_conc_density - (10 * a * self.calc_data['ssd_value'])

                    # Update status
                    self.tac_content['Agg_status'] = 'Same types, uncrushed'

                else:
                    # The desired line label
                    desired_line = 2.65
                    self.calc_data['ssd_value'] = desired_line

                    # Find the index of the dataframe that contains the line below the desired line (2.6)
                    lower_index = int((desired_line - 2.4) * 10)

                    # Find the index of the dataframe that contains the line above the desired line (2.7)
                    upper_index = lower_index + 1 if lower_index < 5 else 5

                    # Interpolate the x and y values
                    x_lower = figure_5[lower_index]['x']
                    y_lower = figure_5[lower_index][' y']
                    x_upper = figure_5[upper_index]['x']
                    y_upper = figure_5[upper_index][' y']

                    x_desired = x_lower + (desired_line - (lower_index / 10 + 2.4)) / 0.1 * (x_upper - x_lower)
                    y_desired = y_lower + (desired_line - (lower_index / 10 + 2.4)) / 0.1 * (y_upper - y_lower)

                    # Store these values for further plotting
                    self.graph_temp['ssd_spec_x'] = x_desired
                    self.graph_temp['ssd_spec_y'] = y_desired

                    # Wet concrete density assumed for mixed aggregates (2.65)
                    wet_conc_density = interpolate(x=x_desired, y=y_desired, target_var=fw_content)
                    self.calc_data['density_from_plot'] = wet_conc_density
                    self.calc_data['calc_wet_conc_density'] = wet_conc_density - (10 * a * self.calc_data['ssd_value'])

                    # Update status
                    self.tac_content['Agg_status'] = 'Diff types'

            else:
                # Status dictionary
                self.tac_content = {'ssd_value': 'specified'}

                # Convert the specified relative density (ssd) value from string to float
                desired_line = float(self.data['Additional info']['Relative density of agg'])
                self.calc_data['ssd_value'] = desired_line

                # Find the index of the dataframe that contains the line below the desired line
                lower_index = int((desired_line - 2.4) * 10)

                # Find the index of the dataframe that contains the line above the desired line
                # Handle the upper limit of 2.9
                upper_index = lower_index + 1 if lower_index < 5 else 5

                # Interpolate the x and y values
                x_lower = figure_5[lower_index]['x']
                y_lower = figure_5[lower_index][' y']
                x_upper = figure_5[upper_index]['x']
                y_upper = figure_5[upper_index][' y']

                x_desired = x_lower + (desired_line - (lower_index / 10 + 2.4)) / 0.1 * (x_upper - x_lower)
                y_desired = y_lower + (desired_line - (lower_index / 10 + 2.4)) / 0.1 * (y_upper - y_lower)

                # Store these values for further plotting
                self.graph_temp['ssd_spec_x'] = x_desired
                self.graph_temp['ssd_spec_y'] = y_desired

                # Calculate the wet concrete density
                wet_conc_density = interpolate(x=x_desired, y=y_desired, target_var=fw_content)

                # Adjust the wet concrete density to allow for its air content
                self.calc_data['density_from_plot'] = wet_conc_density
                self.calc_data['calc_wet_conc_density'] = wet_conc_density - (10 * a * self.calc_data['ssd_value'])

    def plot_figure_v(self, status: str, mode: str):
        """
        Plots figure v, estimated wet density of fully compacted concrete.
        :param status: string value indicating the cases of user specified ssd values
        :param mode: (str) ['DOE', 'AEM', 'PFA', 'GGBS'] the concrete mix design mode
        """
        # Generate the datapoints for figure 5
        figure_5 = generate_figure_v()

        if mode == 'DOE' or mode == 'PFA' or mode == 'GGBS':
            # Graph parameters
            wcd = self.calc_data['calc_wet_conc_density']
            fw_content = self.calc_data['fw_content']

            # Legend and colors
            names = ['2.4', '2.5', '2.6 (Assumed for uncrushed aggregates)',
                     '2.7 (Assumed for crushed aggregates)',
                     '2.8', '2.9']

            fig_v_colors = ['#FF5773', '#00689D', '#A61B1B',
                            '#D69600', '#9932CC', '#009E48', '#14FCE9']

            # Plot lines through 2.4 to 2.9
            traces = []  # List to store each trace for each plot
            for i in range(6):
                trace = go.Scatter(
                    x=figure_5[i]['x'],
                    y=figure_5[i][' y'],
                    mode='lines',
                    name=names[i],
                    line=dict(color=fig_v_colors[i], width=2))

                traces.append(trace)

            # Create figure 5
            fig_v = go.Figure(data=traces)

            if status == 'crushed and uncrushed, unspecified':
                # Display the 2.65 line
                fig_v.add_trace(
                    go.Scatter(
                        x=self.graph_temp['ssd_spec_x'],
                        y=self.graph_temp['ssd_spec_y'],
                        mode='lines',
                        name='2.65 (Assumed for crushed and uncrushed aggregates)',
                        line=dict(color=fig_v_colors[6], width=2)
                    )
                )

            elif status == 'crushed or uncrushed, unspecified':
                # There's nothing extra to display
                pass

            elif status == 'specified':
                ssd_plot_display_val = str(self.data['Additional info']['Relative density of agg'])

                # Display the desired line
                fig_v.add_trace(
                    go.Scatter(
                        x=self.graph_temp['ssd_spec_x'],
                        y=self.graph_temp['ssd_spec_y'],
                        mode='lines',
                        name=ssd_plot_display_val,
                        line=dict(color=fig_v_colors[6], width=2)
                    )
                )

            # Make a vertical line that moves from the x-axis to the plot
            fig_v.add_shape(
                type='line',
                x0=fw_content,
                y0=0,
                x1=fw_content,
                y1=wcd,
                line=dict(color=white_color, width=2.1, dash='dash'))

            # Make a horizontal line that moves from the y-axis to the plot
            fig_v.add_shape(
                type='line',
                x0=0,
                y0=wcd,
                x1=fw_content,
                y1=wcd,
                line=dict(color=white_color, width=2.1, dash='dash'))

            # Customize the gridlines
            fig_v.update_xaxes(gridcolor=graph_colors[4], gridwidth=0.5)
            fig_v.update_yaxes(gridcolor=graph_colors[4], gridwidth=0.5)

            # Axis titles
            xaxis_title = 'Free-water content (kg/m' + '<sup>3</sup>' + ')'
            yaxis_title = 'Wet density of concrete mix (kg/m' + '<sup>3</sup>' + ')'

            # Edit the layout
            fig_v.update_layout(
                width=620,
                height=440,
                autosize=True,
                paper_bgcolor=transparent,
                plot_bgcolor=transparent,
                font_family=calibri,
                margin=dict(l=50, r=50, b=50, t=50, pad=4),
                font_size=13,
                xaxis_title=xaxis_title,
                xaxis_range=[100, 280],
                yaxis_title=yaxis_title,
                yaxis_range=[2100, 2800],
                legend=dict(xanchor='right', yanchor='top', font=dict(size=10),
                            title='Relative density of combined aggregate (on saturated and surface-dry basis',
                            orientation='v'),
                template='plotly_dark')

            # Add the point (fw_content, wcd) as an annotation in the plot
            tag = f"Estimated mix density = {np.round(wcd, 2)} kg/m<sup>3</sup>"
            fig_v.add_annotation(
                x=fw_content,
                y=wcd,
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
                ax=50,
                ay=50,
                bordercolor=white_color,
                borderwidth=2,
                borderpad=4,
                bgcolor=BG,
                opacity=0.99123345
            )

            # Save the figure temporarily
            self.fig_v_png_image = plotly_image_converter(fig_v)

        elif mode == 'AEM':

            # Graph parameters
            wcd = self.calc_data['density_from_plot']
            fw_content = self.calc_data['fw_content']

            # Legend and colors
            names = ['2.4', '2.5', '2.6 (Assumed for uncrushed aggregates)',
                     '2.7 (Assumed for crushed aggregates)',
                     '2.8', '2.9']

            fig_v_colors = ['#FF5773', '#00689D', '#A61B1B',
                            '#D69600', '#9932CC', '#009E48', '#14FCE9']

            # Plot lines through 2.4 to 2.9
            traces = []  # List to store each trace for each plot
            for i in range(6):
                trace = go.Scatter(
                    x=figure_5[i]['x'],
                    y=figure_5[i][' y'],
                    mode='lines',
                    name=names[i],
                    line=dict(color=fig_v_colors[i], width=2))

                traces.append(trace)

            # Create figure 5
            fig_v = go.Figure(data=traces)

            if status == 'crushed and uncrushed, unspecified':
                # Display the 2.65 line
                fig_v.add_trace(
                    go.Scatter(
                        x=self.graph_temp['ssd_spec_x'],
                        y=self.graph_temp['ssd_spec_y'],
                        mode='lines',
                        name='2.65 (Assumed for crushed and uncrushed aggregates)',
                        line=dict(color=fig_v_colors[6], width=2)
                    )
                )

            elif status == 'crushed or uncrushed, unspecified':
                # There's nothing extra to display
                pass

            elif status == 'specified':
                ssd_plot_display_val = str(self.data['Additional info']['Relative density of agg'])

                # Display the desired line
                fig_v.add_trace(
                    go.Scatter(
                        x=self.graph_temp['ssd_spec_x'],
                        y=self.graph_temp['ssd_spec_y'],
                        mode='lines',
                        name=ssd_plot_display_val,
                        line=dict(color=fig_v_colors[6], width=2)
                    )
                )

            # Make a vertical line that moves from the x-axis to the plot
            fig_v.add_shape(
                type='line',
                x0=fw_content,
                y0=0,
                x1=fw_content,
                y1=wcd,
                line=dict(color=white_color, width=2.1, dash='dash'))

            # Make a horizontal line that moves from the y-axis to the plot
            fig_v.add_shape(
                type='line',
                x0=0,
                y0=wcd,
                x1=fw_content,
                y1=wcd,
                line=dict(color=white_color, width=2.1, dash='dash'))

            # Customize the gridlines
            fig_v.update_xaxes(gridcolor=graph_colors[4], gridwidth=0.5)
            fig_v.update_yaxes(gridcolor=graph_colors[4], gridwidth=0.5)

            # Axis titles
            xaxis_title = 'Free-water content (kg/m' + '<sup>3</sup>' + ')'
            yaxis_title = 'Wet density of concrete mix (kg/m' + '<sup>3</sup>' + ')'

            # Edit the layout
            fig_v.update_layout(
                width=620,
                height=440,
                autosize=True,
                paper_bgcolor=transparent,
                plot_bgcolor=transparent,
                font_family=calibri,
                margin=dict(l=50, r=50, b=50, t=50, pad=4),
                font_size=13,
                xaxis_title=xaxis_title,
                xaxis_range=[100, 280],
                yaxis_title=yaxis_title,
                yaxis_range=[2100, 2800],
                legend=dict(xanchor='right', yanchor='top', font=dict(size=10),
                            title='Relative density of combined aggregate (on saturated and surface-dry basis',
                            orientation='v'),
                template='plotly_dark')

            # Add the point (fw_content, wcd) as an annotation in the plot
            tag = f"Estimated mix density = {np.round(wcd, 2)} kg/m<sup>3</sup>"
            fig_v.add_annotation(
                x=fw_content,
                y=wcd,
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
                ax=50,
                ay=50,
                bordercolor=white_color,
                borderwidth=2,
                borderpad=4,
                bgcolor=BG,
                opacity=0.99123345
            )

            # Save the figure temporarily
            self.fig_v_png_image = plotly_image_converter(fig_v)

    def override_density(self):
        """
        Override the calculated wet density with a specified value, if provided.
        """
        if self.null_check('Mix Parameters', 'Concrete density'):
            self.calc_data['wet_conc_density'] = self.calc_data['calc_wet_conc_density']

            # Used for reporting
            self.specified_conc_density = False

        else:
            self.calc_data['wet_conc_density'] = float(self.data['Mix Parameters']['Concrete density'])

            # Update for reporting
            self.specified_conc_density = True

    def compute_total_agg_content(self, mode: str):
        """
        Calculates the total aggregate content depending on the design mode
        :param mode: (str) ['DOE', 'AEM', 'PFA', 'GGBS'] the concrete mix design mode
        """
        # Calculate the total aggregate content
        if mode == 'DOE' or mode == 'AEM':
            # Parameters
            d = self.calc_data['wet_conc_density']
            c = self.calc_data['cement_content']
            w = self.calc_data['fw_content']

            self.calc_data['total_agg_content'] = d - c - w

        elif mode == 'PFA':
            # Parameters
            d = self.calc_data['wet_conc_density']
            c_plus_f = self.calc_data['final_cementitious_content']
            w = self.calc_data['fw_content']

            self.calc_data['total_agg_content'] = d - c_plus_f - w

        elif mode == 'GGBS':
            # Parameters
            d = self.calc_data['wet_conc_density']
            c_plus_g = self.calc_data['final_cementitious_content']
            w = self.calc_data['fw_content']

            self.calc_data['total_agg_content'] = d - c_plus_g - w

    def compute_fine_agg_proportion(self, mode: str):
        """
        Determines the fine aggregate proportion from figure 6,
        this is performed by a `FineAggPortioner` class
        :param mode: (str) ['DOE', 'AEM', 'PFA', 'GGBS'] the concrete mix design mode
        """

        if mode == 'DOE' or mode == 'AEM' or mode == 'PFA' or mode == 'GGBS':
            if self.null_check('Additional info', 'Percentage passing 600um sieve'):

                self.calc_data['perc_passing'] = 60

                portioner = FineAggPortioner(
                    self.calc_data['modified_fwc_ratio'],
                    self.calc_data['max_agg_size'],
                    self.data['Specified variables']['Slump'],
                    60
                )

                # Determine the fine aggregate proportion
                portioner.determine_proportion()
                self.calc_data['fine_agg_prop'] = portioner.fine_agg_proportion

                # Keep the class for further use
                self.portioner = portioner

            elif float(self.data['Additional info']['Percentage passing 600um sieve']) > 100:
                # Call an input error
                self.perc_pass_aberration = True

            else:
                perc_passing = float(self.data['Additional info']['Percentage passing 600um sieve'])
                self.calc_data['perc_passing'] = perc_passing

                portioner = FineAggPortioner(
                    self.calc_data['modified_fwc_ratio'],
                    self.calc_data['max_agg_size'],
                    self.data['Specified variables']['Slump'],
                    perc_passing
                )
                # Determine the fine aggregate proportion
                portioner.determine_proportion()
                self.calc_data['fine_agg_prop'] = portioner.fine_agg_proportion

                # Keep the class for further use
                self.portioner = portioner

    def plot_fine_agg_proportion(self):
        """
        Visualizes figure 6
        """
        # Make the visualization
        fig_vi = self.portioner.plot()

        # Save the figure temporarily
        self.fig_vi_png_image = plotly_image_converter(fig_vi)

    def compute_agg_content(self, mode: str):
        """
        Determine the fine and coarse aggregates using the proportion of fine aggregates and the total aggregate content
        :param mode: (str) ['DOE', 'AEM', 'PFA', 'GGBS'] the concrete mix design mode
        """
        if mode == 'DOE' or mode == 'PFA' or mode == 'GGBS':
            # Define parameters
            total_agg_content = self.calc_data['total_agg_content']
            fine_agg_proportion = self.calc_data['fine_agg_prop'] / 100

            # Determine the fine aggregate content
            self.calc_data['calc_fine_agg_content'] = total_agg_content * fine_agg_proportion

            # Determine the coarse aggregate content
            self.calc_data['calc_coarse_agg_content'] = total_agg_content - self.calc_data['calc_fine_agg_content']

        elif mode == 'AEM':
            if self.null_check('Additional info', 'Fine Aggregate Reduction'):
                fagg_reduction = 0
            else:
                fagg_reduction = float(self.data['Additional info']['Fine Aggregate Reduction'])

            # Define parameters
            total_agg_content = self.calc_data['total_agg_content']
            fine_agg_proportion = self.calc_data['fine_agg_prop'] / 100

            # Determine the fine aggregate content
            self.calc_data['calc_fine_agg_content'] = (total_agg_content * fine_agg_proportion) - (
                    fagg_reduction / 100 * total_agg_content)

            # Determine the coarse aggregate content
            self.calc_data['calc_coarse_agg_content'] = total_agg_content - self.calc_data['calc_fine_agg_content']

    def oven_dry_batching(self):
        """
        Obtain masses if the aggregates are to be batched in an oven dry condition
        """
        null_fagg_state = self.null_check('Additional info', 'Absorption of Fine Aggregate')
        null_cagg_state = self.null_check('Additional info', 'Absorption of Coarse Aggregate')

        fagg_content = self.calc_data['calc_fine_agg_content']
        fagg_absorption = self.data['Additional info']['Absorption of Fine Aggregate']
        cagg_content = self.calc_data['calc_coarse_agg_content']
        cagg_absorption = self.data['Additional info']['Absorption of Coarse Aggregate']

        if not null_fagg_state and not null_cagg_state:

            # If both aggregates are to be batched in oven dry conditions
            self.odb_status = 'both aggregates'
            # Mass of oven dry aggregates
            fagg_mass = fagg_content * (100 / (100 + float(fagg_absorption)))
            cagg_mass = cagg_content * (100 / (100 + float(cagg_absorption)))

            self.calc_data['fine_agg_content'] = fagg_mass
            self.calc_data['odb_fine'] = fagg_mass
            self.calc_data['coarse_agg_content'] = cagg_mass
            self.calc_data['odb_coarse'] = cagg_mass

            # Water Required for absorption
            added_h20_mass = (fagg_content - fagg_mass) + (cagg_content - cagg_mass)
            self.calc_data['added_h20_mass'] = added_h20_mass
            self.calc_data['new_fw_content'] = self.calc_data['fw_content'] + added_h20_mass

        elif not null_fagg_state and null_cagg_state:
            # If fine aggregate content will be batched in oven dry condition
            self.odb_status = 'fine aggregate only'
            fagg_mass = fagg_content * (100 / (100 + float(fagg_absorption)))

            # Mass of oven dry fine aggregate
            self.calc_data['fine_agg_content'] = fagg_mass
            self.calc_data['odb_fine'] = fagg_mass
            self.calc_data['coarse_agg_content'] = self.calc_data['calc_coarse_agg_content']
            self.calc_data['odb_coarse'] = 0

            # Water Required for absorption
            added_h20_mass = (fagg_content - fagg_mass)
            self.calc_data['added_h20_mass'] = added_h20_mass
            self.calc_data['new_fw_content'] = self.calc_data['fw_content'] + added_h20_mass

        elif null_fagg_state and not null_cagg_state:
            # If coarse aggregate content will be batched in oven dry condition
            self.odb_status = 'coarse aggregate only'
            cagg_mass = cagg_content * (100 / (100 + float(cagg_absorption)))

            # Mass of oven dry fine aggregate
            self.calc_data['coarse_agg_content'] = cagg_mass
            self.calc_data['odb_coarse'] = cagg_mass
            self.calc_data['fine_agg_content'] = self.calc_data['calc_fine_agg_content']
            self.calc_data['odb_fine'] = 0

            # Water Required for absorption
            added_h20_mass = (cagg_content - cagg_mass)
            self.calc_data['added_h20_mass'] = added_h20_mass
            self.calc_data['new_fw_content'] = self.calc_data['fw_content'] + added_h20_mass

        elif null_fagg_state and null_cagg_state:
            # If the aggregates will not to be batched in oven dry condition
            self.odb_status = 'none'
            self.calc_data['coarse_agg_content'] = self.calc_data['calc_coarse_agg_content']
            self.calc_data['fine_agg_content'] = self.calc_data['calc_fine_agg_content']
            self.calc_data['added_h20_mass'] = 0
            self.calc_data['new_fw_content'] = self.calc_data['fw_content']
            self.calc_data['odb_fine'] = 0
            self.calc_data['odb_coarse'] = 0

    def proportion_coarse_agg(self):
        """
        Determines the proportion of the single sized coarse aggregates used.
        """
        # A guide of 1:2 and 1:1.5:3 will be used for [10,20,0] [10, 0, 40], [0, 20, 40] & [10, 20, 40]
        if self.calc_data['aggregate_sizes'] in [[10, 20, 0], [10, 0, 40], [0, 20, 40], [10, 20, 40]]:

            # Aggregate sizes
            size_10mm, size_20mm, size_40mm = self.calc_data['aggregate_sizes']

            if size_40mm != 0 and size_20mm != 0 and size_10mm != 0:
                # Make proportions on a 10, 20 and 40mm on a 1:1.5:3 ratio
                self.calc_data["proportioned_10mm"] = (1 / 5.5) * self.calc_data['coarse_agg_content']
                self.calc_data["proportioned_20mm"] = (1.5 / 5.5) * self.calc_data['coarse_agg_content']
                self.calc_data["proportioned_40mm"] = (3 / 5.5) * self.calc_data['coarse_agg_content']
                self.calc_data["str_agg_sizes"] = '10mm, 20mm, 40mm'
                self.calc_data['cagg_proportions'] = [self.calc_data['proportioned_10mm'],
                                                      self.calc_data["proportioned_20mm"],
                                                      self.calc_data["proportioned_40mm"]]

            elif size_40mm == 0:
                # Make proportions 10 & 20mm on a 1:2 ratio
                self.calc_data["proportioned_10mm"] = (1 / 3) * self.calc_data['coarse_agg_content']
                self.calc_data["proportioned_20mm"] = (2 / 3) * self.calc_data['coarse_agg_content']
                self.calc_data["proportioned_40mm"] = 0
                self.calc_data['str_agg_sizes'] = '10mm, 20mm'
                self.calc_data['cagg_proportions'] = [self.calc_data['proportioned_10mm'],
                                                      self.calc_data["proportioned_20mm"]]

            elif size_20mm == 0:
                # Make proportions 10 & 40mm on a 1:2 ratio
                self.calc_data["proportioned_10mm"] = (1 / 3) * self.calc_data['coarse_agg_content']
                self.calc_data["proportioned_20mm"] = 0
                self.calc_data["proportioned_40mm"] = (2 / 3) * self.calc_data['coarse_agg_content']
                self.calc_data['str_agg_sizes'] = '10mm, 40mm'
                self.calc_data['cagg_proportions'] = [self.calc_data['proportioned_10mm'],
                                                      self.calc_data["proportioned_40mm"]]
            elif size_10mm == 0:
                # Make proportions 20 & 40mm on a 1:2 ratio
                self.calc_data["proportioned_10mm"] = 0
                self.calc_data["proportioned_20mm"] = (1 / 3) * self.calc_data['coarse_agg_content']
                self.calc_data["proportioned_40mm"] = (2 / 3) * self.calc_data['coarse_agg_content']
                self.calc_data['str_agg_sizes'] = '20mm, 40mm'
                self.calc_data['cagg_proportions'] = [self.calc_data['proportioned_20mm'],
                                                      self.calc_data["proportioned_40mm"]]
        else:
            # Retrieve the only single aggregate size
            single_agg_size = [agg for agg in self.calc_data['aggregate_sizes'] if agg != 0][0]

            self.calc_data['str_agg_sizes'] = f'{single_agg_size}mm'
            self.calc_data['cagg_proportions'] = [self.calc_data['coarse_agg_content']]

    def summarize_results(self, mode: str):
        """
        Summarizes the results into 'self.design_results' for reporting cases.

        :param mode: (str) ['DOE', 'AEM', 'PFA', 'GGBS'] the concrete mix design mode
        """
        # Summarize the design results in self.design_results
        self.design_results = {
            'cement': [np.round(self.calc_data['cement_content'], 2),
                       snap_to_nearest_five(self.calc_data['cement_content'])],
            'water': [np.round(self.calc_data['new_fw_content'], 2),
                      snap_to_nearest_five(self.calc_data['new_fw_content'])],
            'fagg': [np.round(self.calc_data['fine_agg_content'], 2),
                     snap_to_nearest_five(self.calc_data['fine_agg_content'])],
            'cagg': [np.round(self.calc_data['coarse_agg_content'], 2),
                     snap_to_nearest_five(self.calc_data['coarse_agg_content'])],
            'odb_batching': self.odb_status,
            'cagg_sizes': self.calc_data['str_agg_sizes'],
            'cagg_proportioning': [np.round(self.calc_data['cagg_proportions'], 2),
                                   snap_to_nearest_five(self.calc_data['cagg_proportions'])]
        }

        # Pfa & ggbs content in their respective modes
        if mode == 'PFA':
            self.design_results['pfa'] = [np.round(self.calc_data['F'], 2),
                                          snap_to_nearest_five(self.calc_data['F'])]

        elif mode == 'GGBS':
            self.design_results['ggbs'] = [np.round(self.calc_data['G'], 2),
                                           snap_to_nearest_five(self.calc_data['G'])]

    def batch_to_desired_volume(self, mode: str, mix_design_data):
        """
        Converts the quantities required per metre cube to the desired batching volume.
        :param mix_design_data: (dict): Dictionary containing the mix design data tpo be used for batching
        :param mode: (str) ['DOE', 'AEM', 'PFA', 'GGBS'] the concrete mix design mode
        """
        # Retrieve values
        desired_volume = float(self.data['Result Tuning']['Batch volume'])
        desired_unit = self.data['Result Tuning']['Unit']

        if mode == 'DOE' or mode == 'AEM':
            if desired_unit == 'm\u00b3':
                # Define the conversion factor
                conversion_factor = desired_volume

                # Convert from kg/ 1 m3 to kg/ specified m3
                req_keys = ['cement', 'water', 'fagg', 'cagg', 'cagg_proportioning']
                self.design_batch_results = {key: np.round(batch(mix_design_data[key], conversion_factor), 1) for key in
                                             req_keys}

                # Add other properties
                self.design_batch_results['odb_batching'] = mix_design_data['odb_batching']
                self.design_batch_results['cagg_sizes'] = mix_design_data['cagg_sizes']
                self.data['Result Tuning']['md_unit'] = "m<sup>3</sup>"

            elif desired_unit == '\u2113':
                # Define the conversion factor
                conversion_factor = desired_volume * 1e-3

                # Convert from kg/ 1 m3 to kg/ specified litres
                req_keys = ['cement', 'water', 'fagg', 'cagg', 'cagg_proportioning']
                self.design_batch_results = {key: np.round(batch(mix_design_data[key], conversion_factor), 1) for key in
                                             req_keys}

                # Add other properties
                self.design_batch_results['odb_batching'] = mix_design_data['odb_batching']
                self.design_batch_results['cagg_sizes'] = mix_design_data['cagg_sizes']
                self.data['Result Tuning']['md_unit'] = "L"

        elif mode == 'PFA':
            if desired_unit == 'm\u00b3':
                # Define the conversion factor
                conversion_factor = desired_volume

                # Convert from kg/ 1 m3 to kg/ specified m3
                req_keys = ['cement', 'pfa', 'water', 'fagg', 'cagg', 'cagg_proportioning']
                self.design_batch_results = {key: np.round(batch(mix_design_data[key], conversion_factor), 1) for key in
                                             req_keys}

                # Add other properties
                self.design_batch_results['odb_batching'] = mix_design_data['odb_batching']
                self.design_batch_results['cagg_sizes'] = mix_design_data['cagg_sizes']
                self.data['Result Tuning']['md_unit'] = "m<sup>3</sup>"

            elif desired_unit == '\u2113':
                # Define the conversion factor
                conversion_factor = desired_volume * 1e-3

                # Convert from kg/ 1 m3 to kg/ specified litres
                req_keys = ['cement', 'pfa', 'water', 'fagg', 'cagg', 'cagg_proportioning']
                self.design_batch_results = {key: np.round(batch(mix_design_data[key], conversion_factor), 1) for key in
                                             req_keys}

                # Add other properties
                self.design_batch_results['odb_batching'] = mix_design_data['odb_batching']
                self.design_batch_results['cagg_sizes'] = mix_design_data['cagg_sizes']
                self.data['Result Tuning']['md_unit'] = "L"

        elif mode == 'GGBS':
            if desired_unit == 'm\u00b3':
                # Define the conversion factor
                conversion_factor = desired_volume

                # Convert from kg/ 1 m3 to kg/ specified m3
                req_keys = ['cement', 'ggbs', 'water', 'fagg', 'cagg', 'cagg_proportioning']
                self.design_batch_results = {key: np.round(batch(mix_design_data[key], conversion_factor), 1) for key in
                                             req_keys}

                # Add other properties
                self.design_batch_results['odb_batching'] = mix_design_data['odb_batching']
                self.design_batch_results['cagg_sizes'] = mix_design_data['cagg_sizes']
                self.data['Result Tuning']['md_unit'] = "m<sup>3</sup>"

            elif desired_unit == '\u2113':
                # Define the conversion factor
                conversion_factor = desired_volume * 1e-3

                # Convert from kg/ 1 m3 to kg/ specified litres
                req_keys = ['cement', 'ggbs', 'water', 'fagg', 'cagg', 'cagg_proportioning']
                self.design_batch_results = {key: np.round(batch(mix_design_data[key], conversion_factor), 1) for key in
                                             req_keys}

                # Add other properties
                self.design_batch_results['odb_batching'] = mix_design_data['odb_batching']
                self.design_batch_results['cagg_sizes'] = mix_design_data['cagg_sizes']
                self.data['Result Tuning']['md_unit'] = "L"
