"""file_paths.py

This module centralizes storage and access of file paths for various assets, data,
templates, and reports used within OptiMix.
"""

from pathlib import Path


class ProjectPaths:
    """Centralizes storage and access of all project file paths
    """

    def __init__(self):
        """Constructor for ProjectPaths

        """
        self.root_dir = None
        self.project_dir = None
        self.assets_dir = None
        self.data_dir = None
        self.fagg_prop_data_dir = None
        self.fwc_data_dir = None
        self.gui_images_dir = None
        self.aem_dir = None
        self.doe_dir = None
        self.ggbs_dir = None
        self.intro_screen_dir = None
        self.mode_dir = None
        self.pfa_dir = None
        self.window_images_dir = None
        self.icons_dir = None
        self.reports_dir = None
        self.temp_dir = None
        self.fagg_prop_plot_paths = None
        self.fwc_plot_paths = None
        self.aem_assets = None
        self.doe_assets = None
        self.ggbs_assets = None
        self.intro_screen_assets = None
        self.mode_assets = None
        self.pfa_assets = None
        self.icons = None
        self.report_assets = None

        # Return the root and the OptiMix project directories
        self.root_project_dir()

        # Create paths for assets folders and sub-folders
        self.assets_paths()

        # Create paths for all assets in the `/assets` folder
        self.assets_content()

    def root_project_dir(self):
        """Creates path attributes for the root and the Optimix project directories

        """
        self.root_dir = Path(__file__).resolve().parent.parent.parent.parent
        self.project_dir = Path(__file__).resolve().parent.parent.parent

    def assets_paths(self):
        """Creates path attributes for the folders in the `/assets` folder

        """
        # Main assets folder
        self.assets_dir = self.project_dir / "assets"

        # Data folder, its sub-folders and content
        self.data_dir = self.assets_dir / "data"
        self.fagg_prop_data_dir = self.data_dir / "fagg_prop_data"
        self.fwc_data_dir = self.data_dir / "fwc_data"

        # GUI Images folder & its sub-folders
        self.gui_images_dir = self.assets_dir / "gui_images"
        self.aem_dir = self.gui_images_dir / "aem_mode"
        self.doe_dir = self.gui_images_dir / "doe_mode"
        self.ggbs_dir = self.gui_images_dir / "ggbs_mode"
        self.intro_screen_dir = self.gui_images_dir / "intro_screen"
        self.mode_dir = self.gui_images_dir / "mode_selection"
        self.pfa_dir = self.gui_images_dir / "pfa_mode"
        self.window_images_dir = self.gui_images_dir / "window"
        self.icons_dir = self.window_images_dir / "icons"

        # Report templates folder
        self.reports_dir = self.assets_dir / "report_templates"

        # Folder for saving temporary files
        self.temp_dir = self.assets_dir / "temp"

    def assets_content(self):
        """Creates the paths for all .png & .csv files in the `/assets` folder

        """
        # Fine aggregate proportion plot datapoints
        self.fagg_prop_plot_paths = [
            [
                self.fagg_prop_data_dir / '0_10_15_10mm.csv',
                self.fagg_prop_data_dir / '0_10_40_10mm.csv',
                self.fagg_prop_data_dir / '0_10_60_10mm.csv',
                self.fagg_prop_data_dir / '0_10_80_10mm.csv',
                self.fagg_prop_data_dir / '0_10_100_10mm.csv'],

            [
                self.fagg_prop_data_dir / '10_30_15_10mm.csv',
                self.fagg_prop_data_dir / '10_30_40_10mm.csv',
                self.fagg_prop_data_dir / '10_30_60_10mm.csv',
                self.fagg_prop_data_dir / '10_30_80_10mm.csv',
                self.fagg_prop_data_dir / '10_30_100_10mm.csv'
            ],

            [
                self.fagg_prop_data_dir / '30_60_15_10mm.csv',
                self.fagg_prop_data_dir / '30_60_40_10mm.csv',
                self.fagg_prop_data_dir / '30_60_60_10mm.csv',
                self.fagg_prop_data_dir / '30_60_80_10mm.csv',
                self.fagg_prop_data_dir / '30_60_100_10mm.csv'
            ],

            [
                self.fagg_prop_data_dir / '60_180_15_10mm.csv',
                self.fagg_prop_data_dir / '60_180_40_10mm.csv',
                self.fagg_prop_data_dir / '60_180_60_10mm.csv',
                self.fagg_prop_data_dir / '60_180_80_10mm.csv',
                self.fagg_prop_data_dir / '60_180_100_10mm.csv'
            ],

            [
                self.fagg_prop_data_dir / '0_10_15_20mm.csv',
                self.fagg_prop_data_dir / '0_10_40_20mm.csv',
                self.fagg_prop_data_dir / '0_10_60_20mm.csv',
                self.fagg_prop_data_dir / '0_10_80_20mm.csv',
                self.fagg_prop_data_dir / '0_10_100_20mm.csv'],

            [
                self.fagg_prop_data_dir / '10_30_15_20mm.csv',
                self.fagg_prop_data_dir / '10_30_40_20mm.csv',
                self.fagg_prop_data_dir / '10_30_60_20mm.csv',
                self.fagg_prop_data_dir / '10_30_80_20mm.csv',
                self.fagg_prop_data_dir / '10_30_100_20mm.csv'
            ],

            [
                self.fagg_prop_data_dir / '30_60_15_20mm.csv',
                self.fagg_prop_data_dir / '30_60_40_20mm.csv',
                self.fagg_prop_data_dir / '30_60_60_20mm.csv',
                self.fagg_prop_data_dir / '30_60_80_20mm.csv',
                self.fagg_prop_data_dir / '30_60_100_20mm.csv'
            ],

            [
                self.fagg_prop_data_dir / '60_180_15_20mm.csv',
                self.fagg_prop_data_dir / '60_180_40_20mm.csv',
                self.fagg_prop_data_dir / '60_180_60_20mm.csv',
                self.fagg_prop_data_dir / '60_180_80_20mm.csv',
                self.fagg_prop_data_dir / '60_180_100_20mm.csv'
            ],

            [
                self.fagg_prop_data_dir / '0_10_15_40mm.csv',
                self.fagg_prop_data_dir / '0_10_40_40mm.csv',
                self.fagg_prop_data_dir / '0_10_60_40mm.csv',
                self.fagg_prop_data_dir / '0_10_80_40mm.csv',
                self.fagg_prop_data_dir / '0_10_100_40mm.csv'],

            [
                self.fagg_prop_data_dir / '10_30_15_40mm.csv',
                self.fagg_prop_data_dir / '10_30_40_40mm.csv',
                self.fagg_prop_data_dir / '10_30_60_40mm.csv',
                self.fagg_prop_data_dir / '10_30_80_40mm.csv',
                self.fagg_prop_data_dir / '10_30_100_40mm.csv'
            ],

            [
                self.fagg_prop_data_dir / '30_60_15_40mm.csv',
                self.fagg_prop_data_dir / '30_60_40_40mm.csv',
                self.fagg_prop_data_dir / '30_60_60_40mm.csv',
                self.fagg_prop_data_dir / '30_60_80_40mm.csv',
                self.fagg_prop_data_dir / '30_60_100_40mm.csv'
            ],

            [
                self.fagg_prop_data_dir / '60_180_15_40mm.csv',
                self.fagg_prop_data_dir / '60_180_40_40mm.csv',
                self.fagg_prop_data_dir / '60_180_60_40mm.csv',
                self.fagg_prop_data_dir / '60_180_80_40mm.csv',
                self.fagg_prop_data_dir / '60_180_100_40mm.csv'
            ]
        ]
        
        # Free-water/cement ratio plot data paths
        self.fwc_plot_paths = [csv_file for csv_file in self.fwc_data_dir.iterdir()]
        self.fwc_plot_paths = self.fwc_plot_paths[:1] + self.fwc_plot_paths[2:] + self.fwc_plot_paths[1:2]

        # Air entrained design mode assets
        self.aem_assets = {
            'aem_mode_text': self.aem_dir / "aem_text.png",
            'required_entries_image': self.aem_dir / "aem_req.png",
            'opt_entries_image': self.aem_dir / "aem_optional.png",
            'instructions_v_aem': self.aem_dir / "instruction_v.png",
            'fine_agg_reduc_image': self.aem_dir / "fagg_reduc.png"
        }

        # Normal DOE mix design assets
        self.doe_assets = {
            'doe_mode_text': self.doe_dir / "doe_text.png",
            'si_i': self.doe_dir / "stage_instruction_i.png",
            'si_ii': self.doe_dir / "stage_instruction_ii.png",
            'line_i': self.doe_dir / "line_i.png",
            'line_ii': self.doe_dir / "line_ii.png",
            'line_iii': self.doe_dir / "line_iii.png",
            'line_iv': self.doe_dir / "line_iv.png",
            'entry_captions': self.doe_dir / "entry_caption.png",
            'si_clicked': self.doe_dir / "S1_clicked.png",
            'si_clickable': self.doe_dir / "S1_unclicked.png",
            'sii_clicked': self.doe_dir / "S2_clicked.png",
            'sii_clickable': self.doe_dir / "S2_unclicked.png",
            'siii_clicked': self.doe_dir / "S3_clicked.png",
            'siii_clickable': self.doe_dir / "S3_unclicked.png",
            'siv_clicked': self.doe_dir / "S4_clicked.png",
            'siv_clickable': self.doe_dir / "S4_unclicked.png",
            'sv_clicked': self.doe_dir / "S5_clicked.png",
            'sv_clickable': self.doe_dir / "S5_unclicked.png",
            'change_design_button': self.doe_dir / "change_design_button.png",
            'previous_button': self.doe_dir / "previous.png",
            'next_button': self.doe_dir / "next.png",
            'show_results': self.doe_dir / "view_results.png",
            'data_reset': self.doe_dir / "clear_entries.png",
            'slump': self.doe_dir / "slump.png",
            'vebe': self.doe_dir / "vebe.png",
            'si_iii': self.doe_dir / "details.png",
            'ui_line': self.doe_dir / "ui_line.png",
            'max_c': self.doe_dir / "max_c_content.png",
            'min_c': self.doe_dir / "min_c_content.png",
            'instructions_iv': self.doe_dir / "instructions_iv_i.png",
            'rel_density': self.doe_dir / "rel_d.png",
            'conc_density': self.doe_dir / "c_density.png",
            'instructions_iv_i': self.doe_dir / "instructions_iv_i_60.png",
            'instructions_tot_agg': self.doe_dir / "instructions_iv.png",
            'ov_batch_fagg': self.doe_dir / "oven_dry_fagg.png",
            'ov_batch_cagg': self.doe_dir / "oven_dry_cagg.png",
            'instructions_v': self.doe_dir / "instruction_v.png",
            'percent_passing': self.doe_dir / "percent_passing.png",
            'note': self.doe_dir / "note.png",
            'report_title': self.doe_dir / "report_title_si.png",
            'report_stage_i': self.doe_dir / "report_stage_i.png",
            'report_stage_ii': self.doe_dir / "report_stage_ii.png",
            'report_stage_iii': self.doe_dir / "report_stage_iii.png",
            'report_stage_iv': self.doe_dir / "report_stage_iv.png",
            'report_stage_v': self.doe_dir / "report_stage_v.png",
            'report_logo': self.doe_dir / "result_logo.png",
            'report_rectangles': [self.doe_dir / "report_rectangle_i.png",
                                  self.doe_dir / "report_rectangle_ii.png",
                                  self.doe_dir / "report_rectangle_iii.png",
                                  self.doe_dir / "report_rectangle_iv.png",
                                  self.doe_dir / "report_rectangle_v.png",
                                  self.doe_dir / "report_rectangle_vi.png",
                                  self.doe_dir / "report_rectangle_vii.png"],
            'stage_v_instruction': self.doe_dir / "stage_v_instruction.png",
            'svr_on': self.doe_dir / "s5r_on.png",
            'svr_off': self.doe_dir / "s5r_off.png",
            'fmdr_on': self.doe_dir / "fmdr_on.png",
            'fmdr_off': self.doe_dir / "fmdr_off.png",
            'rotn5': self.doe_dir / "rotn5 (1).png",
            'display_ev': self.doe_dir / "dev (1).png",
            'cement_report_a': self.doe_dir / "cement_a.png",
            'kg_unit': self.doe_dir / "kg.png",
            'water_report_a': self.doe_dir / "water_a.png",
            'fagg_report_ssd': self.doe_dir / "fagg_ssd.png",
            'fagg_report_ovd': self.doe_dir / "fagg_odc.png",
            'cagg_10_20_40_ssd_path': self.doe_dir / "cagg_10_20_40_ssd.png",
            'cagg_10_20_ssd_path': self.doe_dir / "cagg_10_20_ssd.png",
            'cagg_10_40_ssd_path': self.doe_dir / "cagg_10_40_ssd.png",
            'cagg_20_40_ssd_path': self.doe_dir / "cagg_20_40_ssd.png",
            'cagg_10_20_40_odc_path': self.doe_dir / "cagg_10_20_40_odc.png",
            'cagg_10_40_odc_path': self.doe_dir / "cagg_10_40_odc.png",
            'cagg_10_20_odc_path': self.doe_dir / "cagg_10_20_odc.png",
            'cagg_20_40_odc_path': self.doe_dir / "cagg_20_40_odc.png",
            'cagg_10_odc_path': self.doe_dir / "cagg_10_odc.png",
            'cagg_20_odc_path': self.doe_dir / "cagg_20_odc.png",
            'cagg_40_odc_path': self.doe_dir / "cagg_40_odc.png",
            'cagg_10_ssd_path': self.doe_dir / "cagg_10_ssd.png",
            'cagg_20_ssd_path': self.doe_dir / "cagg_20_ssd.png",
            'cagg_40_ssd_path': self.doe_dir / "cagg_40_ssd.png",
            'adjust_button': self.doe_dir / "adjust_button.png",
            'file_format_pngs': [self.doe_dir / "xlsx_image.png",
                                 self.doe_dir / "pdf_image.png",
                                 self.doe_dir / "docx_image.png"],
            'table_ii_reporting': self.doe_dir / "table_2.png",
            'table_iii_reporting': self.doe_dir / "table_3.png"
        }

        # GGBS design mode assets
        self.ggbs_assets = {
            'ggbs_mode_text': self.ggbs_dir / "ggbs_text.png",
            'required_entries_ggbs': self.ggbs_dir / "ggbs_si.png",
            'wr_image': self.ggbs_dir / "water_reduc.png",
            'lw_ggbs': self.ggbs_dir / "ggbs_note.png",
            'ggbs_report_a': self.ggbs_dir / "ggbs_report_a.png"
        }

        # Intro screen assets
        self.intro_screen_assets = {
            'optimix_logo': self.intro_screen_dir / "optimix_logo.png",
            'optimix_caption': self.intro_screen_dir / "optimix_caption.png",
            'styled_rectangles': self.intro_screen_dir / "styled_rectangles.png",
            'disclaimer_signal': self.intro_screen_dir / "warning_signal.png",
            'header_texts': self.intro_screen_dir / "text_headers.png",
            'introtext': self.intro_screen_dir / "introtext.png",
            'intro_continue_button': self.intro_screen_dir / "intro_continue_button.png"
        }

        # Mode selection assets
        self.mode_assets = {
            'optimix_logo_ii': self.mode_dir / "optimix_logo_ii.png",
            'select_text': self.mode_dir / "select_text.png",
            'mode_i': self.mode_dir / "DOE.png",
            'mode_ii': self.mode_dir / "AIR.png",
            'mode_iii': self.mode_dir / "PFA.png",
            'mode_iv': self.mode_dir / "GGBS.png",
            'mode_i_n': self.mode_dir / "n1.png",
            'mode_ii_a': self.mode_dir / "a1.png",
            'mode_iii_pf': self.mode_dir / "pf1.png",
            'mode_iv_pg': self.mode_dir / "pg1.png",
            'mode_i_n_alt': self.mode_dir / "n2.png",
            'mode_ii_a_alt': self.mode_dir / "a2.png",
            'mode_iii_pf_alt': self.mode_dir / "pf2.png",
            'mode_iv_pg_alt': self.mode_dir / "pg2.png",
            'back_button': self.mode_dir / "previous.png"
        }

        # pfa mode selection assets
        self.pfa_assets = {
            'pfa_mode_text': self.pfa_dir / "pfa_text.png",
            'stage_ii_instructions_pfa': self.pfa_dir / "stage_ii_instructions_pfa.png",
            'pfa_prop_pl': self.pfa_dir / "pfa_pl.png",
            'cef_image': self.pfa_dir / "cef.png",
            'max_cr': self.pfa_dir / "max_cr.png",
            'lw': self.pfa_dir / "limit_warning.png",
            'pfa_report_a': self.pfa_dir / "pfa_a.png",
            'table_iii_reporting_a': self.pfa_dir / "table_3a.png",
            'table_iii_reporting_b': self.pfa_dir / "table_3b.png",
        }

        # Window icons
        self.icons = {
            'icon_16': self.icons_dir / "optimixicon_16-_1_.ico",
            'icon_24': self.icons_dir / "optimixicon_24.ico",
            'icon_32': self.icons_dir / "optimixicon_32_1_.ico"
        }

        # Report templates
        self.report_assets = {
            'AEM': self.reports_dir / "aem_report.md",
            'GGBS': self.reports_dir / "ggbs_report.md",
            'DOE': self.reports_dir / "normal_doe_report.md",
            'PFA': self.reports_dir / "pfa_report.md"
        }


# Create a ProjectPath object to be used throughout the app
optimix_paths = ProjectPaths()
