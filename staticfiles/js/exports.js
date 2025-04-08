function exportReport(format) {
    // Get the current active tab
    const activeTab = document.querySelector('.nav-pills .nav-link.active');
    const type = activeTab ? activeTab.id.split('-')[0] : 'vet';
    const days = document.getElementById('dateRange').value;
    const timeframe = document.querySelector('.btn-group .btn.active').getAttribute('data-timeframe') || 'daily';
    
    // Build URL with parameters
    const url = `/reports/export/?type=${type}&format=${format}&days=${days}&timeframe=${timeframe}`;
    
    // Show loading indicator
    const loadingToast = showToast('Generating report...', 'info');
    
    // Use fetch to handle the export
    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('Export failed');
            return response.blob();
        })
        .then(blob => {
            // Create download link
            const downloadUrl = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = `inventory_report_${type}_${format}.${format}`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(downloadUrl);
            
            // Show success message
            showToast('Report generated successfully!', 'success');
        })
        .catch(error => {
            console.error('Export error:', error);
            showToast('Failed to generate report', 'error');
        })
        .finally(() => {
            // Remove loading toast
            if (loadingToast) loadingToast.hide();
        });
}

function updateChart(timeframe, tabType) {
    const currentUrl = new URL(window.location.href);
    const activeTab = tabType || document.querySelector('.nav-link.active').id.split('-')[0];
    
    // Update URL parameters
    currentUrl.searchParams.set('timeframe', timeframe);
    currentUrl.searchParams.set('active_tab', activeTab);
    
    // Update active button states in both tabs
    document.querySelectorAll('.btn-group .btn').forEach(btn => {
        const isMatch = btn.getAttribute('data-timeframe') === timeframe;
        btn.classList.toggle('active', isMatch);
    });
    
    window.location.href = currentUrl.toString();
}

function initializeCharts(trendData) {
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0,0,0,0.05)'
                }
            },
            x: {
                grid: {
                    display: false
                }
            }
        },
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    padding: 15,
                    usePointStyle: true
                }
            }
        }
    };

    // Vet Trends Chart
    if (document.getElementById('vetTrendsChart')) {
        new Chart(document.getElementById('vetTrendsChart'), {
            type: 'line',
            data: {
                labels: trendData.vet.dates,
                datasets: [
                    {
                        label: 'Stock In',
                        data: trendData.vet.in_data,
                        borderColor: 'rgba(40, 167, 69, 0.8)',
                        backgroundColor: 'rgba(40, 167, 69, 0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Stock Out',
                        data: trendData.vet.out_data,
                        borderColor: 'rgba(220, 53, 69, 0.8)',
                        backgroundColor: 'rgba(220, 53, 69, 0.1)',
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: chartOptions
        });
    }

    // Office Trends Chart
    if (document.getElementById('officeTrendsChart')) {
        new Chart(document.getElementById('officeTrendsChart'), {
            type: 'line',
            data: {
                labels: trendData.office.dates,
                datasets: [
                    {
                        label: 'Stock In',
                        data: trendData.office.in_data,
                        borderColor: 'rgba(40, 167, 69, 0.8)',
                        backgroundColor: 'rgba(40, 167, 69, 0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Stock Out',
                        data: trendData.office.out_data,
                        borderColor: 'rgba(220, 53, 69, 0.8)',
                        backgroundColor: 'rgba(220, 53, 69, 0.1)',
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: chartOptions
        });
    }

    // Distribution Charts
    const distributionOptions = {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '60%',  // Makes it a doughnut chart
        plugins: {
            legend: {
                position: 'bottom'
            }
        }
    };

    if (document.getElementById('vetDistributionChart')) {
        new Chart(document.getElementById('vetDistributionChart'), {
            type: 'doughnut',
            data: {
                labels: ['Normal Stock', 'Low Stock', 'Out of Stock'],
                datasets: [{
                    data: [
                        trendData.vet.distribution.normal,
                        trendData.vet.distribution.low,
                        trendData.vet.distribution.out
                    ],
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.8)',  // Green for normal
                        'rgba(255, 193, 7, 0.8)',  // Yellow for low
                        'rgba(220, 53, 69, 0.8)'   // Red for out
                    ]
                }]
            },
            options: distributionOptions
        });
    }

    if (document.getElementById('officeDistributionChart')) {
        new Chart(document.getElementById('officeDistributionChart'), {
            type: 'doughnut',
            data: {
                labels: ['Normal Stock', 'Low Stock', 'Out of Stock'],
                datasets: [{
                    data: [
                        trendData.office.distribution.normal,
                        trendData.office.distribution.low,
                        trendData.office.distribution.out
                    ],
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.8)',
                        'rgba(255, 193, 7, 0.8)',
                        'rgba(220, 53, 69, 0.8)'
                    ]
                }]
            },
            options: distributionOptions
        });
    }
}

function createTrendsChart(canvasId, data, options) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [
                {
                    label: 'Stock In',
                    data: data.in_data,
                    borderColor: 'rgba(40, 167, 69, 0.8)',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    fill: true
                },
                {
                    label: 'Stock Out', 
                    data: data.out_data,
                    borderColor: 'rgba(220, 53, 69, 0.8)',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    fill: true
                }
            ]
        },
        options: options
    });
}

function createDistributionChart(canvasId, data, options) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Normal Stock', 'Low Stock', 'Out of Stock'],
            datasets: [{
                data: [data.normal, data.low, data.out],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.8)',
                    'rgba(255, 193, 7, 0.8)',
                    'rgba(220, 53, 69, 0.8)'
                ],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: options
    });
}
