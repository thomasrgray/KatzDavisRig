#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 14:27:01 2019

@author: bradly
"""
# =============================================================================
# Import stuff
# =============================================================================

# import Libraries
import os
import numpy as np
import easygui
import pandas as pd
import itertools
import glob
from datetime import date

# =============================================================================
# # #DEFINE ALL FUNCTIONS
# =============================================================================

def boolean_indexing(v, fillval=np.nan):
    lens = np.array([len(item) for item in v])
    mask = lens[:, None] > np.arange(lens.max())
    out = np.full(mask.shape, fillval)
    out[mask] = np.concatenate(v)
    return out

def MedMS8_reader_stone(file_name, file_check):
    """
    Input: File Name (with directory) from MedAssociates Davis Rig (e.g. .ms8.txt)
    Output: Dictionary containing a dataframe (all lick data categorized), file
            information (animal name, date of recording, etc), and a matrix
            with all latencies between licks by trial
    """
    with open(file_name) as file_input:
        lines = file_input.readlines()

    Detail_Dict = {
        'FileName': None,
        'StartDate': None,
        'StartTime': None,
        'Animal': None,
        'Condition': None,
        'MAXFLick': None,
        'Trials': None,
        'LickDF': None,
        'LatencyMatrix': None
    }
    
    # Extract file name and store
    Detail_Dict['FileName'] = os.path.basename(file_name)
    
    # Store details in dictionary and construct dataframe
    for i, line in enumerate(lines):
        if "Start Date" in line:
            Detail_Dict['StartDate'] = line.split(',')[-1].strip()
        elif "Start Time" in line:
            Detail_Dict['StartTime'] = line.split(',')[-1].strip()
        elif "Animal ID" in line:
            Detail_Dict['Animal'] = line.split(',')[-1].strip()
        elif "Max Wait" in line:
            Detail_Dict['MAXFLick'] = line.split(',')[-1].strip()
        elif "Max Number" in line:
            Detail_Dict['Trials'] = line.split(',')[-1].strip()
        elif "PRESENTATION" in line and "TUBE" in line:
            ID_line = i
        elif len(line.strip()) == 0:
            Trial_data_stop = i
            if ID_line > 0 and Trial_data_stop > 0:
                # Create dataframe
                df = pd.DataFrame(
                    columns=lines[ID_line].split(','),
                    data=[row.split(',') for row in lines[ID_line + 1:Trial_data_stop]]
                )
                
                # Remove spaces in column headers
                df.columns = df.columns.str.replace(' ', '')
                
                # Set concentrations to 0 if concentration column blank
                df['CONCENTRATION'] = df['CONCENTRATION'].str.strip()
                df['CONCENTRATION'] = df['CONCENTRATION'].replace('', 0).astype(float)

                # Convert specific columns to numeric
                df["SOLUTION"] = df["SOLUTION"].str.strip()
                df[["PRESENTATION", "TUBE", "CONCENTRATION", "LICKS", "Latency"]] = \
                    df[["PRESENTATION", "TUBE", "CONCENTRATION", "LICKS", "Latency"]].apply(pd.to_numeric)
                
                # Add in identifier columns
                df.insert(loc=0, column='Animal', value=Detail_Dict['Animal'])
                df.insert(loc=3, column='Trial_num', value='')
                df['Trial_num'] = df.groupby('TUBE').cumcount() + 1
                
                # Store in dictionary
                Detail_Dict['LickDF'] = df
                
                # Grab all ILI data, pad with NaNs to make even matrix
                Detail_Dict['LatencyMatrix'] = boolean_indexing([row.split(',') for row in lines[Trial_data_stop + 1:]])
    
    # Add column if 'Retries' Column does not exist
    if 'Retries' not in df.columns:
        df.insert(df.columns.get_loc("Latency") + 1, 'Retries', '0')
        
    # Check if user has data sheet of study details to add to dataframe
    if file_check:
        detail_df = pd.read_csv(file_check[0], header=0, sep='\t')
        detail_row = np.where(detail_df.Date == Detail_Dict['StartDate'].strip())[0]
        for case in detail_row:
            if (detail_df.Notes[case].lower() in Detail_Dict['FileName'].lower() and
                detail_df.Animal[case] in Detail_Dict['Animal']):
                df.insert(loc=1, column='Notes', value=detail_df.Notes[case].lower())
                df.insert(loc=2, column='Condition', value=detail_df.Condition[case].lower())
                break
    else:
        # Add blank columns
        df.insert(loc=1, column='Notes', value='')
        df.insert(loc=2, column='Condition', value='')

    return Detail_Dict

def LickMicroStructure_stone(dFrame_lick, latency_array, bout_crit):
    """
    Function takes in the dataframe and latency matrix pertaining to all
    licking data obtained from MedMS8_reader_stone as the data sources. This
    requires a bout_crit
    Input: 1) Dataframe and Licking Matrix (obtained from MedMS8_reader_stone)
           2) Bout_crit; variable which is the time (ms) needed to pause between
              licks to count as a bout (details in: Davis 1996 & Spector et al. 1998).
    Output: Appended dataframe with the licks within a bout/trial, latency to
            first lick within trial
    """
    # Find where the last lick occurred in each trial
    last_lick = [np.nanmax(np.where(~np.isnan(x))[0]) for x in latency_array]
    
    # Create function to search rows of matrix avoiding 'runtime error' caused by NaNs
    crit_nan_search = np.frompyfunc(lambda x: (~np.isnan(x)) & (x >= bout_crit), 1, 1)
    
    # Create empty list to store number of bouts by trial
    bouts = []
    ILIs_win_bouts = []
    for i in range(latency_array.shape[0]):
        if last_lick[i] == 0:
            bouts.append(last_lick[i])
            ILIs_win_bouts.append(last_lick[i])
        else:
            bout_pos = np.where(crit_nan_search(latency_array[i, :])).astype(int)
            bout_pos = np.insert(bout_pos, 0, 1)
            bout_dur = np.diff(bout_pos)
            if last_lick[i] != bout_pos[-1]:
                bout_pos = np.insert(bout_pos, len(bout_pos), last_lick[i])
                bout_dur = np.diff(bout_pos)
            bouts.append(np.array(bout_dur))
            trial_ILIs = []
            if len(bout_pos) == 1:
                trial_ILIs.append(latency_array[i, 1])
            if len(bout_pos) != 1:
                for lick in range(len(bout_pos) - 1):
                    if lick == 0:
                        trial_ILIs.append(latency_array[i, 1:bout_pos[lick + 1]])
                    else:
                        trial_ILIs.append(latency_array[i, bout_pos[lick]:bout_pos[lick + 1]])
            ILIs_win_bouts.append(trial_ILIs)
    
    # Store bout count into dataframe
    dFrame_lick["Bouts"] = bouts
    dFrame_lick["ILIs"] = ILIs_win_bouts
    dFrame_lick["Lat_First"] = latency_array[:, 1]
    
    return dFrame_lick

# =============================================================================
# # #BEGIN PROCESSING
# =============================================================================

# Get name of directory where the data files sit, and change to that directory for processing
dir_name = easygui.diropenbox()
os.chdir(dir_name)

# Ask user if they will be using a detailed sheet
msg = "Do you have a datasheet with animal details?"
detail_check = easygui.buttonbox(msg, choices=["Yes", "No"])

if detail_check == 'Yes':
    # Ask user for experimental data sheet if they want to include additional details
    detail_name = easygui.diropenbox(msg='Where is the ".txt" file?')
    file_check = glob.glob(os.path.join(detail_name, '*.txt'))
else:
    file_check = []
   
# Set bout_pause criteria
bout_pause = 500

# Initiate a list to store individual file dataframes
merged_data = []

# Look for the ms8 files in the directory
file_list = os.listdir('./')
for file_name in file_list:
    if file_name.endswith('.txt'):
        file_name = os.path.join(dir_name, file_name)
        
        # Run functions to extract trial data
        out_put_dict = MedMS8_reader_stone(file_name, file_check)
        dfFull = LickMicroStructure_stone(out_put_dict['LickDF'], out_put_dict['LatencyMatrix'], bout_pause)

        # Merge the data into a list
        merged_data.append(dfFull['LickDF'])

# Append dataframe with animal's details
merged_df = pd.concat(merged_data)

# Format to capitalize first letter of labels
merged_df['Condition'] = merged_df.Condition.str.title()

# Extract dataframe for ease of handling
df = merged_df

# Unstack all the ILIs across all bouts to perform math
df_lists = df[['Bouts']].apply(pd.Series)
df['bout_count'] = df_lists.count(axis='columns')
df['Bouts_mean'] = df_lists.mean(axis=1, skipna=True)

# Work on ILI means
df_lists = df[['ILIs']].apply(pd.Series)

all_trials = []
for row in range(df_lists.shape[0]):
    trial_ILI = []
    trial_ILI = [df_lists.iloc[row][i] for i in range(df_lists.iloc[row].shape[0])]
    flatt_trial = list(itertools.chain(*trial_ILI))
    all_trials.append(np.array(flatt_trial))

# Store ILIs extended into dataframe
df['ILI_all'] = all_trials

# Save dataframe for later use/plotting/analyses
df.to_pickle(os.path.join(dir_name, f'{date.today().strftime("%d_%m_%Y")}_grouped_dframe.df'))
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 14:27:01 2019

@author: bradly
"""
# =============================================================================
# Import stuff
# =============================================================================

