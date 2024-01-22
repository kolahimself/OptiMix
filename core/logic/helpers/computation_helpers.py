"""computation_helpers.py

Helper functions for numerical calculations used across all design modes.
"""
import numpy as np
import pandas as pd
from scipy.stats import norm, linregress
from scipy.interpolate import splrep, splev, interp1d
from scipy.signal import savgol_filter

from core.logic.reference_data import table_ii, table_iii_b

from typing import List, Tuple


def compute_risk_factor(defective_rate: float, mean: float = 40, sd: float = 5) -> float:
    """Calculates the risk factor (z-score) for concrete mix design based in defectives.

    :param defective_rate: (float): Percentage of defective samples in the mix (0-100).
    :param mean: Average compressive strength, gotten from fig 1 to be 40
    :param sd: Standard deviation of the compressive strength, gotten from fig 1 to be 5
    :return: z_score (float): The z-score representing the risk factor associated with the given defective rate.

    Key points:
        - Higher risk factor indicates a greater proportion of samples falling below the desired strength.
        - Used for optimizing mix design and quality control on concrete production.
    """
    # Convert defective rate to quantile
    quantile = 1 - (defective_rate / 100)

    # Value of the datapoint in the specific normal distribution (sd=5, mean=40)
    x = norm.ppf(quantile, loc=mean, scale=sd)

    # Compute the z-score
    z_score = (x - mean) / sd

    return z_score


def interpolate(x: np.ndarray | pd.DataFrame | list,
                y: np.ndarray | pd.DataFrame | list,
                target_var: float,
                find_x: bool = False,
                kind: str = 'linear'):
    """
    Interpolate between x and y datapoints

    :param x: (np.ndarray, pd.Dataframe, list) numpy, pandas dataframe or list array containing x values
    :param y: (np.ndarray, pd.Dataframe, list) numpy, pandas dataframe or list numpy array containing y values
    :param target_var: (float) desired interpolation point
    :param find_x: (bool): Performs inverse interpolation for x-values instead
    :param kind: (str): Type of interpolation to be performed, types are ('linear', 'spline')
    :return: f: (float), result of the interpolation
    """
    if kind == 'linear':
        if find_x:
            interpolator = interp1d(x=y[::-1], y=x[::-1], fill_value='extrapolate')
            # f = np.interp(x=target_var, xp=y[::-1], fp=x[::-1])
            return interpolator(target_var)

        else:
            interpolator = interp1d(x=x, y=y, fill_value='extrapolate')
            return interpolator(target_var)

    else:
        if find_x:
            # Reverse interpolation
            # Calculate the spline coefficients with interpolate.splrep
            coeffs = splrep(x=y[::-1], y=x[::-1])

            # Evaluate the spline at the desired point
            f = splev(target_var, coeffs, ext=0)

            return float(f)

        else:
            # Normal interpolation
            # Calculate the spline coefficients with interpolate.splrep
            coeffs = splrep(x=x, y=y)

            # Evaluate the spline at the desired point
            f = splev(target_var, coeffs, ext=0)

            return float(f)


def get_approximate_strength(cement_type: str, coarse_agg_type: str, curing_days: float) -> float:
    """
    Determines the approximate compressive strength from
    cement type (OPC, SRPC, RHPC), coarse aggregate type(Crushed or Uncrushed),
    and target curing age. Reference is table 2 fig 4 in DOE method of mix design.

    :param cement_type: (str): OPC/RHPC/SRPC
    :param coarse_agg_type: (str): Crushed/Uncrushed
    :param curing_days: (float):  Desired curing age.
    """

    # Extract the relevant strength data from the table
    strength_data = table_ii[(cement_type, coarse_agg_type)]
    ages = np.array(list(strength_data.keys()))  # Curing ages
    strengths = np.array(list(strength_data.values()))  # Strengths

    # Perform linear interpolation to estimate strength for the given age
    approximate_strength = interpolate(x=ages, y=strengths, target_var=curing_days)

    return approximate_strength


