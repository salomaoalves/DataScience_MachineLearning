window.onload = function () {
    const change_freq = document.getElementById("freq_nav");
    if (!change_freq) return; // only info pages have the nav buttons

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

    run();
}

//graphic size configs
const margin = {top: 20, right: 50, bottom: 40, left: 180};
const width = 800 - margin.left - margin.right;
const bar_height = 28;

//data: read the csv files created by services/ngram.py
function get_data() {
    const types = ["unagram", "bigram", "trigram"];
    const t = Date.now(); // avoid browser cache, the csv files change at each analysis
    return Promise.all(types.map(type =>
        d3.csv(`/static/dataset/${type}.csv?t=${t}`, row => ({
            key: row[type],
            value: +row[`${type}_frequency`]
        }))
    )).then(([unagram, bigram, trigram]) => ({unagram, bigram, trigram}));
}

//get filters attr
function get_filters() {
    return {
        type: document.querySelector("input[name=ngram_type]:checked").value,
        sort: document.getElementById("ngram_sort").value,
        rows: Math.max(1, +document.getElementById("ngram_rows").value || 15)
    };
}

//apply sort and number of rows
function filter_data(grams, filters) {
    const data = grams[filters.type].slice();
    if (filters.sort === "asc") {
        data.sort((a, b) => a.value - b.value || d3.ascending(a.key, b.key));
    } else {
        data.sort((a, b) => b.value - a.value || d3.ascending(a.key, b.key));
    }
    return data.slice(0, filters.rows);
}

//draw the graphic (horizontal bars, so the n-gram text fits in the labels)
function plot(data, type) {
    const container = d3.select("#ngram_chart");
    container.selectAll("*").remove();

    if (data.length === 0) {
        container.append("p")
            .classed("no-data", true)
            .text(`No ${type} found in this text.`);
        return;
    }

    const height = data.length * bar_height;
    const svg = container.append("svg")
        .attr("id", "chart")
        .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
        .attr("width", width + margin.left + margin.right);
    const chart = svg.append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    //axis
    const x = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value)])
        .nice()
        .range([0, width]);
    const y = d3.scaleBand()
        .domain(data.map(d => d.key))
        .range([0, height])
        .padding(0.2);
    const ticks = Math.min(x.domain()[1], 10);

    //gridlines
    chart.append("g")
        .classed("gridline", true)
        .call(d3.axisBottom(x).ticks(ticks).tickSize(height).tickFormat(""));

    chart.append("g")
        .classed("x axis", true)
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x).ticks(ticks).tickFormat(d3.format("d")));
    chart.append("g")
        .classed("y axis", true)
        .call(d3.axisLeft(y));

    chart.append("text")
        .classed("axis-label", true)
        .attr("x", width / 2)
        .attr("y", height + 35)
        .style("text-anchor", "middle")
        .text("Frequency");

    //bars
    chart.selectAll(".bar")
        .data(data)
        .enter()
        .append("rect")
            .classed("bar", true)
            .attr("x", 0)
            .attr("y", d => y(d.key))
            .attr("height", y.bandwidth())
            .attr("width", 0)
            .on("mouseover", function () { d3.select(this).classed("bar-hover", true); })
            .on("mouseout", function () { d3.select(this).classed("bar-hover", false); })
        .transition()
            .duration(500)
            .attr("width", d => x(d.value));

    //labels
    chart.selectAll(".bar-label")
        .data(data)
        .enter()
        .append("text")
            .classed("bar-label", true)
            .attr("x", d => x(d.value) + 6)
            .attr("y", d => y(d.key) + y.bandwidth() / 2)
            .attr("dy", "0.35em")
            .text(d => d.value);
}

function run() {
    get_data().then(grams => {
        const draw = () => {
            const filters = get_filters();
            plot(filter_data(grams, filters), filters.type);
        };
        document.querySelectorAll("#ngram_filters input, #ngram_filters select")
            .forEach(el => el.addEventListener("change", draw));
        draw();
    }).catch(err => {
        d3.select("#ngram_chart").append("p")
            .classed("no-data", true)
            .text("Could not load the n-grams: " + err);
    });
}
