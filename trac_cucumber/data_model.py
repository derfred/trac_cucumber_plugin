class Feature(object):
    def __init__(self, name, description, scenarios=[], background=None):
        self.name = name
        self.description = description
        self.scenarios = scenarios
        self.background = background

    def result(self):
        if self.background:
            result = [self.background.result()]
        else:
            result = []
        return result_from_results(result + map(lambda s: s.result(), self.scenarios))

class Background(object):
    def __init__(self, description, steps=[]):
        self.description = description
        self.steps = steps

    def result(self):
        return result_from_steps(self.steps)

class Scenario(object):
    def __init__(self, description, steps=[]):
        self.description = description
        self.steps = steps

    def result(self):
        return result_from_steps(self.steps)

class Step(object):
    def __init__(self, keyword, description, status, exception=None, multiline_arg=None):
        self.keyword = keyword
        self.description = description
        self.status = status
        self.exception = exception
        self.multiline_arg = multiline_arg

    def result(self):
        return self.status


def result_from_results(results):
    if all(map(lambda r: r == "passed", results)):
        return "passed"
    elif any(map(lambda r: r == "failed", results)):
        return "failed"
    elif any(map(lambda r: r == "pending", results)):
        return "pending"
    else:
        return "skipped"


def result_from_steps(steps):
    return result_from_results(map(lambda s: s.status, steps))


def parse_step_from_xml(xml_node):
    step = Step(xml_node.findtext("keyword"), xml_node.findtext("description"), xml_node.findtext("status"))
    step.multiline_arg = xml_node.findtext("multiline_arg")
    step.exception = xml_node.findtext("exception")
    return step


def parse_background_from_xml(xml_node):
    background = Background(xml_node.findtext("description"))
    background.steps = map(parse_step_from_xml, xml_node.findall("steps/step"))
    return background


def parse_scenario_from_xml(xml_node):
    scenario = Scenario(xml_node.findtext("description"))
    scenario.steps = map(parse_step_from_xml, xml_node.findall("steps/step"))
    return scenario


def parse_feature_from_xml(xml_node):
    feature = Feature(xml_node.attrib["name"], xml_node.findtext("description"))

    background_node = xml_node.find("background")
    if background_node:
        feature.background = parse_background_from_xml(background_node)
    feature.scenarios = map(parse_scenario_from_xml, xml_node.findall("scenario"))

    return feature
