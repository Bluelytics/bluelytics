

  function fill_table(table, dates, values){

    var add_html = '';

    for(var i=0; i < dates.length; i++){
      add_html +=
        '<tr><td>'
          + dates[i] +
        '</td><td class="min">'
          + values.lower_80[i] +
        '</td><td class="mean">'
          + values.mean[i] +
        '</td><td class="max">'
          + values.upper_80[i] +

        '</td>';
    }
    table.append(add_html);
  }

  function generateForecastGraph(dates_forecasted, dates_history, values_forecasted, values_history){

    var chart_id = "div#forecast_chart";

    var chartElement = $(chart_id);
    chartElement.append('<div class="chart_container"> \
      <div class="chart"></div> \
    </div>');

    var seriesHistory = [];
    var seriesForecastMean = [];
    var seriesForecastMin = [];
    var seriesForecastMax = [];
    var input_item;

    for(var i = 0; i < dates_history.length; i++){
      var tmpDate = DATEPART_FORMAT.parse('01/' + dates_history[i]);
      input_item = {
        x: tmpDate.getTime()/1000,
        y: values_history['history'][i]
      }
      seriesHistory.push(input_item);
      if(i == dates_history.length - 1){
        seriesForecastMin.push(input_item);
        seriesForecastMean.push(input_item);
        seriesForecastMax.push(input_item);
      }

    }

    for(var i = 0; i < dates_forecasted.length; i++){
      var tmpDate = DATEPART_FORMAT.parse('01/' + dates_forecasted[i]);
      input_item = {
        x: tmpDate.getTime()/1000,
        y: values_forecasted['lower_80'][i]
      }
      seriesForecastMin.push(input_item);

      input_item = {
        x: tmpDate.getTime()/1000,
        y: values_forecasted['mean'][i]
      }
      seriesForecastMean.push(input_item);
    
      input_item = {
        x: tmpDate.getTime()/1000,
        y: values_forecasted['upper_80'][i]
      }
      seriesForecastMax.push(input_item);
    
    }

    graphData = [
    {
      data: seriesHistory,
      name: 'Historico',
      color: '#0000ff'
    },
    {
      data: seriesForecastMean,
      name: 'Predicho intermedio',
      color: '#1e90ff'
    },
    {
      data: seriesForecastMin,
      name: 'Predicho minimo',
      color: '#afeeee'
    },
    {
      data: seriesForecastMax,
      name: 'Predicho maximo',
      color: '#afeeee'
    }
    ];

    var graph = new Rickshaw.Graph( {
        element: document.querySelector(chart_id + " > div.chart_container > div.chart"), 
        renderer: 'line',
        series: graphData
    });

    var xAxis = new Rickshaw.Graph.Axis.Time({
        graph: graph
    });

    var yAxis = new Rickshaw.Graph.Axis.Y({
        graph: graph
    });
    var hoverDetail = new Rickshaw.Graph.HoverDetail( {
      graph: graph,
      formatter: function(series, x, y) {
        var date = '<span class="date">' + MONTH_FORMAT(new Date(x * 1000)) + '</span>';
        var swatch = '<span class="detail_swatch" style="background-color: ' + series.color + '"></span><br>';
        var content = swatch + series.name + ": <br><span class=\"x_value\">" + parseFloat(y) + '</span><br>' + date;
        return content;
      }
    } );

    var updGraph = function() {
      
      var el = document.querySelector(chart_id+" div.chart");
      
      graph.configure({
        width: el.offsetWidth,
        height: el.offsetWidth * 0.66
      });

      xAxis.render();
      yAxis.render();
      graph.render();
    };

    updGraph();
    window.addEventListener('resize', updGraph); 
  

  }


  function obtainDataForecast(){
    var dates_forecasted;
    var dates_history;
    var values_forecasted;
    var values_history;

      $.getJSON("/data/forecast/json_dates_forecasted.json", function(json) {
        dates_forecasted = json;
        $.getJSON("/data/forecast/json_dates_history.json", function(json) {
          dates_history = json;
          $.getJSON("/data/forecast/json_forecasted.json", function(json) {
            values_forecasted = json;
            $.getJSON("/data/forecast/json_history.json", function(json) {
              values_history = json;


              fill_table($('table#table_forecast > tbody'),dates_forecasted, values_forecasted);

              generateForecastGraph(dates_forecasted, dates_history, values_forecasted, values_history);
            });
          });
        });
      });
  }