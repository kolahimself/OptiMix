"""reference_data.py

Central storage for diverse reference data in nested dictionaries, dataframes and lists.
"""

import pandas as pd
from typing import Tuple
from core.utils.file_paths import optimix_paths

# Figure 3, relationship between standard deviation and characteristic strength.
figure_iii = {
    'More than 20': pd.DataFrame(
        {
            'Characteristic Strength': [0, 10, 20, 30, 40, 50, 60, 70],
            'Standard Deviation': [0, 2, 4, 4, 4, 4, 4, 4]
        }),

    'Less than 20': pd.DataFrame(
        {
            'Characteristic Strength': [0, 5, 10, 15, 20, 30, 40, 50, 60, 70],
            'Standard Deviation': [0, 2, 4, 6, 8, 8, 8, 8, 8, 8]
        }
    )
}

# Table 2, Approximate compressive strengths (N/mm2) of concrete mixes made with a free water/cement ratio
table_ii = {
    ('OPC', 'Crushed'): {
        3: 27,
        7: 36,
        28: 49,
        91: 56
    },
    ('OPC', 'Uncrushed'): {
        3: 22,
        7: 30,
        28: 42,
        91: 49
    },
    ('SRPC', 'Crushed'): {
        3: 27,
        7: 36,
        28: 49,
        91: 56
    },
    ('SRPC', 'Uncrushed'): {
        3: 22,
        7: 30,
        28: 42,
        91: 49
    },
    ('RHPC', 'Crushed'): {
        3: 34,
        7: 43,
        28: 55,
        91: 61
    },
    ('RHPC', 'Uncrushed'): {
        3: 29,
        7: 37,
        28: 48,
        91: 54
    }
}

# Figure 4, relationship between compressive strength and free-water/cement ratio
chart_iv = [pd.read_csv(plot_path) for plot_path in optimix_paths.fwc_plot_paths]

# Table 3, Approximate free-water contents (kg/m3) required to give various levels of workability
table_iii_a = {
    (0, 'Crushed'): {
        '0-10mm': 0,
        '10-30mm': 0,
        '30-60mm': 0,
        '60-180mm': 0
    },
    (10, 'Uncrushed'): {
        '0-10mm': 150,
        '10-30mm': 180,
        '30-60mm': 205,
        '60-180mm': 225
    },
    (10, 'Crushed'): {
        '0-10mm': 180,
        '10-30mm': 205,
        '30-60mm': 230,
        '60-180mm': 250
    },
    (20, 'Uncrushed'): {
        '0-10mm': 135,
        '10-30mm': 160,
        '30-60mm': 180,
        '60-180mm': 195
    },
    (20, 'Crushed'): {
        '0-10mm': 170,
        '10-30mm': 190,
        '30-60mm': 210,
        '60-180mm': 225
    },
    (40, 'Uncrushed'): {
        '0-10mm': 115,
        '10-30mm': 140,
        '30-60mm': 160,
        '60-180mm': 175
    },
    (40, 'Crushed'): {
        '0-10mm': 155,
        '10-30mm': 175,
        '30-60mm': 190,
        '60-180mm': 205
    }
}

table_iii_b = {
    0: {
        '0-10mm': 0,
        '10-30mm': 0,
        '30-60mm': 0,
        '60-180mm': 0
    },
    10: {
        '0-10mm': 5,
        '10-30mm': 5,
        '30-60mm': 5,
        '60-180mm': 10
    },
    20: {
        '0-10mm': 10,
        '10-30mm': 10,
        '30-60mm': 10,
        '60-180mm': 15
    },
    30: {
        '0-10mm': 15,
        '10-30mm': 15,
        '30-60mm': 20,
        '60-180mm': 20
    },
    40: {
        '0-10mm': 20,
        '10-30mm': 20,
        '30-60mm': 25,
        '60-180mm': 25
    },
    50: {
        '0-10mm': 25,
        '10-30mm': 25,
        '30-60mm': 30,
        '60-180mm': 30
    }
}


