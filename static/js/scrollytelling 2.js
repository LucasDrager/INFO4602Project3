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
    }
}

// Setup Scrollama
scroller
    .setup({
        step: '.step',
        offset: 0.5,
        debug: false
    })
    .onStepEnter(handleStepEnter);

// Handle window resize
window.addEventListener('resize', scroller.resize);

// Initial chart render
renderChart(chart1Spec);
