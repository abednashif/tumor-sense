function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function handleThemeChange() {
    var themePicker = document.getElementById('theme');
    var selectedTheme = themePicker.value;
    setCookie('theme', selectedTheme, 365);

    if (selectedTheme === '☀️') {
        document.documentElement.style.setProperty('--base', '#cfcfcf');
        document.documentElement.style.setProperty('--text', '#212121');
        document.documentElement.style.setProperty('--card-text', '#404040');
        document.documentElement.style.setProperty('--card-bg', '#b4babfe0');
    } else if (selectedTheme === '🌑') {
        document.documentElement.style.setProperty('--base', '#212121');
        document.documentElement.style.setProperty('--text', '#cfcfcf');
        document.documentElement.style.setProperty('--card-text', '#c5c5c5');
        document.documentElement.style.setProperty('--card-bg', '#333333');
    }
}

function initializeTheme() {
    var theme = getCookie('theme');
    if (theme === '☀️') {
        document.getElementById('theme').value = '☀️';
    } else if (theme === '🌑') {
        document.getElementById('theme').value = '🌑';
    }
}

window.addEventListener('load', function () {
    initializeTheme();
    document.getElementById('theme').addEventListener('change', handleThemeChange);
});
