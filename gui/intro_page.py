"""This module contains the IntroPage class for displaying the introductory page

"""

import tkinter as tk

from core.logic.helpers.output_helpers import load_tk_image
from core.utils.file_paths import optimix_paths
from core.utils.themes import BG


class IntroPage(tk.Frame):
    """
    Displays the app description, features, a disclaimer & a button
    """

    def __init__(self, master, controller):
        """
        Initiates widgets for this page's content.
        :param master: The main application frame
        :param controller: instance for accessing instances at OptiMixApp
        """
        super().__init__(master)
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=True)
        self.optimix_logo = None

        # Create a canvas for displaying content in this page
        self.canvas = tk.Canvas(
            self,
            bg=BG,
            width=1000,
            height=630,
            highlightthickness=0
        )
        self.canvas.place(x=0, y=0)

        # Display the logo and caption
        self.display_ipage_header()

        # Display page content
        self.display_ipage_content()

        # The continue button
        self.display_ipage_button()

    def display_ipage_header(self):
        """Display the logo and caption for OptiMix"""

        # Display the optimix logo
        ol = load_tk_image(optimix_paths.intro_screen_assets['optimix_logo'])
        self.optimix_logo = ol

        self.canvas.create_image(
            185.0,
            85.0,
            image=ol
        )

        # Display the logo's caption
        oc = load_tk_image(optimix_paths.intro_screen_assets['optimix_caption'])
        self.canvas.optimix_caption = oc
        self.canvas.create_image(
            195.0,
            146.0,
            image=oc
        )

    def display_ipage_content(self):
        """Displays the introductory content for OptiMix"""

        # Display the styled rectangles
        sr = load_tk_image(optimix_paths.intro_screen_assets['styled_rectangles'])
        self.canvas.styled_rectangles = sr
        self.canvas.create_image(
            505.0,
            429.0,
            image=sr
        )

        # Display the styled rectangles
        sr = load_tk_image(optimix_paths.intro_screen_assets['styled_rectangles'])
        self.canvas.styled_rectangles = sr
        self.canvas.create_image(
            505.0,
            429.0,
            image=sr
        )

        # Display the disclaimer signal
        ds = load_tk_image(optimix_paths.intro_screen_assets['disclaimer_signal'])
        self.canvas.disclaimer_signal = ds
        self.canvas.create_image(
            920.0,
            219.0,
            image=ds
        )

        # Display the header text
        ht = load_tk_image(optimix_paths.intro_screen_assets['header_texts'])
        self.canvas.header_texts = ht
        self.canvas.create_image(
            507.85152435302734,
            223.30999755859375,
            image=ht
        )

        # Display the introductory text
        itt = load_tk_image(optimix_paths.intro_screen_assets['introtext'])
        self.canvas.introtext = itt
        self.canvas.create_image(
            500.32400131225586,
            427.906005859375,
            image=itt
        )

    def display_ipage_button(self):
        """Displays the 'Continue' button."""
        # Display the continue button
        icb = load_tk_image(optimix_paths.intro_screen_assets['intro_continue_button'])
        self.canvas.intro_continue_button = icb  # reference to the continue button image

        tk.Button(
            self.canvas,
            image=icb,
            cursor='hand2',
            borderwidth=0,
            background=BG,
            overrelief="raised",
            highlightthickness=0,
            highlightbackground=BG,
            activebackground=BG,
            command=lambda: self.show_design_mode_page(),
            takefocus=False
        ).place(
            x=842.0,
            y=525.0,
        )

    def show_design_mode_page(self):
        """Button action for switching to the next page"""
        # Close the current frame
        self.forget()

        # Raise the Design Mode selection frame
        self.controller.page_frames[1].pack(fill=tk.BOTH, expand=True)
