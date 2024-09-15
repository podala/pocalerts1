const { parentPort, workerData } = require('worker_threads');
const ExcelJS = require('exceljs');

(async () => {
  const { filePath, startRow, endRow } = workerData;
  const workbook = new ExcelJS.Workbook();
  await workbook.xlsx.readFile(filePath);
  const worksheet = workbook.getWorksheet(1);

  const extractedFields = [];

  for (let rowNumber = startRow; rowNumber <= endRow; rowNumber++) {
    const row = worksheet.getRow(rowNumber);
    if ([1, 2, 200].includes(row.number)) {
      extractedFields.push({
        header: `Header ${row.number}`,
        value: row.getCell(2).value,  // Assuming the value is in column B
      });
    }
  }

  // Send the result back to the parent thread
  parentPort.postMessage(extractedFields);
})();
