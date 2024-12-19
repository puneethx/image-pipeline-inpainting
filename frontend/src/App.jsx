import './App.css';
import React, { useState, useRef } from 'react';
import CanvasDraw from 'react-canvas-draw';
import { Upload, Trash2, Wand2 as Magic, Image as ImageIcon } from 'lucide-react'; // Importing icons for UI elements.

const App = () => {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [maskImage, setMaskImage] = useState(null);
  const [brushRadius, setBrushRadius] = useState(8);
  const [canvasSize, setCanvasSize] = useState({ width: 600, height: 400 });
  const [ogDimensions, setOgDimensions] = useState({ width: 0, height: 0 });
  const [savedImages, setSavedImages] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState(null);

  const canvasRef = useRef(null); // Ref to access the CanvasDraw component directly.

  // Function to calculate the aspect ratio of an uploaded image file and adjust dimensions accordingly.
  const calculateAspectRatio = (file) => {
    return new Promise((resolve) => {
      const img = new Image(); // Create a new Image object to load the file.
      img.onload = () => {
        setOgDimensions({
          width: img.width,
          height: img.height
        });
        
        const aspectRatio = img.width / img.height;
        let newWidth = 600;
        let newHeight = 600 / aspectRatio;
        
        if (newHeight > 800) {
          newHeight = 800;
          newWidth = 800 * aspectRatio;
        }
        
        resolve({ width: Math.floor(newWidth), height: Math.floor(newHeight) });
      };
      img.src = URL.createObjectURL(file);
    });
  };

  // Function to handle image upload and prepare the canvas for drawing.
  const handleImageUpload = async (event) => {
    const file = event.target.files?.[0]; // Get the uploaded file from input.
    if (file) {
      if (canvasRef.current) {
        canvasRef.current.clear(); // Clear the canvas if it exists before uploading a new image.
      }
      setMaskImage(null);
      setSavedImages(null);
      setError(null);

      const dimensions = await calculateAspectRatio(file); // Calculate and set new dimensions based on uploaded image.
      setCanvasSize(dimensions);

      const reader = new FileReader();
      reader.onload = (e) => {
        setUploadedImage(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  // Convert base64 string to Blob for uploading to server.
  const base64ToBlob = async (base64) => {
    const response = await fetch(base64);
    return response.blob();
  };

  // Function to generate a mask based on user drawing and save both images to the server.
  const generateMaskAndSave = async () => {
    if (!canvasRef.current) return;
    setIsGenerating(true);
  
    const canvas = canvasRef.current.canvasContainer?.children[1];
    const ctx = canvas.getContext('2d');
  
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;
    const tempCtx = tempCanvas.getContext('2d');
  
    tempCtx.fillStyle = 'black';
    tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
  
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
  
    for (let i = 0; i < data.length; i += 4) {
      if (data[i + 3] > 0) {
        tempCtx.fillStyle = 'white';
        const x = (i / 4) % canvas.width;
        const y = Math.floor((i / 4) / canvas.width);
        tempCtx.fillRect(x, y, 1, 1);
      }
    }
  
    const maskDataUrl = tempCanvas.toDataURL();
    setMaskImage(maskDataUrl);
  
    // Prepare form data for uploading images
    const formData = new FormData();
    const originalBlob = await base64ToBlob(uploadedImage);
    const maskBlob = await base64ToBlob(maskDataUrl);
  
    const originalExt = uploadedImage.split(';')[0].split('/')[1];
    formData.append('original', originalBlob, `original.${originalExt}`);
    formData.append('mask', maskBlob, 'mask.png');
  
    // Send images to server
    const response = await fetch('http://localhost:8000/api/upload', {
      method: 'POST',
      body: formData,
    });
  
    const result = await response.json();
    setSavedImages(result);
  
    setIsGenerating(false);
  };
  
  // Function to clear the canvas and reset states
  const clearCanvas = () => {
    if (canvasRef.current) {
      canvasRef.current.clear();
      setMaskImage(null);
      setSavedImages(null);
      setError(null);
    }
  };

  // Function to determine display style for images based on their dimensions
  const getImageDisplayStyle = () => {
    const containerWidth = Math.min(canvasSize.width, 500);
    const scale = containerWidth / canvasSize.width;
    const displayHeight = canvasSize.height * scale;

    return {
      width: containerWidth,
      height: displayHeight,
      objectFit: 'contain'
    };
  };

  return (
    <div className="App">
      <h1 className="title">Image Pipeline</h1>
      <p className="desc">
        Upload an image and draw on it to create a mask. The mask will highlight 
        the areas you've drawn in white against a black background.
      </p>

      <div className="upload-area">
        <label>
          <Upload className="upload-icon" size={20} />
          <div className="upload-text">
            {uploadedImage ? 'Replace Image' : 'Upload Image'}
          </div>
          <div className="upload-subtext"> (JPEG/PNG format)</div>
          <input
            className='upload-input'
            type="file"
            accept="image/jpeg,image/png"
            onChange={handleImageUpload}
            style={{ display: 'none' }}
          />
        </label>
      </div>

      {uploadedImage && ( // Render this section only if an image has been uploaded
        <div className="canvas-container">
          <CanvasDraw
            ref={canvasRef}
            brushRadius={brushRadius}
            brushColor="white"
            backgroundColor="rgba(0,0,0,0)"
            imgSrc={uploadedImage}
            canvasWidth={canvasSize.width}
            canvasHeight={canvasSize.height}
            hideGrid={true}
            lazyRadius={0}
            immediateLoading={true}
            saveData={null}
            loadTimeOffset={0}
          />

          <div className="controls">
            <div className="brush-controls">
              <label className="brush-label">Brush Size:</label>
              <input
                type="range"
                min="1"
                max="50"
                value={brushRadius}
                onChange={(e) => setBrushRadius(Number(e.target.value))}
                className="brush-slider"
              />
              <span className="brush-size">{brushRadius}px</span>
            </div>

            <div className="buttonDiv">
              <button 
                className="buttonone" 
                onClick={generateMaskAndSave}
                disabled={isGenerating}
              >
                <Magic size={16} />
                {isGenerating ? 'Generating...' : 'Generate Mask'}
              </button>
              <button className="buttontwo" onClick={clearCanvas}>
                <Trash2 size={16} />
                Clear
              </button>
            </div>
          </div>

          {(savedImages && maskImage) && ( // Render this section only if images have been saved successfully
            <div className="img-display">
              {/* Display the Images */}
              <div className="img-card">
                <div className="img-header">
                  <ImageIcon size={16} />
                  <h3 className="img-title">Original Image</h3>
                  <span className="img-dimensions">
                    {ogDimensions.width} × {ogDimensions.height}
                  </span>
                </div>
                <div className="img-content">
                  <img
                    src={savedImages.original_path}
                    alt="Original"
                    className="preview-img"
                    style={getImageDisplayStyle()}
                  />
                </div>
              </div>

              <div className="img-card">
                <div className="img-header">
                  <Magic size={16} />
                  <h3 className="img-title">Generated Mask</h3>
                  <span className="img-dimensions">
                    {ogDimensions.width} × {ogDimensions.height}
                  </span>
                </div>
                <div className="img-content">
                  <img
                    src={savedImages.mask_path}
                    alt="Mask"
                    className="preview-img"
                    style={getImageDisplayStyle()}
                  />
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="error-message" style={{ color: 'red', marginTop: '1rem' }}>
              Error: {error}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default App;