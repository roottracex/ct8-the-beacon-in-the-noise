const SOC_CONFIG = {
    telemetry: "/api/telemetry/",
    investigation: "SOC-REF-1042"
};

console.log("[SOC] Analyst console initialized");
console.log("[SOC] Investigation reference:", SOC_CONFIG.investigation);
console.log("[SOC] Telemetry service:", SOC_CONFIG.telemetry);


/*
 * Internal analyst helpers.
 * Some investigation services are not linked from the SOC interface.
 */

function inspectEndpoint(reference) {
    return SOC_CONFIG.telemetry + reference;
}


function resolveIndicator(reference) {
    const service = "/api/ioc/";
    return service + reference;
}

function collectArtifact(reference, indicator) {
    const evidenceService = "/api/evidence/";
    
    console.log("[SOC] Artifact collector initialized");
    console.log("[SOC] IOC:", indicator);

    return evidenceService + reference;
}

function validateRecovery(token) {
    const recoveryService = "/api/validate/";
    
    console.log("[SOC] Recovery validation service ready");

    return recoveryService + token;
}


function verifyArtifact(artifactId) {
    const artifactService = "/api/artifact/";

    console.log("[SOC] Artifact verification service ready");
    console.log("[SOC] Artifact ID:", artifactId);

    return artifactService + artifactId;
}