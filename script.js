const menuItems = document.querySelectorAll('#menu li');
const ingredientsContainer = document.getElementById('ingredients');

const ingredientsData = {
    classic: ['Лаваш, мясо, лук, капуста, соус', 'Цена: 250₽'],
    spicy: ['Лаваш, острый фарш, лук, капуста, острый соус', 'Цена: 270₽'],
    chicken: ['Лаваш, курица, лук, капуста, соус', 'Цена: 280₽']
};

menuItems.forEach(item => {
    item.addEventListener('click', () => {
        const shaurmaType = item.dataset.shaurma;
        ingredientsContainer.innerHTML = ingredientsData[shaurmaType].join('<br>');
        ingredientsContainer.style.display = 'block';
    });
});


