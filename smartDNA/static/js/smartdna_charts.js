     var data;
     var chart;

      // Load the Visualization API and the piechart package.
      google.charts.load('current', {'packages':['corechart']});

      // Set a callback to run when the Google Visualization API is loaded.
      google.charts.setOnLoadCallback(drawPieChart);
      google.charts.setOnLoadCallback(drawPieAnalysisChart);
      // Callback that creates and populates a data table,
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawPieChart() {
        // Create our data table.
        var jsonData = $.ajax({
          url: "/live_chart_data",
          dataType: "json",
          async: false
          }).responseText;
          
      // Create our data table out of JSON data loaded from server.
      var data = new google.visualization.DataTable(jsonData);


        // Set chart options
        var options = {'title':'Audit Overview- Total Scans',
			'titlePosition': 'none',
			chartArea:{left:10,top:10,width:"100%",height:"80%"},
                        legend: {position: 'right',alignment:'end'},
                	'width':400,
                	'height':300};

        // Instantiate and draw our chart, passing in some options.
        chart = new google.visualization.PieChart(document.getElementById('pie_out'));
        chart.draw(data, options);
      }

      function drawPieAnalysisChart() {
        // Create our data table.
        var jsonData = $.ajax({
          url: "/dashboard/get_latest/",
          dataType: "json",
          async: false
          }).responseText;
          
      // Create our data table out of JSON data loaded from server.
      var data = new google.visualization.DataTable(jsonData);


        // Set chart options
        var options = {'title':'Audit Overview- Total Scans',pieHole: 0.4,'pieSliceText':'value-and-percentage',
      'titlePosition': 'none',
      chartArea:{left:10,top:10,width:"100%",height:"80%"},
                        legend: {position: 'right',alignment:'end'},
                  'width':400,
                  'height':300};

        // Instantiate and draw our chart, passing in some options.
        chart = new google.visualization.PieChart(document.getElementById('pie_analysis_out'));
        chart.draw(data, options);
      }

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Month', 'Registered', 'Tampered', 'Verified'],
          ['Feb 2016', 7800, 455, 4500],
          ['March 2016', 9000, 550, 4500],
          ['April 2016', 10000, 500, 6000],
          ['May 2016', 11700, 660, 9500],
          ['June 2016', 6600, 420, 5000],
          ['July 2016', 10300, 440, 5500]
        ]);
        var options = {
          chart: {
            title: 'Scanned data per month',
            subtitle: 'Registered, Verified and Tampered: last 6 month',
          }
        };
        var chart = new google.charts.Bar(document.getElementById('columnchart_material'));
        chart.draw(data, options);
      }
