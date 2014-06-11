
/*
Global functions
*/


var DATE_FORMAT = d3.time.format("%d/%m/%Y %H:%M:%S");
var DATEPART_FORMAT = d3.time.format("%d/%m/%Y");
var MONTH_FORMAT = d3.time.format("%m/%Y");




/*
Generic functions
*/

function sumVar(varName){
  var passVar = varName;
  return function(a,b){
     return  a + b[passVar];
   };
}

function union(array1, array2) {
    var hash = {}, union = [];
    $.each($.merge($.merge([], array1), array2), function (index, value) { hash[value] = value; });
    $.each(hash, function (key, value) { union.push(key); } );
    return union;
}


function addxPerc(data, perc){
decimal = (100 + perc) / 100;

newd = jQuery.extend({}, data);
newd.source = newd.source + "_mas" + perc;
newd.value_sell *= decimal;
newd.value_avg *= decimal;
newd.value_buy *= decimal;
return newd;
}


function average_sources(data){
    only_blue = _.filter(data, function(s){return s.source != 'oficial';});

    return {
      'value_sell': only_blue.reduce(sumVar('value_sell'), 0)/only_blue.length,
      'value_buy': only_blue.reduce(sumVar('value_buy'), 0)/only_blue.length,
      'value_avg': only_blue.reduce(sumVar('value_avg'), 0)/only_blue.length,
    };
}


function round_number(num, dec) {
    return Math.round(num * Math.pow(10, dec)) / Math.pow(10, dec);
}