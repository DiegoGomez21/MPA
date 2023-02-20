function confirmDelete() {
    const deleteForm = document.getElementById('delete-post-form');
    deleteForm.addEventListener('submit', function(e) {
        const confirmed = confirm('¿Estás seguro de que deseas eliminar este post?');
        if (!confirmed) {
            e.preventDefault();
        }
    });
    const methodInput = document.createElement('input');
    methodInput.setAttribute('type', 'hidden');
    methodInput.setAttribute('name', '_method');
    methodInput.setAttribute('value', 'DELETE');
    deleteForm.appendChild(methodInput);
}
