"""aem_results.py

This module displays mix design results for every stage in the air entrained
mix design mode

"""

import tkinter as tk

from core.utils.themes import *
from core.utils.file_paths import optimix_paths
from core.logic.helpers.output_helpers import result_preparer, to_xlsx, generate_md_report, to_pdf, to_word, color_entry, \
    entry_check, get_path, load_tk_image


class StageOneResults(tk.Toplevel):
    """
    Top level frame for a summary of stage one's results.

    Attributes:
        - analyzer `MixDesignAnalyzer`: The instantiated class for backend calculations, used here to retrieve results
        - controller `tk.Frame`: Used for accessing the parent frame
        - stage `str`: the current stage, either 'in_progress' or 'final

    Methods:
        - display_scrollbar(): Displays the scrollbar for the TopLevel window
        - display_header(): Display the OptiMix logo, stage & title
        - display_k(status): Displays the results relating to the determination of risk factor, k
        - display_standard_deviation(status): Displays results pertaining to
                                              variability of strength tests and standard deviation selection
        - display_margin(status): Shows the calculations for margin in mix design
        - display_target_mean_strength(status): Shows calculation of the target mean strength
        - display_target_wc_ratio(status): Displays the results for the determination of the water/cement ratio
        - display_results(): Displays all results
        - fix_boundary(): fix scroll boundary in the TopLevel window
    """

    def __init__(self, analyzer, controller, stage):
        # Instantiate the mix design analyzer
        super().__init__(bg=BG, width=793.92, height=630)
        self.analyzer = analyzer
        self.controller = controller
        self.stage = stage

        # Window settings
        self.title("OptiMix: Stage One Design Results (Air-entrained Concrete Mix)")  # window title
        self.iconbitmap(optimix_paths.icons['icon_16'])  # window icon
        self.resizable(False, True)

        # Create the base canvas
        self.base_canvas = tk.Canvas(
            self,
            bg=BG,
            width=793.92,
            height=630,
            highlightthickness=0
        )
        # Place the base canvas
        self.base_canvas.place(x=0, y=0)
        self.base_canvas.pack(expand=True, fill="both")

        # Display the scrollbar
        self.display_scrollbar()

        # Display the header
        self.display_header()

        # Display the results
        self.display_results()

        # Fix scroll boundary in the top level widget
        self.fix_boundary()

    def display_scrollbar(self):
        """
        Displays the scroll bar by the right side of the new TopLevel for canvas, or any other type of widget
        """
        # Setup mousewheel scrolling
        self.base_canvas.bind(
            '<MouseWheel>',
            lambda event: self.base_canvas.yview_scroll(
                -int(event.delta / 50),
                "units")
        )

        # Make the scroll bar
        scrollbar = tk.Scrollbar(
            master=self,
            orient="vertical",
            cursor='hand2',
            command=self.base_canvas.yview
        )
        self.base_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")

    def display_header(self):
        """
        Displays then header,
        > title,
        > stage,
        > optimix logo
        > Air Entrained Mix Design
        """
        # Display the current stage
        result_stage_i = load_tk_image(optimix_paths.doe_assets['report_stage_i'])
        self.base_canvas.rsi = result_stage_i
        self.base_canvas.create_image(
            101.0,
            96.0,
            image=result_stage_i
        )

        # Display the title "Mix Design results"
        result_title_si = load_tk_image(optimix_paths.doe_assets['report_title'])
        self.base_canvas.rtsi = result_title_si
        self.base_canvas.create_image(
            146.0,
            58.0,
            image=result_title_si,
        )

        # Display the optimix logo
        result_logo = load_tk_image(optimix_paths.doe_assets['report_logo'])
        self.base_canvas.result_logo = result_logo
        self.base_canvas.create_image(
            655.0,
            66.0,
            image=result_logo
        )

        # Display text 'Air entrained mix design'
        self.base_canvas.create_text(628,
                                     102,
                                     fill=white_color,
                                     font=tk.font.Font(family=calibri, size=13, weight='bold'),
                                     text="(Air-entrained Concrete Mix)")

    def display_k(self, status: dict):
        """
        Displays the following where k is to be determined:
        > A background rectangle
        > tab's label ('The Determination of Risk Factor, k)'
        > The defective rate
        > The plot
        > The result

        Displays the following when k is specified:
        > A background rectangle
        > tab's label ('The Determination of Risk Factor, k)'
        > The specified risk factor k
        :param status: (dict): Dictionary class containing current state before displaying report

        Note that a specified margin overrides the need for a determined or specified k,
        hence the margin's case will not be addressed in this function
        """
        if status['k'] == 'Specified':
            # Extract the specified risk factor, k
            k = f"{np.round(self.analyzer.calc_data['k'], 2)}"

            # Display the report tab
            rec_iii = load_tk_image(optimix_paths.doe_assets['report_rectangles'][2])
            self.base_canvas.rec_iii = rec_iii
            self.base_canvas.create_image(
                390.00000762939453,
                270.99998474121094,
                image=rec_iii
            )

            # Show the tab's title "Specified Risk Factor, k"
            self.base_canvas.create_text(210,
                                         210,
                                         fill=white_color,
                                         activefill=np.random.choice(report_title_colors),
                                         font=tk.font.Font(family=helvetica, size=17, weight='bold'),
                                         text="Specified Risk Factor, k")

            # Display the risk factor
            self.base_canvas.create_text(81,
                                         220,
                                         fill=white_color,
                                         anchor='nw',
                                         font=tk.font.Font(family=cambria_math, size=13, slant='roman'),
                                         text=f"Risk factor, k = {k}")

        elif status['k'] == 'To be Determined':
            # Display the report tab
            rec_ii = load_tk_image(optimix_paths.doe_assets['report_rectangles'][1])
            self.base_canvas.rec_ii = rec_ii
            self.base_canvas.create_image(
                390.00000762939453,
                380.99998474121094,
                image=rec_ii
            )

            # Show the tab's title "The Determination of Risk Factor, k"
            self.base_canvas.create_text(275.5,
                                         195,
                                         fill=white_color,
                                         activefill=np.random.choice(report_title_colors),
                                         font=tk.font.Font(family=helvetica, size=17, weight='bold'),
                                         text="The Determination of Risk Factor, k")

            perc_def = np.round(self.analyzer.calc_data['perc_def'], 2)
            k = np.round(float(self.analyzer.calc_data['k']), 2)
            k_text = f"This normal distribution curve shows how a defective rate of {perc_def}% leads to k,\n" \
                     f"a risk factor (z-score) of {k}."
            self.base_canvas.create_text(82,
                                         215,
                                         fill=white_color,
                                         anchor='nw',
                                         font=tk.font.Font(family=calibri, size=11),
                                         text=k_text)

            # Place the visualization
            fig_i = self.analyzer.fig_i_png_image
            self.base_canvas.fig_i = fig_i
            self.base_canvas.create_image(
                390.00000762939453,
                410.99998474121094,
                image=fig_i,
            )
        else:
            pass

    def display_standard_deviation(self, status: dict):
        """
        Variability of strength tests and standard deviation selection
        Displays the following:
        > The report tab,
        > The title,
        > Previous results
        > The graph,
        > The standard deviation,
        :param status: Dictionary class containing current state before displaying report

        Also note that a specified margin overrides the need for a determined or specified standard deviation,
        hence the margin's case will not be addressed in this function.
        """
        if status['k'] == 'To be Determined':
            if status['sd'] == 'Specified':
                # Display the report tab
                rec_vi = load_tk_image(optimix_paths.doe_assets['report_rectangles'][5])
                self.base_canvas.rec_iv = rec_vi
                self.base_canvas.create_image(
                    390.00000762939453,
                    900.99998474121094,
                    image=rec_vi
                )

                # Show the tab's title, "Standard Deviation Selection for Strength Tests"
                self.base_canvas.create_text(320,
                                             678,
                                             fill=white_color,
                                             activefill=np.random.choice(report_title_colors),
                                             font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                             text="Standard Deviation Selection for Strength Tests")

                if self.analyzer.data['Specified variables']['Less Than 20 Results'] == 1:
                    variability_in_prev_result = f"According to specified inputs, previous information concerning the \n" \
                                                 f"variability of strength tests comprises fewer than 20 results🧪.\n"
                else:
                    variability_in_prev_result = f"According to specified inputs, previous information concerning the \n" \
                                                 f"variability of strength tests comprises more than 20 results🧪.\n"

                self.base_canvas.create_text(95,
                                             700,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=variability_in_prev_result)

                # Plot insights
                obtained_sd = np.round(self.analyzer.calc_data['sd'], 2)
                specified_sd = np.round(self.analyzer.calc_data['specified sd'], 2)

                if self.analyzer.innaprop_spec_sd:
                    # If the specified standard deviation is less than the appropriate value obtained
                    plot_insight = f"The obtained standard deviation of {obtained_sd} N/mm\u00b2 will be used, \n" \
                                   f"as it exceeds the specified {specified_sd} N/mm\u00b2"

                    # placement
                    y_coord, y_graph_coord = [1100.00, 913.99998474121094]

                else:
                    # If the specified standard deviation is not less than the obtained sd, which is fine
                    plot_insight = f"The specified standard deviation of {specified_sd} N/mm\u00b2 will be used."

                    # placement
                    y_coord, y_graph_coord = [1110.00, 917.99998474121094]

                self.base_canvas.create_text(95,
                                             y_coord,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=plot_insight)

                # Place the visualization
                fig_iii = self.analyzer.fig_iii_png_image
                self.base_canvas.fig_iii = fig_iii
                self.base_canvas.create_image(
                    395.00000762939453,
                    y_graph_coord,
                    image=fig_iii,
                )

            elif status['sd'] == 'To be Determined':
                # Display the report tab
                rec_vi = load_tk_image(optimix_paths.doe_assets['report_rectangles'][5])
                self.base_canvas.rec_vi = rec_vi
                self.base_canvas.create_image(
                    390.00000762939453,
                    900.99998474121094,
                    image=rec_vi
                )

                # Show the tab's title, "Standard Deviation Selection for Strength Tests"
                self.base_canvas.create_text(320,
                                             678,
                                             fill=white_color,
                                             activefill=np.random.choice(report_title_colors),
                                             font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                             text="Standard Deviation Selection for Strength Tests")

                if self.analyzer.data['Specified variables']['Less Than 20 Results'] == 1:
                    variability_in_prev_result = f"According to specified inputs, previous information concerning the \n" \
                                                 f"variability of strength tests comprises fewer than 20 results🧪.\n"
                else:
                    variability_in_prev_result = f"According to specified inputs, previous information concerning the \n" \
                                                 f"variability of strength tests comprises more than 20 results🧪.\n"

                self.base_canvas.create_text(95,
                                             700,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=variability_in_prev_result)

                # Place the visualization
                fig_iii = self.analyzer.fig_iii_png_image
                self.base_canvas.fig_iii = fig_iii
                self.base_canvas.create_image(
                    395.00000762939453,
                    917.99998474121094,
                    image=fig_iii,
                )

                # Plot insights
                sd = np.round(self.analyzer.calc_data['sd'], 2)
                plot_insight = f'The standard deviation obtained is {sd} N/mm\u00b2'
                self.base_canvas.create_text(95,
                                             1110,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=13),
                                             text=plot_insight)

        elif status['k'] == 'Specified':
            if status['sd'] == 'Specified':
                # Display the report tab
                rec_vi = load_tk_image(optimix_paths.doe_assets['report_rectangles'][5])
                self.base_canvas.rec_iv = rec_vi
                self.base_canvas.create_image(
                    390.00000762939453,
                    670.99998474121094,
                    image=rec_vi
                )

                # Show the tab's title, "Standard Deviation Selection for Strength Tests"
                self.base_canvas.create_text(320,
                                             448,
                                             fill=white_color,
                                             activefill=np.random.choice(report_title_colors),
                                             font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                             text="Standard Deviation Selection for Strength Tests")

                if self.analyzer.data['Specified variables']['Less Than 20 Results'] == 1:
                    variability_in_prev_result = f"According to specified inputs, previous information concerning the \n" \
                                                 f"variability of strength tests comprises fewer than 20 results🧪.\n"
                else:
                    variability_in_prev_result = f"According to specified inputs, previous information concerning the \n" \
                                                 f"variability of strength tests comprises more than 20 results🧪.\n"

                self.base_canvas.create_text(95,
                                             470,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=variability_in_prev_result)

                # Plot insights
                obtained_sd = np.round(self.analyzer.calc_data['sd'], 2)
                specified_sd = np.round(self.analyzer.calc_data['specified sd'], 2)

                if self.analyzer.innaprop_spec_sd:
                    # If the specified standard deviation is less than the appropriate value obtained
                    plot_insight = f"The obtained standard deviation of {obtained_sd} N/mm\u00b2 will be used, \n" \
                                   f"as it exceeds the specified {specified_sd} N/mm\u00b2"

                    # placement
                    y_coord, y_graph_coord = [870.00, 683.99998474121094]

                else:
                    # If the specified standard deviation is not less than the obtained sd, which is fine
                    plot_insight = f"The specified standard deviation of {specified_sd} N/mm\u00b2 will be used."

                    # placement
                    y_coord, y_graph_coord = [874.00, 687.99998474121094]

                self.base_canvas.create_text(95,
                                             y_coord,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=plot_insight)

                # Place the visualization
                fig_iii = self.analyzer.fig_iii_png_image
                self.base_canvas.fig_iii = fig_iii
                self.base_canvas.create_image(
                    395.00000762939453,
                    y_graph_coord,
                    image=fig_iii,
                )

            elif status['sd'] == 'To be Determined':
                # Display the report tab
                rec_vi = load_tk_image(optimix_paths.doe_assets['report_rectangles'][5])
                self.base_canvas.rec_iv = rec_vi
                self.base_canvas.create_image(
                    390.00000762939453,
                    670.99998474121094,
                    image=rec_vi
                )

                # Show the tab's title, "Standard Deviation Selection for Strength Tests"
                self.base_canvas.create_text(320,
                                             448,
                                             fill=white_color,
                                             activefill=np.random.choice(report_title_colors),
                                             font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                             text="Standard Deviation Selection for Strength Tests")

                if self.analyzer.data['Specified variables']['Less Than 20 Results'] == 1:
                    variability_in_prev_result = f"According to specified inputs, previous information concerning the \n" \
                                                 f"variability of strength tests comprises fewer than 20 results🧪.\n"
                else:
                    variability_in_prev_result = f"According to specified inputs, previous information concerning the \n" \
                                                 f"variability of strength tests comprises more than 20 results🧪.\n"

                self.base_canvas.create_text(95,
                                             470,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=variability_in_prev_result)

                # Place the visualization
                fig_iii = self.analyzer.fig_iii_png_image
                self.base_canvas.fig_iii = fig_iii
                self.base_canvas.create_image(
                    395.00000762939453,
                    687.99998474121094,
                    image=fig_iii,
                )

                # Plot insights
                sd = np.round(self.analyzer.calc_data['sd'], 2)
                plot_insight = f'The standard deviation obtained is {sd} N/mm\u00b2'
                self.base_canvas.create_text(95,
                                             880,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=13),
                                             text=plot_insight)

    def display_margin(self, status: dict):
        """
        Displays the following:
        - The dashboard tab
        - The title 'Margin for mix Design'
        - The parameters (k and sd)
        - Calculations and the final results
        :param status: Dictionary class containing current state before displaying report
        """
        if status['Margin'] == 'To be Determined':
            if status['k'] == 'To be Determined':
                # Display the report tab
                rec_ii_m = load_tk_image(optimix_paths.doe_assets['report_rectangles'][2])
                self.base_canvas.rec_ii_m = rec_ii_m
                self.base_canvas.create_image(
                    390.00000762939453,
                    1300.99998474121094,
                    image=rec_ii_m
                )

                # Show the tab's title, "Margin for Mix Design"
                self.base_canvas.create_text(195,
                                             1232,
                                             fill=white_color,
                                             activefill=np.random.choice(report_title_colors),
                                             font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                             text="Margin for Mix Design")

                # Statement of the parameters
                k = np.round(self.analyzer.calc_data['k'], 2)
                sd = np.round(self.analyzer.calc_data['sd'], 2)
                parameters_text = f"Considering the risk factor (k) of {k} and the standard deviation (s) of {sd} N/mm\u00b2,\n" \
                                  f"the Margin (M) is determined as follows:\n"
                self.base_canvas.create_text(90,
                                             1260,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=parameters_text)

                # The equation
                margin_equation = f"M = k × s"
                self.base_canvas.create_text(90,
                                             1279,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=cambria_math, size=12, slant='italic'),
                                             text=margin_equation)

                # Result and insight
                margin_val = np.round(float(self.analyzer.calc_data['margin']), 2)
                margin_result = f"Margin, M = {k} × {sd}, resulting in a {margin_val} N/mm\u00b2 strength increase."

                self.base_canvas.create_text(90,
                                             1355,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=margin_result)
            elif status['k'] == 'Specified':
                # Display the report tab
                rec_ii_m = load_tk_image(optimix_paths.doe_assets['report_rectangles'][2])
                self.base_canvas.rec_ii_m = rec_ii_m
                self.base_canvas.create_image(
                    390.00000762939453,
                    1070.99998474121094,
                    image=rec_ii_m
                )

                # Show the tab's title, "Margin for Mix Design"
                self.base_canvas.create_text(195,
                                             1002,
                                             fill=white_color,
                                             activefill=np.random.choice(report_title_colors),
                                             font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                             text="Margin for Mix Design")

                # Statement of the parameters
                k = np.round(self.analyzer.calc_data['k'], 2)
                sd = np.round(self.analyzer.calc_data['sd'], 2)
                parameters_text = f"Considering the risk factor (k) of {k} and the standard deviation (s) of {sd} N/mm\u00b2,\n" \
                                  f"the Margin (M) is determined as follows:\n"
                self.base_canvas.create_text(90,
                                             1030,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=parameters_text)

                # The equation
                margin_equation = f"M = k × s"
                self.base_canvas.create_text(90,
                                             1049,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=cambria_math, size=12, slant='italic'),
                                             text=margin_equation)

                # Result and insight
                margin_val = np.round(float(self.analyzer.calc_data['margin']), 2)
                margin_result = f"Margin, M = {k} × {sd}, resulting in a {margin_val} N/mm\u00b2 strength increase."

                self.base_canvas.create_text(90,
                                             1125,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=margin_result)
        elif status['Margin'] == 'Specified':
            # Display the report tab
            rec_ii_m = load_tk_image(optimix_paths.doe_assets['report_rectangles'][2])
            self.base_canvas.rec_ii_m = rec_ii_m
            self.base_canvas.create_image(
                390.00000762939453,
                270.99998474121094,
                image=rec_ii_m)

            # Show the tab's title, "Margin for Mix Design"
            self.base_canvas.create_text(195,
                                         225,
                                         fill=white_color,
                                         activefill=np.random.choice(report_title_colors),
                                         font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                         text="Margin for Mix Design")

            # Report content
            margin_val = np.round(float(self.analyzer.calc_data['margin']), 2)
            margin_report = f"The specified increase in characteristic concrete strength is {margin_val} N/mm\u00b2.\n" \
                            f"This margin will be used subsequently in the design of the air-entrained concrete mix.\n"

            self.base_canvas.create_text(90,
                                         270,
                                         fill=white_color,
                                         anchor='nw',
                                         font=tk.font.Font(family=calibri, size=13),
                                         text=margin_report)

    def display_target_mean_strength(self, status: dict):
        """
        Displays the calculation of the target mean strength.
        GUI objects:
        - Title
        - Parameter statement
        - Formula Statement
        - Final result
        :param status: Dictionary class containing current state before displaying report
        """
        if status['Margin'] == 'To be Determined':
            if status['k'] == 'To be Determined':
                # Display the report tab
                rec_ii_fm = load_tk_image(optimix_paths.doe_assets['report_rectangles'][2])
                self.base_canvas.rec_ii_fm = rec_ii_fm
                self.base_canvas.create_image(
                    390.00000762939453,
                    1550.99998474121094,
                    image=rec_ii_fm
                )

                # Show the tab's title, "The Calculation of Target Mean Strength"
                self.base_canvas.create_text(280,
                                             1478,
                                             fill=white_color,
                                             activefill=np.random.choice(report_title_colors),
                                             font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                             text="The Calculation of Target Mean Strength")

                # Statement of the parameters
                fc = np.round(float(self.analyzer.data['Specified variables']['Characteristic Strength']), 2)
                m = np.round(self.analyzer.calc_data['margin'], 2)
                a = np.round(float(self.analyzer.data['Specified variables']['Air Content']), 2)
                loss = np.round(float(self.analyzer.data['Specified variables']['Strength Loss']), 2)

                parameters_text = f"The determination of the target mean strength (f\u2098) involves considering the specified\n" \
                                  f"characteristic strength (f\u05A4) of {fc} N/mm\u00b2, a margin (M) of {m} N/mm,\u00b2\n" \
                                  f"an air content (a) of {a}% in the air entrained mix, and a loss in compressive strength of {loss}%\n" \
                                  f"by volume of air entrained in the mix. The appropriate target mean strength is given by:"
                self.base_canvas.create_text(90,
                                             1505,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=parameters_text)

                # The equation
                fm_equation = f"f\u2098 = (f\u05A4 + M) / (1 - (loss% × a))"
                self.base_canvas.create_text(90,
                                             1549,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=cambria_math, size=12, slant='italic'),
                                             text=fm_equation)

                # Result and insight
                fm_val = np.round(float(self.analyzer.calc_data['fm']), 2)
                fm_result = f"Target mean strength, f\u2098 = {fm_val} N/mm\u00b2 ({fc} + {m} / 1 - {loss} × {a})."

                self.base_canvas.create_text(90,
                                             1609,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=fm_result)

            elif status['k'] == 'Specified':
                # Display the report tab
                rec_ii_fm = load_tk_image(optimix_paths.doe_assets['report_rectangles'][2])
                self.base_canvas.rec_ii_fm = rec_ii_fm
                self.base_canvas.create_image(
                    390.00000762939453,
                    1320.99998474121094,
                    image=rec_ii_fm
                )

                # Show the tab's title, "Margin for Mix Design"
                self.base_canvas.create_text(280,
                                             1247,
                                             fill=white_color,
                                             activefill=np.random.choice(report_title_colors),
                                             font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                             text="The Calculation of Target Mean Strength")

                # Statement of the parameters
                fc = np.round(float(self.analyzer.data['Specified variables']['Characteristic Strength']), 2)
                m = np.round(self.analyzer.calc_data['margin'], 2)
                a = np.round(float(self.analyzer.data['Specified variables']['Air Content']), 2)
                loss = np.round(float(self.analyzer.data['Specified variables']['Strength Loss']), 2)

                parameters_text = f"The determination of the target mean strength (f\u2098) involves considering the specified\n" \
                                  f"characteristic strength (f\u05A4) of {fc} N/mm\u00b2, a margin (M) of {m} N/mm,\u00b2\n" \
                                  f"an air content (a) of {a}% in the air entrained mix, and a loss in compressive strength of {loss}%\n" \
                                  f"by volume of air entrained in the mix. The appropriate target mean strength is given by:"
                self.base_canvas.create_text(90,
                                             1275,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=parameters_text)

                # The equation
                fm_equation = f"f\u2098 = (f\u05A4 + M) / (1 - (loss% × a))"
                self.base_canvas.create_text(90,
                                             1320,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=cambria_math, size=12, slant='italic'),
                                             text=fm_equation)

                # Result and insight
                fm_val = np.round(float(self.analyzer.calc_data['fm']), 2)
                fm_result = f"Target mean strength, f\u2098 = {fm_val} N/mm\u00b2 ({fc} + {m} / 1 - {loss}% × {a})."

                self.base_canvas.create_text(90,
                                             1379,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=fm_result)
        elif status['Margin'] == 'Specified':
            # Display the report tab
            rec_ii_fm = load_tk_image(optimix_paths.doe_assets['report_rectangles'][2])
            self.base_canvas.rec_ii_fm = rec_ii_fm
            self.base_canvas.create_image(
                390.00000762939453,
                520.99998474121094,
                image=rec_ii_fm
            )

            # Show the tab's title, "Margin for Mix Design"
            self.base_canvas.create_text(280,
                                         447,
                                         fill=white_color,
                                         activefill=np.random.choice(report_title_colors),
                                         font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                         text="The Calculation of Target Mean Strength")

            # Statement of the parameters
            fc = np.round(float(self.analyzer.data['Specified variables']['Characteristic Strength']), 2)
            m = np.round(self.analyzer.calc_data['margin'], 2)
            a = np.round(float(self.analyzer.data['Specified variables']['Air Content']), 2)
            loss = np.round(float(self.analyzer.data['Specified variables']['Strength Loss']), 2)

            parameters_text = f"The determination of the target mean strength (f\u2098) involves considering the specified\n" \
                              f"characteristic strength (f\u05A4) of {fc} N/mm\u00b2, a margin (M) of {m} N/mm,\u00b2\n" \
                              f"an air content (a) of {a}% in the air entrained mix, and a loss in compressive strength of {loss}%\n" \
                              f"by volume of air entrained in the mix. The appropriate target mean strength is given by:"
            self.base_canvas.create_text(90,
                                         471,
                                         fill=white_color,
                                         anchor='nw',
                                         font=tk.font.Font(family=calibri, size=12),
                                         text=parameters_text)

            # The equation
            fm_equation = f"f\u2098 = (f\u05A4 + M) / (1 - (loss% × a))"
            self.base_canvas.create_text(90,
                                         518,
                                         fill=white_color,
                                         anchor='nw',
                                         font=tk.font.Font(family=cambria_math, size=12, slant='italic'),
                                         text=fm_equation)

            # Result and insight
            fm_val = np.round(float(self.analyzer.calc_data['fm']), 2)
            fm_result = f"Target mean strength, f\u2098 = {fm_val} N/mm\u00b2 ({fc} + {m} / 1 - {loss}% × {a})."

            self.base_canvas.create_text(90,
                                         579,
                                         fill=white_color,
                                         anchor='nw',
                                         font=tk.font.Font(family=calibri, size=12),
                                         text=fm_result)

    def display_target_wc_ratio(self, status: dict):
        """
        Display the following:
        - Background tab
        - Parameters for using "Table 2"
        - Table 2, Approximate compressive strengths of concrete mixes made with a free wc_ratio of 0.5
        - The determined approximate compressive strength
        - Parameter text,
        - Relationship between compressive strength and free wc_ratio
        - Insight and comparison to a specified maximum
        :param status: Dictionary class containing current state before displaying report
        """
        if status['Margin'] == 'To be Determined':
            if status['k'] == 'To be Determined':
                # Display the report background tab
                rec_v = load_tk_image(optimix_paths.doe_assets['report_rectangles'][4])
                self.base_canvas.rec_v = rec_v
                self.base_canvas.create_image(
                    390.00000762939453,
                    2145.99998474121094,
                    image=rec_v
                )

                # Show the tab's title, "Selection of water to cement ratio"
                self.base_canvas.create_text(280,
                                             1747,
                                             fill=white_color,
                                             activefill=np.random.choice(report_title_colors),
                                             font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                             text="Selection of Target Water/Cement Ratio")

                # Place table 2, approx compressive strength for a wc_ratio of 0.5
                tab_ii = load_tk_image(optimix_paths.doe_assets['table_ii_reporting'])
                self.base_canvas.tab_ii_rep = tab_ii
                self.base_canvas.create_image(
                    387.00000762939453,
                    1890.99998474121094,
                    image=tab_ii
                )

                # Statement of the parameters
                approx = np.round(float(self.analyzer.calc_data['approx_strength']), 2)
                age = self.analyzer.data['Specified variables']['Curing Days']
                cement_type = self.analyzer.data['Specified variables']['Cement Type']
                cagg_type = self.analyzer.data['Additional info']['Coarse Aggregate Type']
                cagg_type = cagg_type[0].lower() + cagg_type[1:]

                full_name = {
                    'OPC': 'Ordinary Portland cement',
                    'SRPC': 'Sulfate-resisting Portland cement',
                    'RHPC': 'Rapid Hardening Portland cement'
                }

                strength_class = {
                    'OPC': 42.5,
                    'SRPC': 42.5,
                    'RHPC': 52.5
                }
                table_ii_insight = f"A strength value of {approx} N/mm\u00b2 was obtained using {age}-day curing,\n" \
                                   f"{full_name[cement_type]} ({cement_type}) strength class {strength_class[cement_type]} and {cagg_type} aggregate.\n"
                self.base_canvas.create_text(89,
                                             2020,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=table_ii_insight)

                # Free-water/cement ratio intro
                fm_val = np.round(float(self.analyzer.calc_data['fm']), 2)
                fwc_ratio_intro = f"To determine the free-water/cement ratio, the approximate strength of {approx} N/mm\u00b2 \n" \
                                  f"and the target mean strength of {fm_val} N/mm\u00b2 are used in the plot below:"

                self.base_canvas.create_text(89,
                                             2092,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=fwc_ratio_intro)

                # Place the visualization
                fig_iv_plot = self.analyzer.fig_iv_png_image
                self.base_canvas.fig_iv = fig_iv_plot
                self.base_canvas.create_image(
                    395.00000762939453,
                    2295.99998474121094,
                    image=fig_iv_plot,
                )

                # Display the final water to cement ratio for the mix
                if not self.analyzer.fwc_is_larger:
                    final_wc_message = f"The required free-water/cement ratio of this concrete mix is {np.round(self.analyzer.calc_data['fwc_ratio'], 2)}."
                    y_coord = 2525
                else:
                    final_wc_message = f"The plot indicates a free-water/cement ratio from the plot above is {np.round(self.analyzer.calc_data['initial_fwc_ratio'], 2)}, \n" \
                                       f"this exceeds the specified maximum of {np.round(float(self.analyzer.data['Specified variables']['Maximum free water-cement ratio']), 2)} for this mix. \n" \
                                       f"Consequently, the required free-water/cement ratio for this concrete mix is {np.round(float(self.analyzer.calc_data['fwc_ratio']), 2)}."
                    y_coord = 2508

                self.base_canvas.create_text(89,
                                             y_coord,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=final_wc_message)

            elif status['k'] == 'Specified':
                # Display the report background tab
                rec_v = load_tk_image(optimix_paths.doe_assets['report_rectangles'][4])
                self.base_canvas.rec_v = rec_v
                self.base_canvas.create_image(
                    390.00000762939453,
                    1915.99998474121094,
                    image=rec_v
                )

                # Show the tab's title, "Selection of water to cement ratio"
                self.base_canvas.create_text(280,
                                             1517,
                                             fill=white_color,
                                             activefill=np.random.choice(report_title_colors),
                                             font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                             text="Selection of Target Water/Cement Ratio")

                # Place table 2, approx compressive strength for a wc_ratio of 0.5
                tab_ii = load_tk_image(optimix_paths.doe_assets['table_ii_reporting'])
                self.base_canvas.tab_ii_rep = tab_ii
                self.base_canvas.create_image(
                    387.00000762939453,
                    1660.99998474121094,
                    image=tab_ii
                )

                # Statement of the parameters
                approx = np.round(float(self.analyzer.calc_data['approx_strength']), 2)
                age = self.analyzer.data['Specified variables']['Curing Days']
                cement_type = self.analyzer.data['Specified variables']['Cement Type']
                cagg_type = self.analyzer.data['Additional info']['Coarse Aggregate Type']
                cagg_type = cagg_type[0].lower() + cagg_type[1:]

                full_name = {
                    'OPC': 'Ordinary Portland cement',
                    'SRPC': 'Sulfate-resisting Portland cement',
                    'RHPC': 'Rapid Hardening Portland cement'
                }

                strength_class = {
                    'OPC': 42.5,
                    'SRPC': 42.5,
                    'RHPC': 52.5
                }
                table_ii_insight = f"A strength value of {approx} N/mm\u00b2 was obtained using {age}-day curing,\n" \
                                   f"{full_name[cement_type]} ({cement_type}) strength class {strength_class[cement_type]} and {cagg_type} aggregate.\n"
                self.base_canvas.create_text(89,
                                             1790,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=table_ii_insight)

                # Free-water/cement ratio intro
                fm_val = np.round(float(self.analyzer.calc_data['fm']), 2)
                fwc_ratio_intro = f"To determine the free-water/cement ratio, the approximate strength of {approx} N/mm\u00b2 \n" \
                                  f"and the target mean strength of {fm_val} N/mm\u00b2 are used in the plot below:"

                self.base_canvas.create_text(89,
                                             1862,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=fwc_ratio_intro)

                # Place the visualization
                fig_iv_plot = self.analyzer.fig_iv_png_image
                self.base_canvas.fig_iv = fig_iv_plot
                self.base_canvas.create_image(
                    395.00000762939453,
                    2065.99998474121094,
                    image=fig_iv_plot,
                )

                # Display the final water to cement ratio for the mix
                if not self.analyzer.fwc_is_larger:
                    final_wc_message = f"The required free-water/cement ratio of this concrete mix is {np.round(self.analyzer.calc_data['fwc_ratio'], 2)}."
                    y_coord = 2295
                else:
                    final_wc_message = f"The plot indicates a free-water/cement ratio from the plot above is {np.round(self.analyzer.calc_data['initial_fwc_ratio'], 2)}, \n" \
                                       f"this exceeds the specified maximum of {np.round(float(self.analyzer.data['Specified variables']['Maximum free water-cement ratio']), 2)} for this mix. \n" \
                                       f"Consequently, the required free-water/cement ratio for this concrete mix is {np.round(float(self.analyzer.calc_data['fwc_ratio']), 2)}."
                    y_coord = 2278

                self.base_canvas.create_text(89,
                                             y_coord,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=12),
                                             text=final_wc_message)

        elif status['Margin'] == 'Specified':
            # Display the report background tab
            rec_v = load_tk_image(optimix_paths.doe_assets['report_rectangles'][4])
            self.base_canvas.rec_v = rec_v
            self.base_canvas.create_image(
                390.00000762939453,
                1115.99998474121094,
                image=rec_v
            )

            # Show the tab's title, "Selection of water to cement ratio"
            self.base_canvas.create_text(280,
                                         717,
                                         fill=white_color,
                                         activefill=np.random.choice(report_title_colors),
                                         font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                         text="Selection of Target Water/Cement Ratio")

            # Place table 2, approx compressive strength for a wc_ratio of 0.5
            tab_ii = load_tk_image(optimix_paths.doe_assets['table_ii_reporting'])
            self.base_canvas.tab_ii_rep = tab_ii
            self.base_canvas.create_image(
                387.00000762939453,
                860.99998474121094,
                image=tab_ii
            )

            # Statement of the parameters
            approx = np.round(float(self.analyzer.calc_data['approx_strength']), 2)
            age = self.analyzer.data['Specified variables']['Curing Days']
            cement_type = self.analyzer.data['Specified variables']['Cement Type']
            cagg_type = self.analyzer.data['Additional info']['Coarse Aggregate Type']
            cagg_type = cagg_type[0].lower() + cagg_type[1:]

            full_name = {
                'OPC': 'Ordinary Portland cement',
                'SRPC': 'Sulfate-resisting Portland cement',
                'RHPC': 'Rapid Hardening Portland cement'
            }

            strength_class = {
                'OPC': 42.5,
                'SRPC': 42.5,
                'RHPC': 52.5
            }
            table_ii_insight = f"A strength value of {approx} N/mm\u00b2 was obtained using {age}-day curing,\n" \
                               f"{full_name[cement_type]} ({cement_type}) strength class {strength_class[cement_type]} and {cagg_type} aggregate.\n"
            self.base_canvas.create_text(89,
                                         990,
                                         fill=white_color,
                                         anchor='nw',
                                         font=tk.font.Font(family=calibri, size=12),
                                         text=table_ii_insight)

            # Free-water/cement ratio intro
            fm_val = np.round(float(self.analyzer.calc_data['fm']), 2)
            fwc_ratio_intro = f"To determine the free-water/cement ratio, the approximate strength of {approx} N/mm\u00b2 \n" \
                              f"and the target mean strength of {fm_val} N/mm\u00b2 are used in the plot below:"

            self.base_canvas.create_text(89,
                                         1062,
                                         fill=white_color,
                                         anchor='nw',
                                         font=tk.font.Font(family=calibri, size=12),
                                         text=fwc_ratio_intro)

            # Place the visualization
            fig_iv_plot = self.analyzer.fig_iv_png_image
            self.base_canvas.fig_iv = fig_iv_plot
            self.base_canvas.create_image(
                395.00000762939453,
                1265.99998474121094,
                image=fig_iv_plot,
            )

            # Display the final water to cement ratio for the mix
            if not self.analyzer.fwc_is_larger:
                final_wc_message = f"The required free-water/cement ratio of this concrete mix is {np.round(self.analyzer.calc_data['fwc_ratio'], 2)}."
                y_coord = 1495
            else:
                final_wc_message = f"The plot indicates a free-water/cement ratio from the plot above is {np.round(self.analyzer.calc_data['initial_fwc_ratio'], 2)}, \n" \
                                   f"this exceeds the specified maximum of {np.round(float(self.analyzer.data['Specified variables']['Maximum free water-cement ratio']), 2)} for this mix. \n" \
                                   f"Consequently, the required free-water/cement ratio for this concrete mix is {np.round(float(self.analyzer.calc_data['fwc_ratio']), 2)}."
                y_coord = 1478

            self.base_canvas.create_text(89,
                                         y_coord,
                                         fill=white_color,
                                         anchor='nw',
                                         font=tk.font.Font(family=calibri, size=12),
                                         text=final_wc_message)

    def display_results(self):
        """
        Serial arrangement of previously defined class methods for displaying the results namely,
        - Margin:
            When margin is to be determined by the software, display the following:
                - risk factor k, (determined or specified)
                - standard deviation, (determined or specified)
            When margin is specified by the user, simply display the specified margin.
        - Target mean strength
        - Water to cement ratio
        """
        # Main Branch I: Calculation of margin
        # Display format when margin is to be determined
        if self.analyzer.null_check('Specified variables', 'Specified Margin'):

            if self.analyzer.calculated_k:
                # Generate the plot for the determination of risk factor
                self.analyzer.plot_k()

                # Generate current status
                current_status = {
                    'Margin': 'To be Determined',
                    'k': 'To be Determined'
                }

                # Display results when k is to be determined
                self.display_k(status=current_status)

                # When standard deviation is to be determined
                if self.analyzer.null_check('Additional info', 'Standard Deviation'):
                    # Update current status
                    current_status['sd'] = 'To be Determined'

                    # Generate the plot for the determination of sd
                    self.analyzer.plot_sd()

                    # When standard deviation is also to be determined, rather than specified
                    self.display_standard_deviation(status=current_status)
                else:
                    # Update current status
                    current_status['sd'] = 'Specified'

                    # Generate the plot for the determination of sd
                    self.analyzer.plot_sd()

                    # When standard deviation in specified
                    self.display_standard_deviation(current_status)
            else:
                # Generate current status
                current_status = {
                    'Margin': 'To be Determined',
                    'k': 'Specified'
                }

                # risk factor k, when specified.
                self.display_k(status=current_status)

                # When standard deviation is to be determined
                if self.analyzer.null_check('Additional info', 'Standard Deviation'):
                    # Update current status
                    current_status['sd'] = 'To be Determined'

                    # Generate the plot for the determination of sd
                    self.analyzer.plot_sd()

                    # When standard deviation is also to be determined, rather than specified
                    self.display_standard_deviation(status=current_status)
                else:
                    # Update current status
                    current_status['sd'] = 'Specified'

                    # Generate the plot for the determination of sd
                    self.analyzer.plot_sd()

                    # When standard deviation in specified
                    self.display_standard_deviation(status=current_status)

            # Update status for creation of margin
            self.display_margin(current_status)

        # Display format when margin is specified
        else:
            current_status = {
                'Margin': 'Specified'
            }

            # Display margin when it is user-specified
            self.display_margin(current_status)

        # Branch II: Calculation of Target Mean Strength
        self.display_target_mean_strength(status=current_status)

        # Branch III: Determination of wc ratio
        self.analyzer.plot_fwc_determination()
        self.display_target_wc_ratio(status=current_status)

    def fix_boundary(self):
        """
        Fixes scroll boundary in the top level widget
        """
        # Get the bounding box of all items
        bbox = self.base_canvas.bbox("all")

        # Add allowance on top and at the bottom
        top_allowance = 45
        bottom_allowance = 45
        bbox = (bbox[0], bbox[1] - top_allowance, bbox[2], bbox[3] + bottom_allowance)

        # Update scroll region to include all objects
        self.base_canvas.update_idletasks()
        self.base_canvas.config(scrollregion=bbox)


