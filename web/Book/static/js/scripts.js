const initInitEElement = () => {
    // 초기화
    const myModalEl = document.getElementById("signModal");

    const myModalEl_ClickEventListener = (e) => {
        const modal = new mdb.Modal(myModalEl);
        modal.show();
    };
        myModalEl.onclick(myModalEl_ClickEventListener);
    };

