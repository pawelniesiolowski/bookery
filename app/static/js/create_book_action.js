const CreateBookAction = (() => {
    const init = () => {
        const form = document.getElementById('bookery-save-book-action');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const title = e.target.elements.namedItem('title').value;
                if (!validateTitle(title)) {
                    return;
                }

                const getHref = e.target.dataset.get.replace('xxx', title);
                createBook(getHref, e.target);
            });
        }
    };

    const validateTitle = (title) => {
        const error = document.getElementById('bookery-book-form-title');
        const errorContent = error.firstElementChild;
        if (!title) {
            errorContent.textContent = 'Tytuł jest wymagany';
            error.classList.remove('disabled');
            return false;
        }
        if (title.length < 2) {
            errorContent.textContent = 'Tytuł musi składać się z co najmniej dwóch liter';
            error.classList.remove('disabled');
            return false;
        }
        error.classList.add('disabled');
        return true;
    };

    const createBook = (href, form) => {
        return fetch(href)
            .then(response => response.json())
            .then(data => {
                if (data.data) {
                    const title = form.elements.namedItem('title').value;
                    const info = `Książka o takim tytule już istnieje w katalogu. Czy na pewno chcesz dodać: ${title}?`;
                    const buttonText = 'Dodaj';
                    const action = () => HTMLFormElement.prototype.submit.call(form);
                    const modalContent = ModalContentCreator.create(info, buttonText, action);
                    ModalWindow.init(modalContent);
                } else {
                    HTMLFormElement.prototype.submit.call(form);
                }
            })
        ;
    };

    return {
        init: init
    };
})();

CreateBookAction.init();
