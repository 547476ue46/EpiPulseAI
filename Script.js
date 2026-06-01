document.addEventListener("DOMContentLoaded", function () {

  // 📊 Usage Chart
  const ctx1 = document.getElementById('usageChart');

  new Chart(ctx1, {
    type: 'line',
    data: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [{
        label: 'AI Usage',
        data: [12, 19, 8, 15, 22, 30, 28],
        borderColor: '#7c5cff',
        backgroundColor: 'rgba(124,92,255,0.2)',
        tension: 0.4
      }]
    }
  });

  // 📊 Performance Chart
  const ctx2 = document.getElementById('performanceChart');

  new Chart(ctx2, {
    type: 'bar',
    data: {
      labels: ['Speed', 'Accuracy', 'Uptime', 'UX'],
      datasets: [{
        label: 'Performance',
        data: [90, 85, 95, 88],
        backgroundColor: [
          '#7c5cff',
          '#4cc9f0',
          '#00d4ff',
          '#9b5cff'
        ]
      }]
    }
  });

});