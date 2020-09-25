const DeleteBookAction = (() => {
    const init = () => {
        const button = document.getElementById('bookery-delete-book-action');
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const deleteHref = e.target.href;
            const redirectHref = e.target.dataset.redirect;
            const bookTitle = e.target.dataset.title;
            const deleteDiv = createModalContent(deleteHref, redirectHref, bookTitle);
            ModalWindow.init(deleteDiv);
        });
    };

    const createModalContent = (deleteHref, redirectHref, bookTitle) => {
        const container = document.createElement('div');
        container.setAttribute('class', 'container');

        const rowDiv1 = document.createElement('div');
        rowDiv1.setAttribute('class', 'row');
        const colDiv1 = document.createElement('div');
        colDiv1.setAttribute('class', 'col text-center');
        const text = document.createElement('p');
        text.textContent = `Czy na pewno chcesz usunąć książkę "${bookTitle}"?`;
        colDiv1.appendChild(text);
        rowDiv1.appendChild(colDiv1);
        container.appendChild(rowDiv1);

        const rowDiv2 = document.createElement('div');
        rowDiv2.setAttribute('class', 'row mt-3');
        const colDiv2 = document.createElement('div');
        colDiv2.setAttribute('class', 'col text-center');
        const deleteButton = document.createElement('button');
        deleteButton.setAttribute('class', 'btn btn-danger bookery-action');
        deleteButton.textContent = 'Usuń';
        deleteButton.addEventListener('click', (e) => { deleteBook(deleteHref, redirectHref); });
        colDiv2.appendChild(deleteButton);
        const cancelButton = document.createElement('button');
        cancelButton.setAttribute('class', 'btn btn-default bookery-action-last');
        cancelButton.textContent = 'Anuluj';
        cancelButton.addEventListener('click', (e) => { e.preventDefault(); ModalWindow.closeModal(); });
        colDiv2.appendChild(cancelButton);
        rowDiv2.appendChild(colDiv2);
        container.appendChild(rowDiv2);
        return container;
    };

    const deleteBook = (deleteHref, redirectHref) => {
        fetch(deleteHref, {method: 'DELETE'})
            .then(response => {
                ModalWindow.closeModal();
                if (response.status == 204) {
                    window.location.replace(redirectHref);
                } else {
                    throw new Error(`The book could not be deleted. Response status ${response.status}`);
                }
            })
            .catch((error) => {
                alert('Niestety nie udało się usunąć książki');
                console.log(error);
            });
        ;
    };

    return {
        init: init
    }
})();

DeleteBookAction.init();
