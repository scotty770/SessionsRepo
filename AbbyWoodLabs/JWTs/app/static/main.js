function clickButton() {
    fetch('/click', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.flag) {
                document.getElementById("flag").textContent = data.flag;
            } else if (data.clicks !== undefined) {
                document.getElementById("clicks").textContent = data.clicks;
            }
        })
        .catch(err => console.error("Error:", err));
}
