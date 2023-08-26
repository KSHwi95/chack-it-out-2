// 팝업버튼 = btn
const btn = document.getElementById('popupBtn');
// 모달창 = modal
const modal = document.getElementById('modalWrap');
// 모달창-취소 = cancel
const cancel = document.getElementById('cancel');

// btn을 .onclick 하면 = function(){ 실행 }
btn.onclick = function() {
  modal.style.display = 'block';
}

cancel.onclick = function() {
  modal.style.display = 'none';
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

