$(function() {
  
  function showTooltip(x, y, contents) {
    $('<div id="tooltip">' + contents + '</div>').css( {
        position: 'absolute',
        display: 'none',
        top: y + 5,
        left: x + 5,
        border: '1px solid #fdd',
        padding: '2px',
        'background-color': '#fee',
        opacity: 0.80
    }).appendTo("body").fadeIn(200);
  }
  var previousPoint = null;
  $("#timeline").bind("plothover", function (event, pos, item) {

    if (item) {
      if (previousPoint != item.dataIndex) {
        previousPoint = item.dataIndex;
          
        $("#tooltip").remove();
        var x = item.datapoint[0].toFixed(0),
            y = item.datapoint[1].toFixed(1);
          
        showTooltip(item.pageX, item.pageY,
                    "Day " + x + ", Frequency of <b>" + item.series.label + "</b>: " + y + " times the average.");
      }
    }
    else {
      $("#tooltip").remove();
      previousPoint = null;s
    }
  });

  $("#timeline").bind("plotclick", function (event, pos, item) {
        if (item) {
            $("#clickdata").text("You clicked point " + item.dataIndex + " in " + item.series.label + ". with value " + item.datapoint[1]);
            //location.href = ;
            plot.highlight(item.series, item.datapoint);
        }
    });
});