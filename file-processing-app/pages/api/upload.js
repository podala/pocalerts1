import { parseForm } from '../../lib/formidableConfig';
import { processFileInChunks } from '../../lib/fileUtils';
import axios from 'axios';
import fs from 'fs';

// Disable Next.js body parsing for this route
export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      const { files } = await parseForm(req);
      const filePath = files.file.filepath;

      let progress = 0;

      // Function to update progress
      const updateProgress = (newProgress) => {
        progress = newProgress;
      };

      // Get total rows in the Excel file (you might need to load the file to determine this)
      const totalRows = 13000;  // Replace this with dynamic calculation based on file content
      const chunkSize = 1000;   // Number of rows each worker thread will process

      // Process the file in chunks using worker threads
      const extractedFields = await processFileInChunks(filePath, totalRows, chunkSize, updateProgress);

      // Send the extracted fields to another application
      const response = await axios.post('https://target-application.com/api/receive', {
        fields: extractedFields,
      });

      // Clean up the uploaded file
      fs.unlink(filePath, () => {});

      if (response.status === 200) {
        return res.status(200).json({ success: true, message: 'Fields sent successfully' });
      } else {
        throw new Error('Failed to send fields');
      }
    } catch (error) {
      return res.status(500).json({ success: false, message: 'File processing failed', error });
    }
  } else {
    return res.status(405).json({ message: 'Method Not Allowed' });
  }
}
