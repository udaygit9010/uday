function checkNews() {
    let newsText = document.getElementById("news_input").value;

    if (!newsText) {
        alert("Please enter some news text!");
        return;
    }

    fetch("https://uday-qb88.onrender.com/predict", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: "news_text=NASA plans to launch a new Mars rover in 2025."
})
.then(res => res.json())
.then(data => console.log(data));

    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("accuracy").textContent = data.Accuracy;
        document.getElementById("analysis").textContent = data.AI_Analysis;
        let sourcesList = document.getElementById("sources");
        sourcesList.innerHTML = ""; // Clear previous results

        if (data.Trusted_News_Links.length > 0) {
            data.Trusted_News_Links.forEach(news => {
                let li = document.createElement("li");
                let a = document.createElement("a");
                a.href = news.link;
                a.textContent = news.title;
                a.target = "_blank";
                li.appendChild(a);
                sourcesList.appendChild(li);
            });
        } else {
            sourcesList.innerHTML = "<li>No matching news found</li>";
        }

        document.getElementById("result").style.display = "block";
    })
    .catch(error => console.error("Error:", error));
}