class StageTwoResults(tk.Toplevel):
    """
    Top level frame for a summary of stage two's results

    Attributes:
        - analyzer `MixDesignAnalyzer`: The instantiated class for backend calculations, used here to retrieve results
        - controller `tk.Frame`: Used for accessing the parent frame
        - stage `str`: the current stage, either 'in_progress' or 'final

    Methods:
        - display_scrollbar(): Displays the scrollbar for the TopLevel window
        - display_header(): Display the OptiMix logo, stage & title
        - display_fw_content(status): Displays the calculations pertaining to free water content
        - display_results(): Displays all results
        - fix_boundary(): fix scroll boundary in the TopLevel window
    """

    def __init__(self, analyzer, controller, stage):
        # Instantiate the mix design analyzer
        super().__init__(bg=BG, width=793.92, height=630)
        self.analyzer = analyzer
        self.controller = controller
        self.stage = stage

        # Import the index
        self.index = self.controller.index

        # Window settings
        self.title("OptiMix: Stage Two Design Results (Air-entrained Concrete Mix)")  # window title
        self.iconbitmap(optimix_paths.icons['icon_16'])  # window icon
        self.resizable(False, True)

        # Create the base canvas
        self.base_canvas = tk.Canvas(
            self,
            bg=BG,
            width=793.92,
            height=630,
            highlightthickness=0
        )
        # Place the base canvas
        self.base_canvas.place(x=0, y=0)
        self.base_canvas.pack(expand=True, fill="both")

        # Display the scrollbar
        self.display_scrollbar()

        # Display the header
        self.display_header()

        # Display the results
        self.display_results()

        # Fix scroll boundary in the top level widget
        self.fix_boundary()

    def display_scrollbar(self):
        """
        Displays the scroll bar by the right side of the new TopLevel for canvas, or any other type of widget
        """
        # Setup mousewheel scrolling
        self.base_canvas.bind(
            '<MouseWheel>',
            lambda event: self.base_canvas.yview_scroll(
                -int(event.delta / 50),
                "units")
        )

        # Make the scroll bar
        scrollbar = tk.Scrollbar(
            master=self,
            orient="vertical",
            cursor='hand2',
            command=self.base_canvas.yview
        )
        self.base_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")

    def display_header(self):
        """
        Displays then header,
        > title,
        > stage,
        > optimix logo
        > Air entrained mix design
        """
        # Display the current stage
        result_stage_ii = load_tk_image(optimix_paths.doe_assets['report_stage_ii'])
        self.base_canvas.rsii = result_stage_ii
        self.base_canvas.create_image(
            101.0,
            96.0,
            image=result_stage_ii
        )

        # Display the title "Mix Design results"
        result_title_sii = load_tk_image(optimix_paths.doe_assets['report_title'])
        self.base_canvas.rtsii = result_title_sii
        self.base_canvas.create_image(
            146.0,
            58.0,
            image=result_title_sii,
        )

        # Display the optimix logo
        result_logo = load_tk_image(optimix_paths.doe_assets['report_logo'])
        self.base_canvas.result_logo = result_logo
        self.base_canvas.create_image(
            655.0,
            66.0,
            image=result_logo
        )

        # Display text 'Air entrained mix design'
        self.base_canvas.create_text(628,
                                     102,
                                     fill=white_color,
                                     font=tk.font.Font(family=calibri, size=13, weight='bold'),
                                     text="(Air-entrained Concrete Mix)")

    def display_fw_content(self, status: dict):
        """
        Display's the following:
        - Background tab
        - Table 3, "Approximate free-water content (kg/m3) required to give various levels of workability"
        - Parameters and result
        :param status: (dict): Dictionary class containing current state before displaying report
        """
        if status['fw_content'] == 'Different Agg Types':
            # Display the background tab
            rec_i = load_tk_image(optimix_paths.doe_assets['report_rectangles'][4])
            self.base_canvas.rec_i = rec_i
            self.base_canvas.create_image(
                390.00000762939453,
                611.99998474121094,
                image=rec_i
            )

            # Show the tab's title, "Concrete Workability: Determining the free-water content of the mix"
            self.base_canvas.create_text(390,
                                         205,
                                         fill=white_color,
                                         activefill=np.random.choice(report_title_colors),
                                         font=tk.font.Font(family=calibri, size=16, weight='bold'),
                                         text="Concrete Workability: Determining the Free-water Content of the Mix")

            # Place table 3
            tab_iii = load_tk_image(optimix_paths.doe_assets['table_iii_reporting'])
            self.base_canvas.tab_iii_rep = tab_iii
            self.base_canvas.create_image(
                387.00000762939453,
                435.99998474121094,
                image=tab_iii
            )

            # Parameters and results..
            coarse_agg_type = self.analyzer.data['Additional info']['Coarse Aggregate Type']
            fine_agg_type = self.analyzer.data['Additional info']['Fine Aggregate Type']
            cagg_type = coarse_agg_type[0].lower() + coarse_agg_type[1:]  # make lower case all through
            fagg_type = fine_agg_type[0].lower() + fine_agg_type[1:]  # make lower case all through
            max_agg_size = self.analyzer.calc_data['max_agg_size']
            slump_value = self.analyzer.data['Specified variables']['Slump']
            modified_slump_value = self.analyzer.calc_data['modified_slump_value']
            w = self.analyzer.calc_data['fw_content']

            # Improve vocabulary
            vocab = {
                '0-10mm': ['0 - 10mm', 'exceeding 12 seconds'],
                '10-30mm': ['10 - 30mm', 'range of 6-12 seconds'],
                '30-60mm': ['30 - 60mm', 'range of 3-6 seconds'],
                '60-180mm': ['60 - 180mm', 'range of 0-3 seconds']
            }

            # Retrieve the fw_content for fine aggregate and coarse aggregate,
            wf = self.analyzer.calc_data['wf']
            wc = self.analyzer.calc_data['wc']

            # Display text
            text = f"For a concrete mix featuring a maximum aggregate size of {max_agg_size}mm, \n" \
                   f"{fagg_type} fine aggregate type, {cagg_type} coarse aggregate type, \n" \
                   f"and a desired slump range of {vocab[slump_value][0]} (corresponding to a Vebe time \n" \
                   f"{vocab[slump_value][1]}.\n" \
                   f"\n" \
                   f"As a result of the introduction of entrained air into the concrete mix,\n" \
                   f"a lower workability category is selected from the table;\n" \
                   f"{vocab[modified_slump_value][0]}, (corresponding to a Vebe time {vocab[modified_slump_value][1]}).\n" \
                   f"\n" \
                   f"The required free-water content is estimated below: \n" \
                   f"                                             \n" \
                   f"0.67W\u2086 + 0.33W\u05A4 = (0.67 × {wf}kg/m\u00b3) + (0.33 × {wc}kg/m\u00b3) = {np.round(w, 1)} kg/m\u00b3\n" \
                   f"                                             \n" \
                   f"where  W\u2086 is the free water content appropriate to type of fine aggregate \n" \
                   f"and    W\u05A4 is the free water content appropriate to type of fine aggregate \n"
            self.base_canvas.create_text(89,
                                         660.99998474121094,
                                         fill=white_color,
                                         anchor='nw',
                                         font=tk.font.Font(family=calibri, size=13),
                                         text=text)

        elif status['fw_content'] == 'Same Agg Type':
            # Display the background tab
            rec_i = load_tk_image(optimix_paths.doe_assets['report_rectangles'][4])
            self.base_canvas.rec_i = rec_i
            self.base_canvas.create_image(
                390.00000762939453,
                611.99998474121094,
                image=rec_i
            )

            # Show the tab's title, "Concrete Workability: Determining the free-water content of the mix"
            title = f"Concrete Workability: \n" \
                    f"Determining the Free-water Content of the Mix\n"
            self.base_canvas.create_text(333,
                                         260,
                                         fill=white_color,
                                         activefill=np.random.choice(report_title_colors),
                                         font=tk.font.Font(family=calibri, size=19, weight='bold'),
                                         text=title)

            # Place table 3
            tab_iii = load_tk_image(optimix_paths.doe_assets['table_iii_reporting'])
            self.base_canvas.tab_iii_rep = tab_iii
            self.base_canvas.create_image(
                387.00000762939453,
                500.99998474121094,
                image=tab_iii
            )

            # Parameters and results..
            fine_agg_type = self.analyzer.data['Additional info']['Fine Aggregate Type']
            fagg_type = fine_agg_type[0].lower() + fine_agg_type[1:]  # make lower case all through
            max_agg_size = self.analyzer.calc_data['max_agg_size']
            slump_value = self.analyzer.data['Specified variables']['Slump']
            modified_slump_value = self.analyzer.calc_data['modified_slump_value']
            w = self.analyzer.calc_data['fw_content']

            # Improve vocabulary
            vocab = {
                '0-10mm': ['0 - 10mm', 'exceeding 12 seconds'],
                '10-30mm': ['10 - 30mm', 'range of 6-12 seconds'],
                '30-60mm': ['30 - 60mm', 'range of 3-6 seconds'],
                '60-180mm': ['60 - 180mm', 'range of 0-3 seconds']
            }

            # Display text
            text = f"For a concrete mix featuring a maximum aggregate size of {max_agg_size}mm, \n" \
                   f"{fagg_type} aggregate type, and a desired slump range of {vocab[slump_value][0]}\n" \
                   f"(corresponding to a Vebe time {vocab[slump_value][1]}),\n" \
                   f"\n" \
                   f"the required free-water content is {w} kg/m\u00b3.\n" \
                   f"\n" \
                   f"Note that the required water content ({w}kg/m\u00b3) above is taken\n" \
                   f"from the lower workability category in the table,\n" \
                   f"{vocab[modified_slump_value][0]}, (corresponding to a Vebe time {vocab[modified_slump_value][1]}).\n" \
                   f"This is as a result of the introduction of entrained air into the concrete mix." \

            self.base_canvas.create_text(89,
                                         750.99998474121094,
                                         fill=white_color,
                                         anchor='nw',
                                         font=tk.font.Font(family=calibri, size=13),
                                         text=text)

    def display_results(self):
        """
        All reports concerning the concrete workability, hence the determination of free water content
        There are only two different cases in this section:
         - When coarse and fine aggregates are of the same type
         - When coarse and fine aggregate are of different types
        """
        if self.analyzer.different_agg_types:
            # Generate current status
            current_status = {'fw_content': 'Different Agg Types'}

            # Display the results for the determination of free water content
            self.display_fw_content(status=current_status)
        else:
            # Generate current status
            current_status = {'fw_content': 'Same Agg Type'}

            # Display the results for the determination of free water content
            self.display_fw_content(status=current_status)

    def fix_boundary(self):
        """
        Fixes scroll boundary in the top level widget
        """
        # Get the bounding box of all items
        bbox = self.base_canvas.bbox("all")

        # Add allowance on top and at the bottom
        top_allowance = 45
        bottom_allowance = 45
        bbox = (bbox[0], bbox[1] - top_allowance, bbox[2], bbox[3] + bottom_allowance)

        # Update scroll region to include all objects
        self.base_canvas.update_idletasks()
        self.base_canvas.config(scrollregion=bbox)


