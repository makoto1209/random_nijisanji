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
        let req = new XMLHttpRequest(); // HTTPでファイルを読み込むためのXMLHttpRrequestオブジェクトを生成
        req.open("get", "./data/liver.csv", true); // アクセスするファイルを指定
        req.send(null); // HTTPリクエストの発行
        
        // レスポンスが返ってきたらconvertCSVtoArray()を呼ぶ	
        req.onload = function(){
            // convertCSVtoArray(req.responseText); // 渡されるのは読み込んだCSVデータ
            let str = req.responseText;
            let result = []; // 最終的な二次元配列を入れるための配列
            let tmp = str.split("\n"); // 改行を区切り文字として行を要素とした配列を生成
        
            // 各行ごとにカンマで区切った文字列を要素とした二次元配列を生成
            for(let i=0; i<tmp.length; ++i){
                result[i] = tmp[i].split('  ');
            }
        }
        return result;
    }
    // ランダムでIDを決めて保存
    // メンバ変数に入れ込む
}