"""
This module displays all stages and handles the data collection, processing and transition in the
normal concrete mix design stages
"""

from core.logic.helpers.output_helpers import color_entry, load_tk_image
from core.utils.themes import *
from core.utils.file_paths import optimix_paths

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class StageOne(tk.Frame):
    """
    Displays all widgets for the mix design stage one,
        - collects the input data
        - processes the input data for design and report viewing
        
    Attributes:
        - master_si `tk.Frame`: The main content frame
        - analyzer `MixDesignAnalyzer`: Object for backend logic
        - controller `tk.Frame()`: Controller for accessing the main frame
        
    Methods:
        - display_fimages(): Displays images for the UI
        - display_entries(): Displays the entries
        - set_active(): Shows that an entry is active by changing its color
        - display_checkbutton(): Shows 'Less than 20 results' checkbutton
        - display_menus(): Displays the cement and aggregate type menu selections
        - collect_data(): Saves the data supplied by the user in MixDesignAnalyzer class
        - set_inputs_to_default(): Resets the supplied inputs
        - special_check(): Special check for the input checks
        - check_fill_status(): Checks the inputs for possible errors
        - calculate(): Perform backend calculations based on the saved inputs
    """

    def __init__(self, master_si, analyzer, controller):
        super().__init__(master_si, bg=BG)
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=True)

        # Update the page index
        self.controller.index = 0

        # Instantiate the mix design analyzer
        self.analyzer = analyzer

        # Define instance variables with default values
        self.selected_fagg_type = None
        self.fagg_type = None
        self.cagg_type = None
        self.selected_cagg_type = None
        self.toggle_status = None
        self.days = None
        self.x_strength = None
        self.s_margin = None
        self.spec_k = None
        self.max_fc_ratio = None
        self.sd = None
        self.defective_rate = None
        self.toggle = None
        self.cement_type = None
        self.selected_cement_type = None
        self.stage_frame = None
        self.cement_default_selection = None
        self.c_default_selection = None
        self.f_default_selection = None
        self.fill_status = None

        # Create a canvas that holds all widgets for design stage one
        self.stage_canvas = tk.Canvas(
            self,
            bg=BG,
            width=770,
            height=550,
            highlightthickness=0
        )
        self.stage_canvas.place(x=230, y=0)
        self.stage_canvas.pack(fill=tk.BOTH, expand=True)

        # Display figma imported images
        self.display_fimages()

        # Display entries
        self.display_entries()

        # Make a list of all entries, color change and perform numerical check
        self.entry_list = [self.x_strength, self.days, self.defective_rate,
                           self.sd, self.spec_k, self.s_margin, self.max_fc_ratio]

        self.set_active()

        # Display the 20 result limit checkbutton
        self.display_checkbutton()

        # Display the Cement aggregate type option menus
        self.display_menus()

    def display_fimages(self):
        """
        Displays preset images
        """
        # Display the stage instructions
        instruction_i = load_tk_image(optimix_paths.doe_assets['si_i'])
        self.stage_canvas.si_i = instruction_i
        self.stage_canvas.create_image(
            504.04998779296875,
            192.36000061035156,
            image=instruction_i
        )

        # Display UI lines (for distinction and aesthetics)
        li = load_tk_image(optimix_paths.doe_assets['line_i'])
        lii = load_tk_image(optimix_paths.doe_assets['line_ii'])

        self.stage_canvas.line_i = li
        self.stage_canvas.line_ii = lii

        self.stage_canvas.create_image(
            574.0,
            77.0,
            image=li
        )

        self.stage_canvas.create_image(
            593.0,
            370.0,
            image=lii
        )

        # Display entry texts
        entry_texts = load_tk_image(optimix_paths.doe_assets['entry_captions'])
        self.stage_canvas.entry_caption = entry_texts
        self.stage_canvas.create_image(
            577.2250061035156,
            292.05750274658203,
            image=entry_texts
        )

    def display_entries(self):
        """
        Handles display, color transitions and data storage in tk entry widgets
        """

        # Entry 1 (Characteristic Strength)
        # Return previously saved values
        x_strength_value = tk.StringVar(self.stage_canvas)
        x_strength_value.set(self.analyzer.data['Specified variables']['Characteristic Strength'])

        # Display entry 1
        self.x_strength = tk.Entry(
            self.stage_canvas,
            textvariable=x_strength_value,
            background=BG,
            foreground=white_color,
            font=lato,
            highlightthickness=1
        )
        self.x_strength.place(
            x=457.0,
            y=99.0,
            width=77.0,
            height=28.0
        )

        # Entry 2 (Curing Days)
        # Return previously saved values
        days_value = tk.StringVar(self.stage_canvas)
        days_value.set(self.analyzer.data['Specified variables']['Curing Days'])

        self.days = tk.Entry(
            self.stage_canvas,
            textvariable=days_value,
            background=BG,
            foreground=white_color,
            font=lato,
            highlightthickness=1
        )
        self.days.place(
            x=667.0,
            y=99.0,
            width=63.0,
            height=28.0
        )

        # Entry 3 (Defective Rate)
        # Return previously saved values
        defective_rate_value = tk.StringVar(self.stage_canvas)
        defective_rate_value.set(self.analyzer.data['Specified variables']['Defective Rate'])

        self.defective_rate = tk.Entry(
            self.stage_canvas,
            textvariable=defective_rate_value,
            background=BG,
            foreground=white_color,
            font=lato,
            highlightthickness=1
        )
        self.defective_rate.place(
            x=457.0,
            y=150.0,
            width=77.0,
            height=28.0
        )

        # Entry 4 (Custom Standard Deviation)
        # Return previously saved values
        sd_value = tk.StringVar(self.stage_canvas)
        sd_value.set(self.analyzer.data['Additional info']['Standard Deviation'])

        self.sd = tk.Entry(
            self.stage_canvas,
            textvariable=sd_value,
            background=BG,
            foreground=white_color,
            font=lato,
            highlightthickness=1
        )
        self.sd.place(
            x=457.0,
            y=395.0,
            width=77.0,
            height=28.0
        )

        # Entry 5 (Specified k)
        # Return previously saved values
        spec_k_value = tk.StringVar(self.stage_canvas)
        spec_k_value.set(self.analyzer.data['Additional info']['Specified k'])

        self.spec_k = tk.Entry(
            self.stage_canvas,
            textvariable=spec_k_value,
            background=BG,
            foreground=white_color,
            font=lato,
            highlightthickness=1
        )
        self.spec_k.place(
            x=836.0,
            y=395.0,
            width=63.0,
            height=28.0
        )

        # Entry 6 (Specified Margin)
        # Return previously saved values
        s_margin_value = tk.StringVar(self.stage_canvas)
        s_margin_value.set(self.analyzer.data['Specified variables']['Specified Margin'])

        self.s_margin = tk.Entry(
            self.stage_canvas,
            textvariable=s_margin_value,
            background=BG,
            foreground=white_color,
            font=lato,
            highlightthickness=1
        )
        self.s_margin.place(
            x=457.0,
            y=454.0,
            width=77.0,
            height=28.0
        )

        # Entry 7 (Maximum free water-cement ratio)
        # Return previously saved values
        max_fc_value = tk.StringVar(self.stage_canvas)
        max_fc_value.set(self.analyzer.data['Specified variables']['Maximum free water-cement ratio'])

        self.max_fc_ratio = tk.Entry(
            self.stage_canvas,
            textvariable=max_fc_value,
            background=BG,
            foreground=white_color,
            font=lato,
            highlightthickness=1
        )
        self.max_fc_ratio.place(
            x=836.0,
            y=454.0,
            width=63.0,
            height=28.0
        )

    def set_active(self):
        """
        >   Colors every entry as long as the entry is active,
            the color is selected randomly from 100 colors in an angular gradient,
            check `colors` in the `themes` module for more
        """
        # Color every entry upon focus
        [color_entry(entry=form) for form in self.entry_list]

    def display_checkbutton(self):
        """
        Displays the "Less than 20 results" check button
        """
        # Less Than 20 results toggle
        self.toggle_status = tk.IntVar(self.stage_canvas,
                                       value=self.analyzer.data['Specified variables']['Less Than 20 Results'])

        # Create the checkbutton
        self.toggle = tk.Checkbutton(
            master=self.stage_canvas,
            variable=self.toggle_status,
            takefocus=False,
            cursor='hand2',
            background=BG,
            activebackground=BG,
            selectcolor=BG,
            foreground=np.random.choice(colors),
            activeforeground=np.random.choice(colors))
        self.toggle.place(
            x=640.0,
            y=155.0,
        )

    def display_menus(self):
        """
        Displays the following:
        > The Cement type option menu, either OPC, RHPC, SRPC
        > The coarse aggregate type; crushed / uncrushed
        > The fine aggregate type: crushed / uncrushed
        """

        # Create a custom style for the option menu widget
        menu_style = ttk.Style()
        menu_style.configure(
            'Custom.TMenubutton',
            background=ALT_BG,
            activebackground=BG,
            activbeforeground=white_color,
            foreground=white_color,
            font=lato,
            arrowcolor=np.random.choice(colors),
            highlightbackground=BG
        )
        menu_style.map(
            'Custom.TMenubutton',
            background=[('active', BG)],
            highlightcolor=[('focus', BG)]
        )        
        
        # Cement type selection
        cement_types = ['OPC', 'SRPC', 'RHPC']

        # Selected Option
        self.selected_cement_type = tk.StringVar(self.stage_canvas)

        # Make a default selection
        self.cement_default_selection = self.analyzer.data['Specified variables']['Cement Type']

        # Cement type OptionMenu
        self.cement_type = ttk.OptionMenu(
            self.stage_canvas,
            self.selected_cement_type,
            self.cement_default_selection,
            style='Custom.TMenubutton',
            *cement_types
        )

        # Display the cement type selection
        self.cement_type.place(
            x=274.0,
            y=240.0,
            width=77,
            height=35
        )

        # Customize the cement menu
        self.cement_type.config(cursor='hand2')

        # Customize the cement menu dropdown
        self.cement_type['menu'].config(
            background=BG,
            activebackground=ALT_BG,
            selectcolor=cement_select_color,
            borderwidth=0,
            fg=white_color,
            font=lato,
            relief='sunken'
        )

        # Coarse Aggregate type selection
        agg_types = ['Crushed', 'Uncrushed']

        # Selected coarse aggregate type
        self.selected_cagg_type = tk.StringVar(self.stage_canvas)

        # Make a default selection
        self.c_default_selection = self.analyzer.data['Additional info']['Coarse Aggregate Type']

        # Coarse Aggregate type OptionMenu
        self.cagg_type = ttk.OptionMenu(
            self.stage_canvas,
            self.selected_cagg_type,
            self.c_default_selection,
            style='Custom.TMenubutton',
            *agg_types
        )

        # Customize the coarse aggregate menu
        self.cagg_type.config(cursor='hand2')

        # Customize the cement menu dropdown
        self.cagg_type['menu'].config(
            background=BG,
            activebackground=ALT_BG,
            selectcolor=cagg_select_color,
            borderwidth=0,
            fg=white_color,
            font=lato,
            relief='sunken'
        )

        # Display the coarse aggregate option menu
        self.cagg_type.place(
            x=493.0,
            y=240.0,
            width=120,
            height=35
        )

        # Selected fine aggregate type
        self.selected_fagg_type = tk.StringVar(self.stage_canvas)

        # Make a default selection
        self.f_default_selection = self.analyzer.data['Additional info']['Fine Aggregate Type']

        # Fine Aggregate type OptionMenu
        self.fagg_type = ttk.OptionMenu(
            self.stage_canvas,
            self.selected_fagg_type,
            self.f_default_selection,
            style='Custom.TMenubutton',
            *agg_types
        )

        # Customize the fine aggregate menu
        self.fagg_type.config(cursor='hand2')

        # Customize the fine aggregate menu dropdown
        self.fagg_type['menu'].config(
            background=BG,
            activebackground=ALT_BG,
            selectcolor=fagg_select_color,
            borderwidth=0,
            fg=white_color,
            font=lato,
            relief='sunken'
        )

        # Display the fine aggregate option menu
        self.fagg_type.place(
            x=746.0,
            y=240.0,
            width=120,
            height=35
        )

    def collect_data(self):
        """
        Retrieves data from every widget
        """
        # Characteristic strength
        self.analyzer.sync_input(self.x_strength, 'Specified variables', 'Characteristic Strength')

        # Curing days
        self.analyzer.sync_input(self.days, 'Specified variables', 'Curing Days')

        # Defective rate
        self.analyzer.sync_input(self.defective_rate, 'Specified variables', 'Defective Rate')

        # Custom standard deviation
        self.analyzer.sync_input(self.sd, 'Additional info', 'Standard Deviation')

        # Specified k
        self.analyzer.sync_input(self.spec_k, 'Additional info', 'Specified k')

        # Specified margin
        self.analyzer.sync_input(self.s_margin, 'Specified variables', 'Specified Margin')

        # Maximum free water-cement ratio
        self.analyzer.sync_input(self.max_fc_ratio, 'Specified variables',
                                 'Maximum free water-cement ratio')

        # Less than 20 results toggle
        self.analyzer.sync_input(self.toggle, 'Specified variables',
                                 'Less Than 20 Results', var_name=self.toggle_status)

        # Cement Selection
        self.analyzer.sync_input(self.cement_type, 'Specified variables',
                                 'Cement Type', option_var=self.selected_cement_type)

        # Fine Aggregate type selection
        self.analyzer.sync_input(self.fagg_type, 'Additional info',
                                 'Fine Aggregate Type', option_var=self.selected_fagg_type)

        # Coarse Aggregate type selection
        self.analyzer.sync_input(self.cagg_type, 'Additional info',
                                 'Coarse Aggregate Type', option_var=self.selected_cagg_type)

    def set_inputs_to_default(self):
        """
        Sets all entries to default
        """
        # Set all entries to their default values
        # noinspection PyUnresolvedReferences
        [entry.delete(0, tk.END) for entry in self.entry_list]

    def special_check(self):
        """
        This method checks whether k and percentage defectiveness are empty,
        This is needed cause it requires calculation to be performed first
        """
        fill_status = []
        messagebox_has_been_shown = False
        # Save data before selection
        self.collect_data()

        # Perform the special check in the defined analyzer class
        self.analyzer.special_check()

        # Case where both defective rate and k are both empty
        if self.analyzer.empty_defective_rate_and_k:
            if messagebox_has_been_shown:
                # Update the state alone, no need to repeat the messagebox
                # messagebox_has_been_shown = True
                pass

                # Update the fill state
                fill_status.append(False)

            else:
                # where both boxes and margin are empty
                messagebox.showerror(
                    title="Input Required",
                    message="Please specify any of the following:\n\n"
                            "• Margin (N/mm\u00b2), \n"
                            "• Defective rate (%),\n"
                            "• k, an appropriate value allowed for percentage defectives below characteristic"
                            " strength.",
                    parent=self.stage_canvas
                )

                # Update message display status
                # messagebox_has_been_shown = True

                # Update the state
                fill_status.append(False)

        else:
            # The two inputs are valid
            fill_status.append(True)

        # Update the state
        self.fill_status = fill_status

    def check_fill_status(self):
        """
        Checks the fill status for compulsory entries.
        Returns False to a fill_status list if any of the entries are empty.
        Empty entries (the compulsory ones) will render the calculations useless.
        """
        fill_status = []
        messagebox_has_been_shown = False

        # Deal with the errors for the main entries
        for entry in [self.x_strength, self.days]:
            value = entry.get().strip()

            if not value or (value and not value.replace('.', '').isdigit()):

                if messagebox_has_been_shown:
                    # Update the state alone, no need to repeat the messagebox
                    messagebox_has_been_shown = True

                    # Update the fill state
                    fill_status.append(False)
                else:
                    # If the entry is empty or the user entered a non-numeric value, display an error message
                    messagebox.showerror(
                        title="Invalid input",
                        message="Please input valid values for the specified requirements",
                        parent=self.stage_canvas
                    )

                    # Update message display status
                    messagebox_has_been_shown = True

                    # Clear the entry
                    entry.delete(0, tk.END)

                    # Update the state
                    fill_status.append(False)

            else:
                # The input is valid
                fill_status.append(True)

        # Deal with entry errors for the remaining entries.
        for entry in [text_box for text_box in self.entry_list if text_box not in [self.x_strength, self.days]]:
            value = entry.get().strip()

            if value and not value.replace('.', '').isdigit():
                if messagebox_has_been_shown:
                    # Update the state alone, no need to repeat the messagebox
                    messagebox_has_been_shown = True

                    # Update the fill state
                    fill_status.append(False)
                else:
                    # If the entry is empty or the user entered a non-numeric value, display an error message
                    messagebox.showerror(
                        title="Invalid input",
                        message="Please input valid values",
                        parent=self.stage_canvas
                    )

                    # Update message display status
                    messagebox_has_been_shown = True

                    # Clear the entry
                    entry.delete(0, tk.END)

                    # Update the state
                    fill_status.append(False)

            else:
                # The input is valid
                fill_status.append(True)

        self.fill_status = fill_status

    def calculate(self):
        """
        Performs mix design calculations on the mix design data class (DOE method)
        Also given that the compulsory entries have been filled
        """
        # Perform concrete mix design using British DOE method
        self.analyzer.calculate_k()
        self.analyzer.calculate_sd()
        self.analyzer.calculate_margin(mode='DOE')
        self.analyzer.calculate_target_mean_strength(mode='DOE')
        self.analyzer.calculate_approx_strength(mode='DOE')
        self.analyzer.calculate_fwc_ratio(mode='DOE')


