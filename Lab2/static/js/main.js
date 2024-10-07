/*
 * This is just for autograding, you can ignore it.
 */
document.addEventListener("securitypolicyviolation", (e) => {
    let reportToUrl="/csp";
    fetch(reportToUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/csp-report"
        },
        body: JSON.stringify({
            "csp-report":{
                "blocked-uri": e.blockedURI,
                "document-uri": e.documentURI,
                "original-policy": e.originalPolicy,
                "referrer": e.referrer,
                "script-sample": e.sample,
                "source-file": e.sourceFile,
                "violated-directive": e.violatedDirective
            }
        }),
        cache: "no-cache",
        referrerPolicy: "no-referrer"
    });
});