import streamlit as st
import function

todos = function.get_todos()

def add_todo():
    # Capitalize the first letter of each word in the new to-do
    todo = st.session_state["new_todo"].title() + "\n"
    todos.append(todo)
    function.write_todos(todos)
    # Clear the input box after adding the to-do item
    st.session_state["new_todo"] = ""

def update_todo(index, updated_todo):
    todos[index] = updated_todo.title() + "\n"
    function.write_todos(todos)

st.title("My Todo App")
st.subheader("This Todo Web App is created by Dario Galvagno")
st.write("This app is to increase your productivity")

for index, todo in enumerate(todos):
    cols = st.columns([4, 1, 1])  # Adjust the column widths as needed

    # Check if edit mode is enabled for this todo item
    if st.session_state.get(f"edit_mode_{index}", False):
        new_todo = cols[0].text_input("Edit Todo:", value=todo.strip(), key=f"edit_input_{index}")

        if cols[1].button("Update", key=f"update_{index}"):
            update_todo(index, new_todo)
            st.session_state[f"edit_mode_{index}"] = False
            st.rerun()

        if cols[2].button("Cancel", key=f"cancel_{index}"):
            st.session_state[f"edit_mode_{index}"] = False
            st.rerun()

    else:
        checkbox_key = f"todo_{index}"  # Unique key for each checkbox
        if cols[0].checkbox(todo, key=checkbox_key):
            todos.pop(index)
            function.write_todos(todos)
            del st.session_state[checkbox_key]
            st.rerun()

        # Add an "Edit" button next to each todo
        if cols[1].button("Edit", key=f"edit_{index}"):
            st.session_state[f"edit_mode_{index}"] = True
            st.rerun()

# Add the new to-do input box
st.text_input(label="", placeholder="Add a new todo...",
              on_change=add_todo, key="new_todo")

