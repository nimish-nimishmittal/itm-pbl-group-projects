function doPost(e) {
  var sheet = SpreadsheetApp.openById("1Y1R3iVb-34k-w34sR8RqQwLf05cr9eJIbVBxpUKo5v8").getActiveSheet();
  
  // Add headings if the sheet is empty
  if (sheet.getLastRow() == 0) {
    var headings = ["Timestamp", "Full Name", "Phone Number", "Email Address"];
    sheet.appendRow(headings);
  }
  
  var row = [];
  row.push(new Date()); // Timestamp
  row.push(e.parameter.name);
  row.push(e.parameter.number);
  row.push(e.parameter.email);
  
  sheet.appendRow(row);
  
  return ContentService.createTextOutput("Form submission successful");
}