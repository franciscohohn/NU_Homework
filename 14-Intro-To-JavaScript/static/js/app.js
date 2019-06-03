// from data.js
var tableData = data;

var tbody = d3.select("tbody")
var table = d3.select("table");

//  Use d3 to update cells from data
data.forEach(function(ufoInfo) {
  var row = tbody.append("tr");
  Object.entries(ufoInfo).forEach(function([key, value]) {
    // Append a cell to the row for each value in ufoInfo
    var cell = row.append("td");
    cell.text(value);
  });
});

// Select the submit button
var submit = d3.select("#filter-btn");
submit.on("click", function() {
  
  
  // Prevent page refresh
  d3.event.preventDefault();

 
  // Set user input as variable
  var inputDate = d3.select("#datetime");
  var inputValue = inputDate.property("value");
  console.log(inputValue);

// Filter Data variable
var filteredData = tableData.filter(tableData => tableData.datetime === inputValue);

  //Clears the previously posted table before it loops through the inputted date
  tbody.text("")

  // Loop through the filtered date from user input
  filteredData.forEach(function(datefilter) {
    console.log(datefilter);
    var dateselection = tbody.append("tr");
    Object.entries(datefilter).forEach(function([key, value]) {
        var item = dateselection.append("td");
        item.text(value);
    });
  });
});