def generate_alert(severity):
    if severity == "High":
        return "High priority alert."
    if severity == "Medium":
        return "Medium priority alert."
    return "Low priority alert."