# import Libraries
import os
import numpy as np
import easygui
import pandas as pd
import itertools
import glob
from datetime import date

# =============================================================================
# # #DEFINE ALL FUNCTIONS
# =============================================================================

def boolean_indexing(v, fillval=np.nan):
    lens = np.array([len(item) for item in v])
    mask = lens[:, None] > np.arange(lens.max())
    out = np.full(mask.shape, fillval)
    out[mask] = np.concatenate(v)
    return out

def MedMS8_reader_stone(file_name, file_check):
    """
    Input: File Name (with directory) from MedAssociates Davis Rig (e.g. .ms8.txt)
    Output: Dictionary containing a dataframe (all lick data categorized), file
            information (animal name, date of recording, etc), and a matrix
            with all latencies between licks by trial
    """
    with open(file_name) as file_input:
        lines = file_input.readlines()

    Detail_Dict = {
        'FileName': None,
        'StartDate': None,
        'StartTime': None,
        'Animal': None,
        'Condition': None,
        'MAXFLick': None,
        'Trials': None,
        'LickDF': None,
        'LatencyMatrix': None
    }
    
    # Extract file name and store
    Detail_Dict['FileName'] = os.path.basename(file_name)
    
    # Store details in dictionary and construct dataframe
    for i, line in enumerate(lines):
        if "Start Date" in line:
            Detail_Dict['StartDate'] = line.split(',')[-1].strip()
        elif "Start Time" in line:
            Detail_Dict['StartTime'] = line.split(',')[-1].strip()
        elif "Animal ID" in line:
            Detail_Dict['Animal'] = line.split(',')[-1].strip()
        elif "Max Wait" in line:
            Detail_Dict['MAXFLick'] = line.split(',')[-1].strip()
        elif "Max Number" in line:
            Detail_Dict['Trials'] = line.split(',')[-1].strip()
        elif "PRESENTATION" in line and "TUBE" in line:
            ID_line = i
        elif len(line.strip()) == 0:
            Trial_data_stop = i
            if ID_line > 0 and Trial_data_stop > 0:
                # Create dataframe
                df = pd.DataFrame(
                    columns=lines[ID_line].split(','),
                    data=[row.split(',') for row in lines[ID_line + 1:Trial_data_stop]]
                )
                
                # Remove spaces in column headers
                df.columns = df.columns.str.replace(' ', '')
                
                # Set concentrations to 0 if concentration column blank
                df['CONCENTRATION'] = df['CONCENTRATION'].str.strip()
                df['CONCENTRATION'] = df['CONCENTRATION'].replace('', 0).astype(float)

                # Convert specific columns to numeric
                df["SOLUTION"] = df["SOLUTION"].str.strip()
                df[["PRESENTATION", "TUBE", "CONCENTRATION", "LICKS", "Latency"]] = \
                    df[["PRESENTATION", "TUBE", "CONCENTRATION", "LICKS", "Latency"]].apply(pd.to_numeric)
                
                # Add in identifier columns
                df.insert(loc=0, column='Animal', value=Detail_Dict['Animal'])
                df.insert(loc=3, column='Trial_num', value='')
                df['Trial_num'] = df.groupby('TUBE').cumcount() + 1
                
                # Store in dictionary
                Detail_Dict['LickDF'] = df
                
                # Grab all ILI data, pad with NaNs to make even matrix
                Detail_Dict['LatencyMatrix'] = boolean_indexing([row.split(',') for row in lines[Trial_data_stop + 1:]])
    
    # Add column if 'Retries' Column does not exist
    if 'Retries' not in df.columns:
        df.insert(df.columns.get_loc("Latency") + 1, 'Retries', '0')
        
    # Check if user has data sheet of study details to add to dataframe
    if file_check:
        detail_df = pd.read_csv(file_check[0], header=0, sep='\t')
        detail_row = np.where(detail_df.Date == Detail_Dict['StartDate'].strip())[0]
        for case in detail_row:
            if (detail_df.Notes[case].lower() in Detail_Dict['FileName'].lower() and
                detail_df.Animal[case] in Detail_Dict['Animal']):
                df.insert(loc=1, column='Notes', value=detail_df.Notes[case].lower())
                df.insert(loc=2, column='Condition', value=detail_df.Condition[case].lower())
                break
    else:
        # Add blank columns
        df.insert(loc=1, column='Notes', value='')
        df.insert(loc=2, column='Condition', value='')

    return Detail_Dict

