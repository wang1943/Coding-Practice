import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import numpy as np
import scipy.optimize as opt

# Function to open file dialog and select multiple files
def select_files():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_paths = filedialog.askopenfilenames(title="Select CSV Files", filetypes=[("CSV Files", "*.csv")])
    return list(file_paths)

def gaussian(x, a, x0, sigma):
        return a * np.exp(-(x - x0)**2 / (2 * sigma**2))

# Function to calculate the Full Width at Half Maximum (FWHM)
def calculate_fwhm(x, y):
    # Fit Gaussian, p0 is the initial guess for the fitting coefficients
    params, _ = opt.curve_fit(gaussian, x, y)

    # Calculate FWHM
    fwhm = 2 * np.sqrt(2 * np.log(2)) * params[2]
    return fwhm


# Plot function
def plot_data(x, y, label, xlabel, ylabel, title, output_fname):
    fig, ax = plt.subplots()
    ax.plot(x, y, label=label)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.savefig(f'{output_fname}_{label.split()[0]}.png')


def pre_processing(ions_of_interests, general_info, skiprows, show_plots=True):
    # Select multiple files
    file_paths = select_files()

    for input_fname in file_paths:
        # Read the CSV file
        data = pd.read_csv(input_fname, skiprows=skiprows)

        new_ion_data = data[general_info + ions_of_interests]
        normalized_ion_data = new_ion_data.div(new_ion_data[ions_of_interests].sum(axis=1), axis=0) * 100

        # Extract distance and normalized concentrations
        distance = data[general_info[0]]
        output_fname = 'raw_' + input_fname.split('/')[-1].split('.')[0]
        xlabel = 'Distance (nm)'
        ylabel = 'Normalized Concentration (%)'

        for label in ions_of_interests:
            concentration = normalized_ion_data[label]
            # Export csv
            normalized_ion_data.to_csv(f'{output_fname}_normalized_SiGeB.csv', index=False)
            # Plot
            plot_data(distance, concentration, label=label, xlabel=xlabel, ylabel=ylabel,
                    title=f'{label.split()[0]} vs {xlabel} ({output_fname})', 
                    output_fname=output_fname)



    if show_plots:
        plt.show()
    

def post_processing(pre_ions_of_interests, post_ions_of_interests, general_info, show_plots=True):
    # Select multiple files
    file_paths = select_files()

    fwhm = []

    for input_fname in file_paths:
        # Read the CSV file
        data = pd.read_csv(input_fname)

        # Extract distance and normalized concentrations
        distance = data[general_info[0]]
        output_fname = 'processed_' + input_fname.split('/')[-1].split('.')[0]
        xlabel = 'Distance (nm)'
        ylabel = 'Normalized Concentration (%)'

        for label in post_ions_of_interests:
            concentration = data[label]
            fwhm.append(calculate_fwhm(distance, concentration))

    scaling_factor = np.mean(fwhm) / np.array(fwhm)
    print('The average FWHM is:', np.mean(fwhm))
    for input_fname in file_paths:
        # Read the CSV file
        data = pd.read_csv(input_fname)
        output_fname = 'processed_' + input_fname.split('/')[-1].split('.')[0]
        data['scaled_distance (nm)'] = data[general_info[0]] * scaling_factor
        
        # Plot
        for label in pre_ions_of_interests:
            concentration = data[label]
            # Export csv
            data.to_csv(f'{output_fname}_normalized_SiGeB.csv', index=False)
            # Plot
            plot_data(data['scaled_distance (nm)'], concentration, label=label, xlabel=xlabel, ylabel=ylabel,
                    title=f'{label.split()[0]} vs {xlabel} ({output_fname})', 
                    output_fname=output_fname)



    if show_plots:
        plt.show()



if __name__ == "__main__":

    # No need to change unless file format changes
    skiprows = 1

    # Frequently used parameters, need input
    pre_ions_of_interests = ['Si atom%', 'Ge atom%', 'B atom%']
    general_info = ['Distance (nm)']

    pre_processing(pre_ions_of_interests, general_info, skiprows)

    post_ions_of_interests = ['Ge atom%']

    post_processing(pre_ions_of_interests, post_ions_of_interests, general_info)


    pass