const ModalContentCreator = (() => {
    const create = (info, buttonText, action, additionalDiv = '') => {
        const container = document.createElement('div');
        container.setAttribute('class', 'container');

        const rowDiv1 = document.createElement('div');
        rowDiv1.setAttribute('class', 'row');
        const colDiv1 = document.createElement('div');
        colDiv1.setAttribute('class', 'col text-center');
        const text = document.createElement('p');
        text.textContent = info;
        colDiv1.appendChild(text);
        rowDiv1.appendChild(colDiv1);
        container.appendChild(rowDiv1);

        if (additionalDiv != '') {
            const additionalRowDiv = document.createElement('div');
            additionalRowDiv.setAttribute('class', 'row');
            additionalRowDiv.appendChild(additionalDiv);
            container.appendChild(additionalRowDiv);
        }

        const rowDiv2 = document.createElement('div');
        rowDiv2.setAttribute('class', 'row mt-3');
        const colDiv2 = document.createElement('div');
        colDiv2.setAttribute('class', 'col text-center');
        const deleteButton = document.createElement('button');
        deleteButton.setAttribute('class', 'btn btn-danger bookery-action');
        deleteButton.textContent = buttonText;
        deleteButton.addEventListener('click', () => { action(); });
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

    return {
        create: create
    };
})();
