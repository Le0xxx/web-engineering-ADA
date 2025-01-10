const menuItems = document.querySelectorAll('#menu li');
const ingredientsContainer = document.getElementById('ingredients');

const ingredientsData = {
    classic: {
        text: ['Лаваш, мясо, лук, капуста, соус', 'Цена: 230₽'],
        image: 'images/classic-shaurma.jpg' // Путь к изображению классической шаурмы
    },
    spicy: {
        text: ['Лаваш, острый фарш, лук, капуста, острый соус', 'Цена: 250₽'],
        image: 'images/spicy-shaurma.jpg' // Путь к изображению острой шаурмы
    },
    chicken: {
        text: ['Лаваш, курица, лук, капуста, соус', 'Цена: 220₽'],
        image: 'images/chicken-shaurma.jpg' // Путь к изображению шаурмы с курицей
    }
};

menuItems.forEach(item => {
    item.addEventListener('click', () => {
        const shaurmaType = item.dataset.shaurma;
        let ingredientsHTML = `<img src="${ingredientsData[shaurmaType].image}" alt="${shaurmaType} шаурма"><br>`;
        ingredientsHTML += ingredientsData[shaurmaType].text.join('<br>');
        ingredientsContainer.innerHTML = ingredientsHTML;
        ingredientsContainer.style.display = 'block';
    });
});
