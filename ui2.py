import shutil
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="File & Folder Manager", page_icon="📁", layout="centered")

# Base directory the app operates in (same as Path("") in the original code)
BASE = Path(".").resolve()


def list_items():
    """Return all files/folders (recursive) relative to BASE."""
    items = []
    for p in BASE.rglob("*"):
        rel = p.relative_to(BASE)
        # hide Streamlit/python internals for a cleaner view
        if any(part.startswith(".") or part == "__pycache__" for part in rel.parts):
            continue
        items.append(rel)
    return sorted(items, key=lambda x: str(x).lower())


def safe_path(name: str) -> Path:
    """Resolve a user-provided name and make sure it stays inside BASE."""
    p = (BASE / name).resolve()
    if BASE not in p.parents and p != BASE:
        raise ValueError("Path must stay inside the working directory.")
    return p


def folders():
    return [str(i) for i in list_items() if (BASE / i).is_dir()]


def files():
    return [str(i) for i in list_items() if (BASE / i).is_file()]


# ---------------- Operations ----------------
def create_folder(name):
    try:
        p = safe_path(name)
        p.mkdir()
        st.success("Folder created successfully")
    except Exception as err:
        st.error(f"Sorry, an error occurred: {err}")


def update_folder(old_name, new_name):
    try:
        p = safe_path(old_name)
        new_p = safe_path(new_name)
        if p.exists() and p.is_dir():
            p.rename(new_p)
            st.success("Your folder name is updated successfully")
        else:
            st.warning("Sorry, no such folder exists")
    except Exception as err:
        st.error(f"An error occurred: {err}")


def delete_folder(name):
    try:
        p = safe_path(name)
        if p.exists() and p.is_dir():
            shutil.rmtree(p)
            st.success("Folder deleted successfully")
        else:
            st.warning("No such folder exists")
    except Exception as err:
        st.error(f"There was an error: {err}")


def create_file(name, data):
    try:
        p = safe_path(name)
        if not p.exists():
            p.write_text(data)
            st.success("File created successfully")
        else:
            st.warning("Sorry, a file with this name already exists")
    except Exception as err:
        st.error(f"An error occurred: {err}")


def update_file_rename(name, new_name):
    try:
        p = safe_path(name)
        new_p = safe_path(new_name)
        if not new_p.exists():
            p.rename(new_p)
            st.success("Your file name is changed successfully")
        else:
            st.warning("Sorry, this name already exists")
    except Exception as err:
        st.error(f"An error occurred: {err}")


def update_file_append(name, data):
    try:
        with open(safe_path(name), "a") as fs:
            fs.write(" " + data)
        st.success("Data appended successfully")
    except Exception as err:
        st.error(f"An error occurred: {err}")


def update_file_overwrite(name, data):
    try:
        safe_path(name).write_text(data)
        st.success("Data changed successfully")
    except Exception as err:
        st.error(f"An error occurred: {err}")


def delete_file(name):
    try:
        p = safe_path(name)
        if p.exists() and p.is_file():
            p.unlink()
            st.success("File deleted successfully")
        else:
            st.warning("Sorry, no such file exists")
    except Exception as err:
        st.error(f"An error occurred: {err}")


# ---------------- UI ----------------
st.title("📁 File & Folder Manager")

menu = st.sidebar.radio(
    "Options",
    [
        "Read files and folders",
        "Create a folder",
        "Update a folder",
        "Delete a folder",
        "Create a file",
        "Read a file",
        "Update a file",
        "Delete a file",
    ],
)

if menu == "Read files and folders":
    st.subheader("Files and folders")
    items = list_items()
    if items:
        for i, v in enumerate(items, 1):
            icon = "📂" if (BASE / v).is_dir() else "📄"
            st.write(f"{i} : {icon} {v}")
    else:
        st.info("Nothing here yet.")

elif menu == "Create a folder":
    st.subheader("Create a folder")
    name = st.text_input("Folder name")
    if st.button("Create folder"):
        if name.strip():
            create_folder(name.strip())
        else:
            st.warning("Please enter a folder name")

elif menu == "Update a folder":
    st.subheader("Rename a folder")
    fl = folders()
    if fl:
        old = st.selectbox("Select folder to update", fl)
        new = st.text_input("New folder name")
        if st.button("Rename folder"):
            if new.strip():
                update_folder(old, new.strip())
            else:
                st.warning("Please enter a new name")
    else:
        st.info("No folders available.")

elif menu == "Delete a folder":
    st.subheader("Delete a folder")
    fl = folders()
    if fl:
        name = st.selectbox("Select folder to delete", fl)
        confirm = st.checkbox("I confirm I want to delete this folder and everything in it")
        if st.button("Delete folder", type="primary"):
            if confirm:
                delete_folder(name)
            else:
                st.warning("Please tick the confirmation box")
    else:
        st.info("No folders available.")

elif menu == "Create a file":
    st.subheader("Create a file")
    name = st.text_input("File name (with extension, e.g. notes.txt)")
    data = st.text_area("Write what you want in this file", height=200)
    if st.button("Create file"):
        if name.strip():
            create_file(name.strip(), data)
        else:
            st.warning("Please enter a file name")

elif menu == "Read a file":
    st.subheader("Read a file")
    fl = files()
    if fl:
        name = st.selectbox("Select file", fl)
        if st.button("Read file"):
            try:
                content = safe_path(name).read_text()
                st.write("Your file content is :-")
                st.code(content, language=None)
            except Exception as err:
                st.error(f"An error occurred: {err}")
    else:
        st.info("No files available.")

elif menu == "Update a file":
    st.subheader("Update a file")
    fl = files()
    if fl:
        name = st.selectbox("Select file", fl)
        action = st.radio(
            "Action",
            ["Rename the file", "Append something to the file", "Overwrite the file content"],
        )
        if action == "Rename the file":
            new = st.text_input("New name with extension")
            if st.button("Rename"):
                if new.strip():
                    update_file_rename(name, new.strip())
                else:
                    st.warning("Please enter a new name")
        elif action == "Append something to the file":
            data = st.text_area("What do you want to append?")
            if st.button("Append"):
                update_file_append(name, data)
        else:
            data = st.text_area("What do you want to overwrite with?")
            if st.button("Overwrite"):
                update_file_overwrite(name, data)
    else:
        st.info("No files available.")

elif menu == "Delete a file":
    st.subheader("Delete a file")
    fl = files()
    if fl:
        name = st.selectbox("Select file to delete", fl)
        confirm = st.checkbox("I confirm I want to delete this file")
        if st.button("Delete file", type="primary"):
            if confirm:
                delete_file(name)
            else:
                st.warning("Please tick the confirmation box")
    else:
        st.info("No files available.")
        