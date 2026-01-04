/**
 * SIP Calculator Widget
 * Calculates future value, total investment, and wealth gain for SIP investments
 */

class SIPCalculator {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`Container '${containerId}' not found`);
            return;
        }
        this.render();
        this.attachEventListeners();
    }

    render() {
        this.container.innerHTML = `
            <div class="sip-calculator-widget" style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h3 style="margin-top: 0; color: #333;">SIP Calculator</h3>

                <div class="calculator-inputs" style="margin-bottom: 20px;">
                    <div class="input-group" style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: 500;">
                            Monthly Investment (₹)
                        </label>
                        <input type="number" id="sipMonthly" class="form-control"
                               value="5000" min="500" step="500"
                               style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                        <input type="range" id="sipMonthlySlider" class="form-range"
                               value="5000" min="500" max="100000" step="500"
                               style="width: 100%; margin-top: 5px;">
                    </div>

                    <div class="input-group" style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: 500;">
                            Investment Period (Years)
                        </label>
                        <input type="number" id="sipYears" class="form-control"
                               value="10" min="1" max="40" step="1"
                               style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                        <input type="range" id="sipYearsSlider" class="form-range"
                               value="10" min="1" max="40" step="1"
                               style="width: 100%; margin-top: 5px;">
                    </div>

                    <div class="input-group" style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: 500;">
                            Expected Return (% p.a.)
                        </label>
                        <input type="number" id="sipReturn" class="form-control"
                               value="12" min="1" max="30" step="0.5"
                               style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                        <input type="range" id="sipReturnSlider" class="form-range"
                               value="12" min="1" max="30" step="0.5"
                               style="width: 100%; margin-top: 5px;">
                    </div>
                </div>

                <div class="calculator-results" style="background: #f5f5f5; padding: 15px; border-radius: 6px;">
                    <div class="result-row" style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span style="font-weight: 500;">Total Investment:</span>
                        <span id="totalInvested" style="font-weight: bold; color: #2196F3;">₹0</span>
                    </div>
                    <div class="result-row" style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span style="font-weight: 500;">Expected Returns:</span>
                        <span id="expectedReturns" style="font-weight: bold; color: #4CAF50;">₹0</span>
                    </div>
                    <div class="result-row" style="display: flex; justify-content: space-between; padding-top: 10px; border-top: 2px solid #ddd;">
                        <span style="font-weight: 600; font-size: 16px;">Future Value:</span>
                        <span id="futureValue" style="font-weight: bold; font-size: 18px; color: #FF5722;">₹0</span>
                    </div>
                </div>

                <div class="result-chart" style="margin-top: 20px; height: 250px;">
                    <canvas id="sipResultChart"></canvas>
                </div>
            </div>
        `;
    }

    attachEventListeners() {
        // Input fields
        const monthlyInput = document.getElementById('sipMonthly');
        const yearsInput = document.getElementById('sipYears');
        const returnInput = document.getElementById('sipReturn');

        // Sliders
        const monthlySlider = document.getElementById('sipMonthlySlider');
        const yearsSlider = document.getElementById('sipYearsSlider');
        const returnSlider = document.getElementById('sipReturnSlider');

        // Sync input with slider
        monthlyInput.addEventListener('input', (e) => {
            monthlySlider.value = e.target.value;
            this.calculate();
        });
        monthlySlider.addEventListener('input', (e) => {
            monthlyInput.value = e.target.value;
            this.calculate();
        });

        yearsInput.addEventListener('input', (e) => {
            yearsSlider.value = e.target.value;
            this.calculate();
        });
        yearsSlider.addEventListener('input', (e) => {
            yearsInput.value = e.target.value;
            this.calculate();
        });

        returnInput.addEventListener('input', (e) => {
            returnSlider.value = e.target.value;
            this.calculate();
        });
        returnSlider.addEventListener('input', (e) => {
            returnInput.value = e.target.value;
            this.calculate();
        });

        // Initial calculation
        this.calculate();
    }

    calculate() {
        const monthly = parseFloat(document.getElementById('sipMonthly').value) || 0;
        const years = parseInt(document.getElementById('sipYears').value) || 0;
        const returnRate = parseFloat(document.getElementById('sipReturn').value) || 0;

        // Calculate SIP future value
        const monthlyRate = returnRate / 100 / 12;
        const months = years * 12;

        let futureValue = 0;
        if (monthlyRate > 0) {
            // FV = P × [(1 + r)^n - 1] / r × (1 + r)
            futureValue = monthly * (((Math.pow(1 + monthlyRate, months) - 1) / monthlyRate) * (1 + monthlyRate));
        } else {
            futureValue = monthly * months;
        }

        const totalInvested = monthly * months;
        const expectedReturns = futureValue - totalInvested;

        // Update display
        document.getElementById('totalInvested').textContent = this.formatCurrency(totalInvested);
        document.getElementById('expectedReturns').textContent = this.formatCurrency(expectedReturns);
        document.getElementById('futureValue').textContent = this.formatCurrency(futureValue);

        // Update chart
        this.updateChart(totalInvested, expectedReturns);
    }

    updateChart(invested, returns) {
        const ctx = document.getElementById('sipResultChart');
        if (!ctx) return;

        // Destroy existing chart if any
        if (this.chart) {
            this.chart.destroy();
        }

        const data = {
            labels: ['Total Invested', 'Expected Returns'],
            datasets: [{
                data: [invested, returns],
                backgroundColor: ['#2196F3', '#4CAF50'],
                borderWidth: 0
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
                        position: 'bottom',
                        labels: {
                            font: {
                                size: 12
                            },
                            padding: 10,
                            generateLabels: function(chart) {
                                const data = chart.data;
                                return data.labels.map((label, i) => {
                                    const value = data.datasets[0].data[i];
                                    return {
                                        text: `${label}: ${SIPCalculator.formatCurrencyStatic(value)}`,
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
                                const value = context.parsed;
                                return `${context.label}: ${SIPCalculator.formatCurrencyStatic(value)}`;
                            }
                        }
                    }
                }
            }
        };

        this.chart = new Chart(ctx, config);
    }

    formatCurrency(amount) {
        if (amount >= 10000000) {
            return '₹' + (amount / 10000000).toFixed(2) + ' Cr';
        } else if (amount >= 100000) {
            return '₹' + (amount / 100000).toFixed(2) + ' L';
        } else if (amount >= 1000) {
            return '₹' + (amount / 1000).toFixed(2) + ' K';
        }
        return '₹' + amount.toFixed(0);
    }

    static formatCurrencyStatic(amount) {
        if (amount >= 10000000) {
            return '₹' + (amount / 10000000).toFixed(2) + ' Cr';
        } else if (amount >= 100000) {
            return '₹' + (amount / 100000).toFixed(2) + ' L';
        } else if (amount >= 1000) {
            return '₹' + (amount / 1000).toFixed(2) + ' K';
        }
        return '₹' + amount.toFixed(0);
    }
}

// ==================== Lumpsum Calculator ====================

class LumpsumCalculator {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`Container '${containerId}' not found`);
            return;
        }
        this.render();
        this.attachEventListeners();
    }

    render() {
        this.container.innerHTML = `
            <div class="lumpsum-calculator-widget" style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h3 style="margin-top: 0; color: #333;">Lumpsum Calculator</h3>

                <div class="calculator-inputs" style="margin-bottom: 20px;">
                    <div class="input-group" style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: 500;">
                            Investment Amount (₹)
                        </label>
                        <input type="number" id="lumpsumAmount" class="form-control"
                               value="100000" min="1000" step="1000"
                               style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                    </div>

                    <div class="input-group" style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: 500;">
                            Investment Period (Years)
                        </label>
                        <input type="number" id="lumpsumYears" class="form-control"
                               value="10" min="1" max="40" step="1"
                               style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                        <input type="range" id="lumpsumYearsSlider" class="form-range"
                               value="10" min="1" max="40" step="1"
                               style="width: 100%; margin-top: 5px;">
                    </div>

                    <div class="input-group" style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: 500;">
                            Expected Return (% p.a.)
                        </label>
                        <input type="number" id="lumpsumReturn" class="form-control"
                               value="12" min="1" max="30" step="0.5"
                               style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                        <input type="range" id="lumpsumReturnSlider" class="form-range"
                               value="12" min="1" max="30" step="0.5"
                               style="width: 100%; margin-top: 5px;">
                    </div>
                </div>

                <div class="calculator-results" style="background: #f5f5f5; padding: 15px; border-radius: 6px;">
                    <div class="result-row" style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span style="font-weight: 500;">Invested Amount:</span>
                        <span id="lumpsumInvested" style="font-weight: bold; color: #2196F3;">₹0</span>
                    </div>
                    <div class="result-row" style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span style="font-weight: 500;">Expected Returns:</span>
                        <span id="lumpsumReturns" style="font-weight: bold; color: #4CAF50;">₹0</span>
                    </div>
                    <div class="result-row" style="display: flex; justify-content: space-between; padding-top: 10px; border-top: 2px solid #ddd;">
                        <span style="font-weight: 600; font-size: 16px;">Future Value:</span>
                        <span id="lumpsumFutureValue" style="font-weight: bold; font-size: 18px; color: #FF5722;">₹0</span>
                    </div>
                </div>
            </div>
        `;
    }

    attachEventListeners() {
        const amountInput = document.getElementById('lumpsumAmount');
        const yearsInput = document.getElementById('lumpsumYears');
        const returnInput = document.getElementById('lumpsumReturn');
        const yearsSlider = document.getElementById('lumpsumYearsSlider');
        const returnSlider = document.getElementById('lumpsumReturnSlider');

        amountInput.addEventListener('input', () => this.calculate());

        yearsInput.addEventListener('input', (e) => {
            yearsSlider.value = e.target.value;
            this.calculate();
        });
        yearsSlider.addEventListener('input', (e) => {
            yearsInput.value = e.target.value;
            this.calculate();
        });

        returnInput.addEventListener('input', (e) => {
            returnSlider.value = e.target.value;
            this.calculate();
        });
        returnSlider.addEventListener('input', (e) => {
            returnInput.value = e.target.value;
            this.calculate();
        });

        this.calculate();
    }

    calculate() {
        const amount = parseFloat(document.getElementById('lumpsumAmount').value) || 0;
        const years = parseInt(document.getElementById('lumpsumYears').value) || 0;
        const returnRate = parseFloat(document.getElementById('lumpsumReturn').value) || 0;

        // Calculate future value: FV = PV × (1 + r)^n
        const futureValue = amount * Math.pow(1 + (returnRate / 100), years);
        const returns = futureValue - amount;

        document.getElementById('lumpsumInvested').textContent = SIPCalculator.formatCurrencyStatic(amount);
        document.getElementById('lumpsumReturns').textContent = SIPCalculator.formatCurrencyStatic(returns);
        document.getElementById('lumpsumFutureValue').textContent = SIPCalculator.formatCurrencyStatic(futureValue);
    }
}

// Export
window.SIPCalculator = SIPCalculator;
window.LumpsumCalculator = LumpsumCalculator;