class StageTwo(tk.Frame):
    """
    Displays all widgets for the mix design stage two
        - collects the input data
        - processes the input data for design and report viewing

    Attributes:
        - master_sii `tk.Frame`: The main content frame
        - analyzer `MixDesignAnalyzer`: Object for backend logic
        - controller `tk.Frame()`: Controller for accessing the parent frame

    Methods:
        - display_fimages(): Displays images for the UI
        - display_menus(): Displays the cement and aggregate type menu selections
        - display_checkbuttons(): Aggregate size selections
        - on_slump_value_selected(): Simultaneous vebe time selection
        - on_vebe_time_selected(): Simultaneous slump time selection
        - collect_data(): Saves the data supplied by the user in MixDesignAnalyzer class
        - set_inputs_to_default(): Resets the supplied inputs
        - check_fill_status(): Checks the inputs for possible errors
        - calculate(): Perform backend calculations based on the saved inputs
    """

    def __init__(self, master_sii, analyzer, controller):
        super().__init__(master_sii, bg=BG)
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=True)

        # Update the page index
        self.controller.index = 1

        # Instantiate the mix design analyzer
        self.analyzer = analyzer

        # Instantiate some default objects
        self.vebe = None
        self.vebe_default_selection = None
        self.selected_vebe = None
        self.slump = None
        self.slump_default_selection = None
        self.selected_slump = None
        self.forty_mm_agg = None
        self.forty_status = None
        self.twenty_mm_agg = None
        self.twenty_status = None
        self.ten_mm_agg = None
        self.ten_status = None
        self.fill_status = None

        # Create a canvas that holds all widgets for design stage two
        self.stage_canvas = tk.Canvas(
            self,
            bg=BG,
            width=770,
            height=550,
            highlightthickness=0
        )
        self.stage_canvas.place(x=230, y=0)
        self.stage_canvas.pack(fill=tk.BOTH, expand=True)

        # Display figma imported images
        self.display_fimages()

        # Display the slump selection and the vebe time selection
        self.display_menus()

        # Display check buttons for multiple aggregate sizes
        self.display_checkbuttons()

    def display_fimages(self):
        """
        Displays preset images
        """
        # Display the stage instructions
        instruction_ii = load_tk_image(optimix_paths.doe_assets['si_ii'])
        self.stage_canvas.si_ii = instruction_ii
        self.stage_canvas.create_image(
            476.45001220703125,
            192.36000061035156,
            image=instruction_ii
        )

        # Display the UI lines
        liii = load_tk_image(optimix_paths.doe_assets['line_iii'])
        liv = load_tk_image(optimix_paths.doe_assets['line_iv'])

        self.stage_canvas.line_iii = liii
        self.stage_canvas.line_iv = liv

        self.stage_canvas.create_image(
            589.0,
            78.0,
            image=liii
        )

        self.stage_canvas.create_image(
            592.0,
            368.0,
            image=liv
        )

        # Display the slump selection caption
        s_caption = load_tk_image(optimix_paths.doe_assets['slump'])
        self.stage_canvas.slump = s_caption
        self.stage_canvas.create_image(
            337.6927490234375,
            117.95249938964844,
            image=s_caption
        )

        # Display the vebe time selection caption
        v_caption = load_tk_image(optimix_paths.doe_assets['vebe'])
        self.stage_canvas.vebe = v_caption
        self.stage_canvas.create_image(
            631.7715454101562,
            117.95249938964844,
            image=v_caption
        )

    def display_menus(self):
        """
        Displays the option menus for retrieving the slump value or vebe time values.

        The two option menus are simultaneous, selecting 0-10mm will imply >12s for example.
        The globally set option menu style is automatically inherited
        """
        # Selected Options
        self.selected_slump = tk.StringVar(self.stage_canvas)
        self.selected_vebe = tk.StringVar(self.stage_canvas)

        # Slump value & vebe time selection options
        slump_categories = ['0-10mm', '10-30mm', '30-60mm', '60-180mm']
        vebe_categories = ['>12s', '6-12s', '3-6s', '0-3s']

        # Make default selections
        self.slump_default_selection = self.analyzer.data['Specified variables']['Slump']
        self.vebe_default_selection = vebe_categories[0]

        # Slump OptionMenu
        self.slump = ttk.OptionMenu(
            self.stage_canvas,
            self.selected_slump,
            self.slump_default_selection,
            style='Custom.TMenubutton',
            command=lambda event: self.on_slump_value_selected(),
            *slump_categories
        )

        # Display the slump selection
        self.slump.place(
            x=274.0,
            y=140,
            width=120,
            height=35
        )

        # Customize the slump menu
        self.slump.config(cursor='hand2')

        # Customize the slump menu dropdown
        self.slump['menu'].config(
            background=BG,
            activebackground=ALT_BG,
            selectcolor=slump_select_color,
            borderwidth=0,
            fg=white_color,
            font=lato,
            relief='sunken'
        )

        # Vebe time OptionMenu
        self.vebe = ttk.OptionMenu(
            self.stage_canvas,
            self.selected_vebe,
            self.vebe_default_selection,
            style='Custom.TMenubutton',
            command=lambda event: self.on_vebe_time_selected(),
            *vebe_categories
        )

        # Display the vebe selection
        self.vebe.place(
            x=560,
            y=140,
            width=120,
            height=35
        )

        # Customize the vebe menu
        self.vebe.config(cursor='hand2')

        # Customize the vebe menu dropdown
        self.vebe['menu'].config(
            background=BG,
            activebackground=ALT_BG,
            selectcolor=vebe_select_color,
            borderwidth=0,
            fg=white_color,
            font=lato,
            relief='sunken'
        )

    def display_checkbuttons(self):
        """
        Displays the checkbuttons for the 10mm, 20mm and 40mm aggregate sizes
        """
        # 10mm checkbutton
        self.ten_status = tk.IntVar(self.stage_canvas,
                                    value=self.analyzer.data['Specified variables']['10mm'])

        # Create the checkbutton for 10mm aggregate size
        self.ten_mm_agg = tk.Checkbutton(
            master=self.stage_canvas,
            variable=self.ten_status,
            takefocus=False,
            cursor='hand2',
            background=BG,
            offvalue=0,
            onvalue=10,
            activebackground=BG,
            selectcolor=BG,
            foreground='white',
            activeforeground='white',
            borderwidth=0,
            text='10mm',
            font=ubuntu,
            relief='groove')
        self.ten_mm_agg.place(
            x=274.0,
            y=396
        )

        # 20mm checkbutton
        self.twenty_status = tk.IntVar(self.stage_canvas,
                                       value=self.analyzer.data['Specified variables']['20mm'])

        # Create the checkbutton for 20mm aggregate size
        self.twenty_mm_agg = tk.Checkbutton(
            master=self.stage_canvas,
            variable=self.twenty_status,
            takefocus=False,
            cursor='hand2',
            background=BG,
            activebackground=BG,
            selectcolor=BG,
            offvalue=0,
            onvalue=20,
            foreground='white',
            activeforeground='white',
            borderwidth=0,
            text='20mm',
            font=ubuntu,
            relief='groove'
        )
        self.twenty_mm_agg.place(
            x=382,
            y=396,
        )

        # 40mm checkbutton
        self.forty_status = tk.IntVar(self.stage_canvas,
                                      value=self.analyzer.data['Specified variables']['40mm'])

        # Create the checkbutton for 10mm aggregate size
        self.forty_mm_agg = tk.Checkbutton(
            master=self.stage_canvas,
            variable=self.forty_status,
            takefocus=False,
            cursor='hand2',
            background=BG,
            activebackground=BG,
            selectcolor=BG,
            offvalue=0,
            onvalue=40,
            foreground='white',
            activeforeground='white',
            borderwidth=0,
            text='40mm',
            font=ubuntu,
            relief='groove')
        self.forty_mm_agg.place(
            x=490,
            y=396,
        )

    def on_slump_value_selected(self):
        """
        Sets the vebe time range option menu simultaneously
        """
        # Retrieve the slump selection
        selected_option = self.selected_slump.get()

        if selected_option == '0-10mm':
            self.selected_vebe.set('>12s')
        elif selected_option == '10-30mm':
            self.selected_vebe.set('6-12s')
        if selected_option == '30-60mm':
            self.selected_vebe.set('3-6s')
        elif selected_option == '60-180mm':
            self.selected_vebe.set('0-3s')

    def on_vebe_time_selected(self):
        """
        Sets the slump value range option menu simultaneously
        """
        # Retrieve the vebe selection
        selected_option = self.selected_vebe.get()

        if selected_option == '>12s':
            self.selected_slump.set('0-10mm')
        elif selected_option == '6-12s':
            self.selected_slump.set('10-30mm')
        elif selected_option == '3-6s':
            self.selected_slump.set('30-60mm')
        elif selected_option == '0-3s':
            self.selected_slump.set('60-180mm')

    def collect_data(self):
        """
        Retrieves data from every widget
        """
        # Slump type Selection
        self.analyzer.sync_input(self.slump, 'Specified variables',
                                 'Slump', option_var=self.selected_slump)

        # 10mm aggregate size toggle
        self.analyzer.sync_input(self.ten_mm_agg, 'Specified variables',
                                 '10mm', var_name=self.ten_status)

        # 20mm aggregate size toggle
        self.analyzer.sync_input(self.twenty_mm_agg, 'Specified variables',
                                 '20mm', var_name=self.twenty_status)

        # 40mm aggregate size toggle
        self.analyzer.sync_input(self.forty_mm_agg, 'Specified variables',
                                 '40mm', var_name=self.forty_status)

    def set_inputs_to_default(self):
        """Sets all text entries and selection to default"""
        pass

    def check_fill_status(self):
        """
        Checks the fill status for compulsory entries
        """
        fill_status = []
        messagebox_has_been_shown = False

        agg_sizes = [self.ten_status.get(),
                     self.twenty_status.get(),
                     self.forty_status.get()]

        # Creates the list of whether the checkbuttons are ticked or not ticked
        for aggregate in agg_sizes:
            if aggregate == 0:
                fill_status.append(False)
            else:
                fill_status.append(True)

        # Checks if all  the aggregate sizes are unchecked (have a value of zero)
        if all(element == 0 for element in fill_status):
            output_status = [False, False]
            self.fill_status = output_status

            if messagebox_has_been_shown:
                # Update the state alone, no need to repeat the messagebox
                # messagebox_has_been_shown = True
                pass

            else:
                # If the entry is empty or the user entered a non-numeric value, display an error message
                messagebox.showerror(
                    title="Invalid input",
                    message="Select an aggregate size",
                    parent=self.stage_canvas
                )

                # Update message display status
                # messagebox_has_been_shown = True

        else:
            output_status = [True, True]
            self.fill_status = output_status

    def calculate(self):
        """
        Performs mix design calculations on the mix design data class (DOE method)
        Also given that the compulsory entries have been filled
        """
        self.analyzer.calculate_fw_content(mode='DOE')


