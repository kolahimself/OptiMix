"""output_helpers.py

Functions for report generation and file handling
"""
import tkinter as tk

import plotly.io as pio
from tkinter import filedialog

import markdown2
import pdfkit
from htmldocx import HtmlToDocx

import numpy as np
import pandas as pd

import re
import io
import os
import time
import warnings
from pathlib import Path

from core.logic.reference_data import generate_full_labels_and_values
from core.utils.file_paths import optimix_paths, wkhtmltopdf_path
from core.utils.themes import colors, white_color


def batch(quantities: list, batch_volume: float) -> list:
    """
    Converts the quantities required per metre cube to the desired batching volume.
    :param quantities: The quantities to be adjusted
    :param batch_volume: Batching volume to be adjusted to
    """
    batched_volume = [np.multiply(quantity, batch_volume) for quantity in quantities]

    return batched_volume


def oven_dry_batching(odb_status: int, labels: list, values: list, mix_design_results: list) -> None:
    """
    Appends ven dry batching results to the result label and values for .xlsx reporting
    :param odb_status:  Specified oven dry batching of aggregates status
    :param labels: (list): A list containing labels that will turn out as an Excel column in the report
    :param values: (list): A list containing values that will turn out as an Excel column in the report
    :param mix_design_results: [a, b, c, d] a list of `analyzer.data`, analyzer.calc_data, analyzer.design_results,
                               analyzer.design_batch_results
    """
    if odb_status == 'both aggregates':
        # Fine Aggregates
        labels.append("Fine Aggregate Content for Oven Dry Batching")
        values.append(mix_design_results[1]['fine_agg_content'])

        # Coarse Aggregates
        labels.append("Coarse Aggregate Content for Oven Dry Batching")
        values.append(mix_design_results[1]['coarse_agg_content'])

        # Water added for absorption
        labels.append("Required Water for Absorption")
        values.append(mix_design_results[1]['added_h20_mass'])

        # Final Water content
        labels.append("Final Water Content")
        values.append(mix_design_results[1]['new_fw_content'])

    elif odb_status == 'fine aggregate only':
        # Fine Aggregates
        labels.append("Fine Aggregate Content for Oven Dry Batching")
        values.append(mix_design_results[1]['fine_agg_content'])

        # Water added for absorption
        labels.append("Required Water for Absorption")
        values.append(mix_design_results[1]['added_h20_mass'])

        # Final Water content
        labels.append("Final Water Content")
        values.append(mix_design_results[1]['new_fw_content'])

    elif odb_status == 'coarse aggregate only':
        # Fine Aggregates
        labels.append("Coarse Aggregate Content for Oven Dry Batching")
        values.append(mix_design_results[1]['coarse_agg_content'])

        # Water added for absorption
        labels.append("Required Water for Absorption")
        values.append(mix_design_results[1]['added_h20_mass'])

        # Final Water content
        labels.append("Final Water Content")
        values.append(mix_design_results[1]['new_fw_content'])

    elif odb_status is None:
        pass


