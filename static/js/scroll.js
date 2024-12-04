// Initialize Scrollama
var scroller = scrollama();

// Function to render the chart
function renderChart(spec) {
    vegaEmbed('#chart', spec, { actions: false }).then(function(result) {
        // Additional interactions can be added here
    }).catch(console.error);
}

// Handle step enter events
function handleStepEnter(response) {
    // Log the current step
    console.log('Entering step', response.element.dataset.step);

    // Remove active class from all steps
    document.querySelectorAll('.step').forEach(function(step) {
        step.classList.remove('active');
    });
    // Add active class to current step
    response.element.classList.add('active');

    var step = response.element.dataset.step;
    if (step === '1') {
        renderChart(chart1Spec);
    } else if (step === '2') {
        renderChart(chart2Spec);
    } else if (step === '3') {
        renderChart(chart3Spec);
    }
}

// Setup Scrollama
scroller
    .setup({
        step: '.step',
        offset: 0.7, // Adjust offset to trigger the step earlier
        debug: false
    })
    .onStepEnter(handleStepEnter);

// Handle window resize
window.addEventListener('resize', scroller.resize);

// Initial chart render
renderChart(chart1Spec);

function renderChart(spec) {
    vegaEmbed('#chart', spec, {
        actions: false,
        renderer: 'svg', // Ensures compatibility across browsers
        defaultStyle: true // Applies default Vega styling
    }).then(function(result) {
        // Additional interactions can be added here
    }).catch(console.error);
}

// Render additional charts
function renderAdditionalCharts() {
    vegaEmbed('#chart4', chart4Spec, { actions: false });
    vegaEmbed('#chart5', chart5Spec, { actions: false });
    vegaEmbed('#chart6', chart6Spec, { actions: false });
}

// Ensure initial render of the first scrollytelling chart
renderChart(chart1Spec);

// Render additional charts for new sections
renderAdditionalCharts();

