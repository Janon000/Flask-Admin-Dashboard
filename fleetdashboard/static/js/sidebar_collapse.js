//https://gitlab.com/mckenzieflavius/collapseable-sidebar/-/blob/main/app.js

let open = true;

function toggleCollapse() {
    const nav = document.querySelector('.page');

    if (open) {
    console.log('it is open, closing now');
        nav.classList.add('active');
        open = !open;
    } else {
        console.log('it is closed, opening now');
        nav.classList.remove('active');
        open = !open;
    }
}


