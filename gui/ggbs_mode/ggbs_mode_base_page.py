"""
This module contains the GGBSModePage class that performs mix design for ground granulated
blast-furnace slag concrete.
All related GUI, data collection, computations are performed in this script

"""

from gui.ggbs_mode.ggbs_mode_stages import StageOne, StageTwo, StageThree, StageFour, StageFive
from gui.ggbs_mode.ggbs_results import StageOneResults, StageTwoResults, StageThreeResults, StageFourResults, StageFiveResults
from core.logic.helpers.output_helpers import load_tk_image, remove_index
from core.logic.mix_design import MixDesignAnalyzer
from core.utils.file_paths import optimix_paths
from core.utils.themes import *

import tkinter as tk
from tkinter import ttk

# Create the analyzer for OptiMix's real time design
analyzer = MixDesignAnalyzer()


# noinspection PyMissingOrEmptyDocstring
class GGBSModePage(tk.Frame):
    """
    Base class for the normal concrete mix design mode

    Attributes:
        - app_frame `tk.Frame`: The main content frame, serving as parent
        - controller `tk.Tk`: Controller for accessing the main frame.

    Methods:
        - display_left_tab(): Displays the left tab
        - display_bottom_frame(): Displays the bottom frame
        - reset_input(): clears all the supplied input
        - view_results(): Raises a TopLevel window for the mix design result for the stage
        - previous_stage(): switches to the previous stage
        - next_stage(): Switches to the next stage
        - save_data(): Stores the user's data
        - configure_button_transitions(): Handles button transitions during switching
        - switch_to_stage_one/two/three/four/five(): Switches to these respective stages freely
        - back(): Changes to the mode selection page
        """
    def __init__(self, master, controller):
        super().__init__(master, bg=BG)

        self.controller = controller
        self.analyzer = analyzer
        self.pack(fill=tk.BOTH, expand=True)

        self.results = None
        self.stage_button_five = None
        self.default_stage_images = None
        self.bottom_canvas = None
        self.stage_button_list = None
        self.stage_button_four = None
        self.stage_button_three = None
        self.stage_button_two = None
        self.stage_button_one = None
        self.tab_canvas = None
        self.tab_frame = None
        self.bottom_frame = None
        self.nb = None

        # Create a list of all concrete mix design stages in the DOE mode
        self.stage_frames = [StageOne(self, self.analyzer, self),
                             StageTwo(self, self.analyzer, self),
                             StageThree(self, self.analyzer, self),
                             StageFour(self, self.analyzer, self),
                             StageFive(self, self.analyzer, self)]

        # Create a list of all the result windows for all stages
        self.results = {
            0: StageOneResults,
            1: StageTwoResults,
            2: StageThreeResults,
            3: StageFourResults,
            4: StageFiveResults,
        }

        # Display the left tab
        self.display_left_tab()

        # Display the bottom frame
        self.display_bottom_frame()

        # Show Stage One at startup
        self.index = 0
        [stage.forget() for stage in remove_index(self.stage_frames, 0)]

        # Define the active stage button images
        self.si = load_tk_image(optimix_paths.doe_assets['si_clicked'])
        self.sii = load_tk_image(optimix_paths.doe_assets['sii_clicked'])
        self.siii = load_tk_image(optimix_paths.doe_assets['siii_clicked'])
        self.siv = load_tk_image(optimix_paths.doe_assets['siv_clicked'])
        self.sv = load_tk_image(optimix_paths.doe_assets['sv_clicked'])
        self.button_image_list = [self.si, self.sii, self.siii, self.siv, self.sv]

        # Create a list of all stage transitioning buttons
        self.stage_button_list = [self.stage_button_one, self.stage_button_two,
                                  self.stage_button_three, self.stage_button_four,
                                  self.stage_button_five]

    def display_left_tab(self):
        """
        A large function that displays:
        > The Small Optimix Logo
        > The current design mode (GGBS Mix Design)
        > All stage buttons
        > The change design button
        """
        # Create a frame to hold stage tabs
        self.tab_frame = tk.Frame(self,
                                  bg=ALT_BG,
                                  width=230,
                                  height=630)
        self.tab_frame.place(x=0, y=0)

        # Create a canvas to hold widgets in the tab frame
        self.tab_canvas = tk.Canvas(self.tab_frame,
                                    bg=ALT_BG,
                                    width=228,
                                    height=630,
                                    highlightthickness=0)
        self.tab_canvas.place(x=0, y=0)

        # Display the smaller optimix logo
        ol_iii = load_tk_image(optimix_paths.mode_assets['optimix_logo_ii'])
        self.tab_canvas.optimix_logo_ii = ol_iii
        self.tab_canvas.create_image(
            111.79084777832031,
            59.338420867919915,
            image=ol_iii)

        # Display the current design mode (GGBS Mix design)
        mode_text = load_tk_image(optimix_paths.ggbs_assets['ggbs_mode_text'])
        self.tab_canvas.aem_mode_text = mode_text
        self.tab_canvas.create_image(
            126.58000183105469,
            155.13999938964844,
            image=mode_text
        )

        # Create a custom style for the Stage change buttons
        stage_button_style = ttk.Style()
        stage_button_style.configure(
            'Stage.TButton',
            borderwidth=0,
            background=ALT_BG,
            relief="raised",
            highlightthickness=0,
            highlightbackground=ALT_BG,
            activebackground=ALT_BG)

        # Handle dynamic button changes ()
        stage_button_style.map(
            'Stage.TButton',
            background=[('active', ALT_BG)],
            highlightcolor=[('focus', ALT_BG)])

        # Stage 1 Button (Depiction of the current tab/stage)
        s1_button = load_tk_image(optimix_paths.doe_assets['si_clicked'])
        self.tab_canvas.si_clicked = s1_button

        # Alternative clickable button image
        s1_clickable = load_tk_image(optimix_paths.doe_assets['si_clickable'])
        self.tab_canvas.si_clickable = s1_clickable

        self.stage_button_one = ttk.Button(
            self.tab_canvas,
            takefocus=False,
            image=s1_button,
            style='Stage.TButton',
            command=self.switch_to_stage_one,
            cursor='hand2',
        )
        self.stage_button_one.place(
            x=35.0,
            y=237.0
        )

        # Stage 2 Button (Can be clicked, moves to stage 2)
        s2_clickable = load_tk_image(optimix_paths.doe_assets['sii_clickable'])  # Load the Image
        self.tab_canvas.sii_clickable = s2_clickable

        self.stage_button_two = ttk.Button(
            self.tab_canvas,
            takefocus=False,
            image=s2_clickable,
            style='Stage.TButton',
            command=self.switch_to_stage_two,
            cursor='hand2'
        )
        self.stage_button_two.place(
            x=35.0,
            y=278.0,
        )

        # Stage 3 Button (Can be clicked, moves to stage 3)
        s3_clickable = load_tk_image(optimix_paths.doe_assets['siii_clickable'])
        self.tab_canvas.siii_clickable = s3_clickable

        self.stage_button_three = ttk.Button(
            self.tab_canvas,
            takefocus=False,
            image=s3_clickable,
            style='Stage.TButton',
            command=self.switch_to_stage_three,
            cursor='hand2'
        )
        self.stage_button_three.place(
            x=35.0,
            y=319.0
        )

        # Stage 4 Button (Can be clicked, moves to stage 4)
        s4_clickable = load_tk_image(optimix_paths.doe_assets['siv_clickable'])
        self.tab_canvas.siv_clickable = s4_clickable

        self.stage_button_four = ttk.Button(
            self.tab_canvas,
            takefocus=False,
            image=s4_clickable,
            style='Stage.TButton',
            command=self.switch_to_stage_four,
            cursor='hand2'
        )
        self.stage_button_four.place(
            x=35.0,
            y=360.0
        )

        # Stage 5 Button (Can be clicked, moves to stage 5)
        s5_clickable = load_tk_image(optimix_paths.doe_assets['sv_clickable'])
        self.tab_canvas.sv_clickable = s5_clickable

        self.stage_button_five = ttk.Button(
            self.tab_canvas,
            takefocus=False,
            image=s5_clickable,
            style='Stage.TButton',
            command=self.switch_to_stage_five,
            cursor='hand2'
        )
        self.stage_button_five.place(
            x=35.0,
            y=401.0
        )

        # Create a list of all default stage button images
        self.default_stage_images = [s1_clickable, s2_clickable, s3_clickable, s4_clickable, s5_clickable]

        # Create a custom style for the change design button
        tab_button_style = ttk.Style()
        tab_button_style.configure(
            'CustomTab.TButton',
            borderwidth=0,
            background=ALT_BG,
            relief="raised",
            highlightthickness=0,
            highlightbackground=ALT_BG,
            activebackground=ALT_BG
        )

        # Handle dynamic button changes ()
        tab_button_style.map(
            'CustomTab.TButton',
            background=[('active', ALT_BG)],
            highlightcolor=[('focus', ALT_BG)]
        )

        # Display the change Design mode button
        mode_change_button = load_tk_image(optimix_paths.doe_assets['change_design_button'])
        self.tab_canvas.change_design_button = mode_change_button
        ttk.Button(
            self.tab_canvas,
            takefocus=False,
            image=mode_change_button,
            style='CustomTab.TButton',
            cursor='hand2',
            command=self.back
        ).place(
            x=20.0,
            y=550.0
        )

    def display_bottom_frame(self):
        """
        Displays the following:
        > A previous button that switches to the previous stage
        > A 'View results button for viewing design results in real time'
        > A next button that switches to the next stage
        """

        # Create a bottom frame that holds other switching buttons
        self.bottom_frame = tk.Frame(
            self,
            bg=BG,
            width=770,
            height=80
        )
        self.bottom_frame.place(x=230, y=550)

        # Create a canvas for holding the bottom buttons
        self.bottom_canvas = tk.Canvas(
            self,
            bg=BG,
            width=770,
            height=80,
            highlightthickness=0
        )
        self.bottom_canvas.place(x=230, y=550)

        # Create a custom style for the bottom change buttons
        bottom_button_style = ttk.Style()
        bottom_button_style.configure(
            'Bottom.TButton',
            borderwidth=0,
            background=BG,
            relief="raised",
            highlightthickness=0,
            highlightbackground=BG,
            activebackground=BG)

        # Handle dynamic button changes ()
        bottom_button_style.map(
            'Bottom.TButton',
            background=[('active', BG)],
            highlightcolor=[('focus', BG)]
        )

        # Data reset button
        data_reset_button = load_tk_image(optimix_paths.doe_assets['data_reset'])
        self.bottom_canvas.data_rest = data_reset_button

        ttk.Button(
            self.bottom_canvas,
            takefocus=False,
            image=data_reset_button,
            style='Bottom.TButton',
            command=self.reset_input,
            cursor='hand2'
        ).place(
            x=35,
            y=0
        )

        # Previous Stage button
        previous_stage_button = load_tk_image(optimix_paths.doe_assets['previous_button'])
        self.bottom_canvas.previous_button = previous_stage_button

        ttk.Button(
            self.bottom_canvas,
            takefocus=False,
            image=previous_stage_button,
            style='Bottom.TButton',
            command=self.previous_stage,
            cursor='hand2'
        ).place(
            x=455,
            y=0
        )

        # View results button
        view_results = load_tk_image(optimix_paths.doe_assets['show_results'])
        self.bottom_canvas.show_results = view_results
        ttk.Button(
            self.bottom_canvas,
            takefocus=False,
            image=view_results,
            style='Bottom.TButton',
            command=self.view_results,
            cursor='hand2'
        ).place(
            x=521,
            y=0)

        # Next stage button
        # Show 'next button' on other pages
        next_stage_button = load_tk_image(optimix_paths.doe_assets['next_button'])
        self.bottom_canvas.next_button = next_stage_button
        self.nb = ttk.Button(
            self.bottom_canvas,
            takefocus=False,
            image=next_stage_button,
            style='Bottom.TButton',
            command=self.next_stage,
            cursor='hand2')
        self.nb.place(
            x=658,
            y=0
        )

    def reset_input(self):
        """
        Resets all the input in the current page to their defaults
        """
        self.stage_frames[self.index].set_inputs_to_default()

    def view_results(self, stage='in_progress'):
        """
        View the design stage results in real time
        :param stage: the current stage, either 'in_progress' or 'final'
        """
        # Check for missing compulsory entries
        self.stage_frames[self.index].check_fill_status()

        # Needed to do this, k and perc def or margin check
        if self.index == 0:
            self.stage_frames[self.index].special_check()
        else:
            pass

        if all(self.stage_frames[self.index].fill_status):
            # Save the input data
            self.save_data(self.index)

            # Perform mix design
            self.stage_frames[self.index].calculate()

            # Display the design stage results based on the current page
            self.results[self.index](self.analyzer, self, stage)

    def previous_stage(self):
        """
        Checks the index of the current page and switches to the previous page.
        Should the current page be stage one, the command will switch to the design mode selection
        """
        if self.index == 0:
            # Switch to the previous design selection page
            self.back()

        else:
            # Check for missing compulsory entries
            self.stage_frames[self.index].check_fill_status()
            if all(self.stage_frames[self.index].fill_status):
                # Save the input data
                self.save_data(self.index)

                # Perform mix design
                self.stage_frames[self.index].calculate()

                # Forget the current frame
                self.stage_frames[self.index].forget()

                # Ensure that page switching is cyclic
                self.index = (self.index - 1) % len(self.stage_frames)

                # Handle stage button changes
                # noinspection PyTypeChecker
                self.configure_button_transition(self.index,
                                                 self.button_image_list[self.index],
                                                 self.stage_button_list[self.index])

                # Move to the previous stage, make necessary adjustments
                self.stage_frames[self.index].pack(fill=tk.BOTH, expand=True)

            else:
                # Stay on the current stage due to incomplete entries
                pass

    def next_stage(self):
        """
        Checks the index of the current page and switches to the next page.
        Should the current page be stage one, the command will switch to the design mode selection
        """
        if self.index == 4:
            # Last stage, show the mix design results
            # Check for missing compulsory entries
            self.stage_frames[self.index].check_fill_status()

            if all(self.stage_frames[self.index].fill_status):
                # Save the input data
                self.save_data(self.index)

                # Perform mix design
                self.stage_frames[self.index].calculate()

                # Show the mix design results
                self.view_results('final')

                # Check whether the result window is closed
                # is_closed = not StageFiveResults.winfo_exists() if str(StageFiveResults) in locals() else True

                # Forget the current frame
                self.stage_frames[self.index].forget()

                # Ensure that page switching is cyclic
                self.index = (self.index + 1) % len(self.stage_frames)

                # Handle stage button changes
                # noinspection PyTypeChecker
                self.configure_button_transition(self.index,
                                                 self.button_image_list[self.index],
                                                 self.stage_button_list[self.index])

                # Move to the next stage, make necessary adjustments
                self.stage_frames[self.index].pack(fill=tk.BOTH, expand=True)

            else:
                # Stay on the current stage due to incomplete entries
                pass

        elif self.index == 0:
            # Check for missing compulsory entries
            self.stage_frames[self.index].check_fill_status()

            # Needed to do this, k and perc def or margin check
            self.stage_frames[self.index].special_check()

            if all(self.stage_frames[self.index].fill_status):
                # Save the input data
                self.save_data(self.index)

                # Perform mix design
                self.stage_frames[self.index].calculate()

                # Forget the current frame
                self.stage_frames[self.index].forget()

                # Ensure that page switching is cyclic
                self.index = (self.index + 1) % len(self.stage_frames)

                # Handle stage button changes
                # noinspection PyTypeChecker
                self.configure_button_transition(self.index,
                                                 self.button_image_list[self.index],
                                                 self.stage_button_list[self.index])

                # Move to the next stage, make necessary adjustments
                self.stage_frames[self.index].pack(fill=tk.BOTH, expand=True)

            else:
                # Stay on the current stage due to incomplete entries
                pass

        else:
            # Check for missing compulsory entries
            self.stage_frames[self.index].check_fill_status()

            if all(self.stage_frames[self.index].fill_status):
                # Save the input data
                self.save_data(self.index)

                # Perform mix design
                self.stage_frames[self.index].calculate()

                # Forget the current frame
                self.stage_frames[self.index].forget()

                # Ensure that page switching is cyclic
                self.index = (self.index + 1) % len(self.stage_frames)

                # Handle stage button changes
                # noinspection PyTypeChecker
                self.configure_button_transition(self.index,
                                                 self.button_image_list[self.index],
                                                 self.stage_button_list[self.index])

                # Move to the next stage, make necessary adjustments
                self.stage_frames[self.index].pack(fill=tk.BOTH, expand=True)

            else:
                # Stay on the current stage due to incomplete entries
                pass

    def save_data(self, stage_index):
        """
        Ensures that the collected data is saved, this is bound to the clicking of any button
        :param stage_index: The index of the stage in `self.stage_frames`
        """
        self.stage_frames[stage_index].collect_data()

    def configure_button_transition(self, button_index: int, new_image, current_button):
        """
        Function that performs image configurations and transitions during the click of a button
        :param current_button: The current button experiencing transitioning
        :param button_index: The index of the stage button
        :param new_image: The new image to be shown when the button is clicked
        """

        # Configure the current button to use the new image
        current_button.configure(image=new_image)

        # Configure all other buttons to use their default images
        for i in range(len(self.stage_button_list)):
            if i != button_index:
                # noinspection PyUnresolvedReferences
                self.stage_button_list[i].configure(image=self.default_stage_images[i])

    def switch_to_stage_one(self):
        """
        > Saves the data in the current stage
        > Handles button transitioning
        > Switches to stage one
        """
        if self.index == 0:
            # Check for missing compulsory entries
            self.stage_frames[0].check_fill_status()

            # Needed to do this, k and percent_def
            self.stage_frames[0].special_check()

        else:
            # Check for missing compulsory entries
            self.stage_frames[self.index].check_fill_status()

        if all(self.stage_frames[self.index].fill_status):
            # Save the entered data
            self.save_data(self.index)

            # Perform mix design
            self.stage_frames[self.index].calculate()

            # Load the image to show that the button is clicked
            self.tab_canvas.si_clicked = self.si

            # Handle button image tab transitions
            self.configure_button_transition(0, self.si, self.stage_button_one)

            # Forget the current frame
            self.stage_frames[self.index].forget()

            # Move to the previous stage, make necessary adjustments
            self.index = 0
            self.stage_frames[self.index].pack(fill=tk.BOTH)

        else:
            # Stay in the current page
            pass

    def switch_to_stage_two(self):
        """
        > Saves the data in the current stage
        > Handles button transitioning
        > Switches to stage two
        """
        if self.index == 0:
            # Check for missing compulsory entries
            self.stage_frames[0].check_fill_status()

            # Needed to do this, k and perc def or margin check
            self.stage_frames[0].special_check()
        else:
            # Check for missing compulsory entries
            self.stage_frames[self.index].check_fill_status()

        if all(self.stage_frames[self.index].fill_status):
            # Save the entered data
            self.save_data(self.index)

            # Perform mix design
            self.stage_frames[self.index].calculate()

            # Load the image to show that the button is clicked
            self.tab_canvas.sii_clicked = self.sii

            # Handle button image tab transitions
            self.configure_button_transition(1, self.sii, self.stage_button_two)

            # Forget the current frame
            self.stage_frames[self.index].forget()

            # Move to the previous stage, make necessary adjustments
            self.index = 1
            self.stage_frames[self.index].pack(fill=tk.BOTH)

        else:
            # Stay in the current page
            pass

    def switch_to_stage_three(self):
        """
        > Saves the data in the current stage
        > Handles button transitioning
        > Switches to stage three
        """
        if self.index == 0:
            # Check for missing compulsory entries
            self.stage_frames[0].check_fill_status()

            # Needed to do this, k and perc def or margin check
            self.stage_frames[0].special_check()
        else:
            # Check for missing compulsory entries
            self.stage_frames[self.index].check_fill_status()

        if all(self.stage_frames[self.index].fill_status):
            # Save the entered data
            self.save_data(self.index)

            # Perform mix design
            self.stage_frames[self.index].calculate()

            # Load the image to show that the button is clicked
            self.tab_canvas.siii_clicked = self.siii

            # Handle button image tab transitions
            self.configure_button_transition(2, self.siii, self.stage_button_three)

            # Forget the current frame
            self.stage_frames[self.index].forget()

            # Move to the previous stage, make necessary adjustments
            self.index = 2
            self.stage_frames[self.index].pack(fill=tk.BOTH)

        else:
            # Stay in the current page
            pass

    def switch_to_stage_four(self):
        """
        > Saves the data in the current stage
        > Handles button transitioning
        > Switches to stage four
        """
        if self.index == 0:
            # Check for missing compulsory entries
            self.stage_frames[0].check_fill_status()

            # Needed to do this, k and perc def or margin check
            self.stage_frames[0].special_check()
        else:
            # Check for missing compulsory entries
            self.stage_frames[self.index].check_fill_status()

        if all(self.stage_frames[self.index].fill_status):
            # Save the entered data
            self.save_data(self.index)

            # Perform mix design
            self.stage_frames[self.index].calculate()

            # Load the image to show that the button is clicked
            self.tab_canvas.siv_clicked = self.siv

            # Handle button image tab transitions
            self.configure_button_transition(3, self.siv, self.stage_button_four)

            # Forget the current frame
            self.stage_frames[self.index].forget()

            # Move to the previous stage, make necessary adjustments
            self.index = 3
            self.stage_frames[self.index].pack(fill=tk.BOTH)

        else:
            # Stay in the current page
            pass

    def switch_to_stage_five(self):
        """
        > Saves the data in the current stage
        > Handles button transitioning
        > Switches to stage five
        """
        if self.index == 0:
            # Check for missing compulsory entries
            self.stage_frames[0].check_fill_status()

            # Needed to do this, k and perc def or margin check
            self.stage_frames[0].special_check()
        else:
            # Check for missing compulsory entries
            self.stage_frames[self.index].check_fill_status()

        if all(self.stage_frames[self.index].fill_status):
            # Save the entered data
            self.save_data(self.index)

            # Perform mix design
            self.stage_frames[self.index].calculate()

            # Load the image to show that the button is clicked
            self.tab_canvas.sv_clicked = self.sv

            # Handle button image tab transitions
            self.configure_button_transition(4, self.sv, self.stage_button_five)

            # Forget the current frame
            self.stage_frames[self.index].forget()

            # Move to the previous stage, make necessary adjustments
            self.index = 4
            self.stage_frames[self.index].pack(fill=tk.BOTH)

        else:
            # Stay in the current stage
            pass

    def back(self):
        """
        Switches to the previous design selection page
        """
        # Clear the current page
        self.forget()

        # Move to the previous page (mode selection page)
        self.controller.page_frames[1].pack(fill=tk.BOTH, expand=True)
