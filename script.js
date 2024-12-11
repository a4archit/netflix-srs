 function fetchRecommendations() {
            window.location.href = window.location.href.split('?')[0] + "?button_clicked=true";

            // const input = document.getElementById("movieInput").value;
            // const recommendations = document.getElementById("recommendations");

            // if (input.trim() === "") {
            //     recommendations.style.color = "#f44336"; // Red for empty input
            //     recommendations.innerHTML = "<p>Please enter a movie name!</p>";
            // } else {
            //     recommendations.style.color = "#000"; // Reset color
            //     recommendations.innerHTML = `
            //         <p>Recommended movies based on "${input}":</p>
            //         <ul>
            //             <li>Movie 1</li>
            //             <li>Movie 2</li>
            //             <li>Movie 3</li>
            //             <li>Movie 4</li>
            //             <li>Movie 5</li>
            //         </ul>
            //     `;
            // }
        }

        function clearInput() {
            document.getElementById("movieInput").value = "";
            document.getElementById("recommendations").innerHTML = "";
        }
