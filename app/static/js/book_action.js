const BookAction = (() => {
    const init = () => {
        const actions = document.getElementById('bookery-book-action');
        const specialActions = document.getElementById('bookery-book-action-table');
        const title = actions.dataset.name;
        actions.addEventListener('click', (e) => {
            const actionId = e.target.id;
            const actionHref = e.target.dataset.href;
            if (actionId == 'bookery-receive') {
                const info = `Ile egzemplarzy książki "${title}" chcesz dodać?`;
                const buttonText = 'Dodaj';
                const action = (e) => receiveAction(e, actionHref);
                const additionalDiv = createFormWithCopies('receive');
                const modalContent = ModalContentCreator.create(info, buttonText, action, additionalDiv);
                ModalWindow.init(modalContent);
            } else if (actionId == 'bookery-release') {
                const info = `Ile egzemplarzy książki "${title}" i komu chcesz wydać?`;
                const buttonText = 'Wydaj';
                const action = (e) => releaseAction(e, actionHref);
                createReleaseDiv(e.target.dataset.receivershref, (releaseAdditionalDiv) => {
                    const modalContent = ModalContentCreator.create(info, buttonText, action, releaseAdditionalDiv);
                    ModalWindow.init(modalContent);
                });
            } else if (actionId == 'bookery-sell') {
                const info = `Ile egzemplarzy książki "${title}" chcesz sprzedać?`;
                const buttonText = 'Sprzedaj';
                const additionalDiv = createFormWithCopies('sell');
                const action = (e) => sellAction(e, actionHref);
                const modalContent = ModalContentCreator.create(info, buttonText, action, additionalDiv);
                ModalWindow.init(modalContent);
            }
        });
        specialActions.addEventListener('click', (e) => {
            if (e.target.classList.contains('bookery-book-action-special')) {
                e.preventDefault();
                const copies = e.target.dataset.copies;
                const href = e.target.getAttribute('href');
                const info = `Ile z ${copies} wydanych egzemplarzy książki "${title}" udało się sprzedać?`;
                const buttonText = 'Sprzedaj';
                const additionalDiv = createFormWithCopies('sell-received');
                const action = (e) => sellReceivedAction(e, href);
                const modalContent = ModalContentCreator.create(info, buttonText, action, additionalDiv);
                ModalWindow.init(modalContent);

            }
        });
    };

    const createFormWithCopies = (name) => {
        const form = document.createElement('form');
        form.setAttribute('id', `${name}-form`);

        const formGroup = document.createElement('div');
        formGroup.setAttribute('class', 'form-group');
        form.appendChild(formGroup);

        const rowDiv = document.createElement('div');
        rowDiv.setAttribute('class', 'row');
        formGroup.appendChild(rowDiv);

        const colDiv = document.createElement('div');
        colDiv.setAttribute('class', 'col-md-4 offset-md-4');
        rowDiv.appendChild(colDiv);

        const input = document.createElement('input');
        input.setAttribute('type', 'number');
        input.setAttribute('placeholder', 'Egz.');
        input.setAttribute('class', 'form-control');
        input.setAttribute('name', 'copies');
        colDiv.appendChild(input);

        return form;
    };

    const createReleaseDiv = (receiversHref, modalInitialize) => {
        fetch(receiversHref)
        .then(response => {
            return response.json();
        })
        .then(data => {
            const receivers = data.data;
            const releaseDiv = doCreateReleaseDiv(receivers);
            modalInitialize(releaseDiv);
        })
    };

    const doCreateReleaseDiv = (receivers) => {
        const form = document.createElement('form');
        form.setAttribute('id', 'release-form');

        const firstFormGroup = document.createElement('div');
        firstFormGroup.setAttribute('class', 'form-group');
        form.appendChild(firstFormGroup);

        const firstRowDiv = document.createElement('div');
        firstRowDiv.setAttribute('class', 'row');
        firstFormGroup.appendChild(firstRowDiv);

        const firstColDiv = document.createElement('div');
        firstColDiv.setAttribute('class', 'col-md-4');
        firstRowDiv.appendChild(firstColDiv);

        const input = document.createElement('input');
        input.setAttribute('type', 'number');
        input.setAttribute('placeholder', 'Egz.');
        input.setAttribute('class', 'form-control');
        input.setAttribute('name', 'copies');
        firstColDiv.appendChild(input);

        const secColDiv = document.createElement('div');
        secColDiv.setAttribute('class', 'col-md-8');
        firstRowDiv.appendChild(secColDiv);

        const select = document.createElement('select');
        select.setAttribute('class', 'form-control');
        select.setAttribute('name', 'receiver');
        for (const receiver of receivers) {
            const option = document.createElement('option');
            option.setAttribute('value', receiver.id);
            option.textContent = receiver.name;
            select.appendChild(option);
        }
        secColDiv.appendChild(select);

        const secFormGroup = document.createElement('div');
        secFormGroup.setAttribute('class', 'form-group');
        form.appendChild(secFormGroup);

        const secRowDiv = document.createElement('div');
        secRowDiv.setAttribute('class', 'row');
        secFormGroup.appendChild(secRowDiv);

        const colDiv = document.createElement('div');
        colDiv.setAttribute('class', 'col-md-12');
        secRowDiv.appendChild(colDiv);

        const textarea = document.createElement('textarea');
        textarea.setAttribute('placeholder', 'Komentarz');
        textarea.setAttribute('class', 'form-control');
        textarea.setAttribute('name', 'comment');
        colDiv.appendChild(textarea);

        return form;
    }

    const receiveAction = (e, actionHref) => {
        e.preventDefault();
        const form = document.getElementById('receive-form');
        const copies = form.elements.namedItem('copies').value;
        const data = {copies: copies};
        return doAction(data, actionHref);
    };

    const releaseAction = (e, actionHref) => {
        e.preventDefault();
        const form = document.getElementById('release-form');
        const copies = form.elements.namedItem('copies').value;
        const receiver = form.elements.namedItem('receiver').value;
        const comment = form.elements.namedItem('comment').value;
        const data = {copies: copies, receiver: receiver, comment: comment};
        return doAction(data, actionHref);
    };

    const sellAction = (e, actionHref) => {
        e.preventDefault();
        const form = document.getElementById('sell-form');
        const copies = form.elements.namedItem('copies').value;
        const data = {copies: copies};
        return doAction(data, actionHref);
    };

    const sellReceivedAction = (e, actionHref) => {
        e.preventDefault();
        const form = document.getElementById('sell-received-form');
        const copies = form.elements.namedItem('copies').value;
        const data = {copies: copies};
        return doAction(data, actionHref);
    };

    const doAction = (data, actionHref) => {
        fetch(actionHref, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {'Content-Type': 'application/json'}
        })
        .then(response => {
            ModalWindow.closeModal();
            return response.json();
        })
        .then(response => {
            if (response.status == 201) {
                window.location.reload(true);
            } else if (response.status == 400 || response.status == 404 || response.status == 500) {
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
