%%writefile bizcard.py
from streamlit_option_menu import option_menu
import pandas as pd
import streamlit as st
import easyocr
import sqlite3 as sql
import os
import cv2
import matplotlib.pyplot as plt
import re

# SETTING PAGE CONFIGURATIONS
st.set_page_config(
    page_title="BizCardX: Extracting Business Card Data with OCR",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": """# This OCR app is created by Mariya Stephen!"""},
)
st.markdown(
    "<h1 style='text-align: center; color: black;'>BizCardX: Extracting Business Card Data with OCR</h1>",
    unsafe_allow_html=True,
)

# SETTING-UP BACKGROUND IMAGE
def setting_bg():
    st.markdown(
        f""" <style>.stApp {{
                        background: url("https://i.ibb.co/7kDB8Pw/fabio-oy-Xis2k-ALVg-unsplash.jpg");
                        background-size: cover}}
                     </style>""",
        unsafe_allow_html=True,
    )

setting_bg()

# CREATING OPTION MENU
selected = option_menu(None, ["Home","Upload & Extract","Modify"], 
                       icons=["house","cloud-upload","pencil-square"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "35px", "text-align": "centre", "margin": "0px", "--hover-color": "#6495ED"},
                               "icon": {"font-size": "35px"},
                               "container" : {"max-width": "6000px"},
                               "nav-link-selected": {"background-color": "#6495ED"}})

# INITIALIZING THE EasyOCR READER
reader = easyocr.Reader(["en"], gpu=True)

# CONNECTING WITH SQLITE DATABASE
mydb = sql.connect("bizcardx_db.sqlite", check_same_thread=False)
mycursor = mydb.cursor()

# TABLE CREATION
mycursor.execute(
    '''CREATE TABLE IF NOT EXISTS card_data
                   (id INTEGER PRIMARY KEY ,
                    company_name TEXT,
                    card_holder TEXT,
                    designation TEXT,
                    mobile_number TEXT,
                    email TEXT,
                    website TEXT,
                    area TEXT,
                    city TEXT,
                    state TEXT,
                    pin_code TEXT,
                    image BLOB
                    )'''
)

# HOME MENU
if selected == "Home":
    st.markdown("## :green[**Technologies Used :**] Python, Easy OCR, Streamlit, SQL, Pandas")
    st.markdown(
        "## :green[**Overview :**] In this Streamlit web app, you can upload an image of a business card and extract relevant information from it using EasyOCR. You can view, modify, or delete the extracted data in this app. This app also allows users to save the extracted information into a database along with the uploaded business card image. The database can store multiple entries, each with its business card image and extracted information."
    )

