(function () {
    function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(function (row) { return row.startsWith('csrftoken='); });
        return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : '';
    }

    function createController(options) {
        const root = options.root || document;
        const endpointTemplate = options.endpointTemplate;
        const panelSlot = root.querySelector('[data-facility-panel-slot]');
        const modalShell = root.querySelector('[data-facility-modal-shell]');
        const modalContent = root.querySelector('[data-facility-modal-content]');
        const cache = new Map();
        let activeId = null;

        if (!endpointTemplate || !panelSlot || !modalShell || !modalContent) {
            return null;
        }

        function endpointFor(id) {
            return endpointTemplate.replace('__id__', String(id));
        }

        function resetInjectedContent() {
            activeId = null;
            panelSlot.classList.remove('has-detail');
            panelSlot.innerHTML = options.placeholderHtml || '';
            modalContent.innerHTML = '';
        }

        function notifyClose() {
            if (typeof options.onClose === 'function') {
                options.onClose();
            }
        }

        function closeModal() {
            modalShell.hidden = true;
            document.body.classList.remove('has-modal-open');
            resetInjectedContent();
            notifyClose();
        }

        function closePanel() {
            closeModal();
        }

        function bindInjectedActions() {
            const modalOpenButton = panelSlot.querySelector('[data-open-facility-modal]');
            const closePanelButton = panelSlot.querySelector('[data-close-facility-panel]');
            if (modalOpenButton) {
                modalOpenButton.addEventListener('click', function () {
                    modalShell.hidden = false;
                    document.body.classList.add('has-modal-open');
                });
            }
            if (closePanelButton) {
                closePanelButton.addEventListener('click', function () {
                    closePanel();
                });
            }
        }

        function bindModalActions() {
            modalShell.querySelectorAll('[data-close-facility-modal]').forEach(function (element) {
                element.addEventListener('click', function () {
                    closeModal();
                });
            });

            modalShell.querySelectorAll('[data-delete-facility]').forEach(function (element) {
                element.addEventListener('click', async function () {
                    const deleteUrl = element.getAttribute('data-delete-url');
                    const facilityName = element.getAttribute('data-facility-name') || 'this facility';

                    if (!deleteUrl) {
                        return;
                    }

                    if (!window.confirm('Delete ' + facilityName + '? This action cannot be undone.')) {
                        return;
                    }

                    element.disabled = true;

                    try {
                        const response = await fetch(deleteUrl, {
                            method: 'POST',
                            headers: {
                                'X-Requested-With': 'XMLHttpRequest',
                                'X-CSRFToken': getCsrfToken()
                            }
                        });

                        if (!response.ok) {
                            throw new Error('Delete request failed');
                        }

                        cache.delete(activeId);
                        closeModal();
                        window.location.reload();
                    } catch (error) {
                        window.alert('Unable to delete this facility right now.');
                        element.disabled = false;
                    }
                });
            });
        }

        function applyFragments(id, fragments) {
            activeId = String(id);
            panelSlot.innerHTML = fragments.panel_html;
            panelSlot.classList.add('has-detail');
            modalContent.innerHTML = fragments.modal_html;
            bindInjectedActions();
            bindModalActions();
            if (typeof options.onOpen === 'function') {
                options.onOpen(activeId);
            }
        }

        async function openById(id) {
            if (!id) {
                return;
            }
            if (cache.has(String(id))) {
                applyFragments(id, cache.get(String(id)));
                return;
            }
            const response = await fetch(endpointFor(id), {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            if (!response.ok) {
                return;
            }
            const fragments = await response.json();
            cache.set(String(id), fragments);
            applyFragments(id, fragments);
        }

        return {
            openById: openById,
            closePanel: closePanel,
            closeModal: closeModal,
            getActiveId: function () {
                return activeId;
            }
        };
    }

    window.WpcFacilityDetails = {
        createController: createController,
    };
}());
