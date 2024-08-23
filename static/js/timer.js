
const currentUrl = window.location.href;
const url = new URL(currentUrl);
const params = new URLSearchParams(url.search);
const age = params.get("t");
const testDurationMinutes = age || 20;
alert("Click OK when you are ready to start, wish you goodluck.")
const endTime = new Date().getTime() + (testDurationMinutes * 60 * 1000);
const countdown = setInterval(function() {
    const now = new Date().getTime();
    const distance = endTime - now;

    if (distance <= 0) {
        clearInterval(countdown);
        document.querySelector("[timer]").innerHTML = "Test has ended!";
        document.querySelector("form").submit()
    } else {
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        const countdownString = `${minutes}m ${seconds}s`;
        document.querySelector("[timer]").innerHTML = countdownString;
            }
        }, 1000);
