from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load the submodel from the JSON file
def load_submodel():
    with open('Submodel_HMI_HT225HPB.json', 'r') as f:
        return json.load(f)

submodel = load_submodel()

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the AAS Server"

@app.route('/submodel', methods=['GET'])
def get_submodel():
    return jsonify(submodel)

@app.route('/submodel', methods=['POST'])
def update_submodel():
    global submodel
    data = request.json
    for key, value in data.items():
        if key == "submodelElements":
            # Update submodel elements individually
            existing_elements = {element["idShort"]: element for element in submodel["submodelElements"]}
            for element in value:
                existing_elements[element["idShort"]] = element
            submodel["submodelElements"] = list(existing_elements.values())
        else:
            submodel[key] = value
    return jsonify(submodel)

def update_nested_element(elements, id_short, value):
    for element in elements:
        if element['idShort'] == id_short:
            element['value'] = value
            return True
        elif 'value' in element and isinstance(element['value'], list):
            if update_nested_element(element['value'], id_short, value):
                return True
    return False

@app.route('/submodel/element/<id_short>', methods=['POST'])
def update_element(id_short):
    global submodel
    updated = update_nested_element(submodel.get('submodelElements', []), id_short, request.json.get('value'))
    if updated:
        return jsonify(submodel)
    else:
        return jsonify({'error': f'Element {id_short} not found'}), 404

@app.route('/submodel/element/<id_short>', methods=['GET'])
def retrieve_element(id_short):
    def find_element(elements, id_short):
        for element in elements:
            if element['idShort'] == id_short:
                return element
            elif 'value' in element and isinstance(element['value'], list):
                found = find_element(element['value'], id_short)
                if found:
                    return found
        return None

    element = find_element(submodel.get('submodelElements', []), id_short)
    if element:
        return jsonify(element)
    return jsonify({'error': f'Element {id_short} not found'}), 404

@app.route('/submodel/element/<id_short>/clear', methods=['POST'])
def clear_element(id_short):
    def clear_nested_element(elements, id_short):
        for element in elements:
            if element['idShort'] == id_short:
                element['value'] = ""
                return True
            elif 'value' in element and isinstance(element['value'], list):
                if clear_nested_element(element['value'], id_short):
                    return True
        return False

    updated = clear_nested_element(submodel.get('submodelElements', []), id_short)
    if updated:
        return jsonify(submodel)
    else:
        return jsonify({'error': f'Element {id_short} not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
