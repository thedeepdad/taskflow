
console.log("register.js загружен");

const form = document.querySelector("#register-form");
const message = document.querySelector("#message");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const userData = {
        username: form.elements.username.value,
        email: form.elements.email.value,
        password: form.elements.password.value,
    };

    try {
        const response = await fetch("http://localhost:8000/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(userData),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                typeof data.detail === "string"
                    ? data.detail
                    : JSON.stringify(data.detail ?? data)
            );
        }

        // Сохраняем email для следующей страницы
        sessionStorage.setItem(
            "verification_email",
            userData.email
        );

        // Переходим на страницу подтверждения
        window.location.href = "./verify.html";

    } catch (error) {
        console.error(error);
        message.textContent = `Ошибка: ${error.message}`;
    }
});
