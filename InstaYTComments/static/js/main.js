window.onload = function () {
    const change_freq = document.getElementById("freq_nav");
    const change_wordcloud = document.getElementById("wordcloud_nav");
    const change_tfidf = document.getElementById("tfidf_nav");
    const change_sent = document.getElementById("sentiment_nav");
    
    const freq_div = document.getElementById("freq")
    const wordcloud_div = document.getElementById("wordcloud")
    const tfidf_div = document.getElementById("tfidf")
    const sent_div = document.getElementById("sentiment")

    change_freq.addEventListener("click", function () { 
        freq_div.style.display = "block";
        sent_div.style.display = "none";
        tfidf_div.style.display = "none";
        wordcloud_div.style.display = "none";
        run();                
    });
    change_wordcloud.addEventListener("click", function () { 
        freq_div.style.display = "none";
        sent_div.style.display = "none";
        tfidf_div.style.display = "none";
        wordcloud_div.style.display = "block";
    });
    change_tfidf.addEventListener("click", function () { 
        freq_div.style.display = "none";
        sent_div.style.display = "none";
        tfidf_div.style.display = "block";
        wordcloud_div.style.display = "none";
    });
    change_sent.addEventListener("click", function () { 
        freq_div.style.display = "none";
        sent_div.style.display = "block";
        tfidf_div.style.display = "none";
        wordcloud_div.style.display = "none";
    });
}

//get axis
function draw_axis(params){
    
    if(params.initialize === true){
        //drawing gridlines
        this.append("g")
            .call(params.gridlines)
            .classed("gridline", true)
            .attr("transform", "translate(0,0)");

        //drawing axis x e y
        this.append("g")
            .classed("x axis", true)
            .attr("transform", "translate(" + 0 + "," + height + ")")
            .call(params.axis.x)
                .selectAll("text")
                    .classed("x-axis-label", true)
                    .style("text-anchor", "end")
                    .attr("dx", -8)
                    .attr("dy", 8)
                    .attr("transform", "translate(0,0) rotate(-45)");
        this.append("g")
            .classed("y axis", true)
            .attr("transform", "translate(0,0)")
            .call(params.axis.y);

        //labels y e x
        this.select(".y.axis")
            .append("text")
            .attr("x", 30)
            .attr("y", 0)
            .style("text-anchor", "middle")
            .attr("transform", "translate(-50," + height/2 + ") rotate(-90)")
            .text("Médias");
        this.select(".x.axis")
            .append("text")
            .attr("x", 0)
            .attr("y", 0)
            .style("text-anchor", "middle")
            .attr("transform", "translate(" + width/2 + ",145)")
            .text("Disciplinas");
    
    } else if(params.initialize === false){ //variables are not initialized
        this.selectAll("g.x.axis")
            .transition()
            .duration(500)
            .ease("bounce")
            .delay(500)
            .call(params.axis.x);
        this.selectAll(".x-axis-label")
            .style("text-anchor", "end")
            .attr("dx", -8)
            .attr("dy", 8)
            .attr("transform", "translate(0,0) rotate(-45)");
        this.selectAll("g.y.axis")
            .transition()
            .duration(500)
            .ease("bounce")
            .delay(500)
            .call(params.axis.y);
    }
};
function get_axis(ngram){
    //axis values
    var x = d3.scale.ordinal()
        .domain(ngram.map(function(dict){
            return dict.key
        }))
        .rangeBands([0, width]);
    var y = d3.scale.linear()
        .domain([0, d3.max(ngram(function(dict){
            return dict.value
        }))])
        .range([height, 0]);

    //getting axis
    var x_axis = d3.svg.axis()
            .scale(x)
            .orient("bottom");
    var y_axis = d3.svg.axis()
            .scale(y)
            .orient("left");

    // getting grid lines
    var y_gridlines = d3.svg.axis()
                .scale(y)
                .tickSize(-width,0,0)
                .tickFormat("")
                .orient("left");

    return {x_axis, y_axis, y_gridlines}
};

//draw the graphic
function plot(chart, params){
    //graphic color
    var ordinalColorScale = d3.scale.category20();
    var height = get_size_configs(2)

    //axis configs
    var get_axis_obj = get_axis(params.data);
    var x_axis = get_axis_obj.x_axis;
    var y_axis = get_axis_obj.y_axis;
    var y_gridlines = get_axis_obj.y_gridlines;

    draw_axis.call(this, {data: params.data,
                            axis:{ x: x_axis,
                                y: y_axis
                        },
                            gridlines: y_gridlines,
                            initialize: true,
                    });

    // Interartividade ao passar o mouse pelas barras
    chart.selectAll(".bar")
        .data(params.data)
        .enter()
            .append("rect")
            .classed("bar", true)
            .on("mouseover", function(d,i){
                d3.select(this).style("fill", "yellow");
            })
            .on("mousemove", function(d,i){

            })
            .on("mouseout", function(d,i){
                d3.select(this).style("fill", ordinalColorScale(i));
            });

    chart.selectAll(".bar-label")
        .data(params.data)
        .enter()
            .append("text")
            .classed("bar-label", true);
    
    // Define o gráfico de barras
    chart.selectAll(".bar")
        .transition()
        .attr("x", function(d,i){
            return x(d.key);
        })
        .attr("y", function(d,i){
            return y(d.value);
        })
        .attr("height", function(d,i){
            return height - y(d.value);
        })
        .attr("width", function(d){
            return x.rangeBand();
        })
        .style("fill", function(d,i){
            return ordinalColorScale(i);
        });

    // Define os labels
    chart.selectAll(".bar-label")
        .transition()
        .attr("x", function(d,i){
            return x(d.key) + (x.rangeBand()/2)
        })
        .attr("dx", 0)
        .attr("y", function(d,i){
            return y(d.value);
        })
        .attr("dy", -6)
        .text(function(d){
            return d.value;
        });

    chart.selectAll(".bar")
        .data(params.data)
        .exit()
        .remove();

    chart.selectAll(".bar-label")
        .data(params.data)
        .exit()
        .remove();
};

