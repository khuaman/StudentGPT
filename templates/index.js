const userForm = document.querySelector("#userForm");

let questions = []

window.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch("/");
    const data = await response.json();
    users = data;
    renderUser(users);
  });