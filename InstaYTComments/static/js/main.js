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

//get filters attr
function get_filters() {
    return {
        type: document.querySelector("input[name=ngram_type]:checked").value,
        sort: document.getElementById("ngram_sort").value,
        rows: Math.max(1, +document.getElementById("ngram_rows").value || 15)
    };
}

//show only the selected n-gram type, in the selected order and number of rows
//(the rows come from the server sorted by most frequent)
function draw() {
    const filters = get_filters();
    document.querySelectorAll(".ngram_list").forEach(list => {
        const selected = list.dataset.type === filters.type;
        list.style.display = selected ? "block" : "none";
        if (!selected) return;

        const rows = Array.from(list.querySelectorAll(".ngram_row"));
        rows.sort((a, b) => a.dataset.order - b.dataset.order);
        if (filters.sort === "asc") rows.sort((a, b) => a.dataset.frequency - b.dataset.frequency); // stable: keeps alphabetical order on ties
        rows.forEach((row, i) => {
            list.appendChild(row);
            row.style.display = i < filters.rows ? "flex" : "none";
        });
    });
}

function run() {
    document.querySelectorAll(".ngram_list").forEach(list => {
        list.querySelectorAll(".ngram_row").forEach((row, i) => row.dataset.order = i);
    });
    document.querySelectorAll("#ngram_filters input, #ngram_filters select")
        .forEach(el => el.addEventListener("change", draw));
    draw();
}
