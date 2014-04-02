
/*
Functions for graph
*/


  function transformData(inputData, variable){
    var graphData = [];
    var palette = new Rickshaw.Color.Palette();

    for (key in sourceData){
      var source = sourceData[key].name;
      var sourceDesc = sourceData[key].description;
      srcd = {
        data: 
          inputData
            .filter(function(d){return d.source == source;})
            .map(function(d){return {x: d.epoch, y:+(d[variable].toFixed(4))};})
        ,
        name: sourceDesc,
        color: palette.color()
      }

      graphData.push(srcd);
    }

    return graphData;
  }

  function generateGraph(id, inputData){

    var chart_id = "div#"+id;

    var chartElement = $(chart_id);
    chartElement.append('<div class="chart_container"> \
      <div class="chart"></div> \
      <br> \
      <div class="slider"></div> \
    </div>');

    var graph = new Rickshaw.Graph( {
        element: document.querySelector(chart_id + " > div.chart_container > div.chart"), 
        renderer: 'line',
        series: inputData,
        min:7
    });


    var slider = new Rickshaw.Graph.RangeSlider.Preview({
        graph: graph,
        element: document.querySelector(chart_id+" div.slider")
    });

    var previewXAxis = new Rickshaw.Graph.Axis.Time({
      graph: slider.previews[0]
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
        var date = '<span class="date">' + new Date(x * 1000).toString() + '</span>';
        var swatch = '<span class="detail_swatch" style="background-color: ' + series.color + '"></span>';
        var content = swatch + series.name + ": " + parseFloat(y) + '<br>' + date;
        return content;
      }
    } );


    var updGraph = function() {
      
      var el = document.querySelector(chart_id+" div.chart");
      
      graph.configure({
        width: el.offsetWidth,
        height: el.offsetWidth * 0.66
      });

      slider.configure({
        width:el.offsetWidth
      });
      slider.render();

      previewXAxis.render();
      xAxis.render();
      yAxis.render();
      graph.render();
    };

    updGraph();
    window.addEventListener('resize', updGraph); 

    return graph;
  }


function graph_set_variable(variable){
  $('.chart_block').addClass('hidden');
  $('#dailychart_'+variable).removeClass('hidden');
}

function graph_switch_variable(el){
  var variable = el.getAttribute('data-var');

  graph_set_variable(variable);

  $('ul#var_select li.active').removeClass('active');
  $(el).addClass('active');
  return false;
}

function prepareGraphs(){
    var add_20perc = _.chain(blueData)
    .filter(function(e){return e.source == "oficial";})
    .map(function(e){
              return addxPerc(e, 20);
            })
    .value()
  ;

  var add_35perc = _.chain(blueData)
    .filter(function(e){return e.source == "oficial";})
    .map(function(e){
              return addxPerc(e, 35);
            })
    .value()
  ;

  blueFixed = jQuery.merge(jQuery.merge(add_20perc, add_35perc), blueData);

  var label_20perc = {"name": "oficial_mas20", "description": "Oficial + 20%"};
  var label_35perc = {"name": "oficial_mas35", "description": "Oficial + 35%"};
  sourceData.push(label_20perc);
  sourceData.push(label_35perc);

  var transfBlueData = _.chain(blueFixed).map(function(b){
    var tmp_date = DATE_FORMAT.parse(b.date);
    b.epoch = tmp_date.getTime()/1000;
    b.datepart = DATEPART_FORMAT(tmp_date);
    return b;
  }).value();


  var dailyGraphReady = {
    'value_sell':transformData(transfBlueData, 'value_sell'),
    'value_avg':transformData(transfBlueData, 'value_avg'),
    'value_buy':transformData(transfBlueData, 'value_buy')
  };

  var dailyGraph_sell = generateGraph("dailychart_sell", dailyGraphReady['value_sell']);
  var dailyGraph_avg = generateGraph("dailychart_avg", dailyGraphReady['value_avg']);
  var dailyGraph_buy = generateGraph("dailychart_buy", dailyGraphReady['value_buy']);
  
  graph_set_variable('avg');
}