class StageThree(tk.Frame):
    """Displays all widgets for the mix design stage three
        - collects the input data
        - processes the input data for design and report viewing

    Attributes:
        - master_siii `tk.Frame`: The main content frame
        - analyzer `MixDesignAnalyzer`: Object for backend logic
        - controller `tk.Frame()`: Controller for accessing the main frame

    Methods:
        - display_fimages(): Displays images for the UI
        - display_entries(): Displays the entries
        - set_active(): Shows that an entry is active by changing its color
        - collect_data(): Saves the data supplied by the user in MixDesignAnalyzer class
        - set_inputs_to_default(): Resets the supplied inputs
        - check_fill_status(): Checks the inputs for possible errors
        - calculate(): Perform backend calculations based on the saved inputs
    """

    def __init__(self, master_siii, analyzer, controller):
        super().__init__(master_siii, bg=BG)
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=True)

        # Update the page index
        self.controller.index = 2

        self.analyzer = analyzer

        # Define instance variables with default values
        self.max_c = None
        self.min_c = None
        self.fill_status = None

        # Create a canvas that holds all widgets for design stage three
        self.stage_canvas = tk.Canvas(
            self,
            bg=BG,
            width=770,
            height=550,
            highlightthickness=0
        )
        self.stage_canvas.place(x=230, y=0)
        self.stage_canvas.pack(fill=tk.BOTH, expand=True)

        # Display figma imported images
        self.display_fimages()

        # Display entries
        self.display_entries()

        # Make a list of all entries, color change and perform numerical check
        self.entry_list = [self.max_c, self.min_c]
        self.set_active()

    def display_fimages(self):
        """Displays UI images"""
        # Display the stage instructions
        instruction_iii = load_tk_image(optimix_paths.doe_assets['si_iii'])
        self.stage_canvas.si_iii = instruction_iii
        self.stage_canvas.create_image(
            570.7200012207031,
            47.2550048828125,
            image=instruction_iii
        )

        # Display the UI line
        liii = load_tk_image(optimix_paths.doe_assets['ui_line'])
        self.stage_canvas.line_iii = liii

        self.stage_canvas.create_image(
            589,
            78,
            image=liii
        )

        # Display entry texts
        max_c_content = load_tk_image(optimix_paths.doe_assets['max_c'])
        self.stage_canvas.max_c = max_c_content
        self.stage_canvas.create_image(
            434.7124938964844,
            130.0574951171875,
            image=max_c_content
        )

        min_c_content = load_tk_image(optimix_paths.doe_assets['min_c'])
        self.stage_canvas.min_c = min_c_content
        self.stage_canvas.create_image(
            434.7124938964844,
            202.0574951171875,
            image=min_c_content
        )

    def display_entries(self):
        """
        Handles display, color transitions and data storage in tk entry widgets
        """

        # Entry 1 (Maximum Cement Content)
        # Return previously saved values
        max_c_value = tk.StringVar(self.stage_canvas)
        max_c_value.set(self.analyzer.data['Specified variables']['Maximum cement content'])

        # Display entry 1
        self.max_c = tk.Entry(
            self.stage_canvas,
            textvariable=max_c_value,
            background=BG,
            foreground=white_color,
            font=lato,
            highlightthickness=1
        )
        self.max_c.place(
            x=457.0,
            y=115,
            width=77.0,
            height=28.0
        )

        # Entry 2 (Minimum Cement Content)
        # Return previously saved values
        min_c_value = tk.StringVar(self.stage_canvas)
        min_c_value.set(self.analyzer.data['Specified variables']['Minimum cement content'])

        # Display entry 2
        self.min_c = tk.Entry(
            self.stage_canvas,
            textvariable=min_c_value,
            background=BG,
            foreground=white_color,
            font=lato,
            highlightthickness=1
        )
        self.min_c.place(
            x=457,
            y=188,
            width=77.0,
            height=28.0
        )

    def set_active(self):
        """
        >   Colors every entry as long as the entry is active,
            the color is selected randomly from 100 colors in an angular gradient,
            check `colors` in the `themes` module for more

        `color_entry` and has been created in `config.core`
        """
        # Color every entry upon focus
        [color_entry(entry=form) for form in self.entry_list]

    def collect_data(self):
        """
        Retrieves data from every widget
        """
        # Maximum Cement Content
        self.analyzer.sync_input(self.max_c, 'Specified variables', 'Maximum cement content')

        # Minimum Cement Content
        self.analyzer.sync_input(self.min_c, 'Specified variables', 'Minimum cement content')

    def set_inputs_to_default(self):
        """Sets all text entries and selections to default"""
        # Set all entries to their default values
        # noinspection PyUnresolvedReferences
        [entry.delete(0, tk.END) for entry in self.entry_list]

    def check_fill_status(self):
        """
        Checks the fill status for compulsory entries
        """
        messagebox_has_been_shown = False
        fill_status = None

        # Perform background calculations before proceeding to check
        self.collect_data()
        self.analyzer.calculate_cement_content(mode='DOE')

        if self.analyzer.invalid_cc_entry:
            # The user entered a non-numeric value, display an error message
            if messagebox_has_been_shown:
                # Update the state alone, no need to repeat the messagebox
                # messagebox_has_been_shown = True
                pass

            else:
                # If the user entered a non-numeric value, display an error message
                messagebox.showerror(
                    title="Invalid input",
                    message="Input valid values for the cement content limits.",
                    parent=self.stage_canvas
                )

                # Update message display status
                # messagebox_has_been_shown = True
                pass

                [entry.delete(0, tk.END) for entry in self.entry_list]
                fill_status = [False, False]

        elif not self.analyzer.feasibility_status:
            # If calculated cement content is higher than specified maximum, show warning
            fill_status = [False, False]
            messagebox.showwarning(
                title="Warning:  Infeasible Specification",
                message=("The selected materials may not meet the simultaneous "
                         "requirements of strength and workability.\n\n"
                         "Consider the following options:\n"
                         "  • Change the type of cement.\n"
                         "  • Modify the type and maximum size of aggregate.\n"
                         "  • Adjust the level of workability of the concrete.\n"
                         "  • Use a water-reducing admixture."),
                parent=self.stage_canvas
            )
            # Clear the entry
            self.max_c.delete(0, tk.END)

            # Reset the feasibility status
            self.analyzer.feasibility_status = True

        elif self.analyzer.feasibility_status:
            # Continue..
            fill_status = [True, True]

        else:
            # Proceed with background design, there are a few more checks though:
            if self.analyzer.min_is_more_than_max:

                if messagebox_has_been_shown:
                    # Update the state alone, no need to repeat the messagebox
                    # messagebox_has_been_shown = True
                    pass

                else:
                    # If the entry is empty or the user entered a non-numeric value, display an error message
                    messagebox.showerror(
                        title="Invalid Limits",
                        message="Supply valid limits.",
                        parent=self.stage_canvas
                    )

                    # Update message display status
                    # messagebox_has_been_shown = True

                    [entry.delete(0, tk.END) for entry in self.entry_list]
                    self.analyzer.min_is_more_than_max = False
                    fill_status = [False, False]

            elif not self.analyzer.min_is_more_than_max:
                # The input is valid
                fill_status = [True, True]

        self.fill_status = fill_status

    def calculate(self):
        """
        Performs mix design calculations on the mix design data class (DOE method)
        Also given that the compulsory entries have been filled
        """
        self.analyzer.calculate_cement_content(mode='DOE')


