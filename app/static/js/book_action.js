const BookAction = (() => {
    const init = () => {
        const actions = document.getElementById('bookery-book-action');
        const title = actions.dataset.name;
        actions.addEventListener('click', (e) => {
            const actionId = e.target.id;
            const actionHref = e.target.dataset.href;
            if (actionId == 'bookery-receive') {
                const info = `Ile egzemplarzy książki "${title}" chcesz dodać?`;
                const buttonText = 'Dodaj';
                const action = () => doAction(actionHref);
                const additionalDiv = createAdditionalDiv();
                const modalContent = ModalContentCreator.create(info, buttonText, action, additionalDiv);
                ModalWindow.init(modalContent);
            }
        });
    };

    const createAdditionalDiv = () => {
        const colDiv = document.createElement('div');
        colDiv.setAttribute('class', 'col-md-3 offset-md-4');
        const input = document.createElement('input');
        input.setAttribute('type', 'number');
        input.setAttribute('class', 'form-control');
        input.setAttribute('id', 'bookery-book-copies');
        colDiv.appendChild(input);
        return colDiv;
    };

    const doAction = (actionHref, data) => {
        const copies = document.getElementById('bookery-book-copies').value;
        fetch(actionHref, {
            method: 'POST',
            body: JSON.stringify({copies: copies}),
            headers: {'Content-Type': 'application/json'}
        })
        .then(response => {
            ModalWindow.closeModal();
            return response.json();
        })
        .then(response => {
            if (response.status == 201) {
                window.location.reload(true);
            } else if (response.status == 400 || response.status == 404) {
                alert(response.error)
            } else {
                console.log(response.error);
            }
        });
    };

    return {
        init: init
    };
})();

BookAction.init();
