
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