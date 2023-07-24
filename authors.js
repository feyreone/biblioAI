// Assuming the CSV file is named "data.csv"
const csvFilePath = '/Users/wannurfarahinwanrusmadi/Downloads/cleaned_data.csv';
const dropdown = document.getElementById('dropdown');

// Read the CSV file using a server-side language like Python or JavaScript's Fetch API
fetch(csvFilePath)
  .then(response => response.text())
  .then(data => {
    // Split the data into rows
    const rows = data.split('\n');

    // Extract the header row to get the column names
    const headerRow = rows[0].split(',');

    // Extract the column you want for the dropdown
    const dropdownColumn = headerRow.indexOf('author_name');

    // Iterate over the remaining rows and create options for the dropdown
    for (let i = 1; i < rows.length; i++) {
      const row = rows[i].split(',');
      const option = document.createElement('option');
      option.text = row[dropdownColumn];
      dropdown.add(option);
    }
  });
