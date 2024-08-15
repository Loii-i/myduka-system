const totalSales = 123456;
const totalProfit = 789012;

// Set metrics data
document.getElementById("total-sales").innerText = totalSales.toLocaleString();
document.getElementById("total-profit").innerText = totalProfit.toLocaleString();


// Bar Chart Initialization
new Chart(document.getElementById("bar-chart"), {
    type: 'bar',
    data: {
        labels: {{ p_name | safe }},
    datasets: [
    {
        label: "Sales",
        backgroundColor: "#1f77b4",
        borderColor: "#1f77b4",
        borderWidth: 2,
        hoverBackgroundColor: "#3e95cd",
        hoverBorderColor: "#3e95cd",
        data: {{ p_sales | safe }}
            },
    {
        label: "Profit",
        backgroundColor: "#ff7f0e",
        borderColor: "#ff7f0e",
        borderWidth: 2,
        hoverBackgroundColor: "#ff9d4e",
        hoverBorderColor: "#ff9d4e",
        data: {{ prof_tot | safe }}
            }
]
    },
    options: {
    responsive: true,
    legend: {
        display: true,
        labels: {
            fontColor: '#ffffff'
        }
    },
    title: {
        display: true,
        text: 'profit per sales',
        fontColor: '#ffffff'
    },
    scales: {
        xAxes: [{
            barPercentage: 0.7, // Make bars wider
            gridLines: {
                color: "rgba(255,255,255,0.1)"
            },
            ticks: {
                fontColor: "#ffffff"
            }
        }],
        yAxes: [{
            ticks: {
                beginAtZero: true,
                fontColor: "#ffffff"
            },
            gridLines: {
                color: "rgba(255,255,255,0.1)"
            }
        }]
    },
    tooltips: {
        mode: 'index',
        intersect: false,
        backgroundColor: 'rgba(0,0,0,0.7)',
        bodyFontColor: '#ffffff',
        titleFontColor: '#ffffff',
        borderColor: '#000000',
        borderWidth: 1
    },
    hover: {
        mode: 'nearest',
        intersect: true
    }
}
});


// Line Chart Initialization for Daily Sales and Profit
new Chart(document.getElementById("line-chart"), {
    type: 'line',
    data: {
        labels: {{ sales_d | safe }}, // Assuming date corresponds to dates
    datasets: [{
        label: "Daily Sales",
        borderColor: "#3e95cd",
        fill: false,
        data: {{ sales_amount | safe }}  // Assuming sales_d corresponds to daily sales data
        },
    {
        label: "Daily Profit",
        borderColor: "#8e5ea2",
        fill: false,
        data: {{ prof_amount | safe }}  // Assuming profit_d corresponds to daily profit data
        }]
    },
    options: {
    legend: {
        display: true
    },
    title: {
        display: true,
        text: 'Daily Sales and Profit'
    },
    scales: {
        yAxes: [{
            ticks: {
                beginAtZero: true
            }
        }]
    }
}
});