def linear_function(x: np.ndarray, coeffs: list) -> np.ndarray:
    """Calculates the y-values from x values such that the relationship is linear

    :param x: (np.ndarray): The x-values
    :param coeffs: (list): [a, b]: coefficients a & b in y = ax + b
    :return: y: (np.ndarray): The y-value calculated using equation of a line.
    """
    # Apply linear function
    y = np.multiply(coeffs[0], x) + coeffs[1]

    return y


def create_linear_points(x_range: list, coeffs: list, number_of_points: int = 400) -> pd.DataFrame:
    """Makes x-y datapoints for a linear function using the defined range and coefficients

    :param x_range: (list): [start, end] list containing starting and ending x points
    :param coeffs: (list): [a, b]: coefficients a & b in y = ax + b
    :param number_of_points: (int): Desired number of points, default is 300. Computation optimum

    :return: (pd.DataFrame): returns a dataframe containing 2 columns, 'x' and 'y'
    """
    # Generate x-value datapoints using the specified range
    x_vals = np.linspace(x_range[0], x_range[1], num=number_of_points)

    # Make the plot
    return pd.DataFrame({
        'x': pd.Series(x_vals),
        ' y': pd.Series(linear_function(x_vals, coeffs))
    })


def generate_figure_v() -> List[pd.DataFrame]:
    """
    Generates datapoints for the lines depicting the relative density at ssd in figure 5
    :return: figure_v: Dataframe containing each line from 2.4 till 2.9
    """
    # X-axis range (free-water content, from 100 - 260 as seen in figure 5)
    fwc_range = [100, 260]

    # List of coefficients for 2.4, 2.5, 2.6, 2.7, 2.8 & 2.9 lines
    ssd_coeffs = [
        [-0.925, 2402],
        [-1.03125, 2493.125],
        [-1.25, 2605],
        [-1.4375, 2703.75],
        [-1.59375, 2804.375],
        [-1.71875, 2896.875]
    ]

    # Efficiently create the datapoints for each ssd line in figure_v
    figure_v = [create_linear_points(fwc_range, coeffs) for coeffs in ssd_coeffs]

    return figure_v


def fit_linreg(x_range: list, y: pd.Series | np.ndarray) -> list:
    """Finds the equation of the best fitting line through linear regression.

    :param x_range: (list): [start, end] list containing starting and ending x points
    :param y: corresponding values of the x values to be used.
    :return: coefficients: (list): returns slope and intercept as coefficients [slope, intercept]
    """
    # Generate x values given the range
    x = np.linspace(x_range[0], x_range[1], num=len(y))

    # Create the linear regression model
    linreg = linregress(x, y)

    # Retrieve the slope and intercept as coefficients
    coefficients = [linreg.slope, linreg.intercept]

    return coefficients


def compute_fwc_ratio(fm: float, approx_strength: float) -> float:
    """
    Computes the free-water/cement ratio based on these relations:

    f_m/approx_strength = -0.2 + 0.6(1/fwc) for approx_strength > 30 N/mm2
    f_m/approx_strength = -0.73 + 0.865(1/fwc) for approx_strength <= 30 30 N/mm2

    :param fm: (float): the target mean strength
    :param approx_strength: Approximate compressive strengths (N/mm2) of concrete mixes made with a free-water/cement ratio of 0.5
    :return: (fwc_ratio): The free water to cement ratio required to achieve the target mean strength.
    """
    if approx_strength > 30:
        # Compute the required water-cement ratio when approx_strength > 30 N/mm2
        fwc_ratio = 1 / (((fm / approx_strength) + 0.2) / 0.6)

    else:
        # Compute the required water-cement ratio for approx_strengths <= 30 N/mm2
        fwc_ratio = 1 / (((fm / approx_strength) + 0.73) / 0.865)

    return fwc_ratio


