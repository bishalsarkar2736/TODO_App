document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.countdown').forEach(el => {
    const ds = el.dataset.duedate;
    const status =(el.dataset.status || '').trim().toLowerCase();

    if (!ds) return;

    const due = new Date(ds);
    if (isNaN(due)) {
      el.textContent = "Invalid date";
      return;
    }

    console.log('Countdown initialized:', status, ds);

    if (status === 'done' || status ==='completed'){
      el.textContent = "✅ Done";
      el.classList.add("text-success", "fw-semibold")
      return;
    }

    

    function updateCountdown() {
      const now = new Date();
      const diff = due - now;

      if (diff <= 0) {
        el.textContent = "⏰ Due";
        el.classList.add("expired");
        clearInterval(timer);
        return;
      }
      const d = Math.floor(diff / 86400000);
      const h = Math.floor((diff % 86400000) / 3600000);
      const m = Math.floor((diff % 3600000) / 60000);
      el.textContent = `${d}d ${h}h ${m}m`;
    }

    updateCountdown();
    const timer = setInterval(updateCountdown, 1000);


    console.log('Countdown initialized:', el.dataset.status, el.dataset.duedate);

  });


  const toggleBtn = document.getElementById('themeToggle');
  if (toggleBtn) {
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'dark') {
      document.body.classList.add('dark-mode');
      toggleBtn.textContent = '☀️ Light';
    }

    toggleBtn.addEventListener('click', () => {
      document.body.classList.toggle('dark-mode');
      const isDark = document.body.classList.contains('dark-mode');
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
      toggleBtn.textContent = isDark ? '☀️ Light' : '🌙 Dark';
    });
  }

});


