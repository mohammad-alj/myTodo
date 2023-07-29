document.addEventListener('DOMContentLoaded', () => {
    const target = document.getElementById('target');
    target.addEventListener('input', async () => {
        const response = await fetch('/search?q=' + target.value);
        const lists = await response.text();
        document.getElementById('lists').innerHTML = lists;
        console.log(lists)
    });
}, false);