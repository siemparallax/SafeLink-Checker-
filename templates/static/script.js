async function analyzeURL() {


    const input = document.getElementById("urlInput");

    const resultBox = document.getElementById("result");


    const url = input.value.trim();



    if (url === "") {

        resultBox.innerHTML = `
            <div class="result danger">
                <p>Please enter a URL first.</p>
            </div>
        `;

        return;
    }



    resultBox.innerHTML = `
        <div class="result">
            <p>Checking URL...</p>
        </div>
    `;



    try {


        const response = await fetch("/analyze", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                url: url

            })

        });



        const data = await response.json();



        if (data.error) {


            resultBox.innerHTML = `

                <div class="result danger">

                    <p>${data.error}</p>

                </div>

            `;


            return;

        }



        let cssClass = "safe";


        if (data.risk_level === "Medium Risk") {

            cssClass = "medium";

        }


        if (data.risk_level === "High Risk") {

            cssClass = "danger";

        }



        let warnings = "";



        if (data.warnings.length > 0) {


            warnings = "<ul>";


            data.warnings.forEach(item => {


                warnings += `<li>${item}</li>`;


            });


            warnings += "</ul>";

        }

        else {


            warnings = "<p>No security problems found.</p>";

        }




        resultBox.innerHTML = `


            <div class="result ${cssClass}">


                <h3>
                    Analysis Result
                </h3>


                <p>
                    <strong>URL:</strong>
                    ${data.url}
                </p>


                <p>
                    <strong>Risk Level:</strong>
                    ${data.risk_level}
                </p>


                <p>
                    <strong>Score:</strong>
                    ${data.risk_score}/100
                </p>


                <h4>
                    Details
                </h4>


                ${warnings}


            </div>


        `;



    }


    catch(error) {


        resultBox.innerHTML = `


            <div class="result danger">

                <p>
                    Something went wrong.
                </p>

            </div>


        `;


        console.log(error);


    }


}
