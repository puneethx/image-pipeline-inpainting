
# Image Inpainting Widget

A React-based application that allows users to upload images and create masks for image inpainting. The application features an interactive canvas for drawing masks and a backend service for storing the images.

## Features
- **Image upload support**: JPEG/PNG formats are supported.
- **Interactive canvas**: Users can draw masks directly on the uploaded image.
- **Adjustable brush size**: Customize the brush size for drawing.
- **Side-by-side display**: View original and mask images simultaneously.
- **Backend storage**: Image pairs are stored in a database for future access.
---
![Screenshot 2024-12-19 235709](https://github.com/user-attachments/assets/3e09009e-112d-44da-b2c5-b7ae91349c4c)
![Screenshot 2024-12-19 235813](https://github.com/user-attachments/assets/f2ce323b-a277-465e-b41b-f307aef5aea2)
---

## Technologies Used

### Frontend
- **React**: JavaScript library for building user interfaces.
- **react-canvas-draw**: A React component for drawing on a canvas.
- **lucide-react**: A collection of icons for React applications.
- **CSS**: For styling the application.

### Backend
- **FastAPI**: A modern web framework for building APIs with Python 3.12.
- **SQLite**: A lightweight database for storing image data.

## Setup Instructions

### Frontend Setup
1. Clone the repository:
    ```
    git clone https://github.com/puneethx/image-pipeline-inpainting.git
    ```
2. Install dependencies:
    ```
    cd frontend 
    npm install 
    ```
3. Start the development server:
    ```
    npm run dev
    ```

### Backend Setup
1. Install Python dependencies:
    ```
    pip install fastapi uvicorn[standard] python-multipart Pillow
    ```
2. Start the FastAPI server:
    ```
    python -m uvicorn main:app --reload
    ```

## Usage
1. Open the application in your browser (typically at `http://localhost:5173`).
2. Click the file upload button to select an image.
3. Use the canvas to draw a mask on the image.
4. Adjust the brush size using the slider if needed.
5. Click "Generate Mask" to create and view the mask.
6. Use "Clear Canvas" to start over.

## API Endpoints
- **POST /upload**: Upload an image pair (original and mask) to the server.

---

### Thank You :)
