# Data Analysis

This section covers the steps and file structure required to analyze data using the `BAT_reader.py` script.

## Overview

The `BAT_reader.py` script is designed to read `.ms8.txt` files from the MedAssociates Davis Rig, extract relevant data, and generate a structured dataframe. This dataframe can then be used for further analysis, such as calculating lick counts, latency to lick, and identifying licking bouts.

## Instructions for BAT_reader.py

### 1. Data Preparation

- **File Requirements:**
  - `.ms8.txt` files: These are the raw data files from the Davis Rig.
  - Input file: A tab-separated text file (`.txt`) that contains experimental details such as the animal ID, date of experiment, condition, and notes.
  
- **Folder Organization:**
  It is important to organize your data files and the input file in the following structure:

<div class="code-container">
  <button class="copy-button" onclick="copyCode('folder-organization')">Copy</button>
  <pre><code id="folder-organization">
  input_files/
    └─ input_data.txt
  
  data/
    ├─ 0129TG100_pretest.ms8.txt
    ├─ 0129TG101_pretest.ms8.txt
    ├─ 0129TG102_pretest.ms8.txt
    └─ 0129TG103_pretest.ms8.txt
  </code></pre>
</div>

### 2. Input File Format

The input file, which should be placed in the `input_file/` folder, must be formatted exactly as follows:

<div class="code-container">
  <button class="copy-button" onclick="copyCode('input-file-format')">Copy</button>
  <pre><code id="input-file-format">
Animal   Date       Condition   Notes
TG100    2024/01/29 E           Con1
TG101    2024/01/29 U           Con1
TG102    2024/01/29 E           Con1
TG103    2024/01/29 U           Con1
  </code></pre>
</div>

Make sure the dates and names in the input file match those in the `.ms8.txt` files exactly.

### 3. Running BAT_reader.py

1. Place all `.ms8.txt` files into the `data/` folder.
2. Ensure the input file is correctly formatted and located in the `input_files/` folder.
3. Run the `BAT_reader.py` script. When prompted:

![Bat_reader.py Workflow](images/example-image.png)

<div class="code-container">
  <button class="copy-button" onclick="copyCode('folder-organization')">Copy</button>
  <pre><code id="folder-organization">
  run BAT_reader.py
  </code></pre>
</div>

   - Select the `ms8_data/` folder for your data files.
   - Select the `input_files/` folder for your input file.
4. The script will process the data and output a dataframe.

### 4. Data Output

Once processed, the data will be organized into a dataframe that includes the following:
- Lick data categorized by trial
- Latency between licks
- Bout structure (licks grouped based on a defined criterion, e.g., a pause of 500 ms between licks)
  
The processed data will be saved in a file named `grouped_dframe.df`, timestamped with the current date.

## Additional Information

The `Stink_Bat/` folder on the google drive contains basic plotting code for visualizing the data stored in the dataframe. You can customize these plots to suit your experimental needs.

<!-- JavaScript -->
<script>
function copyCode(id) {
  var code = document.getElementById(id);
  var range = document.createRange();
  range.selectNode(code);
  window.getSelection().removeAllRanges();
  window.getSelection().addRange(range);
  document.execCommand('copy');
  window.getSelection().removeAllRanges();
  alert('Code copied to clipboard!');
}
</script>

<!-- CSS -->
<style>
.code-container {
  position: relative;
  padding: 10px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
  margin-bottom: 10px;
}

.copy-button {
  position: absolute;
  top: 2px; /* Adjusted to be slightly higher */
  right: 10px;
  padding: 3px 7px;
  font-size: 14px;
  cursor: pointer;
  background: linear-gradient(135deg, #6c63ff, #a3a1fc); /* Gradient background */
  color: white;
  border: none;
  border-radius: 2px; /* Rounded corners */
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2); /* Shadow for depth */
  transition: background 0.3s, transform 0.2s; /* Smooth transitions */
}

.copy-button:hover {
  background: linear-gradient(135deg, #5a52d0, #9e9bfa); /* Slightly darker on hover */
  transform: scale(1.05); /* Slightly larger on hover */
}

pre, code {
  border: 1px solid #ccc; /* Grey border */
  background-color: #f0f0f0; /* Light grey background */
  padding: 6px;
  border-radius: 2px; /* Optional: for rounded corners */
}
</style>