//get filters attr
function get_type(){
    if (document.getElementById("unagram").value == 1){
        return 1
    } else if (document.getElementById("bigram").value == 1){
        return 2
    } else if (document.getElementById("trigram").value == 1){
        return 3
    }
};
function get_sort(){
    if (document.getElementById("sort_asceding").value == 1){
        return 0
    } else if (document.getElementById("sort_downward").value == 1){
        return 1
    }
};
function get_numb(){
    return document.getElementById("number").value
};
function get_begin(){
    return document.getElementById("head_tail").value
};

//add filters
function filters(unagram, bigram, trigram){
    var filters = d3.select("main")
                    .append("div")
                    .attr("id", "filters");
    filters.append("h1").html("------------Filtros------------")

    //sort data filter
    var sort_filter = filters.append("div")
                             .attr("id", "sort_filter");
    sort_filter.append("h2").html("Sorting type:");
    sort_filter.append("input")
               .attr("type", "radio")
               .attr("id", "sort_asceding")
               .attr("checked", "")
               .attr("value", "sort_asceding");
    sort_filter.append("label")
               .append("for","sort_asceding")
               .html("Asceding");
    sort_filter.append("input")
               .attr("type", "radio")
               .attr("id", "sort_downward")
               .attr("value", "sort_downward");
    sort_filter.append("label")
               .append("for","sort_downward")
               .html("Downward");

    //type data filter
    var type_filter = filters.append("div")
                             .attr("id", "type_filter");
    type_filter.append("h2").html("Which graphic:");
    type_filter.append("input")
               .attr("type", "radio")
               .attr("id", "unagram")
               .attr("checked", "")
               .attr("value", "unagram");
    type_filter.append("label")
               .append("for","unagram")
               .html("Unagram");
    type_filter.append("input")
               .attr("type", "radio")
               .attr("id", "bigram")
               .attr("value", "bigram");
    type_filter.append("label")
               .append("for","bigram")
               .html("Bigram");
    type_filter.append("input")
               .attr("type", "radio")
               .attr("id", "trigram")
               .attr("value", "trigram");
    type_filter.append("label")
               .append("for","trigram")
               .html("Trigram");

    //number of row filter
    var numb_filter = filters.append("div")
                             .attr("id", "numb_filter");
    numb_filter.append("h2").html("Number of rows:");
    numb_filter.append("label")
               .append("for","number")
               .html("Number of rows: ");
    numb_filter.append("input")
               .attr("type", "number")
               .attr("id", "number")
               .attr("value", 20)
               .attr("min",0)
               .attr("max",100);
    numb_filter.append("br")
    numb_filter.append("label")
               .append("for","head_tail")
               .html("Digit 0 for head and 1 for tail: ");
    numb_filter.append("input")
               .attr("type", "number")
               .attr("id", "head_tail")
               .attr("value", 0)
               .attr("min",0)
               .attr("max",1);

    //define button and action
    numb_filter.append("br")
    var send_btn = filters.append("button")  
                          .append("id", "send_filter")
                          .html("Send filters!!!");
    send_btn.on("click", function(){
        var type = get_type();
        if (type === 1){
            var data = unagram;
        } else if (type === 2){
            var data = bigram;
        } else if (type === 3){
            var data = trigram;
        }

        var ascending = function(a,b){
            return a.value - b.value;
        };
        var descending = function(a,b){
            return b.value - a.value;
        };
        var sort = get_sort();
        if(sort === 0){
            data.sort(ascending);
        } else if(sort === 1){
            data.sort(descending);
        }

        var numb = get_numb();
        var begin = get_begin();
        if (begin === 0){
            data = data.slice(0, numb);
        }else if (begin === 1){
            data = data.slice(-1*numb);
        }

        plot.call(chart, {
            data: data,
            initialize: false
        });
    });
};

//data
function get_data(){   
    var unagram_df;
    d3.csv("dataset/bigram.csv", function(data) {
        ungram_df = data;
    });

    var bigram_df;
    d3.csv("dataset/bigram.csv", function(data) {
        bigram_df = data;
    });

    var trigram_df;
    d3.csv("dataset/trigram.csv", function(data) {
        trigram_df = data;
    });

    return {unagram_df, bigram_df, trigram_df}
};

//graphic size configs
function get_size_configs(mode) {
    var margin = {
        top: 58,
        bottom: 150,
        left: 80,
        right: 40
    };
    var h = 450;
    if (mode == 1) {
        var w = 800;
        return {margin, w, h};
    } else if (mode == 2) {
        var height = h - margin.top - margin.bottom;
        return height;
    }
};

function run() {
    //get data
    var grams = get_data();
    console.log(grams)
    var unagram = grams.unagram_df;
    var bigram = grams.bigram_df;
    var trigram = grams.trigram_df;

    //configs
    var configs = get_size_configs(1);
    var margin = configs.margin;
    var w = configs.w;
    var h = configs.h;

    //create SVG
    var svg = d3.select("main")
                .append("svg")
                .attr("id", "chart")
                .attr("width", w)
                .attr("height", h);
    var chart = svg.append("g")
                .attr("display", "block")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")"); 
    
    //get filters
    filters(unagram, bigram, trigram);

    //call plot
    plot.call(chart, {
        data: unagram,
        initialize: true
    });

};