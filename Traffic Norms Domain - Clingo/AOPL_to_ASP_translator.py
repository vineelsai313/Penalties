import re

def parse_aopl_rule(aopl_rule):
    """
    Parse the given AOPL rule into components: label, head action, and body literals.
    """
    label, rest = aopl_rule.split(":")
    head, body = rest.split("if")

    rule_label = label.strip()
    rule_label_set = set(re.findall(r"\b[A-Z][A-Za-z0-9]*\b", rule_label))
    
    head_action = re.sub(r"(normally\s*|permitted|obl|obligated)\((-?\s*.+?)\)", r"\2", head.strip())
    head_action = re.sub(r"^(normally\s*|-\s*)", "", head_action).strip()
    
    action_name, action_vars = head_action.split("(")
    action_vars = action_vars.rstrip(")")
    action_set = set(re.findall(r"\b[A-Z][A-Za-z0-9]*\b", action_vars))
    
    body_literals = [lit.strip() for lit in re.split(r",(?=(?:[^()]*\([^()]*\))*[^()]*$)", body)]
    
    return rule_label, head_action, body_literals, rule_label_set, action_set

def classify_literals(body_literals, rule_label_set, action_set):
    """
    Classify literals into fluents, statics, and remove unnecessary ones.
    """
    filtered_literals = []
    
    for literal in body_literals:
        if literal.startswith("lt") or literal.startswith("gt") or literal.startswith("=") or literal.startswith("!="):
            continue  # Skip numerical conditions
        
        literal_vars = set(re.findall(r"\b[A-Z][A-Za-z0-9]*\b", literal))
        
        if literal_vars & (rule_label_set - action_set):
            filtered_literals.append(f"holds({literal})")
        elif not (literal_vars - action_set):
            continue
        else:
            filtered_literals.append(literal)
    
    return filtered_literals

def translate_aopl_to_asp(aopl_rule):
    """
    Translate an AOPL rule to ASP syntax.
    """
    rule_label, head_action, body_literals, rule_label_set, action_set = parse_aopl_rule(aopl_rule)
    
    head_action = head_action.lstrip('-').strip()
    filtered_literals = classify_literals(body_literals, rule_label_set, action_set)
    
    if filtered_literals:
        asp_body_formatted = ",\n    ".join(filtered_literals)
        asp_rule = f"rule({rule_label}) :-\n    action({head_action}),\n    {asp_body_formatted}."
    else:
        asp_rule = f"rule({rule_label}) :-\n    action({head_action})."
    
    return asp_rule

def aopl_to_asp(aopl_input):
    if aopl_input.startswith("prefer"):
        match = re.match(r"prefer\(([^,]+?\(.*?\)),\s*([^,]+?\(.*?\))\)\.", aopl_input.strip())
        if match:
            rule1, rule2 = match.groups()
            return f"prefer({rule1}, {rule2}) :- rule({rule1}), rule({rule2})."
        else:
            raise ValueError("Invalid prefer rule format")

    if aopl_input.startswith("penalty"):
        match = re.match(r"penalty\((.*?),\s*(\d+)\)(?: if (.+))?\.", aopl_input.strip())
        if match:
            rule_name, value, condition = match.groups()
            condition_clause = f", {condition}" if condition else ""
            return f"penalty({rule_name}, {value}) :- rule({rule_name}){condition_clause}."
        else:
            raise ValueError("Invalid penalty rule format")

    rule_part, conditions_part = aopl_input.split(" if ", 1)
    rule_name, action = rule_part.split(": ", 1)
    rule_name = rule_name.strip()
    action = action.strip().rstrip(".")
    
    if "normally" in rule_part:
        rule_type = f"type({rule_name}, defeasible) :- rule({rule_name}).\n"
        action = action.replace("normally", "").strip()
    else:
        rule_type = f"type({rule_name}, strict) :- rule({rule_name}).\n"
    
    conditions = []
    current_condition = ""
    open_parentheses = 0
    
    for char in conditions_part.strip():
        if char == "," and open_parentheses == 0:
            conditions.append(current_condition.strip())
            current_condition = ""
        else:
            current_condition += char
            if char == "(":
                open_parentheses += 1
            elif char == ")":
                open_parentheses -= 1
    
    if current_condition:
        conditions.append(current_condition.strip().rstrip("."))
    
    asp_output = ""
    asp_output += translate_aopl_to_asp(aopl_input) + "\n"
    asp_output += rule_type
    asp_output += f"head({rule_name}, {action}) :- rule({rule_name}).\n"
    
    for condition in conditions:
        asp_output += f"mbr(b({rule_name}), {condition}) :- rule({rule_name}).\n"
    
    return asp_output

def process_aopl_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        content = infile.read().strip()
        policies = content.split(".")
        
        for policy in policies:
            policy = policy.strip()
            if policy:
                try:
                    asp_output = aopl_to_asp(policy + ".")
                    outfile.write(asp_output + "\n\n")
                except ValueError as e:
                    print(f"Skipping invalid policy: {policy}. Error: {e}")

import os


if __name__ == "__main__":
    current_directory = os.getcwd()
    print(current_directory)
    input_file = input("Enter file name: ")
    output_file = "ASP_policies.txt"
    print("The ASP translation will be in a file titled", output_file)
    process_aopl_file(input_file, output_file)
    print(f"Generated ASP Policies written to {output_file}")
