/**
 * Sistem Reservasi Hotel - Main Client Script
 */

document.addEventListener('DOMContentLoaded', () => {
  // Auto-dismiss alert messages after 5 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 300);
    }, 5000);
  });

  // Calculate stay duration and estimate total price on reservation forms
  const checkinInput = document.getElementById('tanggal_checkin');
  const checkoutInput = document.getElementById('tanggal_checkout');
  const kamarSelect = document.getElementById('kamar_id');
  const totalMalamDisplay = document.getElementById('total_malam_display');
  const totalHargaDisplay = document.getElementById('total_harga_display');

  function calculateReservationSummary() {
    if (!checkinInput || !checkoutInput || !kamarSelect) return;

    const checkinDate = new Date(checkinInput.value);
    const checkoutDate = new Date(checkoutInput.value);

    if (checkinInput.value && checkoutInput.value && checkoutDate > checkinDate) {
      const diffTime = Math.abs(checkoutDate - checkinDate);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

      if (totalMalamDisplay) {
        totalMalamDisplay.textContent = `${diffDays} Malam`;
      }

      const selectedOption = kamarSelect.options[kamarSelect.selectedIndex];
      const hargaPerMalam = selectedOption ? parseFloat(selectedOption.getAttribute('data-harga')) : 0;

      if (!isNaN(hargaPerMalam) && totalHargaDisplay) {
        const totalHarga = diffDays * hargaPerMalam;
        totalHargaDisplay.textContent = new Intl.NumberFormat('id-ID', {
          style: 'currency',
          currency: 'IDR'
        }).format(totalHarga);
      }
    } else if (totalMalamDisplay && totalHargaDisplay) {
      totalMalamDisplay.textContent = '-';
      totalHargaDisplay.textContent = '-';
    }
  }

  if (checkinInput && checkoutInput && kamarSelect) {
    checkinInput.addEventListener('change', calculateReservationSummary);
    checkoutInput.addEventListener('change', calculateReservationSummary);
    kamarSelect.addEventListener('change', calculateReservationSummary);
  }
});

/**
 * Confirm item deletion modal/dialog
 * @param {string} message 
 * @returns {boolean}
 */
function confirmDeletion(message = 'Apakah Anda yakin ingin menghapus data ini?') {
  return confirm(message);
}