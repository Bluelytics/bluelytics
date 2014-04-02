
/*
Functions for gap
*/


  function gapTransformData(inputData, variable){
    var graphData = [];
    var palette = new Rickshaw.Color.Palette();

      srcd = {
        data: 
          _.chain(inputData)
            .map(function(d){return {x: d.epoch, y:+(d[variable].toFixed(2))};})
            .value()
        ,
        name: 'Brecha',
        color: palette.color()
      }

      graphData.push(srcd);

    return graphData;
  }


  function gapGenerateGraph(id, inputData){

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
        var content = swatch + series.name + ": " + parseFloat(y) + '%<br>' + date;
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

function percGapCalc(oficial, blue){
  var gap = blue - oficial;
  return (gap/oficial) * 100;
}

function gapCalc(id, oficial, blue, multiplier){
  var gap = blue - oficial;
  var perc_gap = percGapCalc(oficial, blue);
  $('span#'+id+' > span.value').text("AR$ " + (gap*multiplier).toFixed(2));
  $('span#'+id+' > span.perc').text("(" +perc_gap.toFixed(2)+ "%)");
}

function adjustGap(value){
  gapCalc('gap_1', oficial_value_avg, blue_value_avg, value);
  gapCalc('gap_2', oficial_mas20_avg, blue_value_avg, value);
  gapCalc('gap_3', oficial_mas35_avg, blue_value_avg, value);
}

function initializeGap(){
    
  /* Gap calculator */
  onlyoficial = max_sources.filter(function(s){return s.source == 'oficial';})[0];
  oficial_value_avg = onlyoficial.value_avg;

  avgs = average_sources(max_sources);
  blue_value_avg = avgs.value_avg;

  oficial_mas20_avg = oficial_value_avg * 1.20;
  oficial_mas35_avg = oficial_value_avg * 1.35;

  var baseform = $('#baseform');
  $('input#basecurrency')
  .bind('mouseout keyup change', function() {
    baseform.removeClass('has-error');
    if ($.isNumeric(this.value)){
      adjustGap(this.value);
    }else{
      baseform.addClass('has-error');
    }
  });

  adjustGap(1);


  /* Gap Graph */
  var transfBlueData = _.chain(blueData).map(function(b){
    var tmp_date = new Date(b.date);
    b.epoch = tmp_date.getTime()/1000;
    b.datepart = DATEPART_FORMAT(tmp_date);
    return b;
  }).value();

  var bySourceDate = _.groupBy(transfBlueData, function(a){return a.source+a.datepart;});

  var dailyBlueData = _.map(bySourceDate, function(d){
    return _.max(d, function(a){return a.epoch;});
  });

  var blueByDate = _.groupBy(dailyBlueData, function(a){return a.datepart;});
  
  var dailyBlueGrouped = _.chain(blueByDate).map(function(d){
    var sum_oficial = _.reduce(d, function(memo, sum){
      if (sum.source == 'oficial'){ return memo + sum.value_avg;} else {return memo;}
    }, 0);

    var sum_blue = _.reduce(d, function(memo, sum){
      if (sum.source != 'oficial'){ return memo + sum.value_avg;} else {return memo;}
    }, 0);

    var count_blue = _.chain(d).filter(function(c) {
      return c.source != 'oficial';
    }).size().value();

    return {'epoch': _.max(d, function(a){return a.epoch;}).epoch, 'oficial': sum_oficial, 'blue': sum_blue/count_blue}

  }).filter(function(d){
    return (d.oficial > 0 && d.blue > 0);
  }).value();


  dailyBlueGap = _.map(dailyBlueGrouped, function(d){
    return {'epoch': d.epoch, 'gap': percGapCalc(d.oficial, d.blue)}
  });
  
  var dailyGraph_gap = gapGenerateGraph("dailychart_gap", gapTransformData(dailyBlueGap, 'gap'));
}