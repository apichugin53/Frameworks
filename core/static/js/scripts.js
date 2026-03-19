function apply_action(url, modal_id) {
    const form = document.getElementById(`form_${modal_id}`);
    form.action = url
}