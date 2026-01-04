/**
 * Chart.js Visualizations for Financial Advisor Dashboard
 * Includes: Asset Allocation, Portfolio Growth, Risk Score, Goal Progress
 */

// ==================== Asset Allocation Pie Chart ====================

function renderAssetAllocationChart(allocation, canvasId = 'assetAllocationChart') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas element '${canvasId}' not found`);
        return null;
    }

    const data = {
        labels: ['Equity', 'Debt', 'Gold', 'International', 'Cash'],
        datasets: [{
            data: [
                allocation.equity || 0,
                allocation.debt || 0,
                allocation.gold || 0,
                allocation.international || 0,
                allocation.cash || 0
            ],
            backgroundColor: [
                '#4CAF50',  // Equity - Green
                '#2196F3',  // Debt - Blue
                '#FFD700',  // Gold - Gold
                '#9C27B0',  // International - Purple
                '#9E9E9E'   // Cash - Gray
            ],
            borderWidth: 2,
            borderColor: '#ffffff'
        }]
    };

    const config = {
        type: 'pie',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: {
                            size: 14
                        },
                        padding: 15,
                        generateLabels: function(chart) {
                            const data = chart.data;
                            return data.labels.map((label, i) => {
                                const value = data.datasets[0].data[i];
                                return {
                                    text: `${label}: ${value.toFixed(1)}%`,
                                    fillStyle: data.datasets[0].backgroundColor[i],
                                    hidden: false,
                                    index: i
                                };
                            });
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            return `${label}: ${value.toFixed(1)}%`;
                        }
                    }
                }
            }
        }
    };

    return new Chart(ctx, config);
}

// ==================== Portfolio Growth Line Chart ====================

function renderPortfolioGrowthChart(currentValue, monthlyInvestment, years, expectedReturn, canvasId = 'portfolioGrowthChart') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas element '${canvasId}' not found`);
        return null;
    }

    // Calculate projected values
    const monthlyRate = expectedReturn / 100 / 12;
    const labels = [];
    const investedData = [];
    const projectedData = [];

    let invested = currentValue;
    let projected = currentValue;

    for (let year = 0; year <= years; year++) {
        labels.push(year);
        investedData.push(invested);
        projectedData.push(projected);

        if (year < years) {
            // Add 12 months of SIP
            invested += monthlyInvestment * 12;

            // Calculate compound growth
            for (let month = 0; month < 12; month++) {
                projected = projected * (1 + monthlyRate) + monthlyInvestment;
            }
        }
    }

    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Total Invested',
                data: investedData,
                borderColor: '#2196F3',
                backgroundColor: 'rgba(33, 150, 243, 0.1)',
                borderWidth: 2,
                pointRadius: 3,
                pointHoverRadius: 5,
                fill: true
            },
            {
                label: 'Projected Value',
                data: projectedData,
                borderColor: '#4CAF50',
                backgroundColor: 'rgba(76, 175, 80, 0.1)',
                borderWidth: 3,
                pointRadius: 3,
                pointHoverRadius: 5,
                fill: true
            }
        ]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: {
                            size: 14
                        },
                        padding: 15
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            const value = context.parsed.y;
                            return `${label}: ₹${value.toLocaleString('en-IN', {maximumFractionDigits: 0})}`;
                        }
                    }
                },
                title: {
                    display: true,
                    text: `Portfolio Growth Projection (${expectedReturn}% annual return)`,
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            if (value >= 10000000) {
                                return '₹' + (value / 10000000).toFixed(1) + ' Cr';
                            } else if (value >= 100000) {
                                return '₹' + (value / 100000).toFixed(1) + ' L';
                            }
                            return '₹' + (value / 1000).toFixed(0) + 'K';
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Years',
                        font: {
                            size: 14
                        }
                    }
                }
            }
        }
    };

    return new Chart(ctx, config);
}

// ==================== Risk Score Gauge ====================

