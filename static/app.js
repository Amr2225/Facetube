// Media Query
let x = window.matchMedia("(min-width: 850px)");
if (x.matches){
    console.log('matches')
    const facebook = document.querySelector('.facebook');
    const youtube = document.querySelector('.youtube');
    const container = document.querySelector('.container');

    facebook.addEventListener('mouseenter', () =>container.classList.add('hover-left'));
    facebook.addEventListener('mouseleave', () =>container.classList.remove('hover-left'));

    youtube.addEventListener('mouseenter', () =>container.classList.add('hover-right'));
    youtube.addEventListener('mouseleave', () =>container.classList.remove('hover-right'));
}