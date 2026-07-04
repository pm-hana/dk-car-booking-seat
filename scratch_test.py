import streamlit as st

st.write("Streamlit button:")
if st.button("Target Button", key="target_btn"):
    st.write("Button Clicked!")

# HTML component with iframe trying to access window.parent.document
html_content = """
<html>
<body>
    <button onclick="
        try {
            const doc = window.parent.document || document;
            const buttons = doc.querySelectorAll('button');
            let found = false;
            for (const btn of buttons) {
                if (btn.textContent.includes('Target Button')) {
                    btn.click();
                    found = true;
                    break;
                }
            }
            alert(found ? 'Button clicked in parent!' : 'Button not found in parent');
        } catch (e) {
            alert('Error accessing parent: ' + e);
        }
    ">Click inside iframe</button>
</body>
</html>
"""

st.components.v1.html(html_content, height=100)
