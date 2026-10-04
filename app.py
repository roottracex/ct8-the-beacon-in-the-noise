from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/api/alerts")
def alerts():
    return jsonify({
        "alerts": [
            {
                "id": "ALT-1042",
                "event": "Unusual DNS Activity",
                "source": "10.20.14.21",
                "severity": "HIGH",
                "status": "Investigating"
            },
            {
                "id": "ALT-1039",
                "event": "Multiple Authentication Failures",
                "source": "10.20.14.44",
                "severity": "MEDIUM",
                "status": "Reviewed"
            },
            {
                "id": "ALT-1037",
                "event": "Endpoint Connection",
                "source": "10.20.14.77",
                "severity": "LOW",
                "status": "Resolved"
            }
        ]
    })


@app.route("/alert/<alert_id>")
def investigate(alert_id):

    alerts_data = {
        "ALT-1042": {
            "id": "ALT-1042",
            "title": "Unusual DNS Activity",
            "severity": "HIGH",
            "source": "10.20.14.21",
            "destination": "resolver.internal",
            "status": "Investigating",
            "description": "Repeated DNS requests were observed from the endpoint.",
            "next_step": "Review the associated endpoint telemetry.",
            "reference": "SOC-REF-1042"
        }
    }

    alert = alerts_data.get(alert_id)

    if not alert:
        return "Alert not found", 404

    return render_template("investigate.html", alert=alert)


@app.route("/api/telemetry/<reference>")
def telemetry(reference):

    telemetry_data = {
        "SOC-REF-1042": {
            "reference": "SOC-REF-1042",
            "host": "CT8-WKS-21",
            "source": "10.20.14.21",
            "event_type": "DNS_BEACON",
            "interval": "60 seconds",
            "destination": "resolver.internal",
            "status": "SUSPICIOUS"
        }
    }

    data = telemetry_data.get(reference)

    if not data:
        return "Telemetry not found", 404

    return jsonify(data)


@app.route("/api/ioc/<reference>")
def ioc(reference):

    ioc_data = {
        "SOC-REF-1042": {
            "reference": "SOC-REF-1042",
            "ioc_type": "DOMAIN",
            "indicator": "cdn-sync.cybertec8.local",
            "first_seen": "2026-10-04 18:42:10",
            "confidence": "HIGH",
            "classification": "SUSPICIOUS"
        }
    }

    data = ioc_data.get(reference)

    if not data:
        return "IOC not found", 404

    return jsonify(data)


@app.route("/api/evidence/<reference>")
def evidence(reference):

    evidence_data = {
        "SOC-REF-1042": {
            "reference": "SOC-REF-1042",
            "ioc": "cdn-sync.cybertec8.local",
            "evidence_type": "DNS_BEACON_ARTIFACT",
            "recovery_token": "SOC-BEACON-14",
            "status": "RECOVERED"
        }
    }

    data = evidence_data.get(reference)

    if not data:
        return "Evidence not found", 404

    return jsonify(data)


# Recovery validation stage
@app.route("/api/validate/<token>")
def validate(token):

    validation_data = {
        "SOC-BEACON-14": {
            "status": "VALID",
            "token": "SOC-BEACON-14",
            "incident": "CT8-SOC-14",
            "next_stage": "ARTIFACT_VERIFICATION",
            "artifact_id": "CT8-DNS-14"
        }
    }

    data = validation_data.get(token)

    if not data:
        return "Invalid recovery token", 403

    return jsonify(data)


# Final artifact verification stage
@app.route("/api/artifact/<artifact_id>")
def artifact(artifact_id):

    artifact_data = {
        "CT8-DNS-14": {
            "artifact_id": "CT8-DNS-14",
            "incident": "CT8-SOC-14",
            "type": "DNS_BEACON_ARTIFACT",
            "verification": "PASSED",
            "encoding": "BASE64",
            "payload": "Q1lCRVJURUM4IEFSTUlGQUNUIFZFUkFJRElFRApGbGFnX0NUNHtiZWFjb25faW5fdGhlX25vaXNlfQ=="
        }
    }

    data = artifact_data.get(artifact_id)

    if not data:
        return "Artifact not found", 404

    return jsonify(data)


# Direct recovery endpoint intentionally disabled.
# Participants must follow the investigation chain.
@app.route("/api/recover/<token>")
def recover(token):
    return jsonify({
        "status": "BLOCKED",
        "message": "Direct recovery is not available.",
        "next_step": "Complete recovery validation."
    }), 403


if __name__ == "__main__":
    app.run(debug=True)