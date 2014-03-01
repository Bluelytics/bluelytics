
/*
Functions for main page
*/

function set_source(sourceObj, multiplier){
  calcMultiplier = (100 + multiplier) / 100;
  
  actual_usd = sourceObj.value_avg * calcMultiplier;
  

  return true;
}

function switch_source(el){

  var source = el.getAttribute('data-source');
  if (resolve_set_source(source)){
    $('ul#source_select li.active').removeClass('active');
    $(el).addClass('active');
    update(0);
  }
}

function update(how){
  if(how == 0){
    if(last_change == 0){
      update_fromlocal();
    }else{
      update_fromext();
    }
  }else if(how == 1){
    last_change = 0;
    update(0);
    return;
  }else{
    last_change = 1;
    update(0);
    return;
  }

  $('#calculation_blue > .from').text(actual_usd.toFixed(4));
  $('#calculation_ext > .to').text(dict_currencies[actual_currency].toFixed(4) + ' ' + actual_currency);
  $('#ext_code').text(actual_currency);
}


function update_fromlocal(){
  var act_ars = $('#currency_ars').val();
  var act_ext = (act_ars / actual_usd) * dict_currencies[actual_currency];

  $('#currency_ext').val(act_ext.toFixed(4));
}

function update_fromext(){
  var act_ext = $('#currency_ext').val();
  var act_ars = (act_ext / dict_currencies[actual_currency]) * actual_usd;

  $('#currency_ars').val(act_ars.toFixed(4));
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