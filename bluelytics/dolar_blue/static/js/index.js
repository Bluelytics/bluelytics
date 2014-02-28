
/*
Functions for main page
*/

function set_source(sourceObj, multiplier){
  calcMultiplier = (100 + multiplier) / 100;
  document.querySelector('div#valorCompra div.value').innerHTML =
    (sourceObj.value_buy * calcMultiplier).toFixed(4);
  document.querySelector('div#valorVenta div.value').innerHTML =
    (sourceObj.value_sell * calcMultiplier).toFixed(4);
  document.querySelector('div#valorIntermedio div.value').innerHTML =
    (sourceObj.value_avg * calcMultiplier).toFixed(4);

  if (sourceObj.date){
    document.querySelector('div#last_update p.date').innerHTML = sourceObj.date;
    $('div#last_update').show();
  }else{
    $('div#last_update').hide();
  }

  var head = $('h1');
  if (sourceObj.source == 'oficial'){

    head.text("Dólar oficial");
    if(head.hasClass('blue')){
      head.removeClass('blue');
      head.addClass('oficial');
    }
    
  }else{
    head.text("Dólar blue");
    if(head.hasClass('oficial')){
      head.removeClass('oficial');
      head.addClass('blue');
    }
  }

  return true;
}

function switch_source(el){

  var source = el.getAttribute('data-source');
  if (resolve_set_source(source)){
    $('ul#source_select li.active').removeClass('active');
    $(el).addClass('active');
  }
}

function resolve_set_source(source){
  var resolved_source;
  multiplier=0;
  if(source == "average"){
    resolved_source = average_sources(max_sources);
  }else{
    var splitName = source.split("+");
    if (splitName.length > 1){
      source = splitName[0];
      multiplier= + splitName[1];
    }

    var search = $.grep(max_sources, function(s){return s.source == source;});

    if (search.length == 0){return;}
    else
      resolved_source = search[0];
  }

  return set_source(resolved_source, multiplier);
}