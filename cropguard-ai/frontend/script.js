async function analyzeCrop() {
    const imageInput = document.getElementById("imageInput");
    const resultDiv = document.getElementById("result");

    if (imageInput.files.length === 0) {
        resultDiv.innerHTML = "<p style='color:red'>Please upload an image</p>";
        return;
    }

    const formData = new FormData();
    formData.append("image", imageInput.files[0]);

    resultDiv.innerHTML = "<p>Analyzing...</p>";

    try {
        const response = await fetch("http://127.0.0.1:5000/api/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        resultDiv.innerHTML = `
            <p><b>Disease:</b> ${data.disease}</p>
            <p><b>Confidence:</b> ${data.confidence}%</p>
            <p><b>Advisory:</b> ${data.advisory}</p>
            <p><b>Alert:</b> ${data.alert}</p>
        `;
    } catch (error) {
        resultDiv.innerHTML =
            "<p style='color:red'>Unable to analyze image. Try again.</p>";
    }
}