class StageThreeResults(tk.Toplevel):
    """
    Top level frame for a summary of stage three's results

    Attributes:
        - analyzer `MixDesignAnalyzer`: The instantiated class for backend calculations, used here to retrieve results
        - controller `tk.Frame`: Used for accessing the parent frame
        - stage `str`: the current stage, either 'in_progress' or 'final

    Methods:
        - display_scrollbar(): Displays the scrollbar for the TopLevel window
        - display_header(): Display the OptiMix logo, stage & title
        - display_cement_content_calculation(): Displays the calculations regarding the determination of cement content
        - display_specified_limits(status): Displays the calculations regarding cement content checks
        - display_results(): Displays all results
        - fix_boundary(): fix scroll boundary in the TopLevel window
    """

    def __init__(self, analyzer, controller, stage):
        # Instantiate the mix design analyzer
        super().__init__(bg=BG, width=793.92, height=630)
        self.analyzer = analyzer
        self.controller = controller
        self.stage = stage

        # Import the index
        self.index = self.controller.index

        # Window settings
        self.title("OptiMix: Stage Three Design Results (Air-entrained Concrete Mix)")  # window title
        self.iconbitmap(optimix_paths.icons['icon_16'])  # window icon
        self.resizable(False, True)

        # Create the base canvas
        self.base_canvas = tk.Canvas(
            self,
            bg=BG,
            width=793.92,
            height=630,
            highlightthickness=0
        )
        # Place the base canvas
        self.base_canvas.place(x=0, y=0)
        self.base_canvas.pack(expand=True, fill="both")

        # Display the scrollbar
        self.display_scrollbar()

        # Display the header
        self.display_header()

        # Display the results
        self.display_results()

        # Fix scroll boundary in the top level widget
        self.fix_boundary()

    def display_scrollbar(self):
        """
        Displays the scroll bar by the right side of the new TopLevel for canvas, or any other type of widget
        """
        # Setup mousewheel scrolling
        self.base_canvas.bind(
            '<MouseWheel>',
            lambda event: self.base_canvas.yview_scroll(
                -int(event.delta / 50),
                "units")
        )

        # Make the scroll bar
        scrollbar = tk.Scrollbar(
            master=self,
            orient="vertical",
            cursor='hand2',
            command=self.base_canvas.yview
        )
        self.base_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")

    def display_header(self):
        """
        Displays then header,
        > title,
        > stage,
        > optimix logo
        > Air-entrained mix design
        """
        # Display the current stage
        result_stage_iii = load_tk_image(optimix_paths.doe_assets['report_stage_iii'])
        self.base_canvas.rsiii = result_stage_iii
        self.base_canvas.create_image(
            101.0,
            96.0,
            image=result_stage_iii
        )

        # Display the title "Mix Design results"
        result_title_siii = load_tk_image(optimix_paths.doe_assets['report_title'])
        self.base_canvas.rtsiii = result_title_siii
        self.base_canvas.create_image(
            146.0,
            58.0,
            image=result_title_siii,
        )

        # Display the optimix logo
        result_logo = load_tk_image(optimix_paths.doe_assets['report_logo'])
        self.base_canvas.result_logo = result_logo
        self.base_canvas.create_image(
            655.0,
            66.0,
            image=result_logo
        )

        # Display text 'Air entrained mix design'
        self.base_canvas.create_text(628,
                                     102,
                                     fill=white_color,
                                     font=tk.font.Font(family=calibri, size=13, weight='bold'),
                                     text="(Air-entrained Concrete Mix)")

    def display_cement_content_calculation(self):
        """
        Display the calculations regarding the determination of cement content.
        - Background tab
        - Title
        - The calculation of the cement content
        """
        # Display the background tab
        rec_i = load_tk_image(optimix_paths.doe_assets['report_rectangles'][2])
        self.base_canvas.rec_i = rec_i
        self.base_canvas.create_image(
            390.00000762939453,
            270.99998474121094,
            image=rec_i
        )

        # Show the tab's title, "Determination of cement content"
        self.base_canvas.create_text(245.3,
                                     210,
                                     fill=white_color,
                                     activefill=np.random.choice(report_title_colors),
                                     font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                     text="Determination of Cement Content")

        # Display calculated cement content
        fw_content = np.round(float(self.analyzer.calc_data["fw_content"]), 2)
        fwc_ratio = np.round(float(self.analyzer.calc_data["fwc_ratio"]), 2)
        calc_cc = np.round(float(self.analyzer.calc_data["calc_cement_content"]), 2)

        text = f"Given a free-water content of {fw_content}kg/m\u00b3 and a free-water/cement ratio of {fwc_ratio}, \n" \
               f"the cement content is determined by dividing the free-water content by \n" \
               f"the free-water/cement ratio, this results in a cement content of {calc_cc}kg/m\u00b3."

        self.base_canvas.create_text(81,
                                     245,
                                     fill=white_color,
                                     anchor='nw',
                                     font=tk.font.Font(family=calibri, size=13),
                                     text=text)

    def display_specified_limits(self, status: dict):
        """
        Displays cement content limit checks based on the user's specifications.
        - Background tab
        - Title
        - Limit checks
        :param status: (dict): Dictionary class containing current state before displaying report
        """

        # Place the background tab
        rec_ii = load_tk_image(optimix_paths.doe_assets['report_rectangles'][2])
        self.base_canvas.rec_ii = rec_ii
        self.base_canvas.create_image(
            390.00000762939453,
            500.99998474121094,
            image=rec_ii
        )

        # Show the tab's title, "Cement Content Limit Checks"
        self.base_canvas.create_text(215,
                                     435,
                                     fill=white_color,
                                     activefill=np.random.choice(report_title_colors),
                                     font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                     text="Cement Content Limit Checks")

        if status["max_content"] == 'Specified' and status["min_content"] == 'Specified':

            # Specifications
            max_content = np.round(float(self.analyzer.data['Specified variables']['Maximum cement content']), 2)
            min_content = np.round(float(self.analyzer.data['Specified variables']['Minimum cement content']), 2)

            specs = f"Specified limits include a maximum of {max_content}kg/m\u00b3 and a minimum of {min_content}kg/m\u00b3."

            if status["cement_content"] == "Within Range":
                # When the calculated cement content is within range
                calc_content = np.round(float(self.analyzer.calc_data['calc_cement_content']), 2)

                # Limits
                self.base_canvas.create_text(76,
                                             465,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=13),
                                             text=specs)

                text = f"The calculated cement content, {calc_content}kg/m\u00b3, falls within the specified maximum\n" \
                       f"and minimum limits, making it the required cement content of the air-entrained concrete mix."

                self.base_canvas.create_text(76,
                                             505,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=13),
                                             text=text)

            elif status["cement_content"] == "Below Minimum":
                # When the calculated cement content is below the specified minimum
                calc_content = np.round(float(self.analyzer.calc_data['calc_cement_content']), 2)

                # Limits
                self.base_canvas.create_text(76,
                                             452,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=13),
                                             text=specs)

                text = f"The calculated cement content, {calc_content}kg/m\u00b3, is lower than the specified minimum value.\n" \
                       f"The minimum value, {min_content}kg/m\u00b3 is adopted as the cement content for the air-entrained concrete mix."

                self.base_canvas.create_text(76,
                                             479,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=13),
                                             text=text)

                # Modified water to cement ratio
                fwc_ratio = np.round(float(self.analyzer.calc_data["fwc_ratio"]), 2)
                modified_fwc = np.round(float(self.analyzer.calc_data["modified_fwc_ratio"]), 2)
                text_fwc = f"Due to the modified cement content, the initial free-water/cement ratio, {fwc_ratio}, \n" \
                           f"will be modified by dividing the free water content with the adopted cement content. \n" \
                           f"The modified free-water/cement ratio is {modified_fwc}."

                self.base_canvas.create_text(76,
                                             524,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=13),
                                             text=text_fwc)

        elif status["max_content"] == 'Unspecified' and status["min_content"] == 'Specified':

            # State the specifications
            min_content = np.round(float(self.analyzer.data['Specified variables']['Minimum cement content']), 2)

            specs = f"Specified limits include a minimum value of {min_content}kg/m\u00b3, "

            if status["cement_content"] == "Below Minimum":
                # When the calculated cement content is below the specified minimum
                calc_content = np.round(float(self.analyzer.calc_data['calc_cement_content']), 2)

                # Limits
                self.base_canvas.create_text(76,
                                             452,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=13),
                                             text=specs)

                text = f"The calculated cement content, {calc_content}kg/m\u00b3, is lower than the specified minimum value.\n" \
                       f"The minimum value, {min_content}kg/m\u00b3 is adopted as the cement content for the air-entrained concrete mix."

                self.base_canvas.create_text(76,
                                             479,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=13),
                                             text=text)

                # Modified water to cement ratio
                fwc_ratio = np.round(float(self.analyzer.calc_data["fwc_ratio"]), 2)
                modified_fwc = np.round(float(self.analyzer.calc_data["modified_fwc_ratio"]), 2)

                text_fwc = f"Due to the modified cement content, the initial free-water/cement ratio, {fwc_ratio}, \n" \
                           f"will be modified by dividing the free water content with the adopted cement content. \n" \
                           f"The modified free-water/cement ratio is {modified_fwc}."

                self.base_canvas.create_text(76,
                                             524,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=13),
                                             text=text_fwc)

            elif status["cement_content"] == "Within Range":
                # When the calculated cement content is within range
                calc_content = np.round(float(self.analyzer.calc_data['calc_cement_content']), 2)

                # Limits
                self.base_canvas.create_text(76,
                                             465,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=13),
                                             text=specs)

                text = f"The calculated cement content, {calc_content}kg/m\u00b3, is more than the specified minimum, \n" \
                       f"making it the required cement content for the air entrained concrete mix."

                self.base_canvas.create_text(76,
                                             505,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=13),
                                             text=text)

        elif status["max_content"] == 'Specified' and status["min_content"] == 'Unspecified':
            # State the specifications
            max_content = np.round(float(self.analyzer.data['Specified variables']['Maximum cement content']), 2)

            specs = f"Specified limits include a maximum value of {max_content}kg/m\u00b3,"

            if status["cement_content"] == "Within Range":
                # When the calculated cement content less than the maximum cement content.
                calc_content = np.round(float(self.analyzer.calc_data['calc_cement_content']), 2)

                # Limits
                self.base_canvas.create_text(76,
                                             465,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=13),
                                             text=specs)

                text = f"The calculated cement content, {calc_content}kg/m\u00b3, is lower than the specified maximum, \n" \
                       f"making it the required cement content of the air-entrained concrete mix."

                self.base_canvas.create_text(76,
                                             505,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=13),
                                             text=text)

        elif status["max_content"] == 'Unspecified' and status["min_content"] == 'Unspecified':
            cement_content = np.round(float(self.analyzer.calc_data["cement_content"]), 2)

            specs = f"There are no specified maximum or minimum values,\n" \
                    f"the cement content required for the air-entrained concrete mix is {cement_content}kg/m\u00b3."

            self.base_canvas.create_text(76,
                                         472,
                                         fill=white_color,
                                         anchor='nw',
                                         font=tk.font.Font(family=calibri, size=13),
                                         text=specs)

    def display_results(self):
        """
        Displays the determination of cement content
        Cases:
        - When the calculated cement content is less than a specified limit
        - When the calculated cement content is more than a specified limit
        """
        # Retrieve the cement content specification status
        current_status = self.analyzer.cc_status

        # Display the initial cement content calculations
        self.display_cement_content_calculation()

        # Requirements check
        self.display_specified_limits(status=current_status)

    def fix_boundary(self):
        """
        Fixes scroll boundary in the top level widget
        """
        # Get the bounding box of all items
        bbox = self.base_canvas.bbox("all")

        # Add allowance on top and at the bottom
        top_allowance = 45
        bottom_allowance = 45
        bbox = (bbox[0], bbox[1] - top_allowance, bbox[2], bbox[3] + bottom_allowance)

        # Update scroll region to include all objects
        self.base_canvas.update_idletasks()
        self.base_canvas.config(scrollregion=bbox)


