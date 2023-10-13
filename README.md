







                                                RUN ->packages -> bizcard.py -> Streamlit Run 
                                                run each in sepearte collab cell

Certainly! The provided program is a Streamlit web application called "BizCardX" designed for extracting information from business cards using OCR (Optical Character Recognition). Let's break down the main components and functionality of the program:

### Purpose:
The purpose of the BizCardX application is to allow users to upload an image of a business card and extract relevant information such as company name, cardholder name, designation, contact details, etc., using EasyOCR. Users can also view, modify, delete, and save this extracted information in a SQLite database along with the uploaded business card image.

### Components and Features:

1. **Page Configurations:**
   - The Streamlit application is configured with a custom page title, wide layout, an expanded initial sidebar, and an "About" menu item.

2. **Background Image:**
   - The application features a background image for aesthetic appeal.

3. **Menu Selection:**
   - Users can select from the following menus:
     - **Home:** Provides an overview of the technologies used and the purpose of the application.
     - **Upload & Extract:** Allows users to upload a business card image, process it using EasyOCR, and display the extracted information.
     - **Modify:** Provides options to update, delete, and view the extracted data from the database.

4. **OCR Processing (Upload & Extract Menu):**
   - Users can upload a business card image (in formats like PNG, JPEG, JPG).
   - The uploaded image is processed using EasyOCR to extract text information.
   - Extracted information includes company name, cardholder name, designation, contact details (mobile number, email), website, area, city, state, and pin code.
   - The extracted data is displayed in a Pandas DataFrame and can be uploaded to an SQLite database.

5. **Database Interaction (Upload & Extract & Modify Menus):**
   - The application uses an SQLite database (`bizcardx_db.sqlite`) to store extracted business card information.
   - Users can upload the extracted information (from Upload & Extract menu) to the database.
   - In the Modify menu, users can update or delete existing entries in the database.

6. **User Interface (Modify Menu):**
   - In the Modify menu, users can select a cardholder's name to update the information associated with that card.
   - Users can modify details like company name, cardholder name, designation, contact details, etc.
   - Users can also delete a selected business card entry from the database.
   - Updated data can be viewed in the application.

7. **Visualization:**
   - The application provides visual feedback by displaying the uploaded business card image and highlighting the extracted text using bounding boxes.

8. **Background Tasks:**
   - The application includes background tasks for processing the uploaded image and updating the database, ensuring a responsive user experience.

9. **Error Handling:**
   - The program includes basic error handling to address cases where there is no data available in the database.

### Technologies Used:
- **Programming Language:** Python
- **Libraries/Frameworks:**
  - Streamlit: For creating the web application interface.
  - EasyOCR: For optical character recognition to extract text from images.
  - SQLite: For database storage and interaction.
  - Pandas: For handling and displaying data.
  - OpenCV: For image processing and visualization.
  - Matplotlib: For displaying images and visualizations.

### How to Use:
Users can access the BizCardX application through a web browser. They can navigate through different menus, upload business card images, view extracted information, make modifications, and interact with the SQLite database seamlessly through the user-friendly interface provided by the Streamlit app.

This application is a practical tool for individuals or businesses needing to efficiently manage and extract data from multiple business cards. Users can organize and store business card information in a structured database, making it easier to manage contacts and business relationships.
