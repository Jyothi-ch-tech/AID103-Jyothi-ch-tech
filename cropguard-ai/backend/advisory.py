def generate_advisory(disease, severity):
    if disease == "Healthy":
        return "Crop is healthy recalling regular monitoring."
    if severity == "Medium":
        return "Apply recommended fungicide and monitor for 7 days."
    return "Immediate expert intervention required."