def result_preparer(mix_design_results: [dict, dict, dict, dict],
                    mode: str,
                    accuracy_switch: int,
                    odb_status: int) -> [pd.DataFrame, pd.DataFrame]:
    """Takes in the mix design data and makes a couple of dataframes for xlsx reporting.

    :param odb_status: Specified status for oven dry batching of aggregates
    :param accuracy_switch: 0 or 1, degree of accuracy needed
    :param mode: Mix design mode, 'DOE', 'AEM', 'PFA' or 'GGBS'.
    :param mix_design_results: [a, b, c, d] a list of `analyzer.data`, analyzer.calc_data, analyzer.design_results,
                               analyzer.design_batch_results
    :return: (pd.DataFrame): Mix design results arranged as sheets in a .xlsx file.
    """
    preferred_unit = mix_design_results[0]['Result Tuning']['Unit']
    desired_volume = float(mix_design_results[0]['Result Tuning']['Batch volume'])

    # Dataframe of summary results
    summary_labels = ["Cement (kg/m\u00b3)", "Water (kg/m\u00b3)", "Fine Aggregate (kg/m\u00b3)",
                      "Coarse Aggregate (kg/m\u00b3)", f"Cement (kg per {desired_volume}{preferred_unit})",
                      f"Water (kg per {desired_volume}{preferred_unit})",
                      f"Fine Aggregate (kg per {desired_volume}{preferred_unit})",
                      f"Coarse Aggregates (kg per {desired_volume}{preferred_unit})"]

    summary_values = [mix_design_results[2]['cement'][accuracy_switch], mix_design_results[2]['water'][accuracy_switch],
                      mix_design_results[2]['fagg'][accuracy_switch], mix_design_results[2]['cagg'][accuracy_switch],
                      mix_design_results[3]['cement'][accuracy_switch], mix_design_results[3]['water'][accuracy_switch],
                      mix_design_results[3]['fagg'][accuracy_switch], mix_design_results[3]['cagg'][accuracy_switch]]

    # In case mode == pfa or ggbs
    if mode == 'PFA':
        summary_labels.append("Pulverised Fuel Ash (kg/m\u00b3)")
        summary_labels.append(f"Pulverised Fuel Ash (kg per {desired_volume}{preferred_unit})")
        summary_values.append(mix_design_results[2]['pfa'][accuracy_switch])
        summary_values.append(mix_design_results[3]['pfa'][accuracy_switch])

    elif mode == 'GGBS':
        summary_labels.append("Ground Granulated Blast-furnace Slag (kg/m\u00b3)")
        summary_labels.append(f"Ground Granulated Blast-furnace Slag (kg per {desired_volume}{preferred_unit})")
        summary_values.append(mix_design_results[2]['ggbs'][accuracy_switch])
        summary_values.append(mix_design_results[3]['ggbs'][accuracy_switch])

    else:
        pass

    summary = pd.DataFrame({
        'Materials': pd.Series(summary_labels),
        'Quantities': pd.Series(summary_values)
    })

    # Generate report labels and values for the Excel report
    full_report_labels, full_report_values = generate_full_labels_and_values(mode=mode,
                                                                             mix_design_data=mix_design_results,
                                                                             odb_status=odb_status)

    # Append Results based on calculated oven dry batching
    oven_dry_batching(odb_status, full_report_labels, full_report_values, mix_design_results)

    full_results = pd.DataFrame(
        {
            'Mix Design Parameters': pd.Series(full_report_labels),
            'Values': pd.Series(full_report_values)
        }
    )

    return [summary, full_results]


def to_xlsx(path: str, sheets: [pd.DataFrame, pd.DataFrame]) -> None:
    """Converts dataframes as xlsx sheets, then saves in the specified path

    :param path: The user specified path
    :param sheets: (list(pd.DataFrame, pd.DataFrame)): List containing the results as two different pandas dataframes
    """
    # Input check
    if not isinstance(sheets, list) or len(sheets) != 2 or not all(isinstance(sheet, pd.DataFrame) for sheet in sheets):
        raise TypeError("`sheets` must be a list containing two Pandas DataFrames.")

    with pd.ExcelWriter(path) as writer:
        # Save the dataframes into the Excel file
        sheets[0].to_excel(writer, sheet_name='Mix Design Summary', index=False)
        sheets[1].style.set_properties(**{'text-align': 'center'}).to_excel(writer, sheet_name='Full Mix Design Results',
                                                                            index=False)

        for column in sheets[0]:
            column_width = 50
            col_idx = sheets[0].columns.get_loc(column)
            writer.sheets["Mix Design Summary"].set_column(col_idx, col_idx, column_width)

        for column in sheets[1]:
            column_width = 60
            col_idx = sheets[1].columns.get_loc(column)
            writer.sheets["Full Mix Design Results"].set_column(col_idx, col_idx, column_width)


# Suppress numpy & python equality conflict warning
warnings.simplefilter(action='ignore', category=FutureWarning)


def preprocess(dicts: [dict, dict, dict, dict, dict, dict, dict, dict]) -> dict:
    """
    Pre-processing steps are as follows:
        - Take the snapped to 5kg values of self.analyzer.design_results and self.analyzer.mix_design_results
        - Combines all the results into a single dictionary
        - Converts null values `''` to 0
        - Convert all values to string
        - Expand lists into multiple key-value pairs

    :param dicts: list containing the dictionaries, in order of preferred suffix names
    :return: (dict): combined_dict: combined dictionary
    """
    # Set empty dicts for further processing
    combined_dict = {}
    preprocessed_dict = {}
    dr = {}  # design results snapped to 5 kg
    br = {}  # batch results in desired volume

    # Preprocess the design and batch results
    # transform 'cagg': [345.67, 345] to 'cagg': 345
    for k_dr, val_dr in dicts[5].items():
        dr[k_dr] = val_dr[-1]
    dicts[5] = dr

    for k_br, val_br in dicts[6].items():
        br[k_br] = val_br[-1]
    dicts[6] = br

    # Merge & handle duplicate keys
    for i, d in enumerate(dicts):
        for key, value in d.items():
            new_key = key if key not in combined_dict else f"{key}_{i + 1}"
            combined_dict[new_key] = value

    for k, val in combined_dict.items():
        # Expand lists into multiple key-value pairs
        if isinstance(val, list):
            for item in val:
                new_key = f"{k}_{item}"
                preprocessed_dict[new_key] = str(item)
        else:
            # Replace empty values with 0
            preprocessed_value = np.where(val == '', 0, val)

            # Convert all values to strings
            preprocessed_dict[k] = str(preprocessed_value)

    return preprocessed_dict