function renderRiskScoreGauge(riskScore, canvasId = 'riskScoreGauge') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas element '${canvasId}' not found`);
        return null;
    }

    // Determine color based on risk score
    let color;
    if (riskScore <= 3) {
        color = '#4CAF50';  // Low risk - Green
    } else if (riskScore <= 6) {
        color = '#FFC107';  // Medium risk - Yellow
    } else {
        color = '#F44336';  // High risk - Red
    }

    const data = {
        labels: ['Risk Score', 'Remaining'],
        datasets: [{
            data: [riskScore, 10 - riskScore],
            backgroundColor: [color, '#E0E0E0'],
            borderWidth: 0,
            circumference: 180,
            rotation: 270
        }]
    };

    const config = {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        },
        plugins: [{
            id: 'gaugeText',
            afterDraw: function(chart) {
                const ctx = chart.ctx;
                const centerX = (chart.chartArea.left + chart.chartArea.right) / 2;
                const centerY = (chart.chartArea.top + chart.chartArea.bottom) / 2 + 20;

                ctx.save();
                ctx.font = 'bold 36px Arial';
                ctx.fillStyle = color;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(riskScore.toFixed(1), centerX, centerY);

                ctx.font = '14px Arial';
                ctx.fillStyle = '#666';
                ctx.fillText('/ 10', centerX, centerY + 30);

                ctx.restore();
            }
        }]
    };

    return new Chart(ctx, config);
}

// ==================== Goal Progress Bars ====================

function renderGoalProgress(goals, containerId = 'goalsProgressContainer') {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`Container element '${containerId}' not found`);
        return;
    }

    container.innerHTML = '';

    goals.forEach((goal, index) => {
        const progress = (goal.current_amount / goal.target_amount) * 100;
        const progressCapped = Math.min(progress, 100);

        // Determine color based on progress
        let colorClass = 'progress-low';
        if (progress >= 75) {
            colorClass = 'progress-high';
        } else if (progress >= 40) {
            colorClass = 'progress-medium';
        }

        const goalHtml = `
            <div class="goal-progress-card" style="margin-bottom: 20px;">
                <div class="goal-header" style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <h4 style="margin: 0; font-size: 16px;">${goal.name}</h4>
                    <span class="goal-percentage" style="font-weight: bold; color: #666;">
                        ${progressCapped.toFixed(0)}%
                    </span>
                </div>
                <div class="progress-bar-container" style="background-color: #e0e0e0; border-radius: 10px; height: 20px; overflow: hidden; position: relative;">
                    <div class="progress-bar ${colorClass}" style="
                        width: ${progressCapped}%;
                        height: 100%;
                        background: linear-gradient(90deg, #4CAF50, #66BB6A);
                        transition: width 0.3s ease;
                    "></div>
                </div>
                <div class="goal-details" style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 13px; color: #666;">
                    <span>Current: ₹${goal.current_amount.toLocaleString('en-IN')}</span>
                    <span>Target: ₹${goal.target_amount.toLocaleString('en-IN')}</span>
                </div>
                <div class="goal-meta" style="font-size: 12px; color: #999; margin-top: 4px;">
                    ${goal.target_date ? `Target Date: ${new Date(goal.target_date).toLocaleDateString('en-IN')}` : ''}
                </div>
            </div>
        `;

        container.innerHTML += goalHtml;
    });

    // Add custom CSS for progress colors
    if (!document.getElementById('goal-progress-styles')) {
        const style = document.createElement('style');
        style.id = 'goal-progress-styles';
        style.textContent = `
            .progress-low { background: linear-gradient(90deg, #F44336, #EF5350) !important; }
            .progress-medium { background: linear-gradient(90deg, #FFC107, #FFD54F) !important; }
            .progress-high { background: linear-gradient(90deg, #4CAF50, #66BB6A) !important; }
        `;
        document.head.appendChild(style);
    }
}

// ==================== Category Allocation Bar Chart ====================

function renderCategoryAllocationChart(equityCategories, debtCategories, canvasId = 'categoryAllocationChart') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas element '${canvasId}' not found`);
        return null;
    }

    const data = {
        labels: [
            'Large Cap',
            'Mid Cap',
            'Small Cap',
            'Flexi Cap',
            'Liquid',
            'Short Term',
            'Medium Term',
            'Long Term'
        ],
        datasets: [
            {
                label: 'Equity',
                data: [
                    equityCategories.large_cap || 0,
                    equityCategories.mid_cap || 0,
                    equityCategories.small_cap || 0,
                    equityCategories.flexi_cap || 0,
                    0, 0, 0, 0
                ],
                backgroundColor: '#4CAF50'
            },
            {
                label: 'Debt',
                data: [
                    0, 0, 0, 0,
                    debtCategories.liquid || 0,
                    debtCategories.short_term || 0,
                    debtCategories.medium_term || 0,
                    debtCategories.long_term || 0
                ],
                backgroundColor: '#2196F3'
            }
        ]
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed.y;
                            if (value === 0) return null;
                            return `${context.dataset.label}: ${value.toFixed(1)}%`;
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Category-wise Allocation',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    };

    return new Chart(ctx, config);
}

// ==================== Export Functions ====================

window.FinancialCharts = {
    renderAssetAllocationChart,
    renderPortfolioGrowthChart,
    renderRiskScoreGauge,
    renderGoalProgress,
    renderCategoryAllocationChart
};
