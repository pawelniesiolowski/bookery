const ModalWindow = (() => {
    const init = (content = '') => {
        const previousModalDiv = document.querySelector('.modal-window');
        if (previousModalDiv === null) {
            let modalDiv = createModal();
            appendContentToModal(modalDiv, content);
            bindCenterModal(modalDiv);
            showModal(modalDiv);
            centerModal(modalDiv);
        }
    };

    const createModal = () => {
        const modalDiv = document.createElement('div');
        modalDiv.setAttribute('class', 'modal-window');
        return modalDiv;
    };

    const appendContentToModal = (modalDiv, content) => {
            modalDiv.appendChild(content);
    };

    const bindCenterModal = (modalDiv) => {
        window.addEventListener('resize', () => {
            centerModal(modalDiv);
        });
    };

    const showModal = (modalDiv) => {
        const body = document.getElementsByTagName('body');
        body[0].appendChild(modalDiv);
    };

    const centerModal = (modalDiv) => {
        const height = modalDiv.clientHeight;
        const width = modalDiv.clientWidth;
        const top = (window.innerHeight - height) / 2;
        const left = (window.innerWidth - width) / 2;
        modalDiv.style.cssText = 'top:' + top + 'px;left:' + left + 'px;';
    };

    const closeModal = () => {
        const modalDiv = document.querySelector('.modal-window');
        if (modalDiv) {
            modalDiv.remove();
        }
    };

    return {
        init: init,
        closeModal : closeModal
    };
})();
