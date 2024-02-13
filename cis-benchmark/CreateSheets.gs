function myFunction() {
  // 트리거가 실행되는 시점의 해당 월
  const month = Utilities.formatDate(new Date(), "Asia/Seoul", "MM");
  const currentMonth = parseInt(month);
  const lastMonth = currentMonth - 1;

  const activeSheet = SpreadsheetApp.getActiveSpreadsheet();
  // ActiveSpreadsheet를 이전 월의 worksheet로 셋팅
  activeSheet.setActiveSheet(activeSheet.getSheets()[lastMonth - 1]);
  // 이전 월의 worksheet를 복사
  const copiedSheet = SpreadsheetApp.getActiveSpreadsheet().duplicateActiveSheet();

  copiedSheet.setName(currentMonth + "월");
}
