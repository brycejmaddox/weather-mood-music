const zipInput = document.querySelector(".text-input")
const loading = document.querySelector("#loading")
const weatherText = document.querySelector("#weather-text")
const header = document.querySelector("#header")

zipInput.addEventListener("keydown", async function(event){
    if (event.key === "Enter" ){
        zipInput.style.display = "none"
        header.style.display = "none"
        loading.style.display = "flex"
        const zipCode = zipInput.value;
        const response = await fetch("/get-weather", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({zip : zipCode})   
        });
        const data = await response.json();
        loading.style.display = "none"
        weatherText.style.display = "flex"
        weatherText.textContent = `It looks like it's ${data.condition} out today, how are YOU feeling?`
        console.log(data)
    }
});
