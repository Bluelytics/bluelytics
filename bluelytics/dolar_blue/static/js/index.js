
/*
Functions for main page
*/

function define_changeclass(difference){
  if(difference > 0){
    return 'increment';
  }else if (difference < 0){
    return 'decrement';
  } else{
    return '';
  }
}

function define_changeicon(difference){
  if(difference > 0){
    return 'arrow-up';
  }else if (difference < 0){
    return 'arrow-down';
  } else{
    return 'minus';
  }
}

function set_source(sourceObj, multiplier){
  calcMultiplier = (100 + multiplier) / 100;

  today = sourceObj['today'];
  yesterday = sourceObj['yesterday'];

  var difference_buy = (today.value_buy - yesterday.value_buy) * calcMultiplier;
  var difference_sell = (today.value_sell - yesterday.value_sell) * calcMultiplier;
  var difference_avg = (today.value_avg - yesterday.value_avg) * calcMultiplier;

  document.querySelector('div#valorCompra div.value').innerHTML =
    (today.value_buy * calcMultiplier).toFixed(4)
    + '  <span class="'+define_changeclass(difference_buy)+'">(<span class="glyphicon glyphicon-'+define_changeicon(difference_buy)+'"></span>'+Math.abs(difference_buy).toFixed(4)+')</span>';
  
  document.querySelector('div#valorVenta div.value').innerHTML =
    (today.value_sell * calcMultiplier).toFixed(4)
    + '  <span class="'+define_changeclass(difference_sell)+'">(<span class="glyphicon glyphicon-'+define_changeicon(difference_sell)+'"></span>'+Math.abs(difference_sell).toFixed(4)+')</span>';
  
  document.querySelector('div#valorIntermedio div.value').innerHTML =
    (today.value_avg * calcMultiplier).toFixed(4)
    + '  <span class="'+define_changeclass(difference_avg)+'">(<span class="glyphicon glyphicon-'+define_changeicon(difference_avg)+'"></span>'+Math.abs(difference_avg).toFixed(4)+')</span>';

  if (today.date){
    document.querySelector('div#last_update p.date').innerHTML = DATE_FORMAT(new Date(today.date));
    $('div#last_update').css('visibility','');
  }else{
    $('div#last_update').css('visibility','hidden');
  }

  var head = $('h1');
  if (today.source == 'oficial'){

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
    resolved_source = {'today':average_sources(max_sources), 'yesterday':average_sources(max_sources_yesterday)};
  }else{
    var splitName = source.split("+");
    if (splitName.length > 1){
      source = splitName[0];
      multiplier= + splitName[1];
    }

    var search = $.grep(max_sources, function(s){return s.source == source;});
    var search_yesterday = $.grep(max_sources_yesterday, function(s){return s.source == source;});

    if (search.length == 0){return;}
    else
      resolved_source = {'today':search[0], 'yesterday':search_yesterday[0]};
  }

  return set_source(resolved_source, multiplier);
}