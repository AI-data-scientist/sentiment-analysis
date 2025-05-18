const ctxTrend = document.getElementById('trendChart').getContext('2d');
new Chart(ctxTrend, {
    type: 'line',
    data: {
        labels: DATES,
        datasets: [
            {
                label: 'Positive',
                data: POSITIVES,
                borderColor: '#4CAF50',
                fill: false,
                tension: 0.3
            },
            {
                label: 'Negative',
                data: NEGATIVES,
                borderColor: '#F44336',
                fill: false,
                tension: 0.3
            },
            {
                label: 'Neutral',
                data: NEUTRALS,
                borderColor: '#FFC107',
                fill: false,
                tension: 0.3
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top'
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Date'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Nombre de Tweets'
                },
                beginAtZero: true
            }
        }
    }
});