def LickMicroStructure_stone(dFrame_lick, latency_array, bout_crit):
    """
    Function takes in the dataframe and latency matrix pertaining to all
    licking data obtained from MedMS8_reader_stone as the data sources. This
    requires a bout_crit
    Input: 1) Dataframe and Licking Matrix (obtained from MedMS8_reader_stone)
           2) Bout_crit; variable which is the time (ms) needed to pause between
              licks to count as a bout (details in: Davis 1996 & Spector et al. 1998).
    Output: Appended dataframe with the licks within a bout/trial, latency to
            first lick within trial
    """
    # Find where the last lick occurred in each trial
    last_lick = [np.nanmax(np.where(~np.isnan(x))[0]) for x in latency_array]
    
    # Create function to search rows of matrix avoiding 'runtime error' caused by NaNs
    crit_nan_search = np.frompyfunc(lambda x: (~np.isnan(x)) & (x >= bout_crit), 1, 1)
    
    # Create empty list to store number of bouts by trial
    bouts = []
    ILIs_win_bouts = []
    for i in range(latency_array.shape[0]):
        if last_lick[i] == 0:
            bouts.append(last_lick[i])
            ILIs_win_bouts.append(last_lick[i])
        else:
            bout_pos = np.where(crit_nan_search(latency_array[i, :])).astype(int)
            bout_pos = np.insert(bout_pos, 0, 1)
            bout_dur = np.diff(bout_pos)
            if last_lick[i] != bout_pos[-1]:
                bout_pos = np.insert(bout_pos, len(bout_pos), last_lick[i])
                bout_dur = np.diff(bout_pos)
            bouts.append(np.array(bout_dur))
            trial_ILIs = []
            if len(bout_pos) == 1:
                trial_ILIs.append(latency_array[i, 1])
            if len(bout_pos) != 1:
                for lick in range(len(bout_pos) - 1):
                    if lick == 0:
                        trial_ILIs.append(latency_array[i, 1:bout_pos[lick + 1]])
                    else:
                        trial_ILIs.append(latency_array[i, bout_pos[lick]:bout_pos[lick + 1]])
            ILIs_win_bouts.append(trial_ILIs)
    
    # Store bout count into dataframe
    dFrame_lick["Bouts"] = bouts
    dFrame_lick["ILIs"] = ILIs_win_bouts
    dFrame_lick["Lat_First"] = latency_array[:, 1]
    
    return dFrame_lick