# Results to be exported for .xlsx reporting
def generate_full_labels_and_values(mode: str, mix_design_data: list, odb_status: int) -> Tuple[list, list]:
    """Generate full report labels and values for .xlsx reporting

    :param mode: The current mix design mode (DOE, AEM, PFA or GGBS)
    :param mix_design_data: [a, b, c, d] a list of `analyzer.data`, analyzer.calc_data, analyzer.design_results,
                            analyzer.design_batch_results
    :param odb_status: Specified status for oven dry batching of aggregates
    """
    if mode == 'DOE':
        labels = ["Characteristic Strength (N/mm\u00b2)",
                  "Age (days)",
                  "Proportion Defective (%)",
                  "Risk Factor, k",
                  "Standard Deviation (N/mm\u00b2)",
                  "Margin (N/mm\u00b2)",
                  "Target Mean Strength (N/mm\u00b2)",
                  "Cement Type",
                  "Coarse Aggregate Type",
                  "Fine Aggregate Type",
                  "Approximate Compressive Strength (0.5fwc)",
                  "Predetermined Free-Water/Cement Ratio",
                  "Maximum Free-Water/Cement Ratio",
                  "Slump",
                  "Aggregate Sizes (mm)",
                  "Maximum Aggregate Size (mm)",
                  "Free-Water Content (kg/m\u00b3)",
                  "Calculated Cement Content (kg/m\u00b3)",
                  "Maximum Cement Content (kg/m\u00b3)",
                  "Minimum Cement Content (kg/m\u00b3)",
                  "Final Cement Content",
                  "Modified Free-Water/Cement Ratio",
                  "Relative Density of Aggregate in SSD",
                  "Concrete Density (kg/m\u00b3)",
                  "Total Aggregate Content (kg/m\u00b3)",
                  "Grading of Fine Aggregate (Percentage passing 600\u0370m) (%)",
                  "Proportion of Fine Aggregate (%)",
                  "Fine Aggregate Content (kg/m\u00b3)",
                  "Coarse Aggregate Content (kg/m\u00b3)",
                  "Oven Dry Batching",
                  "Coarse Aggregate Proportioning"]

        values = [mix_design_data[0]['Specified variables']['Characteristic Strength'],
                  mix_design_data[0]['Specified variables']['Curing Days'],
                  mix_design_data[1]['perc_def'],
                  mix_design_data[1]['k'],
                  mix_design_data[1]['sd'],
                  mix_design_data[1]['margin'],
                  mix_design_data[1]['fm'],
                  mix_design_data[0]['Specified variables']['Cement Type'],
                  mix_design_data[0]['Additional info']['Coarse Aggregate Type'],
                  mix_design_data[0]['Additional info']['Fine Aggregate Type'],
                  mix_design_data[1]['approx_strength'],
                  mix_design_data[1]['initial_fwc_ratio'],
                  mix_design_data[0]['Specified variables']['Maximum free water-cement ratio'],
                  mix_design_data[0]['Specified variables']['Slump'],
                  mix_design_data[1]['aggregate_sizes'],
                  mix_design_data[1]['max_agg_size'],
                  mix_design_data[1]['fw_content'],
                  mix_design_data[1]['calc_cement_content'],
                  mix_design_data[0]['Specified variables']['Maximum cement content'],
                  mix_design_data[0]['Specified variables']['Minimum cement content'],
                  mix_design_data[1]['cement_content'],
                  mix_design_data[1]['modified_fwc_ratio'],
                  mix_design_data[1]['ssd_value'],
                  mix_design_data[1]['wet_conc_density'],
                  mix_design_data[1]['total_agg_content'],
                  mix_design_data[1]['perc_passing'],
                  mix_design_data[1]['fine_agg_prop'],
                  mix_design_data[1]['calc_fine_agg_content'],
                  mix_design_data[1]['calc_coarse_agg_content'],
                  odb_status,
                  mix_design_data[1]['cagg_proportions']]

        return labels, values

    elif mode == 'AEM':
        labels = ["Characteristic Strength (N/mm\u00b2)",
                  "Age (days)",
                  "Proportion Defective (%)",
                  "Risk Factor, k",
                  "Standard Deviation (N/mm\u00b2)",
                  "Margin (N/mm\u00b2)",
                  "Air Content (%)",
                  "Compressive Strength Loss (%)",
                  "Target Mean Strength (N/mm\u00b2)",
                  "Cement Type",
                  "Coarse Aggregate Type",
                  "Fine Aggregate Type",
                  "Approximate Compressive Strength (0.5fwc)",
                  "Predetermined Free-Water/Cement Ratio",
                  "Maximum Free-Water/Cement Ratio",
                  "Slump (mm)",
                  "Reduced Slump Category (mm)",
                  "Aggregate Sizes (mm)",
                  "Maximum Aggregate Size (mm)",
                  "Free-Water Content (kg/m\u00b3)",
                  "Calculated Cement Content (kg/m\u00b3)",
                  "Maximum Cement Content (kg/m\u00b3)",
                  "Minimum Cement Content (kg/m\u00b3)",
                  "Final Cement Content (kg/m\u00b3)",
                  "Modified Free-Water/Cement Ratio",
                  "Relative Density of Aggregate in SSD",
                  "Concrete Density from Graphical Interpolation",
                  "Calculated Concrete Density (kg/m\u00b3)",
                  "Total Aggregate Content (kg/m\u00b3)",
                  "Grading of Fine Aggregate (Percentage passing 600\u0370m) (%)",
                  "Proportion of Fine Aggregate (%)",
                  "Fine Aggregate Reduction (%)",
                  "Fine Aggregate Content (kg/m\u00b3)",
                  "Coarse Aggregate Content (kg/m\u00b3)",
                  "Oven Dry Batching",
                  "Coarse Aggregate Proportioning (kg/m\u00b3)"]

        values = [mix_design_data[0]['Specified variables']['Characteristic Strength'],
                  mix_design_data[0]['Specified variables']['Curing Days'],
                  mix_design_data[1]['perc_def'],
                  mix_design_data[1]['k'],
                  mix_design_data[1]['sd'],
                  mix_design_data[1]['margin'],
                  mix_design_data[0]['Specified variables']['Air Content'],
                  mix_design_data[0]['Specified variables']['Strength Loss'],
                  mix_design_data[1]['fm'],
                  mix_design_data[0]['Specified variables']['Cement Type'],
                  mix_design_data[0]['Additional info']['Coarse Aggregate Type'],
                  mix_design_data[0]['Additional info']['Fine Aggregate Type'],
                  mix_design_data[1]['approx_strength'],
                  mix_design_data[1]['initial_fwc_ratio'],
                  mix_design_data[0]['Specified variables']['Maximum free water-cement ratio'],
                  mix_design_data[0]['Specified variables']['Slump'],
                  mix_design_data[1]['modified_slump_value'],
                  mix_design_data[1]['aggregate_sizes'],
                  mix_design_data[1]['max_agg_size'],
                  mix_design_data[1]['fw_content'],
                  mix_design_data[1]['calc_cement_content'],
                  mix_design_data[0]['Specified variables']['Maximum cement content'],
                  mix_design_data[0]['Specified variables']['Minimum cement content'],
                  mix_design_data[1]['cement_content'],
                  mix_design_data[1]['modified_fwc_ratio'],
                  mix_design_data[1]['ssd_value'],
                  mix_design_data[1]['density_from_plot'],
                  mix_design_data[1]['wet_conc_density'],
                  mix_design_data[1]['total_agg_content'],
                  mix_design_data[1]['perc_passing'],
                  mix_design_data[1]['fine_agg_prop'],
                  mix_design_data[0]['Additional info']['Fine Aggregate Reduction'],
                  mix_design_data[1]['calc_fine_agg_content'],
                  mix_design_data[1]['calc_coarse_agg_content'],
                  odb_status,
                  mix_design_data[1]['cagg_proportions']]

        return labels, values

    elif mode == 'PFA':
        labels = ["Characteristic Strength (N/mm\u00b2)",
                  "Age (days)",
                  "Proportion Defective (%)",
                  "Risk Factor, k",
                  "Standard Deviation (N/mm\u00b2)",
                  "Margin (N/mm\u00b2)",
                  "Target Mean Strength (N/mm\u00b2)",
                  "Cement Type",
                  "Coarse Aggregate Type",
                  "Fine Aggregate Type",
                  "Approximate Compressive Strength (0.5fwc)",
                  "Predetermined Free-Water/Cement Ratio",
                  "Slump",
                  "Aggregate Sizes",
                  "Maximum Aggregate Size",
                  "Proportion of pfa (%)",
                  "Cementing Efficiency Factor",
                  "Predetermined Free-Water Content (kg/m\u00b3)",
                  "Free-Water Content Reduction (kg/m\u00b3)",
                  "Free-Water Content (kg/m\u00b3)",
                  "Calculated Cement Content (kg/m\u00b3)",
                  "Maximum Cement Content (kg/m\u00b3)",
                  "Minimum Cement Content (kg/m\u00b3)",
                  "Maximum Free-Water/Cement Ratio",
                  "Modified Free-Water/Cement Ratio",
                  "Portland Cement Content (kg/m\u00b3)",
                  "pfa Content (kg/m\u00b3)",
                  "Total Cementitious Content (kg/m\u00b3)",
                  "Relative Density of Aggregate in SSD",
                  "Concrete Density (kg/m\u00b3)",
                  "Total Aggregate Content (kg/m\u00b3)",
                  "Grading of Fine Aggregate (Percentage passing 600\u0370m) (%)",
                  "Proportion of Fine Aggregate (%)",
                  "Fine Aggregate Content (kg/m\u00b3)",
                  "Coarse Aggregate Content (kg/m\u00b3)",
                  "Oven Dry Batching",
                  "Coarse Aggregate Proportioning"]

        values = [mix_design_data[0]['Specified variables']['Characteristic Strength'],
                  mix_design_data[0]['Specified variables']['Curing Days'],
                  mix_design_data[1]['perc_def'],
                  mix_design_data[1]['k'],
                  mix_design_data[1]['sd'],
                  mix_design_data[1]['margin'],
                  mix_design_data[1]['fm'],
                  mix_design_data[0]['Specified variables']['Cement Type'],
                  mix_design_data[0]['Additional info']['Coarse Aggregate Type'],
                  mix_design_data[0]['Additional info']['Fine Aggregate Type'],
                  mix_design_data[1]['approx_strength'],
                  mix_design_data[1]['initial_fwc_ratio'],
                  mix_design_data[0]['Specified variables']['Slump'],
                  mix_design_data[1]['aggregate_sizes'],
                  mix_design_data[1]['max_agg_size'],
                  mix_design_data[0]['Specified variables']['pfa Proportion'],
                  mix_design_data[0]['Additional info']['Cementing Efficiency Factor'],
                  mix_design_data[1]['initial_fw_content'],
                  mix_design_data[1]['fw_reduction'],
                  mix_design_data[1]['fw_content'],
                  mix_design_data[1]['calc_cement_content'],
                  mix_design_data[0]['Specified variables']['Maximum cement content'],
                  mix_design_data[0]['Specified variables']['Minimum cement content'],
                  mix_design_data[0]['Specified variables']['Maximum free water-cement ratio'],
                  mix_design_data[1]['modified_fwc_ratio'],
                  mix_design_data[1]["C"],
                  mix_design_data[1]["F"],
                  mix_design_data[1]['final_cementitious_content'],
                  mix_design_data[1]['ssd_value'],
                  mix_design_data[1]['wet_conc_density'],
                  mix_design_data[1]['total_agg_content'],
                  mix_design_data[1]['perc_passing'],
                  mix_design_data[1]['fine_agg_prop'],
                  mix_design_data[1]['calc_fine_agg_content'],
                  mix_design_data[1]['calc_coarse_agg_content'],
                  odb_status,
                  mix_design_data[1]['cagg_proportions']]

        return labels, values

    elif mode == 'GGBS':
        labels = ["Characteristic Strength (N/mm\u00b2)",
                  "Age (days)",
                  "Proportion Defective (%)",
                  "Risk Factor, k",
                  "Standard Deviation (N/mm\u00b2)",
                  "Margin (N/mm\u00b2)",
                  "Target Mean Strength (N/mm\u00b2)",
                  "Cement Type",
                  "Coarse Aggregate Type",
                  "Fine Aggregate Type",
                  "Proportion of ggbs (%)",
                  "Approximate Compressive Strength (0.5fwc)",
                  "Predetermined Free-Water/Cement Ratio",
                  "Slump",
                  "Aggregate Sizes",
                  "Maximum Aggregate Size",
                  "Predetermined Free-Water Content (kg/m\u00b3)",
                  "Water Content Reduction (kg/m\u00b3)",
                  "Free-Water Content (kg/m\u00b3)",
                  "Calculated Cement Content (kg/m\u00b3)",
                  "Maximum Cement Content (kg/m\u00b3)",
                  "Minimum Cement Content (kg/m\u00b3)",
                  "Maximum Free-Water/Cement Ratio",
                  "Modified Free-Water/Cement Ratio",
                  "Portland Cement Content (kg/m\u00b3)",
                  "ggbs Content (kg/m\u00b3)",
                  "Total Cementitious Content (kg/m\u00b3)",
                  "Relative Density of Aggregate in SSD",
                  "Concrete Density (kg/m\u00b3)",
                  "Total Aggregate Content (kg/m\u00b3)",
                  "Grading of Fine Aggregate (Percentage passing 600\u0370m) (%)",
                  "Proportion of Fine Aggregate (%)",
                  "Fine Aggregate Content (kg/m\u00b3)",
                  "Coarse Aggregate Content (kg/m\u00b3)",
                  "Oven Dry Batching",
                  "Coarse Aggregate Proportioning"]

        values = [mix_design_data[0]['Specified variables']['Characteristic Strength'],
                  mix_design_data[0]['Specified variables']['Curing Days'],
                  mix_design_data[1]['perc_def'],
                  mix_design_data[1]['k'],
                  mix_design_data[1]['sd'],
                  mix_design_data[1]['margin'],
                  mix_design_data[1]['fm'],
                  mix_design_data[0]['Specified variables']['Cement Type'],
                  mix_design_data[0]['Additional info']['Coarse Aggregate Type'],
                  mix_design_data[0]['Additional info']['Fine Aggregate Type'],
                  mix_design_data[0]['Specified variables']['pfa Proportion'],
                  mix_design_data[1]['approx_strength'],
                  mix_design_data[1]['initial_fwc_ratio'],
                  mix_design_data[0]['Specified variables']['Slump'],
                  mix_design_data[1]['aggregate_sizes'],
                  mix_design_data[1]['max_agg_size'],
                  mix_design_data[1]['initial_fw_content'],
                  mix_design_data[1]['fw_reduction'],
                  mix_design_data[1]['fw_content'],
                  mix_design_data[1]['calc_cement_content'],
                  mix_design_data[0]['Specified variables']['Maximum cement content'],
                  mix_design_data[0]['Specified variables']['Minimum cement content'],
                  mix_design_data[0]['Specified variables']['Maximum free water-cement ratio'],
                  mix_design_data[1]['modified_fwc_ratio'],
                  mix_design_data[1]["C"],
                  mix_design_data[1]["G"],
                  mix_design_data[1]['final_cementitious_content'],
                  mix_design_data[1]['ssd_value'],
                  mix_design_data[1]['wet_conc_density'],
                  mix_design_data[1]['total_agg_content'],
                  mix_design_data[1]['perc_passing'],
                  mix_design_data[1]['fine_agg_prop'],
                  mix_design_data[1]['calc_fine_agg_content'],
                  mix_design_data[1]['calc_coarse_agg_content'],
                  odb_status,
                  mix_design_data[1]['cagg_proportions']]

        return labels, values
