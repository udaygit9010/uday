function checkNews() {
    const newsText = document.getElementById("newsText").value.trim();
    const resultDiv = document.getElementById("result");
    const loader = document.getElementById("loader");

    if (!newsText) {
        alert("Please enter a news headline.");
        return;
    }

    loader.style.display = "block";
    resultDiv.innerHTML = "";

    fetch("https://your-app.onrender.com/predict", {  // Change to your actual URL
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

        let aiAnalysis = data.AI_Analysis || "No analysis available.";
        let newsResults = data.Trusted_News_Links || [];

        let tableHTML = `<h3>${aiAnalysis}</h3><br><table border="1">
                    <tr><th>Title</th><th>Source</th><th>Accuracy</th><th>Verdict</th></tr>`;

        newsResults.forEach(news => {
            let verdict = parseFloat(news.accuracy || 50) > 75 ? "Real ✅" : "Fake ❌";
            tableHTML += `<tr>
                    <td><a href="${news.link}" target="_blank">${news.title}</a></td>
                    <td>${news.source || "Unknown"}</td>
                    <td>${news.accuracy || "N/A"}</td>
                    <td>${verdict}</td>
                </tr>`;
        });

        tableHTML += `</table>`;
        resultDiv.innerHTML = tableHTML;
    })
    .catch(error => {
        loader.style.display = "none";
        resultDiv.innerHTML = `<p style="color: red;">Error fetching results: ${error.message}</p>`;
    });
}
