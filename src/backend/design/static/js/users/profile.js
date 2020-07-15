var ctx = document.getElementById('profileChart');
var max = 15;
var min = 0;
var profileChart = new Chart(ctx, {
  type: 'radar',
  data: {
    labels: ['Crypto', 'Misc', 'Web', 'Forensics', 'Pwn', 'OSINT'],
    datasets: [{
      data: [Math.floor(Math.random() * (max - min + 1) ) + min, 
      Math.floor(Math.random() * (max - min + 1) ) + min, Math.floor(Math.random() * (max - min + 1) ) + min, Math.floor(Math.random() * (max - min + 1) ) + min, Math.floor(Math.random() * (max - min + 1) ) + min, Math.floor(Math.random() * (max - min + 1) ) + min],
      backgroundColor: 'rgba(0,119,204,0.4)',
      borderColor: 'rgba(0,119,204, 0.4)',
      borderWidth: 1,
    }]
  },
  options: {
    scale: {
      pointLabels :{
       fontSize: '12',
       fontColor: 'white',
      },
      yAxes: [{
        ticks: {
          max: 5,
          min: 0,
          stepSize: 5
        }
      }],
      ticks: {
        display: false,
        suggestedMin: 10,
        suggestedMax: 15,
        stepSize: 5,
        beginAtZero: true,
      }
    },
    legend: {
      display: false
    }
  }
});