class StageFour(tk.Frame):
    """
    Displays all widgets for the mix design stage four
        - collects the input data
        - processes the input data for design and report viewing

    Attributes:
        - master_siv `tk.Frame`: The main content frame
        - analyzer `MixDesignAnalyzer`: Object for backend logic
        - controller `tk.Frame()`: Controller for accessing the main frame

    Methods:
        - display_fimages(): Displays images for the UI
        - display_entries(): Displays the entries
        - set_active(): Shows that an entry is active by changing its color
        - collect_data(): Saves the data supplied by the user in MixDesignAnalyzer class
        - set_inputs_to_default(): Resets the supplied inputs
        - check_fill_status(): Checks the inputs for possible errors
        - calculate(): Perform backend calculations based on the saved inputs
    """

    def __init__(self, master_siv, analyzer, controller):
        super().__init__(master_siv, bg=BG)
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=True)

        # Update the page index
        self.controller.index = 3

        self.analyzer = analyzer

        # Define instance variables with default values
        self.c_density = None
        self.rel_d_ssd = None
        self.fill_status = None

        # Create a canvas that holds all widgets for design stage four
        self.stage_canvas = tk.Canvas(
            self,
            bg=BG,
            width=770,
            height=550,
            highlightthickness=0
        )
        self.stage_canvas.place(x=230, y=0)
        self.stage_canvas.pack(fill=tk.BOTH, expand=True)

        # Display figma imported images
        self.display_fimages()

        # Display entries
        self.display_entries()

        # Make a list of all entries, color change and perform numerical check
        self.entry_list = [self.rel_d_ssd, self.c_density]
        self.set_active()

    def display_fimages(self):
        """Displays UI images"""

        # Display the stage instruction
        instruction_iv = load_tk_image(optimix_paths.doe_assets['instructions_tot_agg'])
        self.stage_canvas.instructions_iv = instruction_iv
        self.stage_canvas.create_image(
            560.7200012207031,
            47.2550048828125,
            image=instruction_iv
        )

        # Display the UI lines
        liv = load_tk_image(optimix_paths.doe_assets['ui_line'])
        self.stage_canvas.line_iv = liv

        self.stage_canvas.create_image(
            589,
            78,
            image=liv
        )

        # Display entry texts
        rel_d = load_tk_image(optimix_paths.doe_assets['rel_density'])
        self.stage_canvas.rel_density = rel_d
        self.stage_canvas.create_image(
            334.48748779296875,
            130.95249938964844,
            image=rel_d
        )

        c_density = load_tk_image(optimix_paths.doe_assets['conc_density'])
        self.stage_canvas.conc_density = c_density
        self.stage_canvas.create_image(
            434.7124938964844,
            202.72250366210938,
            image=c_density
        )

    def display_entries(self):
        """
        Handles display, color transitions and data storage in tk entry widgets
        """
        # Entry 1 (Relative density in ssd)
        # Return previously saved values
        ssd_value = tk.StringVar(self.stage_canvas)
        ssd_value.set(self.analyzer.data['Additional info']['Relative density of agg'])

        # Display entry 1
        self.rel_d_ssd = tk.Entry(
            self.stage_canvas,
            textvariable=ssd_value,
            background=BG,
            foreground=white_color,
            font=lato,
            highlightthickness=1
        )
        self.rel_d_ssd.place(
            x=457.0,
            y=115,
            width=77.0,
            height=28.0
        )

        # Entry 2 (Concrete density)
        # Return previously saved values
        c_density_value = tk.StringVar(self.stage_canvas)
        c_density_value.set(self.analyzer.data['Mix Parameters']['Concrete density'])

        # Display entry 2
        self.c_density = tk.Entry(
            self.stage_canvas,
            textvariable=c_density_value,
            background=BG,
            foreground=white_color,
            font=lato,
            highlightthickness=1
        )
        self.c_density.place(
            x=457,
            y=188,
            width=77.0,
            height=28.0
        )

    def set_active(self):
        """
        >   Colors every entry as long as the entry is active,
            the color is selected randomly from 100 colors in an angular gradient,
            check `colors` in the `themes` module for more
        >   Checks if the input is numerical, returns error message on exceptions
        """
        # Color every entry upon focus
        [color_entry(entry=form) for form in self.entry_list]

    def collect_data(self):
        """
        Retrieves data from every widget
        """
        # Relative density of SSD (SSD)
        self.analyzer.sync_input(self.rel_d_ssd, 'Additional info', 'Relative density of agg')

        # Concrete density
        self.analyzer.sync_input(self.c_density, 'Mix Parameters', 'Concrete density')

    def set_inputs_to_default(self):
        """Sets all text entries and selections to default"""
        # Set all entries to their default values
        # noinspection PyUnresolvedReferences
        [entry.delete(0, tk.END) for entry in self.entry_list]

    def check_fill_status(self):
        """
        Checks the fill status for compulsory entries
        """
        # Perform background calculations before proceeding to check
        self.collect_data()
        self.analyzer.ssd_check()   # This function updates the state of 'ssd_value_error' which is used below

        if self.analyzer.ssd_value_error or self.analyzer.invalid_ssd:
            # When there's a non-numeric input, proceed to display warnings
            pass
        else:
            self.analyzer.compute_wet_conc_density(mode='DOE')
            self.analyzer.override_density()
            self.analyzer.compute_total_agg_content(mode='DOE')

        fill_status = []
        messagebox_has_been_shown = False

        for entry in [self.rel_d_ssd, self.c_density]:

            if self.analyzer.ssd_value_error:

                if messagebox_has_been_shown:
                    # Update the state alone, no need to repeat the messagebox
                    messagebox_has_been_shown = True

                    # Update the fill state
                    fill_status.append(False)
                else:
                    # If the entry is empty or the user entered a non-numeric value, display an error message
                    messagebox.showerror(
                        title="Invalid input",
                        message="Please input valid values for the specified requirements",
                        parent=self.stage_canvas
                    )

                    # Update message display status
                    messagebox_has_been_shown = True

                    # Clear the entry
                    entry.delete(0, tk.END)

                    # Update the state
                    fill_status.append(False)

            elif self.analyzer.invalid_ssd:

                # When the specified ssd is not between 2.4 and 2.9
                if messagebox_has_been_shown:
                    # Update the state alone, no need to repeat the messagebox
                    messagebox_has_been_shown = True

                    # Update the fill state
                    fill_status.append(False)
                else:
                    # If the entry is empty or the user entered a value out of range, display an error message
                    messagebox.showerror(
                        title="Invalid input",
                        message="Please input a relative density between 2.4 and 2.9",
                        parent=self.stage_canvas
                    )

                    # Update message display status
                    messagebox_has_been_shown = True

                    # Clear the entry
                    entry.delete(0, tk.END)

                    # Update the state
                    fill_status.append(False)

            else:
                # The input is valid
                fill_status.append(True)

        self.fill_status = fill_status

    def calculate(self):
        """
        Performs mix design calculations on the mix design data class (DOE method)
        Also given that the compulsory entries have been filled
        """
        self.analyzer.ssd_check()
        self.analyzer.compute_wet_conc_density(mode='DOE')
        self.analyzer.override_density()
        self.analyzer.compute_total_agg_content(mode='DOE')


