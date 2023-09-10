document.addEventListener("DOMContentLoaded", function () {
    /*
    fetch("static/translate.json")
    .then(response => response.json())
    .then(data => {
      // Replace text content with translations
      document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        if (data[key]) {
          element.textContent = data[key];
        }
      });
    })

     */


    const getStatsButton1 = document.getElementById("get-stats-button1");
    const getStatsButton2 = document.getElementById("get-stats-button2");
    const getStatsButton3 = document.getElementById("get-stats-button3");
    const getStatsButton4 = document.getElementById("get-stats-button4");
    const getStatsButton5 = document.getElementById("get-stats-button5");
    const getStatsButton6 = document.getElementById("get-stats-button6");
    const imageStats = document.getElementById("statsContainer");
    const graphs1 = document.getElementById("graphs1");
    const graphs2 = document.getElementById("graphs2");
    const graphs3 = document.getElementById("graphs3");
    const graphs4 = document.getElementById("graphs4");
    const graphs5 = document.getElementById("graphs5");
    const graphs6 = document.getElementById("graphs6");
    // Add a change event listener to the "Upload File" button
    const fileInput = document.getElementById("file-input");
    const fileNameDisplay = document.getElementById("file-name");

    fileInput.addEventListener("change", function () {
        const selectedFile = fileInput.files[0];
        if (selectedFile) {
            fileNameDisplay.textContent = "Selected File: " + selectedFile.name;
            fileNameDisplay.style.display = "block";
            imageStats.style.display = "block";
            graphs1.style.display = "block";
            getStatsButton1.style.display = "inline-block";
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            fetch("/numbers", {
                method: "POST",
                body: formData
            }).then(response => response.json())
                .then(data => {
                    const datesInit = document.getElementById("days-init");
                    const datesEnd = document.getElementById("days-end");
                    const msgs = document.getElementById("total-msg");
                    datesInit.innerHTML = "Starting Date: " + data["first"];
                    datesEnd.innerHTML = "Ending Date: " + data["last"];
                    msgs.innerHTML = "Total Messages Analyzed: " + data["len"];
                });
        } else {
            fileNameDisplay.textContent = "";
            fileNameDisplay.style.display = "none";
            getStatsButton1.style.display = "none";
        }
    });

    // First Button
    getStatsButton1.addEventListener("click", function () {
        // Handle the action you want to perform when the user clicks "Get Stats"
        //alert("Getting WhatsApp Stats...");
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        fetch("/hours", {
            method: "POST",
            body: formData
        }).then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const image = document.getElementById('image1');
                image.src = url;
                image.style.display = "block";
                getStatsButton1.style.display = "none";
                graphs2.style.display = "block";
                getStatsButton2.style.display = "inline-block";
            });
    });

    // Second Button
    getStatsButton2.addEventListener("click", function () {
        // Handle the action you want to perform when the user clicks "Get Stats"
        //alert("Getting WhatsApp Stats...");
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        fetch("/months", {
            method: "POST",
            body: formData
        }).then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const image = document.getElementById('image2');
                image.src = url;
                image.style.display = "block";
                getStatsButton2.style.display = "none";
                graphs3.style.display = "block";
                getStatsButton3.style.display = "inline-block";
            });
    });

    // Third Button
    getStatsButton3.addEventListener("click", function () {
        // Handle the action you want to perform when the user clicks "Get Stats"
        //alert("Getting WhatsApp Stats...");
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        fetch("/dayDist", {
            method: "POST",
            body: formData
        }).then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const image = document.getElementById('image3');
                image.src = url;
                image.style.display = "block";
                getStatsButton3.style.display = "none";
                graphs4.style.display = "block";
                getStatsButton4.style.display = "inline-block";
            });
    });

    // Forth Button
    getStatsButton4.addEventListener("click", function () {
        // Handle the action you want to perform when the user clicks "Get Stats"
        //alert("Getting WhatsApp Stats...");
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        fetch("/eachPerson", {
            method: "POST",
            body: formData
        }).then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const image = document.getElementById('image4');
                image.src = url;
                image.style.display = "block";
                getStatsButton4.style.display = "none";
                graphs5.style.display = "block";
                getStatsButton5.style.display = "inline-block";
            });
    });

    // Fifth Button
    getStatsButton5.addEventListener("click", function () {
        // Handle the action you want to perform when the user clicks "Get Stats"
        //alert("Getting WhatsApp Stats...");
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        fetch("/noMess", {
            method: "POST",
            body: formData
        }).then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const image = document.getElementById('image5');
                image.src = url;
                image.style.display = "block";
                getStatsButton5.style.display = "none";
                graphs6.style.display = "block";
                getStatsButton6.style.display = "inline-block";
            });
    });

    //Sixth Button
    getStatsButton6.addEventListener("click", function () {
        // Handle the action you want to perform when the user clicks "Get Stats"
        //alert("Getting WhatsApp Stats...");
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        fetch("/streak", {
            method: "POST",
            body: formData
        }).then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const image = document.getElementById('image6');
                image.src = url;
                image.style.display = "block";
                getStatsButton6.style.display = "none";
            });
    });
});

