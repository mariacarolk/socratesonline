// Máscaras simples de input
document.addEventListener('DOMContentLoaded', () => {
  const phoneInputs = document.querySelectorAll('[data-mask="phone"]');
  phoneInputs.forEach((input) => {
    input.addEventListener('input', () => {
      let v = input.value.replace(/\D/g, '');
      if (v.length > 11) v = v.slice(0, 11);
      if (v.length > 10) {
        // (99) 99999-9999
        v = v.replace(/(\d{2})(\d{5})(\d{4}).*/, '($1) $2-$3');
      } else if (v.length > 6) {
        // (99) 9999-9999
        v = v.replace(/(\d{2})(\d{4})(\d{0,4}).*/, '($1) $2-$3');
      } else if (v.length > 2) {
        v = v.replace(/(\d{2})(\d{0,5}).*/, '($1) $2');
      } else {
        v = v.replace(/(\d*)/, '($1');
      }
      input.value = v;
    });
  });
});





