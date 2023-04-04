// 1. 글쓰기와 수정에서 쓸 수 있는 함수
//// 제목이 비어있거나 또는 5글자 이하라면 경고창 표시하고 진행 멈춤
//// 글 내용이 비어있거나 10글자 이하라면 경고창 표시하고 진행 멈춤
//// 제목이나 글 내용에 바보, 멍청이, 한조 들어있으면 경고창 표시하고 진행 멈춤

function checkwu() {

    let title = document.getElementById('title1').value;
    let content = document.getElementById('content').value;

    // trim() 띄어쓰기 삭제
    
    if (title.length <= 5) {
        alert("제목이 비어있거나 5글자 이하입니다.");
        return false
    }
    
    if (content.length <= 10) {
        alert("내용이 비어있거나 10글자 이하입니다.");
        return false
    }

    let badWords = ['바보', '멍청이', '한조'];

    for (let i = 0; i < badWords.length; i++) {
        if (title.includes(badWords[i]) || content.includes(badWords[i])) {
            alert(badWords[i]+"는(은) 사용할 수 없는 단어입니다.");
            return false
        }
    }

    // if (title.split("바보").length >= 2) {
    //     alert("제목에 바보는 들어가지 못합니다.");
    //     return false
    // }

    // if (title.split("멍청이").length >= 2) {
    //     alert("제목에 멍청이는 들어가지 못합니다.");
    //     return false
    // }

    // if (title.split("한조").length >= 2) {
    //     alert("제목에 한조는 들어가지 못합니다.");
    //     return false
    // }

    // if (content.split("바보").length >= 2) {
    //     alert("내용에 바보는 들어가지 못합니다.");
    //     return false
    // }

    // if (content.split("멍청이").length >= 2) {
    //     alert("내용에 멍청이는 들어가지 못합니다.");
    //     return false
    // }

    // if (content.split("한조").length >= 2) {
    //     alert("내용에 한조는 들어가지 못합니다.");
    //     return false
    // }

}

// 2. 댓글에서 쓸 수 있는 함수
//// 댓글 창 비어있으면 경고창 표시

/*      if (replyText.length === 0) {
            alert("비어있는 댓글로 수정할 수 없습니다.");
            return; // 실행을 바로 멈춘다
        } */

//      if (replyText.length === 0 ) {
//          alert("댓글을 입력할 수 없습니다.");
//          return; // 실행을 바로 멈춘다
//      }