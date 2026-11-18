import streamlit as st
from pathlib import Path
import shutil

st.set_page_config(page_title="File & Folder Manager", page_icon="📁")

st.title("📁 File & Folder Manager")

# --------------------------
# Helper Function
# --------------------------
def get_all_items():
    p = Path(".")
    return list(p.rglob("*"))

# Sidebar Menu
menu = st.sidebar.selectbox(
    "Choose Operation",
    [
        "Create Folder",
        "View Files & Folders",
        "Rename Folder",
        "Delete Folder",
        "Create File",
        "Read File",
        "Update File",
        "Delete File"
    ]
)

# ==========================
# Create Folder
# ==========================
if menu == "Create Folder":

    st.subheader("📂 Create Folder")

    folder_name = st.text_input("Folder Name")

    if st.button("Create Folder"):
        try:
            Path(folder_name).mkdir()
            st.success("Folder Created Successfully")
        except Exception as e:
            st.error(e)

# ==========================
# View Files & Folders
# ==========================
elif menu == "View Files & Folders":

    st.subheader("📜 Files & Folders")

    items = get_all_items()

    if items:
        for item in items:
            st.write(item)
    else:
        st.info("No Files or Folders Found")

# ==========================
# Rename Folder
# ==========================
elif menu == "Rename Folder":

    st.subheader("✏️ Rename Folder")

    old_name = st.text_input("Old Folder Name")
    new_name = st.text_input("New Folder Name")

    if st.button("Rename Folder"):

        try:
            p = Path(old_name)

            if p.exists() and p.is_dir():
                p.rename(new_name)
                st.success("Folder Renamed Successfully")
            else:
                st.error("Folder Not Found")

        except Exception as e:
            st.error(e)

# ==========================
# Delete Folder
# ==========================
elif menu == "Delete Folder":

    st.subheader("🗑️ Delete Folder")

    folder_name = st.text_input("Folder Name")

    if st.button("Delete Folder"):

        try:
            p = Path(folder_name)

            if p.exists() and p.is_dir():
                shutil.rmtree(p)
                st.success("Folder Deleted Successfully")
            else:
                st.error("Folder Not Found")

        except Exception as e:
            st.error(e)

# ==========================
# Create File
# ==========================
elif menu == "Create File":

    st.subheader("📄 Create File")

    file_name = st.text_input("File Name With Extension")
    content = st.text_area("File Content")

    if st.button("Create File"):

        try:
            p = Path(file_name)

            if not p.exists():

                with open(file_name, "w") as f:
                    f.write(content)

                st.success("File Created Successfully")

            else:
                st.error("File Already Exists")

        except Exception as e:
            st.error(e)

# ==========================
# Read File
# ==========================
elif menu == "Read File":

    st.subheader("📖 Read File")

    file_name = st.text_input("File Name")

    if st.button("Read"):

        try:
            p = Path(file_name)

            if p.exists() and p.is_file():

                with open(file_name, "r") as f:
                    st.text_area(
                        "Content",
                        f.read(),
                        height=300
                    )

            else:
                st.error("File Not Found")

        except Exception as e:
            st.error(e)

# ==========================
# Update File
# ==========================
elif menu == "Update File":

    st.subheader("✏️ Update File")

    file_name = st.text_input("File Name")

    action = st.radio(
        "Choose Action",
        ["Rename", "Append", "Overwrite"]
    )

    if action == "Rename":
        new_name = st.text_input("New File Name")

    elif action in ["Append", "Overwrite"]:
        data = st.text_area("Enter Content")

    if st.button("Update File"):

        try:
            p = Path(file_name)

            if p.exists() and p.is_file():

                if action == "Rename":

                    Path(file_name).rename(new_name)
                    st.success("File Renamed Successfully")

                elif action == "Append":

                    with open(file_name, "a") as f:
                        f.write("\n" + data)

                    st.success("Data Appended Successfully")

                elif action == "Overwrite":

                    with open(file_name, "w") as f:
                        f.write(data)

                    st.success("File Overwritten Successfully")

            else:
                st.error("File Not Found")

        except Exception as e:
            st.error(e)

# ==========================
# Delete File
# ==========================
elif menu == "Delete File":

    st.subheader("🗑️ Delete File")

    file_name = st.text_input("File Name")

    if st.button("Delete File"):

        try:
            p = Path(file_name)

            if p.exists() and p.is_file():

                p.unlink()
                st.success("File Deleted Successfully")

            else:
                st.error("File Not Found")

        except Exception as e:
            st.error(e)