def sg_filter(data: pd.DataFrame) -> pd.DataFrame:
    """
    Smoothens the ' y' column of a Dataframe using the Savitzky-Golay filter.
    :param data: (pd.DataFrame): Dataframe containing 'x' and ' y' columns.
    :return: (pd.DataFrame): Dataframe with the same 'x' column and the smoothened ' y' column
    """
    # I want to keep ' y' column as the same title as it is used throughout the backend
    x = data['x']

    # Apply the Savitzky-Golay filter on the y values
    y = pd.Series(savgol_filter(data[' y'], window_length=31, polyorder=2))

    # Create the new dataframe
    df = pd.DataFrame({'x': x, ' y': y})

    return df


def get_fw_reduction(p: float, slump_category: str) -> float:
    """
    Retrieves the required reduction in fw content for the cement-pfa mix from table_iii_b.

    It includes a powerful option of retrieving reductions of pfa proportions in between [10, 20...50] by linear interpolation
    :param p: (float): Proportion of pfa in the cement-pfa mix
    :param slump_category: The category in the slump value falls in, supplied by user
    :return: reduction (float): The required reduction in free water content.
    """
    # Extract needed values
    standard_pfa_values = np.array(list(table_iii_b.keys()))
    slump_values = np.array([table_iii_b[pfa_prop][slump_category] for pfa_prop in standard_pfa_values])

    # Retrieve the reduction via interpolation
    reduction = interpolate(x=standard_pfa_values, y=slump_values,
                            target_var=p, kind='linear')

    return reduction


def offset_curve(x: np.ndarray, y: np.ndarray, d: float) -> Tuple[np.ndarray, np.ndarray]:
    """Generates coordinates of a curve parallel to the given curve with a specified offset distance.

    :param x: (np.ndarray): x-coordinates of the original curve
    :param y: (np.ndarray): y-coordinates of the original curve
    :param d: The desired distance between the original curve and the parallel curve.
    :returns (np.ndarray, np.ndarray): x-coords and y-coords of the generated parallel curve
    """
    # Compute first-order gradients
    first_derivative_x = np.gradient(x)
    first_derivative_y = np.gradient(y)

    # Normalize gradients to get unit normal vectors
    normal_vectors = np.stack((first_derivative_y, -first_derivative_x), axis=1)
    unit_normal_vectors = normal_vectors / np.linalg.norm(normal_vectors, axis=1)[:, np.newaxis]

    # Generate parallel curve coordinates
    x_parallel = x + unit_normal_vectors[:, 0] * d
    y_parallel = y + unit_normal_vectors[:, 1] * d

    # Smoothen the y-coordinates of the parallel curve
    # y_parallel = np.array(sg_filter(pd.DataFrame({'x': x_parallel, ' y': y_parallel})[' y']))

    return x_parallel, y_parallel


def aem_workability_modifier(supplied_slump_category: str) -> str:
    """
    Function that corrects the slump category in order to take the water content from a lower workability,
    used in air-entrained mix design.

    :param supplied_slump_category: (str): The slump category specified by the user
    :return: modified_slump_category: (str)
    """

    # Slump categories
    slump_categories = ['0-10mm', '10-30mm', '30-60mm', '60-180mm']

    if supplied_slump_category in slump_categories:

        # Retrieve the element's index
        index = slump_categories.index(supplied_slump_category)

        if index > 0:
            # Return a lower workability
            modified_slump_category = slump_categories[index - 1]

            return modified_slump_category

    # Use 0-10mm if slump is between 0-10mm
    modified_slump_category = supplied_slump_category

    return modified_slump_category


def snap_to_nearest_five(value: float | int | list | np.ndarray) -> int:
    """
    Rounds off the given value to the nearest multiple of five.

    :param value: (float, int or list): The input value to be rounded.
    :return: int: The rounded value to the nearest multiple of five.
    """
    rounded_value = np.round(np.array(value) / 5) * 5
    rounded_value = rounded_value.astype(int)

    return rounded_value


def batch(quantities: list, batch_volume: float) -> list:
    """
    Converts the quantities required per metre cube to the desired batching volume.
    :param quantities: The quantities to be adjusted
    :param batch_volume: Batching volume to be adjusted to
    """
    batched_volume = [np.multiply(quantity, batch_volume) for quantity in quantities]

    return batched_volume