def process_reports(template_text: str, results) -> str:
    """
    Take in the template test and the engine's results, and processes the template text
    into a standard text ready for formatting

    :param template_text: (str): The template text
    :param results: a list containing the 4 results in dicts from the engine.
    :return: (str): processed_text: The processed text
    """
    # Pre-process the dictionaries into one for direct conversion
    pre_processed_results = preprocess(results)

    # Build a regular expression pattern for all placeholders
    pattern = r"{{{([^}]*)}}}"

    def replace(matching_obj):
        """
        Replace each placeholder with its corresponding value from the dictionary
        :param matching_obj: The corresponding value from the dictionary
        """
        key = matching_obj.group(1)

        return pre_processed_results.get(key, matching_obj.group(0))

    processed_text = re.sub(pattern, replace, template_text)

    return processed_text


def import_md_template(mode: str) -> str:
    """Returns the path to the .md template from the current design mode

    :param mode: The current mix design mode (DOE, AEM, PFA or GGBS)
    :return: md_path: Path to the .md template for processing
    """
    # Retrieve the path to the template file
    md_path = optimix_paths.report_assets[mode]

    return md_path


def generate_md_report(mode: str, design_results: list) -> str:
    """Ensures the current design mode, picks a template and processes the markdown file.

    The markdown file is saved and the path is returned.
    :param design_results: list containing an unpacked `analyzer.data`, 'analyzer.calc_data',
                           'analyzer.design_results', 'analyzer.design_batch_results'
    :param mode: 'DOE', 'AEM', 'PFA' or GGBS
    :return: (str): md_report: Path to the location of the saved md file
    """
    # Get the path to the template .md file
    md_path = import_md_template(mode=mode)

    # Read the markdown file
    with open(md_path, "r") as file:
        template_text = file.read()

    # Process the reports
    processed_text = process_reports(template_text, design_results)

    # Save the updated Markdown text
    save_path = optimix_paths.temp_dir / "mix_design_results.md"
    with open(save_path, "w") as file:
        file.write(processed_text)

    return save_path


def to_pdf(md_file: str, export_path: str):
    """
    Converts the markdown file to pdf given the path of the markdown file
    :param md_file: (str): The path to the markdown file
    :param export_path: (str): The user specified location for saving
    """
    # md2pdf(pdf_file_path=export_path, md_file_path=md_file, base_url=DOE_DIR)
    with open(md_file, 'r') as file:
        md_text = file.read()

    html_text = markdown2.markdown(md_text)
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    pdfkit.from_string(html_text, export_path, configuration=config)


def to_word(md_file: str, export_location: str):
    """
    Converts the markdown file to a docx file given the .md file's location,
    and the user desired location
    :param md_file: (str): The path to the markdown file
    :param export_location: The user specified location for saving
    """
    # Convert the .md file to HTML
    with open(md_file, 'r') as file:
        md_text = file.read()
    html_text = markdown2.markdown(md_text)

    # Save the HTML text to a temporary file
    html_file_path = optimix_paths.temp_dir / "temp.html"
    with open(html_file_path, "w") as f:
        f.write(html_text)

    # Convert html to docx
    convertible = HtmlToDocx()
    convertible.parse_html_file(html_file_path, export_location)

    # Remove the temporary html file
    os.remove(html_file_path)


def color_entry(entry):
    """Handles active entry color changes
    To be used in scripts at the `pages` packages

    :param entry: the entry widget
    """

    def on_entry_focus_in():
        """
        Changes the entry at random from 100 generated colors
        when the entry widget is active
        param event: the binding event of the entry
        """
        entry.config(highlightcolor=np.random.choice(colors))

    def on_entry_focus_out():
        """
        - Changes the highlight color when focus is out

        param event: the binding event of the entry
        """

        entry.config(highlightcolor=white_color)

    # Handle color transitions
    entry.bind("<FocusIn>", lambda event: on_entry_focus_in())

    # Handle numerical validation
    entry.bind("<FocusOut>", lambda event: on_entry_focus_out())


