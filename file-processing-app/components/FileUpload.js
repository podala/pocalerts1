import { useState } from 'react';

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setMessage('Uploading and processing...');

    // Send the file to the backend API
    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();
    
    setLoading(false);
    
    if (result.success) {
      setMessage('Fields successfully sent to the other application.');
    } else {
      setMessage('Failed to process the file.');
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} disabled={loading} />
      <button onClick={handleFileUpload} disabled={!file || loading}>Upload and Process File</button>

      {loading && (
        <div>
          <p>Processing: {progress}%</p>
          <progress value={progress} max="100"></progress>
        </div>
      )}

      {message && <p>{message}</p>}
    </div>
  );
}
