d3.gantt = function(w, h, base_group_id, time_period_start, time_period_end, t) {
  var FIT_TIME_DOMAIN_MODE = "fit";
  var FIXED_TIME_DOMAIN_MODE = "fixed";
  var SPECIFIED_TIME_DOMAIN_MODE = "specified"

  var margin = {
    top : 20,
    right : 0,
    bottom : 20,
    left : 0
  };
  var timeDomainStart = d3.timeDay.offset(new Date(),-3);
  var timeDomainEnd = d3.timeHour.offset(new Date(),+3);
  var timeDomainMode = SPECIFIED_TIME_DOMAIN_MODE;// fixed or fit
  var taskTypes = [];
  var taskStatus = [];
  var width = w;
  var height = h;
  var group_id_to_draw = base_group_id;
  var tickFormat = "%H:%M";
  var tasks = t;
  var x, y, xAxis, yAxis;

  var keyFunction = function(d) {
    return d.startDate + d.taskName + d.endDate;
  };

  var rectTransform = function(d) {
    return "translate(" + x(d.startDate) + "," + y(d.taskName) + ")";
  };


  var initTimeDomain = function() {

    if (timeDomainMode === SPECIFIED_TIME_DOMAIN_MODE){
        if(time_period_start == null || time_period_end == null){
            timeDomainMode = FIT_TIME_DOMAIN_MODE;
        }
        else{
            timeDomainStart = time_period_start;
            timeDomainEnd = time_period_end;
        }
    }

    if (timeDomainMode === FIT_TIME_DOMAIN_MODE) {
      if (tasks === undefined || tasks.length < 1) {
        timeDomainStart = d3.time.day.offset(new Date(), -3);
        timeDomainEnd = d3.time.hour.offset(new Date(), +3);
        return;
      }
      tasks.sort(function(a, b) {
        return a.endDate - b.endDate;
      });
      timeDomainEnd = tasks[tasks.length - 1].endDate;
      tasks.sort(function(a, b) {
        return a.startDate - b.startDate;
      });
      timeDomainStart = tasks[0].startDate;
    }
  };

 function initAxis() {
    x = d3.scaleTime().domain([ timeDomainStart, timeDomainEnd ]).range([ 0, width ]).clamp(true);

    y = d3.scaleBand().domain(taskTypes).rangeRound([ 0, height - margin.top - margin.bottom ], .1);

    xAxis = d3.axisBottom().scale(x).tickFormat(d3.timeFormat("%b %d"))
      .tickSize(8).tickPadding(8);

    yAxis = d3.axisLeft().scale(y).tickSize(0);
  };

  function gantt() {
    
    initTimeDomain();
    initAxis();

    var svg = d3.select(group_id_to_draw)
      .attr("class", "chart")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("class", "gantt-chart")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");

    svg.selectAll(".chart")
      .data(tasks, keyFunction).enter()
      .append("rect")
      .attr("rx", 5)
      .attr("ry", 5)
      .attr("class", function(d){ 
        if(taskStatus[d.status] == null){ return "bar";}
        return taskStatus[d.status];
      }) 
      .attr("y", 0)
      .attr("transform", rectTransform)
      .attr("height", function(d) { return (height - ((margin.top + margin.bottom)*2))/tasks.length; })
      .attr("width", function(d) { 
        return (x(d.endDate) - x(d.startDate)); 
      });

      /* - Removing x-axis for now
      svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0, " + (height - margin.top - margin.bottom) + ")")
        .transition()
        .call(xAxis);
      */
      svg.append("g").attr("class", "y axis").transition().call(yAxis);

      return gantt;

  };

  gantt.redraw = function(tasks) {

    initTimeDomain();
    initAxis();

    var svg = d3.select("svg");

    var ganttChartGroup = svg.select(".gantt-chart");
    var rect = ganttChartGroup.selectAll("rect").data(tasks, keyFunction);

    rect.enter()
      .insert("rect",":first-child")
      .attr("rx", 5)
      .attr("ry", 5)
      .attr("class", function(d){ 
        if(taskStatus[d.status] == null){ return "bar";}
        return taskStatus[d.status];
      }) 
      .transition()
      .attr("y", 0)
      .attr("transform", rectTransform)
      .attr("height", function(d) { return y.range()[1]; })
      .attr("width", function(d) { 
        return (x(d.endDate) - x(d.startDate)); 
      });

      rect.transition()
        .attr("transform", rectTransform)
        .attr("height", function(d) { return y.range()[1]; })
        .attr("width", function(d) { 
          return (x(d.endDate) - x(d.startDate)); 
        });

        rect.exit().remove();

        svg.select(".x").transition().call(xAxis);
        svg.select(".y").transition().call(yAxis);

        return gantt;
  };

  gantt.margin = function(value) {
    if (!arguments.length)
      return margin;
    margin = value;
    return gantt;
  };

  gantt.timeDomain = function(value) {
    if (!arguments.length)
      return [ timeDomainStart, timeDomainEnd ];
    timeDomainStart = +value[0], timeDomainEnd = +value[1];
    return gantt;
  };

  gantt.timeDomainMode = function(value) {
    if (!arguments.length)
      return timeDomainMode;
    timeDomainMode = value;
    return gantt;
  };

  gantt.taskTypes = function(value) {
    if (!arguments.length)
      return taskTypes;
    taskTypes = value;
    return gantt;
  };

  gantt.taskStatus = function(value) {
    if (!arguments.length)
      return taskStatus;
    taskStatus = value;
    return gantt;
  };

  gantt.width = function(value) {
    if (!arguments.length)
      return width;
    width = +value;
    return gantt;
  };

  gantt.height = function(value) {
    if (!arguments.length)
      return height;
    height = +value;
    return gantt;
  };

  gantt.tickFormat = function(value) {
    if (!arguments.length)
      return tickFormat;
    tickFormat = value;
    return gantt;
  };

  return gantt;
};