# =============================================================================
# # #BEGIN PROCESSING
# =============================================================================

# Get name of directory where the data files sit, and change to that directory for processing
dir_name = easygui.diropenbox()
os.chdir(dir_name)

# Ask user if they will be using a detailed sheet
msg = "Do you have a datasheet with animal details?"
detail_check = easygui.buttonbox(msg, choices=["Yes", "No"])

if detail_check == 'Yes':
    # Ask user for experimental data sheet if they want to include additional details
    detail_name = easygui.diropenbox(msg='Where is the ".txt" file?')
    file_check = glob.glob(os.path.join(detail_name, '*.txt'))
else:
    file_check = []
   
# Set bout_pause criteria
bout_pause = 500

# Initiate a list to store individual file dataframes
merged_data = []

# Look for the ms8 files in the directory
file_list = os.listdir('./')
for file_name in file_list:
    if file_name.endswith('.txt'):
        file_name = os.path.join(dir_name, file_name)
        
        # Run functions to extract trial data
        out_put_dict = MedMS8_reader_stone(file_name, file_check)
        dfFull = LickMicroStructure_stone(out_put_dict['LickDF'], out_put_dict['LatencyMatrix'], bout_pause)

        # Merge the data into a list
        merged_data.append(dfFull['LickDF'])

# Append dataframe with animal's details
merged_df = pd.concat(merged_data)

# Format to capitalize first letter of labels
merged_df['Condition'] = merged_df.Condition.str.title()

# Extract dataframe for ease of handling
df = merged_df

# Unstack all the ILIs across all bouts to perform math
df_lists = df[['Bouts']].apply(pd.Series)
df['bout_count'] = df_lists.count(axis='columns')
df['Bouts_mean'] = df_lists.mean(axis=1, skipna=True)

# Work on ILI means
df_lists = df[['ILIs']].apply(pd.Series)

all_trials = []
for row in range(df_lists.shape[0]):
    trial_ILI = []
    trial_ILI = [df_lists.iloc[row][i] for i in range(df_lists.iloc[row].shape[0])]
    flatt_trial = list(itertools.chain(*trial_ILI))
    all_trials.append(np.array(flatt_trial))

# Store ILIs extended into dataframe
df['ILI_all'] = all_trials

# Save dataframe for later use/plotting/analyses
df.to_pickle(os.path.join(dir_name, f'{date.today().strftime("%d_%m_%Y")}_grouped_dframe.df'))
