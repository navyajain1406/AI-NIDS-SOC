
def get_recommended_action(severity):
    actions = {
        "Low": "Continue monitoring",
        "Medium": "Review suspicious traffic",
        "High": "Investigate the security alert",
        "Critical": "Prioritize immediate SOC investigation"
    }

    return actions.get(severity, "Review alert manually")

def add_recommended_actions(results):
    results = results.copy()

    results["recommended_action"] = results["severity"].apply(
        get_recommended_action
    )

    return results