def load_tk_image(file_path: Path | str | io.BytesIO) -> tk.PhotoImage:
    """
    Load an image from the specified path and return a Tkinter PhotoImage object

    :param file_path: (pathlib.Path, io.BytesIO): The file path of the image/bytes object

    :return: photo_image (ImageTk.PhotoImage): Tkinter PhotoImage object representing the loaded image.
    """
    # # Open the image using PIL
    # image = Image.open(path)
    #
    # # Convert the PIL image to a Tkinter PhotoImage
    # photo_image = ImageTk.PhotoImage(image)
    # Handle Path Object
    if isinstance(file_path, Path):
        path = str(file_path)
        try:
            # Open file in binary mode
            with open(path, 'rb') as f:
                data = f.read()
        except IOError as e:
            raise ValueError(f"Error reading image file: {e}") from e

    # Handle string path
    elif isinstance(file_path, str):
        try:
            with open(file_path, "rb") as f:
                data = f.read()
        except IOError as e:
            raise ValueError(f"Error reading image file: {e}") from e

    # Handle in-memory bytes
    elif isinstance(file_path, io.BytesIO):
        data = file_path.getvalue()

    else:
        raise ValueError("Not a valid PNG image")

    # Check for PNG signature (magic bytes)
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError("Not a valid PNG image")

    return tk.PhotoImage(data=data)


def plotly_image_converter(plotly_figure) -> ImageTk.PhotoImage:
    """Converts a plotly figure to an image(*.png)

    Due to a kaleido subprocess error in starting, the following is done before converting the image
        - (--single-process) setting
        - kaleido warmup

    :param plotly_figure:
    :return: png_image: The required image.png for further display in the gui
    """
    # Fix the kaleido subprocess error
    pio.kaleido.scope.chromium_args += ("--single-process",)
    pio.kaleido.scope.mathjax = None

    # Convert the plotly figure to a static image bytes string
    # fig_bytes = io.BytesIO(plotly_figure.to_image(format="png"))
    fig_bytes = io.BytesIO(pio.to_image(fig=plotly_figure, format="png"))

    # Convert the static image bytes string to a Tkinter PhotoImage
    png_image = load_tk_image(fig_bytes)

    return png_image


def entry_check(canvas, entry):
    """
    Checks the input in the entry box
    :param canvas: (tk.Canvas): the target canvas for the top level widget
    :param entry: (tk.Entry) : Tkinter entry box in focus.
    :return fill_status: (list): List that contains true when there are no input errors,
                                 and false when there are input errors
    """
    # Check for incorrect input
    user_input = entry.get().strip()

    if user_input.isnumeric() or user_input.replace('.', '', 1).isnumeric():
        fill_status = [True, True]

    else:
        fill_status = [False, False]

        # Display an error message
        tk.messagebox.showerror(
            title="Invalid input",
            message="Please input a valid value for your desired batching volume.",
            parent=canvas
        )

        # Clear the entry
        entry.delete(0, tk.END)

    return fill_status


def get_path(extension: str):
    """
    Prompts the user to select the path to save the xlsx/pdf/docx file,
    returns the file path for further saving.

    :param extension: THe file type, .xlsx/.docx/.pdf

    :return: (str): file_path: The user's preferred filepath
    """
    if extension == ".xlsx":
        file_path = filedialog.asksaveasfilename(
            confirmoverwrite=True,
            defaultextension=".xlsx",
            filetypes=[("Microsoft Excel Workbook(*.xlsx)", "*.xlsx")],
            initialfile='OptiMix-Concrete-Mix-Design-Results.xlsx',
            title="Choose Export Location"
        )

        return file_path

    elif extension == ".pdf":
        file_path = filedialog.asksaveasfilename(
            confirmoverwrite=True,
            defaultextension=".pdf",
            filetypes=[("PDF Format(*.pdf)", "*.pdf")],
            initialfile='OptiMix-Concrete-Mix-Design-Results.pdf',
            title="Choose PDF Export Location"
        )

        return file_path

    elif extension == ".docx":
        file_path = filedialog.asksaveasfilename(
            confirmoverwrite=True,
            defaultextension=".docx",
            filetypes=[("Microsoft Word Document(*.docx)", "*.docx")],
            initialfile='OptiMix-Concrete-Mix-Design-Results.docx',
            title="Choose DOCX Export Location"
        )

        return file_path


def remove_index(target_list: list, index: int) -> list:
    """
    Remove an element from a list at a specified index

    :param target_list: (list): The input list.
    :param index: (int): The index of the element to remove.
    :return: (list) A new list with the element at the specified index removed
    """
    # Create a copy of the original list
    list_copy = list(target_list)

    # Remove the element at the specified index using del
    del list_copy[index]

    return list_copy
