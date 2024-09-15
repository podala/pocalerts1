const { Worker } = require('worker_threads');
const path = require('path');

/**
 * Splits Excel file into chunks and processes them in parallel using worker threads.
 * @param {string} filePath - The file path of the uploaded Excel file.
 * @param {number} totalRows - Total number of rows in the Excel file.
 * @param {number} chunkSize - Number of rows to process per worker.
 * @param {function} updateProgress - Callback to update progress.
 * @returns {Promise<Array>} - Merged results after processing all chunks.
 */
const processFileInChunks = async (filePath, totalRows, chunkSize, updateProgress) => {
  const workers = [];
  let processedRows = 0;
  const results = [];

  for (let startRow = 1; startRow <= totalRows; startRow += chunkSize) {
    const endRow = Math.min(startRow + chunkSize - 1, totalRows);

    workers.push(
      new Promise((resolve, reject) => {
        const worker = new Worker(path.join(__dirname, 'processWorker.js'), {
          workerData: { filePath, startRow, endRow },
        });

        worker.on('message', (data) => {
          processedRows += (endRow - startRow + 1);
          updateProgress(Math.floor((processedRows / totalRows) * 100));
          resolve(data);  // Return the result from this chunk
        });

        worker.on('error', reject);
        worker.on('exit', (code) => {
          if (code !== 0) reject(new Error(`Worker stopped with exit code ${code}`));
        });
      })
    );
  }

  // Wait for all workers to finish and merge results
  const chunks = await Promise.all(workers);
  return chunks.flat();  // Merge all chunk results into one array
};

module.exports = { processFileInChunks };
