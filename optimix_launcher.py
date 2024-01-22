"""optimix_launcher.py

Launches the OptiMix application, initializing the main window,
managing page transitions, and handling user interactions seamlessly.

"""

import tkinter as tk
from typing import List

from core.utils.themes import BG
from core.utils.file_paths import optimix_paths

from gui.intro_page import IntroPage
from gui.design_mode import DesignModePage

from gui.doe_mode.doe_mode_base_page import DoeModePage
from gui.aem_mode.aem_mode_base_page import AEMModePage
from gui.pfa_mode.pfa_mode_base_page import PFAModePage
from gui.ggbs_mode.ggbs_mode_base_page import GGBSModePage


class OptiMixApp:
    """The base class of the OptiMix application."""

    def __init__(self, master):
        """
        Constructs the main application window, setting its appearance & layout

        """

        # Configure window properties
        master.title("OptiMix")  # Set window title
        master.geometry("1000x630")  # Set window size (width x height)
        master.configure(bg=BG)  # Set background color
        master.iconbitmap(optimix_paths.icons['icon_16'])  # Set window icon
        master.resizable(False, False)  # Disable window resizing

        # Create the main content frame
        self.app_frame = tk.Frame(master,
                                  bg=BG,
                                  height=630,
                                  width=1000,
                                  relief="raised")
        self.app_frame.place(x=0, y=0)
        self.app_frame.pack(fill=tk.BOTH, expand=True)

        # Create page instances
        self.page_frames: List[tk.Frame] = [IntroPage(self.app_frame, self),
                                            DesignModePage(self.app_frame, self),
                                            DoeModePage(self.app_frame, self),
                                            AEMModePage(self.app_frame, self),
                                            PFAModePage(self.app_frame, self),
                                            GGBSModePage(self.app_frame, self)]

        self.minimize_page_stack()

    def minimize_page_stack(self) -> None:
        """
        Efficiently hides all pages except the IntroPage at start, preventing visual clutter
        """
        for page in self.page_frames[1:]:
            page.forget()


# Launch the OptiMix application
root = tk.Tk()
app = OptiMixApp(root)
root.mainloop()
