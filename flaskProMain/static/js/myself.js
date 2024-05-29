// 打开弹窗函数
function openImagePopup(src) {
    document.getElementById('imagePopup').style.display = 'block';
    document.getElementById('popupImage').src = src;
}

// 关闭弹窗函数
function closeImagePopup() {
    document.getElementById('imagePopup').style.display = 'none';
}