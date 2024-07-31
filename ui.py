import streamlit as st
import requests

# Fetch submodel from the server
url = "http://127.0.0.1:5005/submodel"
response = requests.get(url)

if response.status_code == 200:
    submodel_data = response.json()
    st.success("Submodel fetched successfully:")
else:
    st.error(f"Failed to fetch submodel: {response.status_code}")
    st.stop()

# Extract AAS details
aas_id_short = submodel_data['idShort']
aas_identifier = submodel_data['id']
aas_description_en = submodel_data['description'][0]['text']

# Extract Submodel details
submodel_elements = submodel_data["submodelElements"]

# Streamlit Interface
st.title("HMI - Asset Administration Shell UI")
st.write("Generic UI to discover the Asset Administration Shell")

# Navigation
page = st.sidebar.radio("Select View", ["Technical Properties", "Operational Properties"])

# Display AAS details
st.subheader("Asset Administration Shell")
st.markdown(f"**IdShort:** {aas_id_short}")
st.markdown(f"**Identifier:** {aas_identifier}")
st.markdown(f"**Description[en-US]:** {aas_description_en}")

# CSS styling to add borders
st.markdown("""
<style>
    .submodel-box {
        border: 2px solid #2196F3;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 20px;
    }
    .submodel-element-box {
        border: 2px solid #f44336;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Display based on selected page
if page == "Technical Properties":
    submodel = next(item for item in submodel_elements if item['idShort'] == 'TechnicalProperties')
    st.markdown('<div class="submodel-box">', unsafe_allow_html=True)
    st.subheader("TechnicalProperties")
    st.markdown(f"**IdShort:** {submodel['idShort']}")
    st.markdown(f"**Identifier:** {submodel_data['id']}")
    st.markdown(f"**Description[en-US]:** {submodel['description'][0]['text']}")

    st.markdown('<div class="submodel-element-box">', unsafe_allow_html=True)
    st.subheader("Submodel-Elements")
    for element in submodel['value']:
        with st.expander(f"{element['idShort']}", expanded=True):
            st.markdown(f"**Description[en-US]:** {element['description'][0]['text']}")
            value_type = element['valueType'].split(":")[1] if ":" in element['valueType'] else element['valueType']
            st.markdown(f"**ValueType:** {value_type}")
            st.text_input("Value", value=element['value'], key=f"value_{element['idShort']}")
            st.button("Retrieve", key=f"retrieve_{element['idShort']}")
            st.button("Update", key=f"update_{element['idShort']}")
            st.button("Clear", key=f"clear_{element['idShort']}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Operational Properties":
    submodel = next(item for item in submodel_elements if item['idShort'] == 'OperationalProperties')
    st.markdown('<div class="submodel-box">', unsafe_allow_html=True)
    st.subheader("OperationalProperties")
    st.markdown(f"**IdShort:** {submodel['idShort']}")
    st.markdown(f"**Identifier:** {submodel_data['id']}")
    st.markdown(f"**Description[en-US]:** {submodel['description'][0]['text']}")

    st.markdown('<div class="submodel-element-box">', unsafe_allow_html=True)
    st.subheader("Submodel-Elements")
    for element in submodel['value']:
        with st.expander(f"{element['idShort']}", expanded=True):
            st.markdown(f"**Description[en-US]:** {element['description'][0]['text']}")
            value_type = element['valueType'].split(":")[1] if ":" in element['valueType'] else element['valueType']
            st.markdown(f"**ValueType:** {value_type}")
            st.text_input("Value", value=element['value'], key=f"value_{element['idShort']}")
            st.button("Retrieve", key=f"retrieve_{element['idShort']}")
            st.button("Update", key=f"update_{element['idShort']}")
            st.button("Clear", key=f"clear_{element['idShort']}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