class StageFive(tk.Frame):
    """
    Displays all widgets for the mix design stage five
        - collects the input data
        - processes the input data for design and report viewing

    Attributes:
        - master_sv `tk.Frame`: The main content frame
        - analyzer `MixDesignAnalyzer`: Object for backend logic
        - controller `tk.Frame()`: Controller for accessing the main frame

    Methods:
        - display_fimages(): Displays images for the UI
        - display_entries(): Displays the entries
        - set_active(): Shows that an entry is active by changing its color
        - collect_data(): Saves the data supplied by the user in MixDesignAnalyzer class
        - set_inputs_to_default(): Resets the supplied inputs
        - check_fill_status(): Checks the inputs for possible errors
        - calculate(): Perform backend calculations based on the saved inputs
    """

    def __init__(self, master_sv, analyzer, controller):
        super().__init__(master_sv, bg=BG)
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=True)

        # Update the page index
        self.controller.index = 4

        self.analyzer = analyzer

        self.fagg_abs = None
        self.cagg_abs = None
        self.fill_status = None
        self.pp = None

        # Create a canvas that holds all widgets for design stage five
        self.stage_canvas = tk.Canvas(
            self,
            bg=BG,
            width=770,
            height=550,
            highlightthickness=0
        )
        self.stage_canvas.place(x=230, y=0)
        self.stage_canvas.pack(fill=tk.BOTH, expand=True)

        # Display figma imported images
        self.display_fimages()

        # Display percent passing entry
        self.display_entries()

        # A list of all entries, color change and perform numerical check
        self.entry_list = [self.pp, self.cagg_abs, self.fagg_abs]
        self.set_active()

    def display_fimages(self):
        """Displays UI images"""

        # Display the stage instructions
        instruction_v = load_tk_image(optimix_paths.doe_assets['instructions_v'])
        self.stage_canvas.instructions_v = instruction_v
        self.stage_canvas.create_image(
            487.2449951171875,
            49.36000061035156,
            image=instruction_v
        )

        instruction_iv_i = load_tk_image(optimix_paths.doe_assets['instructions_iv'])
        self.stage_canvas.instructions_iv_i = instruction_iv_i
        self.stage_canvas.create_image(
            479.125,
            330.2550048828125,
            image=instruction_iv_i
        )

        # Display UI lines
        lv = load_tk_image(optimix_paths.doe_assets['ui_line'])
        self.stage_canvas.line_v = lv

        self.stage_canvas.create_image(
            589,
            78,
            image=lv
        )

        lv_i = lv
        self.stage_canvas.line_v_i = lv_i

        self.stage_canvas.create_image(
            592.0,
            358.0,
            image=lv_i
        )

        # Display entry texts
        passing = load_tk_image(optimix_paths.doe_assets['percent_passing'])
        self.stage_canvas.perc_passing = passing
        self.stage_canvas.create_image(
            420.32000732421875,
            130.95249938964844,
            image=passing
        )

        oven_dry_fagg = load_tk_image(optimix_paths.doe_assets['ov_batch_fagg'])
        self.stage_canvas.oven_dry_fagg = oven_dry_fagg
        self.stage_canvas.create_image(
            421.0450134277344,
            399.9525146484375,
            image=oven_dry_fagg
        )

        oven_dry_cagg = load_tk_image(optimix_paths.doe_assets['ov_batch_cagg'])
        self.stage_canvas.oven_dry_cagg = oven_dry_cagg
        self.stage_canvas.create_image(
            421.0450134277344,
            470.9525146484375,
            image=oven_dry_cagg
        )

        # Display the assumption note
        assumption = load_tk_image(optimix_paths.doe_assets['note'])
        self.stage_canvas.note = assumption
        self.stage_canvas.create_image(
            507.9224853515625,
            195,
            image=assumption
        )

    def display_entries(self):
        """
        Handles display and data storage in the tk entry widget
        """

        # Entry 1 (Percentage passing)
        # Return previously saved values (60 % by default)
        pp_value = tk.StringVar(self.stage_canvas)
        pp_value.set(self.analyzer.data['Additional info']['Percentage passing 600um sieve'])

        # Display entry 1
        self.pp = tk.Entry(
            self.stage_canvas,
            textvariable=pp_value,
            background=BG,
            foreground=white_color,
            font=lato,
            highlightthickness=1
        )
        self.pp.place(
            x=457.0,
            y=115,
            width=77.0,
            height=28.0
        )

        # Entry 2 Fine aggregate absorption
        # Return previously saved values
        fagg_abs_value = tk.StringVar(self.stage_canvas)
        fagg_abs_value.set(self.analyzer.data['Additional info']['Absorption of Fine Aggregate'])

        # Display entry 2
        self.fagg_abs = tk.Entry(
            self.stage_canvas,
            textvariable=fagg_abs_value,
            background=BG,
            foreground=white_color,
            font=lato,
            highlightthickness=1
        )
        self.fagg_abs.place(
            x=457,
            y=381,
            width=77.0,
            height=28.0
        )

        # Entry 2 Coarse aggregate absorption
        # Return previously saved values
        cagg_abs_value = tk.StringVar(self.stage_canvas)
        cagg_abs_value.set(self.analyzer.data['Additional info']['Absorption of Coarse Aggregate'])

        # Display entry 4
        self.cagg_abs = tk.Entry(
            self.stage_canvas,
            textvariable=cagg_abs_value,
            background=BG,
            foreground=white_color,
            font=lato,
            highlightthickness=1
        )
        self.cagg_abs.place(
            x=457,
            y=454,
            width=77.0,
            height=28.0
        )

    def set_active(self):
        """
        >   Colors every entry as long as the entry is active,
            the color is selected randomly from 100 colors in an angular gradient,
            check `colors` in the `themes` module for more
        >   Checks if the input is numerical, returns error message on exceptions
        """
        # Color every entry upon focus
        [color_entry(entry=form) for form in self.entry_list]

    def collect_data(self):
        """
        Retrieves data from every widget
        """
        # Percentage passing 600um sieve
        self.analyzer.sync_input(self.pp, 'Additional info', 'Percentage passing 600um sieve')

        # Absorption of fine aggregate
        self.analyzer.sync_input(self.fagg_abs, 'Additional info', 'Absorption of Fine Aggregate')

        # Absorption of coarse aggregate
        self.analyzer.sync_input(self.cagg_abs, 'Additional info', 'Absorption of Coarse Aggregate')

    def set_inputs_to_default(self):
        """Sets all text entries and selection to default"""
        # Set all entries to their default values
        # noinspection PyUnresolvedReferences
        [entry.delete(0, tk.END) for entry in self.entry_list]

    def check_fill_status(self):
        """
        Checks the fill status for compulsory entries
        """
        # Perform background calculations before proceeding to check
        self.collect_data()
        self.analyzer.compute_fine_agg_proportion(mode='DOE')
        self.analyzer.compute_agg_content(mode='DOE')
        self.analyzer.oven_dry_batching()
        self.analyzer.proportion_coarse_agg()

        fill_status = []

        for entry in [self.pp]:
            value = entry.get().strip()

            if self.analyzer.perc_pass_aberration:
                entry.delete(0, tk.END)
                entry.insert(0, "Please input a valid value")
                self.analyzer.perc_pass_aberration = False
                fill_status.append(False)

            elif value and not value.replace('.', '').isdigit():
                # The user entered a non-numeric value, display an error message
                entry.delete(0, tk.END)
                entry.insert(0, "Please input a valid value")
                fill_status.append(False)

            elif value == "Please input a valid value":
                # The user has not provided a value, don't change the entry field
                entry.delete(0, tk.END)
                fill_status.append(False)

            else:
                # The input is valid
                fill_status.append(True)

        self.fill_status = fill_status

    def calculate(self):
        """
        Performs mix design calculations on the mix design data class (DOE method)
        Also given that the compulsory entries have been filled
        """
        self.analyzer.compute_fine_agg_proportion(mode='DOE')
        self.analyzer.compute_agg_content(mode='DOE')
        self.analyzer.oven_dry_batching()
        self.analyzer.proportion_coarse_agg()
        self.analyzer.summarize_results(mode='DOE')