class StageFourResults(tk.Toplevel):
    """
    Top level frame for a summary of stage four's results

    Attributes:
        - analyzer `MixDesignAnalyzer`: The instantiated class for backend calculations, used here to retrieve results
        - controller `tk.Frame`: Used for accessing the parent frame
        - stage `str`: the current stage, either 'in_progress' or 'final

    Methods:
        - display_scrollbar(): Displays the scrollbar for the TopLevel window
        - display_header(): Display the OptiMix logo, stage & title
        - display_total_agg_content(status): Displays the calculations regarding the total aggregate content
        - display_results(): Displays all results
        - fix_boundary(): fix scroll boundary in the TopLevel window
    """

    def __init__(self, analyzer, controller, stage):
        # Instantiate the mix design analyzer
        super().__init__(bg=BG, width=793.92, height=630)
        self.analyzer = analyzer
        self.controller = controller
        self.stage = stage

        # Import the index
        self.index = self.controller.index

        # Window settings
        self.title("OptiMix: Stage Four Design Results (Air-entrained Concrete Mix)")  # window title
        self.iconbitmap(optimix_paths.icons['icon_16'])  # window icon
        self.resizable(False, True)

        # Create the base canvas
        self.base_canvas = tk.Canvas(
            self,
            bg=BG,
            width=793.92,
            height=630,
            highlightthickness=0
        )
        # Place the base canvas
        self.base_canvas.place(x=0, y=0)
        self.base_canvas.pack(expand=True, fill="both")

        # Display the scrollbar
        self.display_scrollbar()

        # Display the header
        self.display_header()

        # Display the results
        self.display_results()

        # Fix scroll boundary in the top level widget
        self.fix_boundary()

    def display_scrollbar(self):
        """
        Displays the scroll bar by the right side of the new TopLevel for canvas, or any other type of widget
        """
        # Setup mousewheel scrolling
        self.base_canvas.bind(
            '<MouseWheel>',
            lambda event: self.base_canvas.yview_scroll(
                -int(event.delta / 50),
                "units")
        )

        # Make the scroll bar
        scrollbar = tk.Scrollbar(
            master=self,
            orient="vertical",
            cursor='hand2',
            command=self.base_canvas.yview
        )
        self.base_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")

    def display_header(self):
        """
        Displays then header,
        > title,
        > stage,
        > optimix logo
        """
        # Display the current stage
        result_stage_iv = load_tk_image(optimix_paths.doe_assets['report_stage_iv'])
        self.base_canvas.rsiv = result_stage_iv
        self.base_canvas.create_image(
            101.0,
            96.0,
            image=result_stage_iv
        )

        # Display the title "Mix Design results"
        result_title_siv = load_tk_image(optimix_paths.doe_assets['report_title'])
        self.base_canvas.rtsi = result_title_siv
        self.base_canvas.create_image(
            146.0,
            58.0,
            image=result_title_siv,
        )

        # Display the optimix logo
        result_logo = load_tk_image(optimix_paths.doe_assets['report_logo'])
        self.base_canvas.result_logo = result_logo
        self.base_canvas.create_image(
            655.0,
            66.0,
            image=result_logo
        )

        # Display text 'Air entrained mix design'
        self.base_canvas.create_text(628,
                                     102,
                                     fill=white_color,
                                     font=tk.font.Font(family=calibri, size=13, weight='bold'),
                                     text="(Air-entrained Concrete Mix)")

    def display_total_agg_content(self):
        """
        Displays the following:
        - Background tab
        - The plot which was used in estimating the density of compacted concrete / the overriden value
        """
        if self.analyzer.specified_conc_density:
            # Display the background tab
            rec_tac_small = load_tk_image(optimix_paths.doe_assets['report_rectangles'][2])
            self.base_canvas.rec_tac_small = rec_tac_small
            self.base_canvas.create_image(
                390.00000762939453,
                270.99998474121094,
                image=rec_tac_small
            )

            # Display the title
            self.base_canvas.create_text(286,
                                         205,
                                         fill=white_color,
                                         activefill=np.random.choice(report_title_colors),
                                         font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                         text="Determination of Total Aggregate Content")

            # Needed parameters
            w = np.round(float(self.analyzer.calc_data["fw_content"]), 2)
            c = np.round(float(self.analyzer.calc_data["cement_content"]), 2)
            d = np.round(float(self.analyzer.calc_data['wet_conc_density']), 2)
            tac = np.round(float(self.analyzer.calc_data['total_agg_content']), 2)

            text = f"The previously calculated cement content ({c} kg/m\u00b3) and the free-water content\n" \
                   f"({w} kg/m\u00b3) are subtracted from the provided density of the concrete mix \n" \
                   f"({d}kg/m\u00b3) to determine the total aggregate content of the concrete mix.\n" \
                   f"The total aggregate content of the air-entrained concrete mix is {tac}kg/m\u00b3. \n"

            self.base_canvas.create_text(84.4,
                                         245,
                                         fill=white_color,
                                         anchor='nw',
                                         font=tk.font.Font(family=calibri, size=13),
                                         text=text)

        else:
            # Display the background tab
            rec_tac = load_tk_image(optimix_paths.doe_assets['report_rectangles'][3])
            self.base_canvas.rec_tac = rec_tac
            self.base_canvas.create_image(
                390.00000762939453,
                510.99998474121094,
                image=rec_tac
            )

            # Display the title, "Determination of the total aggregate content"
            self.base_canvas.create_text(286,
                                         205,
                                         fill=white_color,
                                         activefill=np.random.choice(report_title_colors),
                                         font=tk.font.Font(family=calibri, size=17, weight='bold'),
                                         text="Determination of Total Aggregate Content")

            # Possible scenarios based on user inputs and limits,
            if self.analyzer.tac_content['ssd_value'] == 'unspecified':
                if self.analyzer.tac_content['Agg_status'] == 'Same types, crushed':
                    # Plot figure 5
                    self.analyzer.plot_figure_v(status='crushed or uncrushed, unspecified', mode='AEM')

                    # Place the visualization
                    fig_v_plot = self.analyzer.fig_v_png_image
                    self.base_canvas.fig_v = fig_v_plot
                    self.base_canvas.create_image(
                        390.00000762939453,
                        420.99998474121094,
                        image=fig_v_plot,
                    )

                    # Parameters
                    w = np.round(float(self.analyzer.calc_data['fw_content']), 2)
                    c = np.round(float(self.analyzer.calc_data["cement_content"]), 2)
                    d = np.round(float(self.analyzer.calc_data['wet_conc_density']), 2)
                    tac = np.round(float(self.analyzer.calc_data['total_agg_content']), 2)
                    plot_density = np.round(float(self.analyzer.calc_data['density_from_plot']), 2)
                    ac = np.round(float(self.analyzer.data['Specified variables']['Air Content']), 2)

                    # Text
                    display_text = f"A relative density of 2.7 is assumed for crushed aggregates. The air content is {ac}%. \n" \
                                   f"From the plot above, the relative density and the free-water content \n" \
                                   f"({w} kg/m\u00b3) correspond to a wet air-entrained concrete density modified by; \n" \
                                   f"[Wet density ({plot_density})  - (10 × {ac} × 2.7)]. This results in a density of {d} kg/m.\u00b3\n" \
                                   f"\n" \
                                   f"The previously calculated cement content ({c} kg/m\u00b3) and the free-water content\n" \
                                   f"({w} kg/m\u00b3) are subtracted from the estimated density of the concrete mix \n" \
                                   f"({d}kg/m\u00b3) to determine the total aggregate content of the concrete mix.\n" \
                                   f"The total aggregate content of the air-entrained concrete mix is {tac}kg/m\u00b3. \n"

                    self.base_canvas.create_text(84.4,
                                                 647,
                                                 fill=white_color,
                                                 anchor='nw',
                                                 font=tk.font.Font(family=calibri, size=13),
                                                 text=display_text)

                elif self.analyzer.tac_content['Agg_status'] == 'Same types, uncrushed':
                    # Plot figure 5
                    self.analyzer.plot_figure_v(status='crushed or uncrushed, unspecified', mode='AEM')

                    # Place the visualization
                    fig_v_plot = self.analyzer.fig_v_png_image
                    self.base_canvas.fig_v = fig_v_plot
                    self.base_canvas.create_image(
                        390.00000762939453,
                        420.99998474121094,
                        image=fig_v_plot,
                    )

                    # Parameters
                    w = np.round(float(self.analyzer.calc_data['fw_content']), 2)
                    c = np.round(float(self.analyzer.calc_data["cement_content"]), 2)
                    d = np.round(float(self.analyzer.calc_data['wet_conc_density']), 2)
                    tac = np.round(float(self.analyzer.calc_data['total_agg_content']), 2)
                    plot_density = np.round(float(self.analyzer.calc_data['density_from_plot']), 2)
                    ac = np.round(float(self.analyzer.data['Specified variables']['Air Content']), 2)

                    # Text
                    display_text = f"A relative density of 2.6 is assumed for uncrushed aggregates. The air content is {ac}%.\n" \
                                   f"From the plot above, the relative density and the free-water content \n" \
                                   f"({w} kg/m\u00b3) correspond to a wet air-entrained concrete density modified by; \n" \
                                   f"[Wet density ({plot_density})  - (10 × {ac} × 2.6)]. This results in a density of {d} kg/m.\u00b3\n" \
                                   f"\n" \
                                   f"The previously calculated cement content ({c} kg/m\u00b3) and the free-water content\n" \
                                   f"({w} kg/m\u00b3) are subtracted from the estimated density of the concrete mix \n" \
                                   f"({d}kg/m\u00b3) to determine the total aggregate content of the concrete mix.\n" \
                                   f"The total aggregate content of the air-entrained concrete mix is {tac}kg/m\u00b3. \n"

                    self.base_canvas.create_text(84.4,
                                                 647,
                                                 fill=white_color,
                                                 anchor='nw',
                                                 font=tk.font.Font(family=calibri, size=13),
                                                 text=display_text)

                elif self.analyzer.tac_content['Agg_status'] == 'Diff types':
                    # Plot figure 5
                    self.analyzer.plot_figure_v(status='crushed and uncrushed, unspecified', mode='AEM')

                    # Place the visualization
                    fig_v_plot = self.analyzer.fig_v_png_image
                    self.base_canvas.fig_v = fig_v_plot
                    self.base_canvas.create_image(
                        390.00000762939453,
                        420.99998474121094,
                        image=fig_v_plot,
                    )

                    # Parameters
                    w = np.round(float(self.analyzer.calc_data['fw_content']), 2)
                    c = np.round(float(self.analyzer.calc_data["cement_content"]), 2)
                    d = np.round(float(self.analyzer.calc_data['wet_conc_density']), 2)
                    tac = np.round(float(self.analyzer.calc_data['total_agg_content']), 2)
                    plot_density = np.round(float(self.analyzer.calc_data['density_from_plot']), 2)
                    ac = np.round(float(self.analyzer.data['Specified variables']['Air Content']), 2)

                    # Text
                    display_text = f"A relative density of 2.65 is assumed for crushed and uncrushed aggregates. The air \n" \
                                   f"content is {ac}%. From the plot above, the relative density and the free-water content \n" \
                                   f"({w} kg/m\u00b3) correspond to a wet air-entrained concrete density modified by; \n" \
                                   f"[Wet density ({plot_density})  - (10 × {ac} × 2.65)]. This results in a density of {d} kg/m.\u00b3\n" \
                                   f"\n" \
                                   f"The previously calculated cement content ({c} kg/m\u00b3) and the free-water content\n" \
                                   f"({w} kg/m\u00b3) are subtracted from the estimated density of the concrete mix \n" \
                                   f"({d}kg/m\u00b3) to determine the total aggregate content of the concrete mix.\n" \
                                   f"The total aggregate content of the air-entrained concrete mix is {tac}kg/m\u00b3. \n"

                    self.base_canvas.create_text(84.4,
                                                 647,
                                                 fill=white_color,
                                                 anchor='nw',
                                                 font=tk.font.Font(family=calibri, size=13),
                                                 text=display_text)

            elif self.analyzer.tac_content['ssd_value'] == 'specified':
                # Plot figure 5
                self.analyzer.plot_figure_v(status='specified', mode='AEM')

                # Place the visualization
                fig_v_plot = self.analyzer.fig_v_png_image
                self.base_canvas.fig_v = fig_v_plot
                self.base_canvas.create_image(
                    390.00000762939453,
                    420.99998474121094,
                    image=fig_v_plot,
                )

                # Parameters
                w = np.round(float(self.analyzer.calc_data['fw_content']), 2)
                c = np.round(float(self.analyzer.calc_data["cement_content"]), 2)
                d = np.round(float(self.analyzer.calc_data['wet_conc_density']), 2)
                tac = np.round(float(self.analyzer.calc_data['total_agg_content']), 2)
                rd = float(self.analyzer.data['Additional info']['Relative density of agg'])
                plot_density = np.round(float(self.analyzer.calc_data['density_from_plot']), 2)
                ac = np.round(float(self.analyzer.data['Specified variables']['Air Content']), 2)

                # Text
                display_text = f"From the plot above, the specified relative density ({rd}), air content ({ac}%) and the \n" \
                               f"free-water content ({w} kg/m\u00b3) correspond to a wet concrete density modified below;\n" \
                               f"[Wet density ({plot_density})  - (10 × {ac} × {rd})]. This results in a density of {d} kg/m.\u00b3\n" \
                               f"\n" \
                               f"The previously calculated cement content ({c} kg/m\u00b3) and the free-water content\n" \
                               f"({w} kg/m\u00b3) are subtracted from the estimated density of the concrete mix \n" \
                               f"({d}kg/m\u00b3) to determine the total aggregate content of the concrete mix.\n" \
                               f"The total aggregate content of the air-entrained concrete mix is {tac}kg/m\u00b3. \n"

                self.base_canvas.create_text(84.4,
                                             670,
                                             fill=white_color,
                                             anchor='nw',
                                             font=tk.font.Font(family=calibri, size=13),
                                             text=display_text)

    def display_results(self):
        """Displays the report for the determination of total aggregate content"""
        # Display the report for this stage
        self.display_total_agg_content()

    def fix_boundary(self):
        """
        Fixes scroll boundary in the top level widget
        """
        # Get the bounding box of all items
        bbox = self.base_canvas.bbox("all")

        # Add allowance on top and at the bottom
        top_allowance = 45
        bottom_allowance = 45
        bbox = (bbox[0], bbox[1] - top_allowance, bbox[2], bbox[3] + bottom_allowance)

        # Update scroll region to include all objects
        self.base_canvas.update_idletasks()
        self.base_canvas.config(scrollregion=bbox)


