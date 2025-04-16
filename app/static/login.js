



document.getElementById("login").addEventListener("submit", (e) => {

    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    login(username, password);
    

});



async function login(username, password) {

    const params = new URLSearchParams();
    params.append("username", username);
    params.append("password", password);
    

    console.log(username, password)
    const response = await fetch("/login", { 
        method: "POST", 
        headers: { "Content-Type": "application/x-www-form-urlencoded" }, 
        body: params 
    });
    
    if (response.redirected) {
        window.location.href = response.url;
    }

}