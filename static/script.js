function checkNews() {
    const newsText = document.getElementById("newsText").value.trim();
    const resultDiv = document.getElementById("result");
    const loader = document.getElementById("loader");

    if (!newsText) {
        alert("Please enter a news headline.");
        return;
    }

    // Show loader
    loader.style.display = "block";
    resultDiv.innerHTML = "";

    fetch("https://news-detector-vnz4.onrender.com//predict", { 
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ news_text: newsText })
})

    .then(response => response.json())
    .then(data => {
        loader.style.display = "none";

        if (data.error) {
            resultDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
            return;
        }

        let newsResults = data.News_Verification;
        if (newsResults.length === 0) {
            resultDiv.innerHTML = "<p>No matching news found.</p>";
            return;
        }

        let tableHTML = `
            <div class="table-container">
                <table>
                    <tr>
                        <th>Title</th>
                        <th>Source</th>
                        <th>Accuracy</th>
                        <th>Verdict</th>
                    </tr>`;

        newsResults.forEach(news => {
            let verdict = parseFloat(news.accuracy) > 75 ? "Real ✅" : "Fake ❌";
            tableHTML += `
                <tr>
                    <td><a href="${news.link}" target="_blank">${news.title}</a></td>
                    <td>${news.source}</td>
                    <td>${news.accuracy}</td>
                    <td>${verdict}</td>
                </tr>`;
        });

        tableHTML += `</table></div>`;
        resultDiv.innerHTML = tableHTML;
    })
    .catch(error => {
        loader.style.display = "none";
        resultDiv.innerHTML = `<p style="color: red;">Error fetching results: ${error.message}</p>`;
    });
}
