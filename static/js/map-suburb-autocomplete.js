(function () {
    const dataElement = document.getElementById('wa-suburbs-data');
    const fieldRoot = document.querySelector('[data-suburb-autocomplete]');

    if (!dataElement || !fieldRoot) {
        return;
    }

    const suburbs = JSON.parse(dataElement.textContent || '[]');
    const input = fieldRoot.querySelector('[data-suburb-input]');
    const suggestions = fieldRoot.querySelector('[data-suburb-suggestions]');
    const maxResults = 8;
    let activeIndex = -1;
    let visibleMatches = [];

    if (!input || !suggestions) {
        return;
    }

    function normalize(value) {
        return (value || '').trim().toLowerCase();
    }

    function hideSuggestions() {
        suggestions.hidden = true;
        suggestions.innerHTML = '';
        activeIndex = -1;
        visibleMatches = [];
        fieldRoot.classList.remove('is-open');
    }

    function selectSuggestion(value) {
        input.value = value;
        hideSuggestions();
        input.focus();
    }

    function renderSuggestions(matches) {
        suggestions.innerHTML = '';
        activeIndex = -1;
        visibleMatches = matches;

        if (!matches.length) {
            hideSuggestions();
            return;
        }

        matches.forEach(function (suburb, index) {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'suburb-suggestion';
            button.textContent = suburb;
            button.setAttribute('data-suggestion-index', String(index));
            button.addEventListener('mousedown', function (event) {
                event.preventDefault();
                selectSuggestion(suburb);
            });
            suggestions.appendChild(button);
        });

        suggestions.hidden = false;
        fieldRoot.classList.add('is-open');
    }

    function updateActiveSuggestion(nextIndex) {
        const items = suggestions.querySelectorAll('.suburb-suggestion');
        items.forEach(function (item, index) {
            item.classList.toggle('is-active', index === nextIndex);
        });

        if (nextIndex >= 0 && items[nextIndex]) {
            items[nextIndex].scrollIntoView({ block: 'nearest' });
        }
    }

    function findMatches(term) {
        if (!term) {
            return [];
        }

        return suburbs.filter(function (suburb) {
            return normalize(suburb).indexOf(term) !== -1;
        }).slice(0, maxResults);
    }

    input.addEventListener('input', function () {
        const term = normalize(input.value);
        renderSuggestions(findMatches(term));
    });

    input.addEventListener('focus', function () {
        const term = normalize(input.value);
        if (term) {
            renderSuggestions(findMatches(term));
        }
    });

    input.addEventListener('keydown', function (event) {
        if (suggestions.hidden || !visibleMatches.length) {
            return;
        }

        if (event.key === 'ArrowDown') {
            event.preventDefault();
            activeIndex = (activeIndex + 1) % visibleMatches.length;
            updateActiveSuggestion(activeIndex);
        } else if (event.key === 'ArrowUp') {
            event.preventDefault();
            activeIndex = (activeIndex - 1 + visibleMatches.length) % visibleMatches.length;
            updateActiveSuggestion(activeIndex);
        } else if (event.key === 'Enter' && activeIndex >= 0) {
            event.preventDefault();
            selectSuggestion(visibleMatches[activeIndex]);
        } else if (event.key === 'Escape') {
            hideSuggestions();
        }
    });

    document.addEventListener('click', function (event) {
        if (!fieldRoot.contains(event.target)) {
            hideSuggestions();
        }
    });
})();
