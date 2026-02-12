def build_response(analysis):
    return {
        "AI_Analysis": {
            "Detected Disease": analysis["disease"],
            "Severity Level": analysis["severity"],
            "Confidence": analysis["confidence"]
        },
        "Advisory": {
            "Recommendation": "Apply recommended fungicide and monitor crop for 7 days"
        }
    }
