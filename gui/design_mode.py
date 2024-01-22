"""
Contains the `DesignModeWindow` class that provides a GUI for selecting different design modes
for concrete mix design.

The design modes are:
- Normal (DOE - British) concrete mix design
- Air-entraining concrete mix design
- PFA concrete mix design
- GGBS concrete mix design

"""

from core.utils.themes import BG
from core.utils.file_paths import optimix_paths
from core.logic.helpers.output_helpers import load_tk_image

import tkinter as tk
from tkinter import ttk


class DesignModePage(tk.Frame):
    """
    Class for displaying the design mode selection page
    """

    def __init__(self, master, controller):
        super().__init__(master, bg=BG)
        self.ggbs_button = None
        self.pfa_button = None
        self.amd_button = None
        self.nmd_button = None
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=True)

        # Create a canvas for displaying content in this page
        self.canvas = tk.Canvas(
            self,
            bg=BG,
            width=1000,
            height=630,
            highlightthickness=0
        )
        self.canvas.place(x=0, y=0)

        # Add scrollbar, optimix header and page instructions
        self.display_header()

        # Display buttons for design selections
        self.display_buttons()

        # Handle the setting of the default image and the desired mode
        self.handle_button_switch()

        # Fix scroll boundary in the canvas
        self.fix_boundary()

    def display_header(self):
        """
        Display's the scrollbar, header and page instructions
        """
        # Setup mousewheel scrolling
        self.canvas.bind_all(
            '<MouseWheel>',
            lambda event: self.canvas.yview_scroll(
                -int(event.delta / 50),
                "units")
        )

        # Make the scroll bar
        scrollbar = tk.Scrollbar(
            master=self,
            orient="vertical",
            cursor='hand2',
            command=self.canvas.yview
        )
        scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Display the smaller optimix logo
        ol_ii = load_tk_image(optimix_paths.mode_assets['optimix_logo_ii'])
        self.canvas.optimix_logo_ii = ol_ii
        self.canvas.create_image(
            111.79084777832031,
            59.33842086791992,
            image=ol_ii)

        # Display the selection intro text
        st = load_tk_image(optimix_paths.mode_assets['select_text'])
        self.canvas.select_text = st
        self.canvas.create_image(
            347.0,
            130.70999908447266,
            image=st
        )

    def display_buttons(self):
        """Display buttons for design mode selection"""
        # Create a custom style for buttons
        mode_selection_button_style = ttk.Style()
        mode_selection_button_style.theme_use('clam')
        mode_selection_button_style.configure(
            'Custom.TButton',
            borderwidth=0,
            background=BG,
            relief="raised",
            highlightthickness=0,
            highlightbackground=BG
        )

        # Handle dynamic button changes ()
        mode_selection_button_style.map(
            'Custom.TButton',
            background=[('active', BG)],
            highlightcolor=[('focus', BG)]
        )

        # Display the Normal concrete mix design mode option
        normal_md = load_tk_image(optimix_paths.mode_assets['mode_i_n'])
        self.canvas.mode_i_n = normal_md
        self.nmd_button = ttk.Button(
            master=self.canvas,
            image=normal_md,
            command=self.switch_to_doe,
            style='Custom.TButton',
            cursor='hand2',
            takefocus=False)
        self.canvas.create_window(412.5, 250.0, window=self.nmd_button)

        # Display the air entrained concrete mix design mode option
        aem_md = load_tk_image(optimix_paths.mode_assets['mode_ii_a'])
        self.canvas.mode_i_a = aem_md
        self.amd_button = ttk.Button(
            master=self.canvas,
            image=aem_md,
            command=self.switch_to_air,
            style='Custom.TButton',
            cursor='hand2',
            takefocus=False)
        self.canvas.create_window(412.5, 400.0, window=self.amd_button)

        # Display the pfa concrete mix design mode option
        pfa_md = load_tk_image(optimix_paths.mode_assets['mode_iii_pf'])
        self.canvas.mode_i_p = pfa_md
        self.pfa_button = ttk.Button(
            master=self.canvas,
            image=pfa_md,
            command=self.switch_to_pfa,
            style='Custom.TButton',
            cursor='hand2',
            takefocus=False)
        self.canvas.create_window(412.5, 550.0, window=self.pfa_button)

        # Display the pfa concrete mix design mode option
        ggbs_md = load_tk_image(optimix_paths.mode_assets['mode_iv_pg'])
        self.canvas.mode_g = ggbs_md
        self.ggbs_button = ttk.Button(
            master=self.canvas,
            image=ggbs_md,
            command=self.switch_to_ggbs,
            style='Custom.TButton',
            cursor='hand2',
            takefocus=False)
        self.canvas.create_window(412.5, 700.0, window=self.ggbs_button)

    def handle_button_switch(self):
        """
        Once the cursor is hovered on the button,
        the button's image changes image just to show that it is active.
        This function ensures exactly that
        """
        # Mode selection images
        ms_images = {
            self.nmd_button: (load_tk_image(optimix_paths.mode_assets['mode_i_n']),
                              load_tk_image(optimix_paths.mode_assets['mode_i_n_alt'])),

            self.amd_button: (load_tk_image(optimix_paths.mode_assets['mode_ii_a']),
                              load_tk_image(optimix_paths.mode_assets['mode_ii_a_alt'])),

            self.pfa_button: (load_tk_image(optimix_paths.mode_assets['mode_iii_pf']),
                              load_tk_image(optimix_paths.mode_assets['mode_iii_pf_alt'])),

            self.ggbs_button: (load_tk_image(optimix_paths.mode_assets['mode_iv_pg']),
                               load_tk_image(optimix_paths.mode_assets['mode_iv_pg_alt']))
        }

        def on_hovering(event):
            """
            Handles configuration of the button switch when the cursor hovers on it
            
            :param event: the particular event that the function is tied to.
            """
            button = event.widget
            default_img, hover_img = ms_images[button]
            button.config(image=hover_img)

        def on_leaving(event):
            """
            Handles configuration of the button switch when the cursor leaves it
            
            :param event: the particular event that the function is tied to.
            """
            button = event.widget
            default_img, hover_img = ms_images[button]
            button.config(image=default_img)

        # Directly bind the events to the placed buttons
        self.nmd_button.bind('<Enter>', on_hovering)
        self.nmd_button.bind('<Leave>', on_leaving)
        self.amd_button.bind('<Enter>', on_hovering)
        self.amd_button.bind('<Leave>', on_leaving)
        self.pfa_button.bind('<Enter>', on_hovering)
        self.pfa_button.bind('<Leave>', on_leaving)
        self.ggbs_button.bind('<Enter>', on_hovering)
        self.ggbs_button.bind('<Leave>', on_leaving)

        # Ensure default images are set for each button
        self.nmd_button.config(image=ms_images[self.nmd_button][0])
        self.amd_button.config(image=ms_images[self.amd_button][0])
        self.pfa_button.config(image=ms_images[self.pfa_button][0])
        self.ggbs_button.config(image=ms_images[self.ggbs_button][0])

    def switch_to_doe(self):
        """Action: Switch to the normal concrete design doe mode"""
        # Close the current frame
        self.forget()

        # Switch to the DOE mode page
        self.controller.page_frames[2].pack(fill=tk.BOTH, expand=True)

    def switch_to_air(self):
        """Action: Switch to the air entrained concrete mix design"""
        # Close the current frame
        self.forget()

        # Switch to the Air entraining  mix design mode
        self.controller.page_frames[3].pack(fill=tk.BOTH, expand=True)

    def switch_to_pfa(self):
        """Action: Switch to the pfa concrete mix design mode"""
        # Close the current frame
        self.forget()

        # Switch to the PFA mix design mode
        self.controller.page_frames[4].pack(fill=tk.BOTH, expand=True)

    def switch_to_ggbs(self):
        """Action: Switch to the ggbs design mode"""
        # Close the current frame
        self.forget()

        # Switch to the GGBS mix design mode
        self.controller.page_frames[5].pack(fill=tk.BOTH, expand=True)

    def fix_boundary(self):
        """
        Fixes scroll boundary in the top level widget
        """
        # Get the bounding box of all items
        bbox = self.canvas.bbox("all")

        # Add allowance on top and at the bottom
        top_allowance = 40
        bottom_allowance = 40
        bbox = (bbox[0], bbox[1] - top_allowance, bbox[2], bbox[3] + bottom_allowance)

        # Update scroll region to include all objects
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=bbox)
