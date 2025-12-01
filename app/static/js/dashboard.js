document.addEventListener('DOMContentLoaded', () => {
  const ctx = document.getElementById('taskChart');
  if (!ctx) return;

  const done = parseInt(ctx.dataset.done || 0);
  const working = parseInt(ctx.dataset.working || 0);
  const pending = parseInt(ctx.dataset.pending || 0);

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Done', 'Working', 'Pending'],
      datasets: [{
        data: [done, working, pending],
        backgroundColor: ['#198754', '#ffc107', '#dc3545'],
        borderWidth: 2
      }]
    },
    options: {
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: getComputedStyle(document.body).getPropertyValue('--bs-body-color') || '#000'
          }
        }
      }
    }
  });
});