class StageFiveResults(tk.Toplevel):
    """
    Toplevel frame for a summary of stage five's results

    Attributes:
        - analyzer `MixDesignAnalyzer`: The instantiated class for backend calculations, used here to retrieve results
        - controller `tk.Frame`: Used for accessing the parent frame
        - stage `str`: the current stage, either 'in_progress' or 'final

    Methods:
        - generate_canvases(): Creates canvases to be displayed on the top level widget
        - display_scrollbar(): Displays the scrollbar for the TopLevel window
        - display_header(): Display the OptiMix logo, stage & title
        - display_recommended_fineagg_prop(canvas): Shows the results for the recommended value of fine aggregate proportion
        - display_oven_dry_batching(canvas): Reports for value modifications due to specified or unspecified oven dry batching conditions
        - display_v_results(): Switches the report view to stage 5
        - roundoff_to_nearest_five_kg(report_no, canvas): Rounds off all mix design results to the nearest 5kg
        - revert_to_initial_values(report_no, canvas): Reverts the rounded off values to their initial values
        - result_switch(report_no, canvas): Button switch event for that flicks between rounding off and displaying exact values
        - quantity_unit(x, y, canvas): Function that displays 'kg' where employed
        - display_cement_quantity(report_no, canvas): Displays the 'Cement _____ kg'
        - display_water_quantity(report_no, canvas): Displays the 'Water _____ kg'
        - display_fagg_quantity(report_no, canvas, mix_design_results): Displays the 'Fine aggregate _____ kg'
        - display_cagg_quantity(report_no, canvas, mix_design_results): Displays the 'Coarse aggregate _____ kg'
        - display_txt_quantities(report_no, canvas, mix_design_results): Displays the text for all the constituent quantities using canvas.text
        - display_report_a(canvas): Displays quantities of constituents in kg per m3, exact values or round off to the nearest 5kg
        - entry_check(canvas, entry): Checks the input in the entry box
        - config_bv_display(canvas, batch_design_data): Adjusts the display of the batch/trial mix volumes calculated by clicking the 'Adjust' button.
        - adjust_batch_volume(canvas): Adjust the quantities for the trial mix as specified by the user
        - display_trial_mix_essentials(canvas): Displays the instructions, batching volume text box, unit toggle & adjust button for the trial mix report tab
        - display_trial_mix_report(canvas): Displays results for a user specified trial mix
        - export_as(file_format): Exports the mix design data as excel, pdf or docx
        - display_export_options(canvas): Displays export options, for now; .pdf, excel, word
        - display_final_results(canvas): Switches the report view to overall final mix design results
        - fix_boundary(canvas): fix scroll boundary in the TopLevel window
    """

    def __init__(self, analyzer, controller, stage):
        # Instantiate the mix design analyzer
        super().__init__(bg=BG, width=793.92, height=630)
        self.analyzer = analyzer
        self.controller = controller
        self.stage = stage

        # Import the index
        self.index = self.controller.index

        # Window settings
        self.title("OptiMix: Stage Five Design Results (Air-entrained Concrete Mix)")  # window title
        self.iconbitmap(optimix_paths.icons['icon_16'])  # window icon
        self.resizable(False, True)
        self.top_allowance = 45
        self.bottom_allowance = 45

        # Needed variables
        self.scrollbar = None
        self.fmdr_off = None
        self.svr_on = None
        self.base_canvas_f = None
        self.base_canvas_v = None
        self.stage_v_button_on = None
        self.stage_v_button_off = None
        self.final_results_button_on = None
        self.final_results_button_off = None
        self.round_off_to_n5 = None
        self.kg_image = None
        self.display_exact_v = None
        self.value_toggle = None
        self.current_button_a_image = None
        self.cement_qty_txt = ''
        self.bv = None
        self.adjust_button = None
        self.selected_unit = None
        self.unit_default_selection = None
        self.adjust_button_png = None
        self.unit_type = None
        self.messagebox_has_been_shown = False
        self.docx_button = None
        self.xlsx_button = None
        self.pdf_button = None

        # Default result display, 0 for exact value, 1 for round off value
        self.result_accuracy_switch = 0

        # Generate canvases
        self.generate_canvases()

        if self.stage == 'final':
            # Display the final mix design stages
            self.display_final_results()

        elif self.stage == 'in_progress':
            # Display stage five design results
            self.display_v_results()

    def generate_canvases(self):
        """
        Generate canvases to be displayed on the top level widget
        """
        self.base_canvas_f = tk.Canvas(
            self,
            bg=BG,
            width=793.92,
            height=630,
            highlightthickness=0
        )

        self.base_canvas_v = tk.Canvas(
            self,
            bg=BG,
            width=793.92,
            height=630,
            highlightthickness=0
        )

    def display_scrollbar(self, canvas):
        """
        Displays the scroll bar by the right side of the new TopLevel for canvas, or any other type of widget
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        """
        # Setup mousewheel scrolling for in the canvas
        canvas.bind(
            '<MouseWheel>',
            lambda event: canvas.yview_scroll(
                -int(event.delta / 50),
                "units")
        )

        # Make the scroll bar
        self.scrollbar = tk.Scrollbar(
            master=self,
            orient="vertical",
            cursor='hand2',
            command=canvas.yview
        )
        canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")

    def display_header(self, canvas):
        """
        Displays the header,
        > optimix logo
        > instructions
        > transitioning buttons
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        """
        # Display the optimix logo
        result_logo = load_tk_image(optimix_paths.doe_assets['report_logo'])
        canvas.result_logo = result_logo
        canvas.create_image(
            126.0,
            66.0,
            image=result_logo
        )

        # Display instruction
        instruction = load_tk_image(optimix_paths.doe_assets['stage_v_instruction'])
        canvas.instruction = instruction
        canvas.create_image(
            292.0,
            121.0,
            image=instruction
        )

        # Display Transition buttons
        self.stage_v_button_on = load_tk_image(optimix_paths.doe_assets['svr_on'])
        self.stage_v_button_off = load_tk_image(optimix_paths.doe_assets['svr_off'])
        self.final_results_button_on = load_tk_image(optimix_paths.doe_assets['fmdr_on'])
        self.final_results_button_off = load_tk_image(optimix_paths.doe_assets['fmdr_off'])

        # Save the loaded button images in memory for viewing
        canvas.stage_v_button_on = self.stage_v_button_on
        canvas.stage_v_button_off = self.stage_v_button_off
        canvas.final_results_button_on = self.final_results_button_on
        canvas.final_results_button_off = self.final_results_button_off

        # Create a custom style for the stage change buttons
        result_button_style = ttk.Style()
        result_button_style.configure(
            'Results.TButton',
            borderwidth=0,
            background=BG,
            relief="raised",
            highlightthickness=0,
            highlightbackground=BG,
            activebackground=BG
        )

        # Handle dynamic button changes ()
        result_button_style.map(
            'Results.TButton',
            background=[('active', BG)],
            highlightcolor=[('focus', BG)]
        )

        # Display the buttons
        self.svr_on = ttk.Button(
            canvas,
            takefocus=False,
            image=self.stage_v_button_on,
            style='Results.TButton',
            command=self.display_v_results,
            cursor='hand2'
        )
        canvas.create_window(244.0, 175.0, window=self.svr_on)

        self.fmdr_off = ttk.Button(
            canvas,
            takefocus=False,
            image=self.final_results_button_off,
            style='Results.TButton',
            command=self.display_final_results,
            cursor='hand2'
        )
        canvas.create_window(534.0, 175.0, window=self.fmdr_off)

    def display_recommended_fineagg_prop(self, canvas):
        """
        Displays the results for the recommended value of fine aggregate proportion.
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        """
        # Display background rectangle tab
        bg_rec_i = load_tk_image(optimix_paths.doe_assets['report_rectangles'][3])
        canvas.bg_rec_i = bg_rec_i
        canvas.create_image(
            390.00000762939453,
            560.99998474121094,
            image=bg_rec_i
        )

        # Display the title
        canvas.create_text(319,
                           253,
                           fill=white_color,
                           activefill=np.random.choice(report_title_colors),
                           font=tk.font.Font(family=calibri, size=17, weight='bold'),
                           text="Selection of Fine and Coarse Aggregate Contents")

        # Needed parameters
        max_agg_size = self.analyzer.calc_data['max_agg_size']
        slump_value = self.analyzer.data['Specified variables']['Slump']
        fwc_ratio = np.round(float(self.analyzer.calc_data["modified_fwc_ratio"]), 2)
        perc_passing = np.round(float(self.analyzer.calc_data['perc_passing']), 2)

        # Improve vocabulary
        vocab = {
            '0-10mm': ['0 - 10mm', 'exceeding 12 seconds'],
            '10-30mm': ['10 - 30mm', 'range of 6-12 seconds'],
            '30-60mm': ['30 - 60mm', 'range of 3-6 seconds'],
            '60-180mm': ['60 - 180mm', 'range of 0-3 seconds']
        }

        text = f"For a maximum aggregate size of {max_agg_size}mm, a slump range of {vocab[slump_value][0]} \n" \
               f"(corresponding to a Vebe time {vocab[slump_value][1]}), a free-water/cement ratio of {fwc_ratio},\n" \
               f"and a percentage passing of {perc_passing}%. The recommended value for the proportion of \n" \
               f"fine aggregate in the air-entrained mix is determined using the figure below:"

        canvas.create_text(87,
                           280.8,
                           fill=white_color,
                           anchor='nw',
                           font=tk.font.Font(family=calibri, size=13),
                           text=text)

        # Plot the visualization
        self.analyzer.plot_fine_agg_proportion()

        # Place the visualization
        fig_vi_plot = load_tk_image(self.analyzer.fig_vi_png_image)
        canvas.fig_vi = fig_vi_plot
        canvas.create_image(
            393.00000762939453,
            549.99998474121094,
            image=fig_vi_plot,
        )

        # Selection of aggregate contents
        recc_fine_prop = np.round(float(self.analyzer.calc_data['fine_agg_prop']), 2)
        coarse_prop = np.round(float(100 - recc_fine_prop), 2)
        fine_agg_content = np.round(float(self.analyzer.calc_data['calc_fine_agg_content']), 2)
        coarse_agg_content = np.round(float(self.analyzer.calc_data['calc_coarse_agg_content']), 2)
        tot_agg_content = np.round(float(self.analyzer.calc_data['total_agg_content']), 2)
        fagg_reduc = np.round(float(self.analyzer.data['Additional info']['Fine Aggregate Reduction']), 2)

        text_ii = f"With the previously determined total aggregate content ({tot_agg_content}kg/m\u00b3),\n" \
                  f"the calculated fine and coarse aggregate proportion and composition is presented below:\n" \
                  f"• Fine Aggregate:  {fine_agg_content} kg/m\u00b3. ({recc_fine_prop}%) \n" \
                  f"• Coarse Aggregate:  {coarse_agg_content} kg/m\u00b3. ({coarse_prop}%) \n" \
                  f"Note that the fine aggregate content is reduced by {fagg_reduc}% of the total aggregate content.\n" \
                  f"This is done to permit a further small reduction in the water content."

        canvas.create_text(87,
                           765.8,
                           fill=white_color,
                           anchor='nw',
                           font=tk.font.Font(family=calibri, size=13),
                           text=text_ii)

    def display_oven_dry_batching(self, canvas):
        """
        Reports for value modifications due to specified or unspecified oven dry batching conditions
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        """
        # Retrieve result values for oven dry batching
        calc_coarse_agg_content = np.round(float(self.analyzer.calc_data['calc_coarse_agg_content']), 2)
        ov_coarse_mass = np.round(float(self.analyzer.calc_data['coarse_agg_content']), 2)
        calc_fine_agg_content = np.round(float(self.analyzer.calc_data['calc_fine_agg_content']), 2)
        ov_fine_mass = np.round(float(self.analyzer.calc_data['fine_agg_content']), 2)
        water_req_for_absorption = np.round(float(self.analyzer.calc_data['added_h20_mass']), 2)
        fw_content = np.round(float(self.analyzer.calc_data["fw_content"]), 2)
        new_water_content = np.round(float(self.analyzer.calc_data['new_fw_content']), 2)

        if self.analyzer.odb_status == 'none':
            # I don't intend to display a report when oven dry batching is not specified
            pass

        elif self.analyzer.odb_status == 'both aggregates':  # When both aggregates are in oven dry batching conditions
            # Retrieve user input
            cagg_absorption = np.round(float(self.analyzer.data['Additional info']['Absorption of Coarse Aggregate']),
                                       2)
            fagg_absorption = np.round(float(self.analyzer.data['Additional info']['Absorption of Fine Aggregate']), 2)

            # Display background rectangle tab
            odb_rect_i = load_tk_image(optimix_paths.doe_assets['report_rectangles'][5])
            canvas.odb_rect_i = odb_rect_i
            canvas.create_image(
                390.00000762939453,
                1205.99998474121094,
                image=odb_rect_i
            )

            # Display the title
            canvas.create_text(244,
                               990,
                               fill=white_color,
                               activefill=np.random.choice(report_title_colors),
                               font=tk.font.Font(family=calibri, size=17, weight='bold'),
                               text="Oven Dry Batching of Aggregates")

            text = f"To obtain the mass of the aggregates when they are to be batched\n" \
                   f"in an oven-dry condition, the masses of the saturated surface-dry aggregates \n" \
                   f"previously determined ({calc_fine_agg_content}kg/m\u00b3 & {calc_coarse_agg_content}kg/m\u00b3) will be multiplied by 100/(100 + A). \n" \
                   f"A is the specified percentage by mass of water required to bring the dry aggregates\n" \
                   f"to a saturated surface-dry condition.\n" \
                   f"\n" \
                   f"\n" \
                   f"With the specified percentage absorption of {fagg_absorption}% for fine aggregates\n" \
                   f"and the specified percentage absorption of {cagg_absorption}% for coarse aggregates,\n" \
                   f"the required oven-dry masses are presented below: \n" \
                   f"\n" \
                   f"• Mass of oven-dry fine aggregate = {calc_fine_agg_content} × (100 / {100 + fagg_absorption}) = {ov_fine_mass} kg/m\u00b3 \n" \
                   f"• Mass of oven-dry coarse aggregate = {calc_coarse_agg_content} × (100 / {100 + cagg_absorption}) = {ov_coarse_mass} kg/m\u00b3 \n" \
                   f"\n" \
                   f"\n" \
                   f"The amount of the mixing water is increased by the mass of water absorbed by the \n" \
                   f"aggregates to reach the saturated surface-dry condition.\n" \
                   f"\n" \
                   f"Water required for absorption = ({calc_fine_agg_content} - {ov_fine_mass}) + ({calc_coarse_agg_content} - {ov_coarse_mass}) = {water_req_for_absorption} kg/m\u00b3 \n" \
                   f"The water content required for this mix is {fw_content} + {water_req_for_absorption} = {new_water_content}kg/m\u00b3" \
 
            canvas.create_text(88,
                               1010,                            
                               fill=white_color,
                               anchor='nw',
                               font=tk.font.Font(family=calibri, size=13),
                               text=text)

        elif self.analyzer.odb_status == 'fine aggregate only':
            # Retrieve user input
            fagg_absorption = np.round(float(self.analyzer.data['Additional info']['Absorption of Fine Aggregate']), 2)

            odb_rect_ii = load_tk_image(optimix_paths.doe_assets['report_rectangles'][1])
            canvas.odb_rect_ii = odb_rect_ii
            canvas.create_image(
                390.00000762939453,
                1172.99998474121094,
                image=odb_rect_ii
            )

            # Display the title
            canvas.create_text(264,
                               997.5,
                               fill=white_color,
                               activefill=np.random.choice(report_title_colors),
                               font=tk.font.Font(family=calibri, size=17, weight='bold'),
                               text="Oven Dry Batching of Fine Aggregates")

            text_ii = f"To obtain the mass of the fine aggregates when they are to be batched\n" \
                      f"in an oven-dry condition, the mass of the saturated surface-dry fine aggregate \n" \
                      f"previously determined ({calc_fine_agg_content}kg/m\u00b3) will be multiplied by 100/(100 + A). \n" \
                      f"A is the specified percentage by mass of water required to bring the dry fine aggregate\n" \
                      f"to a saturated surface-dry condition.\n" \
                      f"\n" \
                      f"With the specified percentage absorption of {fagg_absorption}% for fine aggregates, \n" \
                      f"the required oven-dry mass is presented below: \n" \
                      f"\n" \
                      f"• Mass of oven-dry fine aggregate = {calc_fine_agg_content} × (100 / {100 + fagg_absorption}) = {ov_fine_mass} kg/m\u00b3 \n" \
                      f"\n" \
                      f"The amount of the mixing water is increased by the mass of water absorbed by the \n" \
                      f"fine aggregates to reach the saturated surface-dry condition.\n" \
                      f"\n" \
                      f"Water required for absorption = {calc_fine_agg_content} - {ov_fine_mass} = {water_req_for_absorption} kg/m\u00b3 \n" \
                      f"The water content required for this mix is {fw_content} + {water_req_for_absorption} = {new_water_content}kg/m\u00b3"

            canvas.create_text(88,
                               1021,
                               fill=white_color,
                               anchor='nw',
                               font=tk.font.Font(family=calibri, size=13),
                               text=text_ii)

        elif self.analyzer.odb_status == 'coarse aggregate only':
            # Retrieve user input
            cagg_absorption = np.round(float(self.analyzer.data['Additional info']['Absorption of Coarse Aggregate']),
                                       2)

            odb_rect_iii = load_tk_image(optimix_paths.doe_assets['report_rectangles'][1])
            canvas.odb_rect_iii = odb_rect_iii
            canvas.create_image(
                390.00000762939453,
                1172.99998474121094,
                image=odb_rect_iii
            )

            # Display the title
            canvas.create_text(277,
                               997.5,
                               fill=white_color,
                               activefill=np.random.choice(report_title_colors),
                               font=tk.font.Font(family=calibri, size=17, weight='bold'),
                               text="Oven Dry Batching of Coarse Aggregates")

            text_iii = f"To obtain the mass of the coarse aggregates when they are to be batched\n" \
                       f"in an oven-dry condition, the mass of the saturated surface-dry coarse aggregate \n" \
                       f"previously determined ({calc_coarse_agg_content}kg/m\u00b3) will be multiplied by 100/(100 + A). \n" \
                       f"A is the specified percentage by mass of water required to bring the dry coarse aggregate\n" \
                       f"to a saturated surface-dry condition.\n" \
                       f"\n" \
                       f"With the specified percentage absorption of {cagg_absorption}% for coarse aggregates, \n" \
                       f"the required oven-dry mass is presented below: \n" \
                       f"\n" \
                       f"• Mass of oven-dry coarse aggregate = {calc_coarse_agg_content} × (100 / {100 + cagg_absorption}) = {ov_coarse_mass} kg/m\u00b3 \n" \
                       f"\n" \
                       f"The amount of the mixing water is increased by the mass of water absorbed by the \n" \
                       f"coarse aggregates to reach the saturated surface-dry condition.\n" \
                       f"\n" \
                       f"Water required for absorption = {calc_coarse_agg_content} - {ov_coarse_mass} = {water_req_for_absorption} kg/m\u00b3 \n" \
                       f"The water content required for this mix is {fw_content} + {water_req_for_absorption} = {new_water_content}kg/m\u00b3"

            canvas.create_text(88,
                               1021,
                               fill=white_color,
                               anchor='nw',
                               font=tk.font.Font(family=calibri, size=13),
                               text=text_iii)

    def display_v_results(self):
        """
        Switches the report view to stage 5
        """
        # Hide previous canvas
        self.base_canvas_f.pack_forget()

        # Top level window configuration
        self.title("OptiMix: Stage Five Design Results (Air-entrained Concrete Mix)")

        # Place the canvas
        self.base_canvas_v.place(x=0, y=0)
        self.base_canvas_v.pack(expand=True, fill="both")

        # Display the scrollbar
        self.display_scrollbar(self.base_canvas_v)

        # Display the header
        self.display_header(self.base_canvas_v)

        # Configure button images, make the stage five result active and final results out of focus
        self.svr_on.configure(image=self.stage_v_button_on)
        self.fmdr_off.configure(image=self.final_results_button_off)

        # Display determination of recommended proportion of fine aggregate
        self.display_recommended_fineagg_prop(self.base_canvas_v)

        # Display results for oven dry batching
        self.display_oven_dry_batching(self.base_canvas_v)

        # Fix scroll boundary in the top level widget
        self.fix_boundary(self.base_canvas_v)

    def roundoff_to_nearest_five_kg(self, report_no: str, canvas):
        """
        Rounds off all mix design results to the nearest 5kg
        Sets self.result_accuracy_switch to 1
        :param report_no: There are three final mix design reports for now, "a", "b" & "c.
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        """
        # Set accuracy result switch to one
        self.result_accuracy_switch = 1

        if report_no == 'a':
            # Round off the cement content quantity
            cement_new_txt = f'{self.analyzer.design_results["cement"][self.result_accuracy_switch]}'
            canvas.itemconfigure(tagOrId='cement_qty', text=cement_new_txt)

            # Round off the water content quantity
            water_new_txt = f'{self.analyzer.design_results["water"][self.result_accuracy_switch]}'
            canvas.itemconfigure(tagOrId='water_qty', text=water_new_txt)

            # Round off the fine aggregate content quantity
            fagg_new_txt = f'{self.analyzer.design_results["fagg"][self.result_accuracy_switch]}'
            canvas.itemconfigure(tagOrId='fagg_qty', text=fagg_new_txt)

            # Round off the coarse aggregate content quantity
            agg_sizes = self.analyzer.design_results['cagg_sizes']

            if agg_sizes == '10mm' or agg_sizes == '20mm' or agg_sizes == '40mm':
                # Round off the values
                cagg_new_txt = f'{self.analyzer.design_results["cagg_proportioning"][self.result_accuracy_switch][0]}'
                canvas.itemconfigure(tagOrId='cagg_qty', text=cagg_new_txt)
                canvas.itemconfigure(tagOrId='cagg_qty_i', text=cagg_new_txt)

            elif agg_sizes == '10mm, 20mm' or agg_sizes == '10mm, 40mm' or agg_sizes == '20mm, 40mm':
                # Round off the values
                cagg = f'{self.analyzer.design_results["cagg"][self.result_accuracy_switch]}'
                cagg_new_txt_i = f'{self.analyzer.design_results["cagg_proportioning"][self.result_accuracy_switch][0]}'
                cagg_new_txt_ii = f'{self.analyzer.design_results["cagg_proportioning"][self.result_accuracy_switch][1]}'

                canvas.itemconfigure(tagOrId='cagg_qty', text=cagg)
                canvas.itemconfigure(tagOrId='cagg_qty_i', text=cagg_new_txt_i)
                canvas.itemconfigure(tagOrId='cagg_qty_ii', text=cagg_new_txt_ii)

            elif agg_sizes == '10mm, 20mm, 40mm':
                # Round off the values
                cagg = f'{self.analyzer.design_results["cagg"][self.result_accuracy_switch]}'
                cagg_new_txt_i = f'{self.analyzer.design_results["cagg_proportioning"][self.result_accuracy_switch][0]}'
                cagg_new_txt_ii = f'{self.analyzer.design_results["cagg_proportioning"][self.result_accuracy_switch][1]}'
                cagg_new_txt_iii = f'{self.analyzer.design_results["cagg_proportioning"][self.result_accuracy_switch][2]}'

                canvas.itemconfigure(tagOrId='cagg_qty', text=cagg)
                canvas.itemconfigure(tagOrId='cagg_qty_i', text=cagg_new_txt_i)
                canvas.itemconfigure(tagOrId='cagg_qty_ii', text=cagg_new_txt_ii)
                canvas.itemconfigure(tagOrId='cagg_qty_iii', text=cagg_new_txt_iii)

        elif report_no == 'b':
            pass

        elif report_no == 'c':
            pass

    def revert_to_initial_values(self, report_no: str, canvas):
        """
        Reverts the rounded off values to their initial values.
        Sets self.result_accuracy_switch to 1
        :param report_no: (str): There are three final mix design reports for now, "a", "b" & "c.
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        """
        # Set accuracy result switch to one
        self.result_accuracy_switch = 0

        if report_no == 'a':
            # Round off the cement content quantity
            cement_new_txt = f'{self.analyzer.design_results["cement"][self.result_accuracy_switch]}'
            canvas.itemconfigure(tagOrId='cement_qty', text=cement_new_txt)

            # Round off the water content quantity
            water_new_txt = f'{self.analyzer.design_results["water"][self.result_accuracy_switch]}'
            canvas.itemconfigure(tagOrId='water_qty', text=water_new_txt)

            # Round off the fine aggregate content quantity
            fagg_new_txt = f'{self.analyzer.design_results["fagg"][self.result_accuracy_switch]}'
            canvas.itemconfigure(tagOrId='fagg_qty', text=fagg_new_txt)

            # Round off the coarse aggregate content quantity
            agg_sizes = self.analyzer.design_results['cagg_sizes']

            if agg_sizes == '10mm' or agg_sizes == '20mm' or agg_sizes == '40mm':
                # Display the proportioned single size aggregate twice..
                cagg_new_txt = f'{self.analyzer.design_results["cagg_proportioning"][self.result_accuracy_switch][0]}'
                canvas.itemconfigure(tagOrId='cagg_qty', text=cagg_new_txt)
                canvas.itemconfigure(tagOrId='cagg_qty_i', text=cagg_new_txt)

            elif agg_sizes == '10mm, 20mm' or agg_sizes == '10mm, 40mm' or agg_sizes == '20mm, 40mm':
                # Display the proportioned single size aggregate thrice..
                cagg = f'{self.analyzer.design_results["cagg"][self.result_accuracy_switch]}'
                cagg_new_txt_i = f'{self.analyzer.design_results["cagg_proportioning"][self.result_accuracy_switch][0]}'
                cagg_new_txt_ii = f'{self.analyzer.design_results["cagg_proportioning"][self.result_accuracy_switch][1]}'

                canvas.itemconfigure(tagOrId='cagg_qty', text=cagg)
                canvas.itemconfigure(tagOrId='cagg_qty_i', text=cagg_new_txt_i)
                canvas.itemconfigure(tagOrId='cagg_qty_ii', text=cagg_new_txt_ii)

            elif agg_sizes == '10mm, 20mm, 40mm':
                # Round off the values
                cagg = f'{self.analyzer.design_results["cagg"][self.result_accuracy_switch]}'
                cagg_new_txt_i = f'{self.analyzer.design_results["cagg_proportioning"][self.result_accuracy_switch][0]}'
                cagg_new_txt_ii = f'{self.analyzer.design_results["cagg_proportioning"][self.result_accuracy_switch][1]}'
                cagg_new_txt_iii = f'{self.analyzer.design_results["cagg_proportioning"][self.result_accuracy_switch][2]}'

                canvas.itemconfigure(tagOrId='cagg_qty', text=cagg)
                canvas.itemconfigure(tagOrId='cagg_qty_i', text=cagg_new_txt_i)
                canvas.itemconfigure(tagOrId='cagg_qty_ii', text=cagg_new_txt_ii)
                canvas.itemconfigure(tagOrId='cagg_qty_iii', text=cagg_new_txt_iii)

        elif report_no == 'b':
            pass

        elif report_no == 'c':
            pass

    def result_switch(self, report_no: str, canvas):
        """
        Button switch event for that flicks between rounding off and displaying exact values
        :param report_no: There are three final mix design reports for now, "a", "b" & "c.
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        """
        if self.current_button_a_image == self.round_off_to_n5:
            # Round off all values in the first report to the nearest 5 kg
            self.roundoff_to_nearest_five_kg(report_no=report_no, canvas=canvas)

            self.current_button_a_image = self.display_exact_v

        else:
            # Display exact values
            self.revert_to_initial_values(report_no=report_no, canvas=canvas)

            self.current_button_a_image = self.round_off_to_n5

        # Switch button image
        self.value_toggle.configure(image=self.current_button_a_image)

    def quantity_unit(self, x: float, y: float, canvas):
        """
        Function that displays 'kg' where deployed
        :param x: (float): X coordinate
        :param y: (float): Y coordinate
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        """
        self.kg_image = load_tk_image(optimix_paths.doe_assets['kg_unit'])
        canvas.image_references.append(self.kg_image)

        # Place the image
        canvas.create_image(x, y, image=self.kg_image)

    def display_cement_quantity(self, report_no: str, canvas):
        """
        Displays the 'Cement _____ kg'
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        :param report_no: There are three final mix design reports for now, "a", "b" & "c.
        """
        if report_no == 'a':
            # Load the image
            cement_a = load_tk_image(optimix_paths.doe_assets['cement_report_a'])
            canvas.cement_a = cement_a

            # Display 'Cement ____ kg'
            canvas.create_image(
                228.00000762939453,
                415.99998474121094,
                image=cement_a
            )

            # Display 'kg'
            self.quantity_unit(x=340, y=415, canvas=canvas)

        elif report_no == 'b':
            # Load the image
            cement_a = load_tk_image(optimix_paths.doe_assets['cement_report_a'])
            canvas.cement_a_tm = cement_a

            # Display 'Cement ____ kg'
            canvas.create_image(
                228.00000762939453,
                975.99998474121094,
                image=cement_a
            )

            # Display 'kg'
            self.quantity_unit(x=340, y=975, canvas=canvas)

    def display_water_quantity(self, report_no: str, canvas):
        """
        Displays the 'Water _____ kg'
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        :param report_no: There are three final mix design reports for now, "a", "b" & "c.
        """
        if report_no == 'a':
            # Load the image
            water_a = load_tk_image(optimix_paths.doe_assets['water_report_a'])
            canvas.water_a = water_a

            # Display 'Water ____ kg'
            canvas.create_image(
                228.00000762939453,
                538.99998474121094,
                image=water_a
            )

            # Display 'kg'
            self.quantity_unit(x=340, y=538, canvas=canvas)

        elif report_no == 'b':
            # Load the image
            water_a = load_tk_image(optimix_paths.doe_assets['water_report_a'])
            canvas.water_a_tm = water_a

            # Display 'Water ____ kg'
            canvas.create_image(
                228.00000762939453,
                1098.99998474121094,
                image=water_a
            )

            # Display 'kg'
            self.quantity_unit(x=340, y=1098, canvas=canvas)

    def display_fagg_quantity(self, report_no: str, canvas, mix_design_results):
        """
        Displays the 'Fine aggregate _____ kg',
        :param report_no: There are three final mix design reports for now, "a", "b" & "c.
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        :param mix_design_results: The final mix design data, it's needed for determining whether fine agg in batched in ssd or ovd
        """
        if report_no == 'a':
            # Load two images, ssd & ovd
            fagg_ssd = load_tk_image(optimix_paths.doe_assets['fagg_report_ssd'])
            fagg_ovd = load_tk_image(optimix_paths.doe_assets['fagg_report_ovd'])

            # Store the images as references
            canvas.fagg_ssd = fagg_ssd
            canvas.fagg_ovd = fagg_ovd

            # Retrieve the odb status
            if mix_design_results['odb_batching'] == 'none' or mix_design_results['odb_batching'] == 'coarse aggregate only':

                # Fine aggregate is batched in ssd, display ssd
                fagg_image = fagg_ssd

            else:
                # Fine aggregate is in oven dry condition
                fagg_image = fagg_ovd

            # Display 'Fine aggregate ____ kg ssd/odc'
            canvas.create_image(
                228.00000762939453,
                675.99998474121094,
                image=fagg_image
            )

            # Display 'kg'
            self.quantity_unit(x=340, y=663, canvas=canvas)

        elif report_no == 'b':
            # Load two images, ssd & ovd
            fagg_ssd = load_tk_image(optimix_paths.doe_assets['fagg_report_ssd'])
            fagg_ovd = load_tk_image(optimix_paths.doe_assets['fagg_report_ovd'])

            # Store the images as references
            canvas.fagg_ssd_tm = fagg_ssd
            canvas.fagg_ovd_tm = fagg_ovd

            # Retrieve the odb status
            if mix_design_results['odb_batching'] == 'none' or mix_design_results['odb_batching'] == 'coarse aggregate only':

                # Fine aggregate is batched in ssd, display ssd
                fagg_image = fagg_ssd

            else:
                # Fine aggregate is in oven dry condition
                fagg_image = fagg_ovd

            # Display 'Fine aggregate ____ kg ssd/odc'
            canvas.create_image(
                228.00000762939453,
                1235.99998474121094,
                image=fagg_image
            )

            # Display 'kg'
            self.quantity_unit(x=340, y=1223, canvas=canvas)

    def display_cagg_quantity(self, report_no: str, canvas, mix_design_results):
        """
        Displays the 'Coarse aggregate _____ kg',
        :param report_no: There are three final mix design reports for now, "a", "b" & "c.
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        :param mix_design_results: The final mix design data, it's needed for determining whether coarse agg in batched in ssd or ovd,
                                   and the aggregate sizes
        """
        # Load 14 images, ssd & ovd
        cagg_10_ssd = load_tk_image(optimix_paths.doe_assets['cagg_10_ssd_path'])
        cagg_20_ssd = load_tk_image(optimix_paths.doe_assets['cagg_20_ssd_path'])
        cagg_40_ssd = load_tk_image(optimix_paths.doe_assets['cagg_40_ssd_path'])
        cagg_10_odc = load_tk_image(optimix_paths.doe_assets['cagg_10_odc_path'])
        cagg_20_odc = load_tk_image(optimix_paths.doe_assets['cagg_20_odc_path'])
        cagg_40_odc = load_tk_image(optimix_paths.doe_assets['cagg_40_odc_path'])
        cagg_10_20_ssd = load_tk_image(optimix_paths.doe_assets['cagg_10_20_ssd_path'])
        cagg_10_40_ssd = load_tk_image(optimix_paths.doe_assets['cagg_10_40_ssd_path'])
        cagg_20_40_ssd = load_tk_image(optimix_paths.doe_assets['cagg_20_40_ssd_path'])
        cagg_10_20_odc = load_tk_image(optimix_paths.doe_assets['cagg_10_20_odc_path'])
        cagg_10_40_odc = load_tk_image(optimix_paths.doe_assets['cagg_10_40_odc_path'])
        cagg_20_40_odc = load_tk_image(optimix_paths.doe_assets['cagg_20_40_odc_path'])
        cagg_10_20_40_ssd = load_tk_image(optimix_paths.doe_assets['cagg_10_20_40_ssd_path'])
        cagg_10_20_40_odc = load_tk_image(optimix_paths.doe_assets['cagg_10_20_40_odc_path'])

        if report_no == 'a':
            # Store the images as references
            canvas.cagg_10_ssd = cagg_10_ssd
            canvas.cagg_20_ssd = cagg_20_ssd
            canvas.cagg_40_ssd = cagg_40_ssd
            canvas.cagg_10_odc = cagg_10_odc
            canvas.cagg_20_odc = cagg_20_odc
            canvas.cagg_40_odc = cagg_40_odc
            canvas.cagg_10_20_ssd = cagg_10_20_ssd
            canvas.cagg_20_40_ssd = cagg_20_40_ssd
            canvas.cagg_10_40_ssd = cagg_10_40_ssd
            canvas.cagg_10_20_odc = cagg_10_20_odc
            canvas.cagg_20_40_odc = cagg_20_40_odc
            canvas.cagg_10_40_odc = cagg_10_40_odc
            canvas.cagg_10_20_40_ssd = cagg_10_20_40_ssd
            canvas.cagg_10_20_40_odc = cagg_10_20_40_odc

            # Retrieve the odb status
            if mix_design_results['odb_batching'] == 'none' or mix_design_results['odb_batching'] == 'fine aggregate only':

                # Coarse aggregate is batched in ssd, display ssd, format: [cagg_image_x, cagg_image_y, kg_x, kg_y, cagg_image]
                cagg_data = {
                    '10mm': [550, 472.99, cagg_10_ssd],
                    '20mm': [550, 472.99, cagg_20_ssd],
                    '40mm': [550, 472.99, cagg_40_ssd],
                    '10mm, 20mm': [550, 494.99, cagg_10_20_ssd],
                    '10mm, 40mm': [550, 494.99, cagg_10_40_ssd],
                    '20mm, 40mm': [550, 494.99, cagg_20_40_ssd],
                    '10mm, 20mm, 40mm': [550, 510.99, cagg_10_20_40_ssd]
                }

            else:
                # Coarse aggregate is in oven dry condition, format: [cagg_image_x, cagg_image_y, kg_x, kg_y, cagg_image]
                cagg_data = {
                    '10mm': [550, 472.99, cagg_10_odc],
                    '20mm': [550, 472.99, cagg_20_odc],
                    '40mm': [550, 472.99, cagg_40_odc],
                    '10mm, 20mm': [550, 494.99, cagg_10_20_odc],
                    '10mm, 40mm': [550, 494.99, cagg_10_40_odc],
                    '20mm, 40mm': [550, 494.99, cagg_20_40_odc],
                    '10mm, 20mm, 40mm': [550, 510.99, cagg_10_20_40_odc]
                }

            agg_sizes = mix_design_results['cagg_sizes']

            # Display 'Coarse aggregate ____ kg ssd/odc'
            canvas.create_image(
                cagg_data[agg_sizes][0],
                cagg_data[agg_sizes][1],
                image=cagg_data[agg_sizes][2],
            )

            # Display 'kg'
            if agg_sizes == '10mm' or agg_sizes == '20mm' or agg_sizes == '40mm':
                # Display 'kg' only twice
                self.quantity_unit(x=665.5, y=418.99, canvas=canvas)
                self.quantity_unit(x=534, y=497.99, canvas=canvas)

            elif agg_sizes == '10mm, 20mm' or agg_sizes == '10mm, 40mm' or agg_sizes == '20mm, 40mm':
                # Display 'kg' only thrice
                self.quantity_unit(x=665.5, y=419.99, canvas=canvas)
                self.quantity_unit(x=534, y=497.99, canvas=canvas)
                self.quantity_unit(x=534, y=537.99, canvas=canvas)

            elif agg_sizes == '10mm, 20mm, 40mm':
                # Display 'kg' four times
                self.quantity_unit(x=665.5, y=419.99, canvas=canvas)
                self.quantity_unit(x=534, y=497.99, canvas=canvas)
                self.quantity_unit(x=534, y=537.99, canvas=canvas)
                self.quantity_unit(x=534, y=577.99, canvas=canvas)

        elif report_no == 'b':
            # Store the images as references
            canvas.cagg_10_ssd_tm = cagg_10_ssd
            canvas.cagg_20_ssd_tm = cagg_20_ssd
            canvas.cagg_40_ssd_tm = cagg_40_ssd
            canvas.cagg_10_odc_tm = cagg_10_odc
            canvas.cagg_20_odc_tm = cagg_20_odc
            canvas.cagg_40_odc_tm = cagg_40_odc
            canvas.cagg_10_20_ssd_tm = cagg_10_20_ssd
            canvas.cagg_20_40_ssd_tm = cagg_20_40_ssd
            canvas.cagg_10_40_ssd_tm = cagg_10_40_ssd
            canvas.cagg_10_20_odc_tm = cagg_10_20_odc
            canvas.cagg_20_40_odc_tm = cagg_20_40_odc
            canvas.cagg_10_40_odc_tm = cagg_10_40_odc
            canvas.cagg_10_20_40_ssd_tm = cagg_10_20_40_ssd
            canvas.cagg_10_20_40_odc_tm = cagg_10_20_40_odc

            # Retrieve the odb status
            if mix_design_results['odb_batching'] == 'none' or mix_design_results['odb_batching'] == 'fine aggregate only':

                # Coarse aggregate is batched in ssd, display ssd, format: [cagg_image_x, cagg_image_y, kg_x, kg_y, cagg_image]
                cagg_data = {
                    '10mm': [550, 1032.99, cagg_10_ssd],
                    '20mm': [550, 1032.99, cagg_20_ssd],
                    '40mm': [550, 1032.99, cagg_40_ssd],
                    '10mm, 20mm': [550, 1054.99, cagg_10_20_ssd],
                    '10mm, 40mm': [550, 1054.99, cagg_10_40_ssd],
                    '20mm, 40mm': [550, 1054.99, cagg_20_40_ssd],
                    '10mm, 20mm, 40mm': [550, 1070.99, cagg_10_20_40_ssd]
                }

            else:
                # Coarse aggregate is in oven dry condition, format: [cagg_image_x, cagg_image_y, kg_x, kg_y, cagg_image]
                cagg_data = {
                    '10mm': [550, 1032.99, cagg_10_odc],
                    '20mm': [550, 1032.99, cagg_20_odc],
                    '40mm': [550, 1032.99, cagg_40_odc],
                    '10mm, 20mm': [550, 1054.99, cagg_10_20_odc],
                    '10mm, 40mm': [550, 1054.99, cagg_10_40_odc],
                    '20mm, 40mm': [550, 1054.99, cagg_20_40_odc],
                    '10mm, 20mm, 40mm': [550, 1070.99, cagg_10_20_40_odc]
                }

            agg_sizes = mix_design_results['cagg_sizes']

            # Display 'Coarse aggregate ____ kg ssd/odc'
            canvas.create_image(
                cagg_data[agg_sizes][0],
                cagg_data[agg_sizes][1],
                image=cagg_data[agg_sizes][2],
            )

            # Display 'kg'
            if agg_sizes == '10mm' or agg_sizes == '20mm' or agg_sizes == '40mm':
                # Display 'kg' only twice
                self.quantity_unit(x=665.5, y=978.99, canvas=canvas)
                self.quantity_unit(x=534, y=1057.99, canvas=canvas)

            elif agg_sizes == '10mm, 20mm' or agg_sizes == '10mm, 40mm' or agg_sizes == '20mm, 40mm':
                # Display 'kg' only thrice
                self.quantity_unit(x=665.5, y=979.99, canvas=canvas)
                self.quantity_unit(x=534, y=1057.99, canvas=canvas)
                self.quantity_unit(x=534, y=1097.99, canvas=canvas)

            elif agg_sizes == '10mm, 20mm, 40mm':
                # Display 'kg' four times
                self.quantity_unit(x=665.5, y=979.99, canvas=canvas)
                self.quantity_unit(x=534, y=1057.99, canvas=canvas)
                self.quantity_unit(x=534, y=1097.99, canvas=canvas)
                self.quantity_unit(x=534, y=1137.99, canvas=canvas)

    def display_txt_quantities(self, report_no: str, canvas, mix_design_results):
        """
        Displays the text for all the constituent quantities using canvas.text
        :param report_no: There are three final mix design reports for now, "a", "b" & "c.
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        :param mix_design_results: The final mix design data, it's needed for determining whether coarse agg in batched in ssd or ovd,
                                   and the aggregate sizes

                                   Mix design data is a dictionary where each key has a value that contains a list of the exact quantity,
                                   and the rounded off quantity, e.g [347.6930, 350]
                                   The index of the list above is selected by assigning 0 or 1 to self.result_accuracy_switch.
        """
        if report_no == 'a':
            # Display the cement content
            cement_txt = f'{mix_design_results["cement"][self.result_accuracy_switch]}'
            canvas.create_text(267.5,
                               413,
                               fill=white_color,
                               anchor='center',
                               justify='center',
                               activefill=np.random.choice(report_title_colors),
                               font=tk.font.Font(family=arial, size=16),
                               text=cement_txt,
                               tag='cement_qty')

            # Display the water content
            water_txt = f'{mix_design_results["water"][self.result_accuracy_switch]}'
            canvas.create_text(267.5,
                               536,
                               fill=white_color,
                               anchor='center',
                               justify='center',
                               activefill=np.random.choice(report_title_colors),
                               font=tk.font.Font(family=arial, size=16),
                               text=water_txt,
                               tag='water_qty')

            # Display the fine aggregate content
            fagg_txt = f'{mix_design_results["fagg"][self.result_accuracy_switch]}'
            canvas.create_text(267.5,
                               661,
                               fill=white_color,
                               anchor='center',
                               justify='center',
                               activefill=np.random.choice(report_title_colors),
                               font=tk.font.Font(family=arial, size=16),
                               text=fagg_txt,
                               tag='fagg_qty')

            # Display the coarse aggregate content
            agg_sizes = mix_design_results['cagg_sizes']

            if agg_sizes == '10mm' or agg_sizes == '20mm' or agg_sizes == '40mm':
                # Display the proportioned single size aggregates twice..
                cagg_txt = f'{mix_design_results["cagg_proportioning"][self.result_accuracy_switch][0]}'
                canvas.create_text(590.5,
                                   416.99,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=16),
                                   text=cagg_txt,
                                   tag='cagg_qty')

                canvas.create_text(465.5,
                                   494.99,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=14),
                                   text=cagg_txt,
                                   tag='cagg_qty_i')

            elif agg_sizes == '10mm, 20mm' or agg_sizes == '10mm, 40mm' or agg_sizes == '20mm, 40mm':
                # Display the proportioned single size aggregates thrice..
                cagg = f'{mix_design_results["cagg"][self.result_accuracy_switch]}'
                cagg_txt_i = f'{mix_design_results["cagg_proportioning"][self.result_accuracy_switch][0]}'
                cagg_txt_ii = f'{mix_design_results["cagg_proportioning"][self.result_accuracy_switch][1]}'
                canvas.create_text(590.5,
                                   417.99,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=16),
                                   text=cagg,
                                   tag='cagg_qty')

                canvas.create_text(465.5,
                                   494.99,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=14),
                                   text=cagg_txt_i,
                                   tag='cagg_qty_i')

                canvas.create_text(465.5,
                                   534.99,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=14),
                                   text=cagg_txt_ii,
                                   tag='cagg_qty_ii')

            elif agg_sizes == '10mm, 20mm, 40mm':
                # Display the proportioned single size aggregates thrice..
                cagg = f'{mix_design_results["cagg"][self.result_accuracy_switch]}'
                cagg_txt_i = f'{mix_design_results["cagg_proportioning"][self.result_accuracy_switch][0]}'
                cagg_txt_ii = f'{mix_design_results["cagg_proportioning"][self.result_accuracy_switch][1]}'
                cagg_txt_iii = f'{mix_design_results["cagg_proportioning"][self.result_accuracy_switch][2]}'
                canvas.create_text(590.5,
                                   417.99,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=16),
                                   text=cagg,
                                   tag='cagg_qty')

                canvas.create_text(465.5,
                                   494.99,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=14),
                                   text=cagg_txt_i,
                                   tag='cagg_qty_i')

                canvas.create_text(465.5,
                                   534.99,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=14),
                                   text=cagg_txt_ii,
                                   tag='cagg_qty_ii')

                canvas.create_text(465.5,
                                   573.5,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=14),
                                   text=cagg_txt_iii,
                                   tag='cagg_qty_iii')
        elif report_no == 'b':
            # Display the cement content
            canvas.create_text(267.5,
                               973,
                               fill=white_color,
                               anchor='center',
                               justify='center',
                               activefill=np.random.choice(report_title_colors),
                               font=tk.font.Font(family=arial, size=16),
                               text='',
                               tag='cement_qty_b')

            # Display the water content
            canvas.create_text(267.5,
                               1096,
                               fill=white_color,
                               anchor='center',
                               justify='center',
                               activefill=np.random.choice(report_title_colors),
                               font=tk.font.Font(family=arial, size=16),
                               text='',
                               tag='water_qty_b')

            # Display the fine aggregate content
            canvas.create_text(267.5,
                               1221,
                               fill=white_color,
                               anchor='center',
                               justify='center',
                               activefill=np.random.choice(report_title_colors),
                               font=tk.font.Font(family=arial, size=16),
                               text='',
                               tag='fagg_qty_b')

            # Display the coarse aggregate content
            agg_sizes = mix_design_results['cagg_sizes']

            if agg_sizes == '10mm' or agg_sizes == '20mm' or agg_sizes == '40mm':
                canvas.create_text(590.5,
                                   976.99,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=16),
                                   text='',
                                   tag='cagg_qty_b')

                canvas.create_text(465.5,
                                   1054.99,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=14),
                                   text='',
                                   tag='cagg_qty_i_b')

            elif agg_sizes == '10mm, 20mm' or agg_sizes == '10mm, 40mm' or agg_sizes == '20mm, 40mm':
                canvas.create_text(590.5,
                                   977.99,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=16),
                                   text='',
                                   tag='cagg_qty_b')

                canvas.create_text(465.5,
                                   1054.99,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=14),
                                   text='',
                                   tag='cagg_qty_i_b')

                canvas.create_text(465.5,
                                   1094.99,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=14),
                                   text='',
                                   tag='cagg_qty_ii_b')

            elif agg_sizes == '10mm, 20mm, 40mm':
                canvas.create_text(590.5,
                                   977.99,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=16),
                                   text='',
                                   tag='cagg_qty_b')

                canvas.create_text(465.5,
                                   1054.99,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=14),
                                   text='',
                                   tag='cagg_qty_i_b')

                canvas.create_text(465.5,
                                   1094.99,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=14),
                                   text='',
                                   tag='cagg_qty_ii_b')

                canvas.create_text(465.5,
                                   1133.5,
                                   fill=white_color,
                                   anchor='center',
                                   justify='center',
                                   activefill=np.random.choice(report_title_colors),
                                   font=tk.font.Font(family=arial, size=14),
                                   text='',
                                   tag='cagg_qty_iii_b')

    def display_report_a(self, canvas):
        """
        Displays quantities of constituents in kg per m3, exact values or round off to the nearest 5kg
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        """

        # Display background rectangle
        bg_rec = load_tk_image(optimix_paths.doe_assets['report_rectangles'][5])
        canvas.bg_rec = bg_rec
        canvas.create_image(
            390.00000762939453,
            505.99998474121094,
            image=bg_rec
        )

        # Display instructions
        x_strength = self.analyzer.data['Specified variables']['Characteristic Strength']
        days = self.analyzer.data['Specified variables']['Curing Days']
        a = self.analyzer.data['Specified variables']['Air Content']

        instruction = f"The quantities of the constituent materials per m\u00b3 required to achieve a \n" \
                      f"concrete strength of {x_strength} N/mm\u00b2 after {days} days with an air content of {a}% are shown below: "

        canvas.create_text(87,
                           270,
                           fill=white_color,
                           anchor='nw',
                           font=tk.font.Font(family=calibri, size=13),
                           text=instruction)

        # Button that rounds off to nearest 5 kg and switches to exact value
        self.round_off_to_n5 = load_tk_image(optimix_paths.doe_assets['rotn5'])
        self.display_exact_v = load_tk_image(optimix_paths.doe_assets['display_ev'])
        canvas.round_off_to_n5 = self.round_off_to_n5
        canvas.display_exact_v = self.display_exact_v

        # Default button state is to show option to round off to nearest 5 kg
        self.current_button_a_image = self.round_off_to_n5
        self.value_toggle = ttk.Button(
            canvas,
            takefocus=False,
            image=self.current_button_a_image,
            style='Results.TButton',
            command=lambda: self.result_switch('a', canvas),
            cursor='hand2'
        )
        canvas.create_window(176.0, 340.0, window=self.value_toggle)

        canvas.image_references = []  # List that stores PhotoImages

        # Display cement___ kg
        self.display_cement_quantity(report_no='a', canvas=canvas)

        # Display water quantity tab
        self.display_water_quantity(report_no='a', canvas=canvas)

        # Display fine aggregate quantity tab
        self.display_fagg_quantity(report_no='a', canvas=canvas, mix_design_results=self.analyzer.design_results)

        # Display coarse aggregate quantity tab
        self.display_cagg_quantity(report_no='a', canvas=canvas, mix_design_results=self.analyzer.design_results)

        # Display the results and values for all quantities
        self.display_txt_quantities(report_no='a', canvas=canvas, mix_design_results=self.analyzer.design_results)

    def config_bv_display(self, canvas, batch_design_data: dict):
        """
        Adjusts the display of the batch/trial mix volumes calculated by clicking the 'Adjust' button.
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        :param batch_design_data: (dict): Dictionary containing values already modified by self.analyzer.batch_to_desired_volume
        """
        # Adjust the batch volume of the cement content quantity
        cement_new_txt = f'{batch_design_data["cement"][self.result_accuracy_switch]}'
        canvas.itemconfigure(tagOrId='cement_qty_b', text=cement_new_txt)

        # Round off the water content quantity
        water_new_txt = f'{batch_design_data["water"][self.result_accuracy_switch]}'
        canvas.itemconfigure(tagOrId='water_qty_b', text=water_new_txt)

        # Round off the fine aggregate content quantity
        fagg_new_txt = f'{batch_design_data["fagg"][self.result_accuracy_switch]}'
        canvas.itemconfigure(tagOrId='fagg_qty_b', text=fagg_new_txt)

        # Round off the coarse aggregate content quantity
        agg_sizes = batch_design_data['cagg_sizes']

        if agg_sizes == '10mm' or agg_sizes == '20mm' or agg_sizes == '40mm':
            # Round off the values
            cagg_new_txt = f'{batch_design_data["cagg_proportioning"][self.result_accuracy_switch][0]}'
            canvas.itemconfigure(tagOrId='cagg_qty_b', text=cagg_new_txt)
            canvas.itemconfigure(tagOrId='cagg_qty_i_b', text=cagg_new_txt)

        elif agg_sizes == '10mm, 20mm' or agg_sizes == '10mm, 40mm' or agg_sizes == '20mm, 40mm':
            # Round off the values
            cagg = f'{batch_design_data["cagg"][self.result_accuracy_switch]}'
            cagg_new_txt_i = f'{batch_design_data["cagg_proportioning"][self.result_accuracy_switch][0]}'
            cagg_new_txt_ii = f'{batch_design_data["cagg_proportioning"][self.result_accuracy_switch][1]}'

            canvas.itemconfigure(tagOrId='cagg_qty_b', text=cagg)
            canvas.itemconfigure(tagOrId='cagg_qty_i_b', text=cagg_new_txt_i)
            canvas.itemconfigure(tagOrId='cagg_qty_ii_b', text=cagg_new_txt_ii)

        elif agg_sizes == '10mm, 20mm, 40mm':
            # Round off the values
            cagg = f'{batch_design_data["cagg"][self.result_accuracy_switch]}'
            cagg_new_txt_i = f'{batch_design_data["cagg_proportioning"][self.result_accuracy_switch][0]}'
            cagg_new_txt_ii = f'{batch_design_data["cagg_proportioning"][self.result_accuracy_switch][1]}'
            cagg_new_txt_iii = f'{batch_design_data["cagg_proportioning"][self.result_accuracy_switch][2]}'

            canvas.itemconfigure(tagOrId='cagg_qty_b', text=cagg)
            canvas.itemconfigure(tagOrId='cagg_qty_i_b', text=cagg_new_txt_i)
            canvas.itemconfigure(tagOrId='cagg_qty_ii_b', text=cagg_new_txt_ii)
            canvas.itemconfigure(tagOrId='cagg_qty_iii_b', text=cagg_new_txt_iii)

    def adjust_batch_volume(self, canvas):
        """
        Adjust the quantities for the trial mix as specified by the user
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        """
        # Check for incorrect input
        fill_status = entry_check(canvas=canvas, entry=self.bv)

        if all(fill_status):
            # Collect the supplied data
            self.analyzer.sync_input(self.bv, 'Result Tuning', 'Batch volume', option_var=self.selected_unit)
            self.analyzer.sync_input(self.unit_type, 'Result Tuning', 'Unit', option_var=self.selected_unit)

            # Convert batching volumes as specified by the user
            self.analyzer.batch_to_desired_volume(mode='AEM', mix_design_data=self.analyzer.design_results)

            # Update the values of the quantities displayed
            self.config_bv_display(canvas, self.analyzer.design_batch_results)

    def display_trial_mix_essentials(self, canvas):
        """
        Displays the instructions, batching volume text box, unit toggle & adjust button for the trial mix report tab
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        :return:
        """
        # Display background rectangle
        bg_rec_tm = load_tk_image(optimix_paths.doe_assets['report_rectangles'][5])
        canvas.bg_rec_tm = bg_rec_tm
        canvas.create_image(
            390.00000762939453,
            1065.99998474121094,
            image=bg_rec_tm
        )

        # Display instructions
        instruction = f"Specify the volume for trial mixing or construction use to view the quantities\n" \
                      f"of constituent materials for the designed concrete mix below: "

        canvas.create_text(87,
                           830,
                           fill=white_color,
                           anchor='nw',
                           font=tk.font.Font(family=calibri, size=13),
                           text=instruction)

        # Display "Desired batching volume:"
        canvas.create_text(87,
                           885,
                           fill=white_color,
                           anchor='nw',
                           font=tk.font.Font(family=calibri, size=13),
                           text="Desired batching volume")

        # Display the batching volume entry box
        batching_volume = tk.StringVar(canvas)
        batching_volume.set(self.analyzer.data['Result Tuning']['Batch volume'])

        self.bv = tk.Entry(
            canvas,
            textvariable=batching_volume,
            foreground=white_color,
            background=report_bg_color,
            font=lato,
            highlightthickness=1
        )

        # Set Active
        color_entry(self.bv)

        canvas.create_window(
            310.0,
            895,
            window=self.bv,
            width=77.0,
            height=31.0
        )

        # Display units, "kg or litres"
        available_units = ['m\u00b3', '\u2113']

        # Selected Option
        self.selected_unit = tk.StringVar(canvas)

        # Make a default selection
        self.unit_default_selection = self.analyzer.data['Result Tuning']['Unit']

        # unit type OptionMenu
        self.unit_type = ttk.OptionMenu(
            canvas,
            self.selected_unit,
            self.unit_default_selection,
            style='Custom.TMenubutton',
            *available_units
        )

        canvas.create_window(
            395.0,
            895,
            window=self.unit_type,
            width=55.0,
            height=31.0
        )

        # Customize the unit menu
        self.unit_type.config(cursor='hand2')

        # Customize the unit menu dropdown
        self.unit_type['menu'].config(
            background=BG,
            activebackground=ALT_BG,
            selectcolor=cement_select_color,
            borderwidth=0,
            fg=white_color,
            font=lato,
            relief='sunken'
        )

        # Button that rounds off to nearest 5 kg and switches to exact value
        self.adjust_button_png = load_tk_image(optimix_paths.doe_assets['adjust_button'])
        canvas.adjust_button = self.adjust_button_png

        self.adjust_button = ttk.Button(
            canvas,
            takefocus=False,
            image=self.adjust_button_png,
            style='Results.TButton',
            command=lambda: self.adjust_batch_volume(canvas),
            cursor='hand2'
        )
        canvas.create_window(490.0, 895.0, window=self.adjust_button)

    def display_trial_mix_report(self, canvas):
        """
        Displays results for a user specified trial mix
        :param canvas:  (tk.Canvas): the target canvas for the top level widget
        """
        # Display instructions, batching volume text box, unit toggle & adjust button
        self.display_trial_mix_essentials(canvas)

        # Display cement___ kg
        self.display_cement_quantity(report_no='b', canvas=canvas)

        # Display water quantity tab
        self.display_water_quantity(report_no='b', canvas=canvas)

        # Display fine aggregate quantity tab
        self.display_fagg_quantity(report_no='b', canvas=canvas, mix_design_results=self.analyzer.design_results)

        # Display coarse aggregate quantity tab
        self.display_cagg_quantity(report_no='b', canvas=canvas, mix_design_results=self.analyzer.design_results)

        # Display the results and values for all quantities
        self.display_txt_quantities(report_no='b', canvas=canvas, mix_design_results=self.analyzer.design_results)

    def export_as(self, file_format):
        """
        Exports the mix design data as excel, pdf, docx or image
        """
        # Generate the .md file report
        md_report = generate_md_report(
            mode='AEM',
            design_results=[
                self.analyzer.data['Specified variables'],
                self.analyzer.data['Additional info'],
                self.analyzer.data['Mix Parameters'],
                self.analyzer.data['Result Tuning'],
                self.analyzer.calc_data,
                self.analyzer.design_results,
                self.analyzer.design_batch_results
            ])

        if file_format == '.xlsx':
            # Check the batch volume
            self.adjust_batch_volume(self.base_canvas_f)

            # Prepare the mix design results
            results = result_preparer(
                mix_design_results=[self.analyzer.data, self.analyzer.calc_data,
                                    self.analyzer.design_results, self.analyzer.design_batch_results],
                mode='AEM',
                accuracy_switch=self.result_accuracy_switch,
                odb_status=self.analyzer.odb_status
            )

            # Prompt user to specify path
            file_path = get_path(extension='.xlsx')

            # Save the .xlsx file
            to_xlsx(path=file_path, sheets=results)

        elif file_format == '.pdf':
            # Prompt user to specify the preferred exporting path
            export_path = get_path(extension='.pdf')

            # Export the mix design results as pdf file
            to_pdf(md_file=md_report, export_path=export_path)

        elif file_format == '.docx':
            # Prompt user to specify the preferred exporting path
            export_path = get_path(extension=".docx")

            # Export the mix design results as docx file
            to_word(md_file=md_report, export_location=export_path)

    def display_export_options(self, canvas):
        """
        Displays export options, for now; .pdf, excel, word
        :param canvas:
        """
        # Display background rectangle
        bg_rec_export = load_tk_image(optimix_paths.doe_assets['report_rectangles'][2])
        canvas.bg_rec_export = bg_rec_export
        canvas.create_image(
            390.00000762939453,
            1470.99998474121094,
            image=bg_rec_export
        )

        # Display the title
        canvas.create_text(209,
                           1405,
                           fill=white_color,
                           activefill=np.random.choice(report_title_colors),
                           font=tk.font.Font(family=calibri, size=17, weight='bold'),
                           text="Mix Design Report Export")

        # Display guide text
        export_text = f"Relevant details and calculations are organized in a standard mix design format. \n" \
                      f"Select your preferred file format for viewing:"

        canvas.create_text(87,
                           1432.8,
                           fill=white_color,
                           anchor='nw',
                           font=tk.font.Font(family=calibri, size=13),
                           text=export_text)

        # Load the button images
        xlsx_image = load_tk_image(optimix_paths.doe_assets['file_format_pngs'][0])
        pdf_image = load_tk_image(optimix_paths.doe_assets['file_format_pngs'][1])
        docx_image = load_tk_image(optimix_paths.doe_assets['file_format_pngs'][2])

        canvas.xlsx_image_doe = xlsx_image
        canvas.pdf_image = pdf_image
        canvas.docx_image = docx_image

        # Display the export buttons
        self.pdf_button = ttk.Button(
            canvas,
            takefocus=False,
            image=pdf_image,
            style='Results.TButton',
            command=lambda: self.export_as(file_format='.pdf'),
            cursor='hand2'
        )
        canvas.create_window(162.0, 1518.0, window=self.pdf_button)

        self.xlsx_button = ttk.Button(
            canvas,
            takefocus=False,
            image=xlsx_image,
            style='Results.TButton',
            command=lambda: self.export_as(file_format='.xlsx'),
            cursor='hand2'
        )
        canvas.create_window(380.0, 1518.0, window=self.xlsx_button)

        self.docx_button = ttk.Button(
            canvas,
            takefocus=False,
            image=docx_image,
            style='Results.TButton',
            command=lambda: self.export_as(file_format='.docx'),
            cursor='hand2'
        )
        canvas.create_window(600.0, 1518.0, window=self.docx_button)

    def display_final_results(self):
        """
        Switches the report view to overall final mix design results
        """
        # Hide previous canvas
        self.base_canvas_v.pack_forget()

        # Top level window configuration
        self.title("OptiMix: Final Design Results (Air-entrained Mix)")

        # Place the canvas
        self.base_canvas_f.place(x=0, y=0)
        self.base_canvas_f.pack(expand=True, fill="both")

        # Display the scrollbar
        self.display_scrollbar(self.base_canvas_f)

        # Display the header
        self.display_header(self.base_canvas_f)

        # Display the first report, quantities per metre-cube, exact or round off to the nearest 5kg
        self.display_report_a(self.base_canvas_f)

        # Display the report for a user-specified trial mix
        self.display_trial_mix_report(self.base_canvas_f)

        # Display options for result export
        self.display_export_options(canvas=self.base_canvas_f)

        # Configure button images, make the stage five result active and final results out of focus
        self.svr_on.configure(image=self.stage_v_button_off)
        self.fmdr_off.configure(image=self.final_results_button_on)

        # Fix scroll boundary in the top level widget
        self.fix_boundary(self.base_canvas_f)

    def fix_boundary(self, canvas):
        """
        Fixes scroll boundary in the top level widget
        :param canvas: (tk.Canvas): the target canvas for the top level widget
        """
        # Get the bounding box of all items
        bbox = canvas.bbox("all")

        # Add allowance on top and at the bottom
        bbox = (bbox[0], bbox[1] - self.top_allowance, bbox[2], bbox[3] + self.bottom_allowance)

        # Update scroll region to include all objects
        canvas.update_idletasks()
        canvas.config(scrollregion=bbox)
