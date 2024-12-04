// Initialize Scrollama
var scroller = scrollama();

// Function to fetch and render the chart
function renderChart(url, elementId) {
    fetch(url)
        .then((response) => response.json())
        .then((spec) => {
            vegaEmbed(elementId, spec, { actions: false });
        })
        .catch(console.error);
}

// Handle step enter events
function handleStepEnter(response) {
    // Log the current step
    console.log("Entering step", response.element.dataset.step);

    // Remove active class from all steps
    document.querySelectorAll(".step").forEach(function (step) {
        step.classList.remove("active");
    });
    // Add active class to current step
    response.element.classList.add("active");

    var step = response.element.dataset.step;
    if (step === "1") {
        renderChart("/static/charts/chart2.json", "#chart");
    } else if (step === "2") {
        renderChart("/static/charts/chart1.json", "#chart");
    } else if (step === "3") {
        renderChart("/static/charts/chart3.json", "#chart");
    }
}

// Setup Scrollama
scroller
    .setup({
        step: ".step",
        offset: 0.7, // Adjust offset to trigger the step earlier
        debug: false,
    })
    .onStepEnter(handleStepEnter);

// Render additional charts
function renderAdditionalCharts() {
    renderChart("/static/charts/chart4.json", "#chart4");
    renderChart("/static/charts/chart5.json", "#chart5");
}

// Render additional charts for new sections
renderAdditionalCharts();
