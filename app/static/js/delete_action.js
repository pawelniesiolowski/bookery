const DeleteAction = (() => {
    const init = (elementId) => {
        const button = document.getElementById(elementId);
        if (button) {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const deleteHref = e.target.href;
                const redirectHref = e.target.dataset.redirect;
                const name = e.target.dataset.name;
                const info = `Czy na pewno chcesz usunąć ${name}?`;
                const buttonText = 'Usuń';
                const action = () => deleteBook(deleteHref, redirectHref);
                const deleteDiv = ModalContentCreator.create(info, buttonText, action);
                ModalWindow.init(deleteDiv);
            });
        }
    };

    const deleteBook = (deleteHref, redirectHref) => {
        fetch(deleteHref, {method: 'DELETE'})
            .then(response => {
                ModalWindow.closeModal();
                if (response.status == 204) {
                    window.location.replace(redirectHref);
                } else {
                    throw new Error(`Item could not be deleted. Response status ${response.status}`);
                }
            })
            .catch((error) => {
                alert('Niestety usunięcie nie powiodło się');
                console.log(error);
            });
        ;
    };

    return {
        init: init
    };
})();
