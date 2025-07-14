def classify_email(email_data, rules):
    """
    Classifies an email based on a set of rules.

    :param email_data: A dictionary containing email details (e.g., 'subject', 'from').
    :param rules: A list of rule objects from the database.
    :return: The category name if a rule matches, otherwise None.
    """
    subject = email_data.get('subject', '').lower()
    sender = email_data.get('from', {}).get('emailAddress', {}).get('address', '').lower()

    for rule in rules:
        field_to_check = subject if rule.field == 'subject' else sender
        value_to_check = rule.value.lower()

        if rule.condition == 'CONTAINS' and value_to_check in field_to_check:
            return rule.category
        elif rule.condition == 'STARTS_WITH' and field_to_check.startswith(value_to_check):
            return rule.category
        # Add more conditions as needed (e.g., ENDS_WITH, EQUALS)

    return None

def get_sample_rules():
    """Returns a list of sample rules for testing."""
    from collections import namedtuple
    Rule = namedtuple('Rule', ['category', 'field', 'condition', 'value'])
    return [
        Rule(category="Errores Críticos", field="subject", condition="CONTAINS", value="[ERROR]"),
        Rule(category="Logs", field="sender", condition="CONTAINS", value="noreply@system.com"),
    ]
