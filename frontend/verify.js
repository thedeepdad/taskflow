
const email = sessionStorage.getItem("verification_email");

const emailMessage = document.querySelector("#email-message");
const form = document.querySelector("#verify-form");
const message = document.querySelector("#message");

if (!email) {
    window.location.href = "./register.html";
} else {
    emailMessage.textContent = `Код отправлен на ${email}`;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const code = form.elements.code.value;

    try {
        const response = await fetch(
            "http://localhost:8000/auth/verify-email",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email: email,
                    code: code,
                }),
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                typeof data.detail === "string"
                    ? data.detail
                    : JSON.stringify(data.detail ?? data)
            );
        }

        message.textContent = "Email успешно подтверждён!";

        sessionStorage.removeItem("verification_email");

        window.location.href = "./login.html";

    } catch (error) {
        console.error(error);
        message.textContent = `Ошибка: ${error.message}`;
    }
});
