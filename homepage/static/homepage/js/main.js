// Текущий год в подвале сайта: не прописан в HTML, его ставит скрипт.
const yearElement = document.getElementById("current-year");

if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}
