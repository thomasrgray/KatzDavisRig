# Davis Rig Software Setup

The Davis Rig software is designed to facilitate experiments with protocols that define tube presentation sequences. Below is a guide to its main features and setup procedures.

**Note:** The MED Davis Rig software is checked by default. If you are using this software with DiLog Instruments hardware, refer to **Appendix A**: "Davis Collect Data with DiLog Hardware."

---

## Main Screen Overview

**Figure 4-2 – Davis Rig Main Screen**

---

## Trial Protocol Panel

### Drop-Down List
This list contains all available protocol files, which have the `.pro` file extension. A protocol file defines the sequence of tube presentations for a particular experiment.

- **Show Button**: Clicking the Show button will open a Presentation List window, which contains a table indicating the tube presentation sequence for the currently selected protocol.

#### **Figure 4-3 – Presentation List**
- **IPI** (Inter-Presentation Interval): Time in seconds between tube presentations.
- **Pres (Presentation)**: Trial number.
- **Tube**: Tube Identification Number (e.g. 1 to 16) to be presented.
- **Concentration**: Concentration of the solution in the presented tube.
- **Solution**: Solution name for the presented tube.
- **LTL (Lick Time Limit)**: Time (in seconds) from the first lick before the shutter closes.
- **Max Licks**: Maximum number of licks before the trial ends. The default is 999, and the trial will end when either the LTL or Max Licks limit is reached, whichever comes first.

### Edit Button
Clicking the **Edit** button allows you to modify the currently selected protocol or create a new one. If "New..." is selected in the drop-down list, you can create a new protocol. For more details, see **Chapter 5 | Creating and Editing a Protocol**.

### Bottle Filling Guide Button
The **Bottle Filling Guide** button opens the **Tube Filling Guide** window for the currently selected protocol.

#### **Figure 4-4 – Tube Filling Guide**
Each tube (from 1 to 16) has a row in the Tube Filling Guide table.  
- The left column shows the concentration of the solution in each tube.  
- The right column shows the name of the solution.  
Both the concentration and solution names are user-defined.

Clicking **Close** in the Tube Filling Guide window will close the guide.

---

## Animal ID Panel

This panel contains a character string field where the user can input an identifier for the animal being studied.  
- The first four characters of the **Animal ID** will appear in the filename of the output data file.  
  - Example: If the Animal ID is "AnID", the filename will start with "AnID" in the output data file.

#### **Figure 4-5 – Animal ID**

---

## Output File Panel

### Directory Path
Defines the directory where the output data will be saved. The default directory path is `C:\DavisData`.

### Data Filename
The format for the output file is:  
`MMDDAnID.MS8`, where:  
- **MM**: The current month (01 for January to 12 for December)  
- **DD**: The day of the month (01 to 31)  
- **AnID**: The first four characters of the Animal ID.  
The file will have a `.MS8` extension.

### Include Retry Count in Data File Checkbox
When this box is checked, any retries needed for a presentation will be included in the data file. For more information, see **Retries at Same Tube** in **Chapter 5**.


## Main Screen Overview

### Notice
By default, **MED Davis Rig** is checked. If using this software with DiLog Instruments hardware, refer to **Appendix A** for Davis Collect Data with DiLog Hardware.

![Davis Rig Main Screen](path_to_image_figure_4_2)

### Trial Protocol Panel

#### Drop Down List
This list contains all available protocol files. Protocol files have the `.pro` file extension. A protocol file defines the sequence of tube presentation for a particular experiment.

#### Show Button
Click the **Show** button to display a Presentation List window, which indicates the tube presentation sequence for the currently selected protocol in the drop-down list.

![Presentation List](path_to_image_figure_4_3)

| Field              | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| **IPI**            | Inter-Presentation Interval (in seconds).                                    |
| **Pres**           | Trial number.                                                               |
| **Tube**           | Identification number (1 to 16) for the tube being presented.                |
| **Concentration**  | Solution concentration in the tube.                                          |
| **Solution**       | Name of the solution in the tube.                                            |
| **LTL**            | Lick Time Limit (time in seconds from the first lick before the shutter closes). |
| **Max Licks**      | Maximum number of licks for this trial before the shutter closes (default 999). |

#### Edit Button
Click the **Edit** button to modify the currently selected protocol or create a new protocol.

#### Bottle Filling Guide Button
This button opens the **Tube Filling Guide** window for the currently selected protocol.

![Tube Filling Guide](path_to_image_figure_4_4)

Each row represents a tube, showing its concentration and solution name.

---

## Animal ID Panel
The Animal ID field allows you to input a unique identifier for the animal being tested. The first four characters of the Animal ID will appear in the output file name. Example: if the ID is `AnID`, the filename will include `AnID`.

![Animal ID](path_to_image_figure_4_5)

## Output File Panel

#### Directory Path
The directory path where output files will be saved. Default path: `C:\DavisData`.

#### Data Filename Format
The data filename follows the format `MMDDAnID.MS8`, where `MM` is the month, `DD` is the day, and `AnID` represents the first four characters of the Animal ID.

#### Include Retry Count in Data File
Check this box to include retry counts in the data file.

---

# Main Window Control Buttons

### Test Hardware Button
Opens the **Test Hardware** window, allowing you to test the Davis Rig table and adjust the table movement direction. The table holds drinking tubes and positions them in front of the access port. It is moved by a stepper motor system.

![Test Hardware](path_to_image_figure_4_6)

#### Show Table Movement Direction Window Button
Opens a window to change table movement direction.

#### Initialize Button
Moves the table to its home position (Tube 1).

#### Open/Close Door Button
Opens or closes the shutter door.

#### Select Tube Panel Buttons
Click a button (1-16) to move the table to the corresponding tube position.

#### Exit Button
Closes the **Test Hardware** window.

### Input Status Panel
Displays status indicators for the hardware.

| Status          | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| **Table Status** | Home: Table is at Tube 1 position. Off: Table is not at the home position.   |
| **Shutter Status** | Open or closed.                                                           |
| **Detector Status** | No Lick or Lick detected by the lickometer circuit.                      |
| **Signal Status** | Bad: Check connections. Poor: Lick block operational but needs cleaning. Good: Signal is strong. |

---

# Creating and Editing a Protocol

### Trial Parameters

From the **Davis Rig Main Window**, select a protocol or "New..." from the **Trial Protocol** dropdown list, then click **Edit** to define the trial parameters.

#### Tube Presentation Sequence Panel
Select the Tube Presentation Sequence file (`.TPS`) to define the tube order. Standard files include **Ascending** or **Descending**.

Custom sequences can be created with a text editor or the **Tube Presentation Sequence Maker** utility. Example:

![Tube Presentation Sequence](path_to_image_figure_5_2)

#### Retries at Same Tube
Defines the number of retries allowed when a lick is not detected. If set to a high value, the system will retry multiple times on the same tube.

#### Session Time Limit
Sets the maximum session time (in minutes) before the session automatically ends.

#### Pre-Presentation Interval Panel
Defines the time between presentations (IPI). Options include:

- **Equal at Min PPI**: Consistent interval for all presentations.
- **Alternate Min then Max PPI**: Alternates between short and long intervals.
- **Pseudorandom Sequence**: Randomized intervals within a defined range.

![Pre-Presentation Interval](path_to_image_figure_5_5)

---
