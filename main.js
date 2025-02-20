$('#random_run_btn').click(function(){
    const LROBJ = new LiverRandom();
    console.log(LROBJ.import_csv());
});

class LiverRandom{
    // メンバ変数を準備
    constructor() {
        this.id;
        this.name;
        this.birthplace;
        this.country;
    }

    // csvを読み込んで配列化
    import_csv(){
        let dataPath = "./data/liver.csv";
        const request = new XMLHttpRequest(); // HTTPでファイルを読み込む
        request.addEventListener('load', (event) => { // ロードさせ実行
            const response = event.target.responseText; // 受け取ったテキストを返す
            output_svg.innerHTML = response; // 表示
        });
        request.open('GET', dataPath, true); // csvのパスを指定
        request.send();
        return result;
    }
    // ランダムでIDを決めて保存
    // メンバ変数に入れ込む
}