# UPLOAD AND EXTRACT MENU
if selected == "Upload & Extract":
    st.markdown("### Upload a Business Card")
    uploaded_card = st.file_uploader("Upload here", type=["png", "jpeg", "jpg"])

    if uploaded_card is not None:
        def save_card(uploaded_card):
            upload_directory = 'uploaded_cards'
            if not os.path.exists(upload_directory):
                os.makedirs(upload_directory)
            uploaded_path = os.path.join(upload_directory, uploaded_card.name).replace("\\", "/")
            with open(uploaded_path, "wb") as f:
                f.write(uploaded_card.read())
            return uploaded_path

        uploaded_path = save_card(uploaded_card)

        def image_preview(image, res):
            for (bbox, text, prob) in res:
                (tl, tr, br, bl) = bbox
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                cv2.putText(
                    image, text, (tl[0], tl[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2
                )
            plt.rcParams["figure.figsize"] = (15, 15)
            plt.axis("off")
            plt.imshow(image)

        image = cv2.imread(uploaded_path)
        res = reader.readtext(uploaded_path)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### You have uploaded the card")
            st.image(uploaded_card)
        with col2:
            with st.spinner("Please wait, processing image..."):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                saved_img = os.path.join("uploaded_cards", uploaded_card.name)
                image = cv2.imread(saved_img)
                res = reader.readtext(saved_img)
                st.markdown("### Image Processed and Data Extracted")
                st.pyplot(image_preview(image, res))

        data = {
            "company_name": [],
            "card_holder": [],
            "designation": [],
            "mobile_number": [],
            "email": [],
            "website": [],
            "area": [],
            "city": [],
            "state": [],
            "pin_code": [],
        }

        def get_data(res):
            for i in res:
                text = i[1]
                if "www" in text.lower() or "www." in text.lower():
                    data["website"].append(text)
                elif "@" in text:
                    data["email"].append(text)
                elif "-" in text:
                    data["mobile_number"].append(text)
                    if len(data["mobile_number"]) == 2:
                        data["mobile_number"] = " & ".join(data["mobile_number"])
                elif res.index(i) == len(res) - 1:
                    data["company_name"].append(text)
                elif res.index(i) == 0:
                    data["card_holder"].append(text)
                elif res.index(i) == 1:
                    data["designation"].append(text)
                if re.findall("^[0-9].+, [a-zA-Z]+", text):
                    data["area"].append(text.split(",")[0])
                elif re.findall("[0-9] [a-zA-Z]+", text):
                    data["area"].append(text)
                match1 = re.findall(".+St , ([a-zA-Z]+).+", text)
                match2 = re.findall(".+St,, ([a-zA-Z]+).+", text)
                match3 = re.findall("^[E].*", text)
                if match1:
                    data["city"].append(match1[0])
                elif match2:
                    data["city"].append(match2[0])
                elif match3:
                    data["city"].append(match3[0])
                state_match = re.findall("[a-zA-Z]{9} +[0-9]", text)
                if state_match:
                    data["state"].append(text[:9])
                elif re.findall("^[0-9].+, ([a-zA-Z]+);", text):
                    data["state"].append(text.split()[-1])
                if len(data["state"]) == 2:
                    data["state"].pop(0)
                if len(text) >= 6 and text.isdigit():
                    data["pin_code"].append(text)
                elif re.findall("[a-zA-Z]{9} +[0-9]", text):
                    data["pin_code"].append(text[10:])

        get_data(res)

        df = pd.DataFrame(data)
        st.success("Data Extracted!")
        st.write(df)

        if st.button("Upload to Database"):
            for i, row in df.iterrows():
                image_binary = uploaded_card.getvalue()
                mycursor.execute(
                    '''INSERT INTO card_data(company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code, image)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (
                        row["company_name"],
                        row["card_holder"],
                        row["designation"],
                        row["mobile_number"],
                        row["email"],
                        row["website"],
                        row["area"],
                        row["city"],
                        row["state"],
                        row["pin_code"],
                        image_binary,
                    ),
                )
                mydb.commit()
            st.success("Uploaded to the database successfully!")

# MODIFY MENU
if selected == "Modify":
    col1,col2,col3 = st.columns([3,3,2])
    col2.markdown("## Alter or Delete the data here")
    column1,column2 = st.columns(2,gap="large")
    try:
        with column1:
            mycursor.execute("SELECT card_holder FROM card_data")
            result = mycursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            selected_card = st.selectbox("Select a card holder name to update", list(business_cards.keys()))
            st.markdown("#### Update or modify any data below")
            mycursor.execute("select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data WHERE card_holder=?",
                            (selected_card,))
            result = mycursor.fetchone()

            # DISPLAYING ALL THE INFORMATIONS
            company_name = st.text_input("Company_Name", result[0])
            card_holder = st.text_input("Card_Holder", result[1])
            designation = st.text_input("Designation", result[2])
            mobile_number = st.text_input("Mobile_Number", result[3])
            email = st.text_input("Email", result[4])
            website = st.text_input("Website", result[5])
            area = st.text_input("Area", result[6])
            city = st.text_input("City", result[7])
            state = st.text_input("State", result[8])
            pin_code = st.text_input("Pin_Code", result[9])

            if st.button("Commit changes to DB"):
                # Update the information for the selected business card in the database
                mycursor.execute("""UPDATE card_data SET company_name=?,card_holder=?,designation=?,mobile_number=?,email=?,website=?,area=?,city=?,state=?,pin_code=?
                                    WHERE card_holder=?""", (company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code,selected_card))
                mydb.commit()
                st.success("Information updated in database successfully.")

        with column2:
            mycursor.execute("SELECT card_holder FROM card_data")
            result = mycursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            selected_card = st.selectbox("Select a card holder name to Delete", list(business_cards.keys()))
            st.write(f"### You have selected :green[**{selected_card}'s**] card to delete")
            st.write("#### Proceed to delete this card?")

            if st.button("Yes Delete Business Card"):
                mycursor.execute(f"DELETE FROM card_data WHERE card_holder='{selected_card}'")
                mydb.commit()
                st.success("Business card information deleted from database.")
    except:
        st.warning("There is no data available in the database")
    
    if st.button("View updated data"):
        mycursor.execute("select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data")
        updated_df = pd.DataFrame(mycursor.fetchall(),columns=["Company_Name","Card_Holder","Designation","Mobile_Number","Email","Website","Area","City","State","Pin_Code"])
        st.write(updated_df)
